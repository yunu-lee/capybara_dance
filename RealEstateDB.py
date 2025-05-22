from typing import List, Dict, Optional
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os
import argparse

class RealEstateDB:
    def __init__(self):
        """
        MongoDB를 사용하여 부동산 데이터를 관리하는 클래스
        """
        # .env 파일에서 MongoDB 연결 정보 로드
        load_dotenv()
        self.mongo_url = os.getenv('MONGODB_URI')
        if not self.mongo_url:
            raise ValueError("MONGODB_URI .env 파일에 설정되어 있지 않습니다.")
            
        # MongoDB 연결
        self.client = MongoClient(self.mongo_url)
        self.db = self.client['real_estate']
        self.collection = self.db['actual_transactions']
        
    def save_data(self, df: pd.DataFrame, lawd_cd: str) -> None:
        """
        DataFrame의 데이터를 MongoDB에 저장 (중복 방지)
        
        Args:
            df (pd.DataFrame): 저장할 데이터
            lawd_cd (str): 법정동 코드
        """
        if df.empty:
            print("저장할 데이터가 없습니다.")
            return
            
        # DataFrame을 딕셔너리 리스트로 변환
        records = df.to_dict('records')
        
        # 각 레코드에 메타데이터 추가
        for record in records:
            record['lawd_cd'] = lawd_cd
            record['created_at'] = datetime.now()
            
            # 중복 체크를 위한 쿼리 생성
            # 거래일자, 아파트명, 동, 층, 면적, 거래금액으로 중복 판단
            query = {
                'lawd_cd': lawd_cd,
                'dealDate': record['dealDate'],
                'aptNm': record['aptNm'],
                'aptDong': record['aptDong'],
                'floor': record['floor'],
                'excluUseAr': record['excluUseAr'],  # area -> excluUseAr로 변경
                'dealAmount': record['dealAmount']
            }
            
            # 중복 데이터가 없으면 삽입
            if not self.collection.find_one(query):
                self.collection.insert_one(record)
                print(f"새로운 거래 데이터가 저장되었습니다: {record['aptNm']} {record['aptDong']}동 {record['dealDate']}")
            else:
                print(f"중복된 거래 데이터가 발견되었습니다: {record['aptNm']} {record['aptDong']}동 {record['dealDate']}")
        
    def load_data(self, lawd_cd: str, start_date: Optional[datetime] = None, 
                 end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        MongoDB에서 데이터를 불러옴
        
        Args:
            lawd_cd (str): 법정동 코드
            start_date (datetime, optional): 시작 날짜
            end_date (datetime, optional): 종료 날짜
            
        Returns:
            pd.DataFrame: 불러온 데이터
        """
        # 쿼리 조건 생성
        query = {'lawd_cd': lawd_cd}
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query['$gte'] = start_date
            if end_date:
                date_query['$lte'] = end_date
            query['dealDate'] = date_query
            
        # 데이터 조회
        cursor = self.collection.find(query)
        df = pd.DataFrame(list(cursor))
        
        if df.empty:
            print("조회된 데이터가 없습니다.")
            return df
            
        # MongoDB의 _id 컬럼 제거
        if '_id' in df.columns:
            df = df.drop('_id', axis=1)
            
        return df
        
    def get_latest_data_date(self, lawd_cd: str) -> Optional[datetime]:
        """
        특정 지역의 가장 최근 데이터 날짜를 조회
        
        Args:
            lawd_cd (str): 법정동 코드
            
        Returns:
            datetime: 가장 최근 데이터 날짜
        """
        result = self.collection.find_one(
            {'lawd_cd': lawd_cd},
            sort=[('dealDate', -1)]
        )
        
        return result['dealDate'] if result else None
        
    def update_data(self, df: pd.DataFrame, lawd_cd: str) -> None:
        """
        기존 데이터를 업데이트하거나 새로운 데이터 추가
        
        Args:
            df (pd.DataFrame): 업데이트할 데이터
            lawd_cd (str): 법정동 코드
        """
        if df.empty:
            print("업데이트할 데이터가 없습니다.")
            return
            
        # 각 레코드에 대해 upsert 수행
        for _, row in df.iterrows():
            record = row.to_dict()
            record['lawd_cd'] = lawd_cd
            record['updated_at'] = datetime.now()
            
            # 거래일자와 법정동 코드로 문서 식별
            query = {
                'lawd_cd': lawd_cd,
                'dealDate': record['dealDate']
            }
            
            # upsert 수행
            self.collection.update_one(
                query,
                {'$set': record},
                upsert=True
            )
            
    def delete_data(self, lawd_cd: str, start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None) -> None:
        """
        데이터 삭제
        
        Args:
            lawd_cd (str): 법정동 코드
            start_date (datetime, optional): 시작 날짜
            end_date (datetime, optional): 종료 날짜
        """
        # 쿼리 조건 생성
        query = {'lawd_cd': lawd_cd}
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query['$gte'] = start_date
            if end_date:
                date_query['$lte'] = end_date
            query['dealDate'] = date_query
            
        # 데이터 삭제
        result = self.collection.delete_many(query)
        print(f"{result.deleted_count}개의 데이터가 삭제되었습니다.")


if __name__ == "__main__":
    # 명령행 인자 파서 설정
    parser = argparse.ArgumentParser(description='부동산 실거래가 데이터 수집 및 저장')
    parser.add_argument('--lawd_cd', type=str, required=True, help='법정동 코드 (예: 11710)')
    parser.add_argument('--months', type=int, default=3, help='조회할 개월 수 (기본값: 3)')
    args = parser.parse_args()
    
    # 사용 예시
    db = RealEstateDB()
    
    print(f"\n법정동 코드 {args.lawd_cd} 데이터 수집 시작...")
    print(f"조회 기간: 최근 {args.months}개월")
    
    # RealEstateRetriever로 데이터 수집
    from RealEstateRetriever import RealEstateRetriever
    retriever = RealEstateRetriever(lawd_cd=args.lawd_cd, months_before=args.months)
    df = retriever.retrieve()
    
    if not df.empty:
        # 데이터 저장
        db.save_data(df, args.lawd_cd)
        
        # 데이터 조회
        loaded_df = db.load_data(args.lawd_cd)
        print(f"조회된 데이터 수: {len(loaded_df)}")
    else:
        print(f"법정동 코드 {args.lawd_cd}에 대한 데이터가 없습니다.") 