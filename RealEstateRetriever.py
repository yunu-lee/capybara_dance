import json
import xmltodict
import pandas as pd
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from Retriever import Retriever
from dotenv import load_dotenv
import os

class RealEstateRetriever(Retriever):
    def __init__(self, lawd_cd: str, months_before: int = 12):
        """
        국토교통부 실거래가 데이터를 수집하는 Retriever
        
        Args:
            lawd_cd (str): 법정동 코드 (예: '11710' - 서울특별시 송파구)
            months_before (int): 현재로부터 몇 개월 전까지의 데이터를 수집할지 (기본값: 12개월)
        """
        super().__init__()
        self.lawd_cd = lawd_cd
        self.months_before = months_before
        self.url = "http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev"
        
        # .env 파일에서 API 키 로드
        load_dotenv()
        self.service_key = os.getenv('DATA_GO_KEY')
        if not self.service_key:
            raise ValueError("DATA_GO_KEY가 .env 파일에 설정되어 있지 않습니다.")
        
    def retrieve(self) -> pd.DataFrame:
        """
        실거래가 데이터를 수집하여 DataFrame으로 반환
        
        Returns:
            pd.DataFrame: 수집된 실거래가 데이터
        """
        try:
            all_df = pd.DataFrame()
            
            for m in range(self.months_before + 1):
                deal_ymd = self._get_past_year_month(m)
                print(f"수집 중: {deal_ymd}")
                
                for page in range(1, 10):  # 최대 9페이지까지
                    payload = {
                        "serviceKey": self.service_key,
                        "pageNo": str(page),
                        "numOfRows": "1000",
                        "LAWD_CD": self.lawd_cd,
                        "DEAL_YMD": deal_ymd
                    }
                    
                    response = requests.get(self.url, params=payload)
                    data = json.loads(json.dumps(xmltodict.parse(response.text)))
                    
                    items = data.get('response', {}).get('body', {}).get('items', {})
                    if not items:
                        break
                        
                    df = pd.DataFrame(items.get('item', []))
                    all_df = pd.concat([all_df, df], ignore_index=True)
            
            if all_df.empty:
                return all_df
                
            # 데이터 전처리
            all_df['dealAmount'] = all_df['dealAmount'].apply(lambda x: x.replace(',', ''))
            
            # 숫자형 컬럼 변환
            numeric_columns = ['dealAmount', 'buildYear', 'dealYear', 'dealMonth', 'dealDay', 'area', 'floor']
            for col in numeric_columns:
                if col in all_df.columns:
                    all_df[col] = pd.to_numeric(all_df[col], errors='coerce')
            
            # 거래일자 컬럼 생성
            all_df['dealDate'] = pd.to_datetime(
                all_df[['dealYear', 'dealMonth', 'dealDay']].astype(str).agg('-'.join, axis=1),
                format='%Y-%m-%d',
                errors='coerce'
            )
            
            # 거래일자 기준 정렬
            all_df.sort_values(by='dealDate', inplace=True)
            all_df.reset_index(drop=True, inplace=True)
            
            # 결과 저장
            self.retrieved_data = all_df
            
            return all_df
            
        except Exception as e:
            print(f"데이터 수집 중 오류 발생: {str(e)}")
            return pd.DataFrame()
    
    def export(self, file_path: Optional[str] = None) -> None:
        """
        수집된 데이터를 CSV 파일로 저장
        
        Args:
            file_path (str, optional): 저장할 파일 경로. 기본값은 현재 날짜로 생성
        """
        if self.retrieved_data is None:
            print("저장할 데이터가 없습니다. retrieve() 메서드를 먼저 실행해주세요.")
            return
            
        if file_path is None:
            file_path = f"real_estate_data_{self.lawd_cd}_{datetime.now().strftime('%Y%m%d')}.csv"
            
        self.retrieved_data.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"데이터가 {file_path}에 저장되었습니다.")
    
    def _get_past_year_month(self, months_ago: int) -> str:
        """
        현재로부터 n개월 전의 년월을 반환
        
        Args:
            months_ago (int): 몇 개월 전인지
            
        Returns:
            str: 'YYYYMM' 형식의 문자열
        """
        today = datetime.now()
        past_date = today - timedelta(days=30 * months_ago)
        return f"{past_date.year}{str(past_date.month).zfill(2)}" 
    
if __name__ == "__main__":
    retriever = RealEstateRetriever(lawd_cd="11710")
    df = retriever.retrieve()
    retriever.export()
    
