import os

from dotenv import load_dotenv

from Retriever import Retriever

import json
import xmltodict
import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt


class DataGoRetriever(Retriever):
    def retrieve(self, **kwargs) -> pd.DataFrame():
        load_dotenv()
        data_go_key = os.getenv('DATA_GO_KEY')
        url = "http://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev?"

        month_before = kwargs.get('month_before')
        if month_before is None:
            month_before = 12

        num_of_rows = '1000'
        lawd_cd = kwargs.get('area_code')  # '11710'  # 법정동 코드 앞자리 5글자 = 법정 구코드 (서울특별시 종로구)

        if lawd_cd is None:
            raise AttributeError('invalid area_code')

        all_df = pd.DataFrame()

        for m in range(month_before + 1):
            DEAL_YMD = self.get_past_year_month(m)
            print(DEAL_YMD)

            for i in range(1, 10):
                payload = "serviceKey=" + data_go_key + "&" + \
                          "pageNo=" + str(i) + "&" + \
                          "numOfRows=" + num_of_rows + "&" \
                                                       "LAWD_CD=" + lawd_cd + "&" + \
                          "DEAL_YMD=" + DEAL_YMD + "&"

                res = requests.get(url + payload)
                data = json.loads(json.dumps(xmltodict.parse(res.text)))
                print(i, data)
                items = data.get('response').get('body').get('items')
                if items:
                    df = pd.DataFrame(items.get('item'))
                    all_df = pd.concat([all_df, df], ignore_index=True)
                else:
                    break

        return all_df

    def export(self):
        pass

    @staticmethod
    def get_past_year_month(month_before):
        today = datetime.date.today()
        past_date = today - datetime.timedelta(days=30 * month_before)
        year = past_date.year
        month = past_date.month
        return str(year) + str(month).zfill(2)


if __name__ == '__main__':
    dgr = DataGoRetriever()

    area_code = {
        '송파구': '11710',

    }
    result = dgr.retrieve(area_code=area_code.get('송파구'), month_before=2)
    print(result)
