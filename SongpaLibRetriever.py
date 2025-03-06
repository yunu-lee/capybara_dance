import pandas as pd
import requests
from bs4 import BeautifulSoup

from Retriever import Retriever


class SongpaLibRetriever(Retriever):
    def retrieve(self) -> pd.DataFrame():

        cookies = {
            '_fwb': '89WcExhieiQWyIvv9c8cQi.1740013933943',
            'JSESSIONID': 'aaahmYqJjrx5m6DR7rNuzt0ZmMnn8QQbqQMABHMaTsdARIUu7uJRQdz00X2F',
            'wcs_bt': '3a0f999342f0c4:1740244178',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko,en;q=0.9,en-US;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://www.splib.or.kr/spwlib/menu/10409/contents/40184/contents.do',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            # 'Cookie': '_fwb=89WcExhieiQWyIvv9c8cQi.1740013933943; JSESSIONID=aaahmYqJjrx5m6DR7rNuzt0ZmMnn8QQbqQMABHMaTsdARIUu7uJRQdz00X2F; wcs_bt=3a0f999342f0c4:1740244178',
        }

        response = requests.get(
            'https://www.splib.or.kr/spwlib/menu/10406/program/30014/eventList.do',
            cookies=cookies,
            headers=headers,
        )

        soup = BeautifulSoup(response.text, 'html.parser')

        all_programs = []

        for i in range(1, 10):
            try:
                article = soup.select_one(
                    f'#contents > div.articleWrap > div:nth-child({i}) > div.infoBox').text.splitlines()
                article = [x.strip() for x in article if x]
                program = {
                    'host': '송파위례도서관',
                    'title': article[1],
                    'audience': article[5],
                    'price': article[8],
                    'class_start': article[10],
                    'class_end': article[12],
                    'class_day_time': article[13],
                    'place': article[14],
                    'register_start': article[16],
                    'register_end': article[18],
                }
                all_programs.append(program)
            except Exception as e:
                print(e)

        df = pd.DataFrame(all_programs)
        df['audience'] = df['audience'].apply(lambda x: x.replace('(', '').replace(')', ''))
        df['price'] = df['price'].apply(lambda x: x.replace('수강료 :', ''))

        self.retrieved_data = df
        return df

    def export(self):
        msg = '송파위례도서관 프로그램 상위 2개\n\n'

        for idx, row in self.retrieved_data[0:min(2, len(self.retrieved_data))].iterrows():
            msg += f"{idx + 1}) {row.get('title')}, {row.get('audience')}, {row.get('price')}, 일정({row.get('class_start')} ~ {row.get('class_end')}, {row.get('class_day_time')}), 등록({row.get('register_start')} ~ {row.get('register_end')})"
            msg += '\n\n'
        msg += 'https://www.splib.or.kr/spwlib/menu/10406/program/30014/eventList.do'

        data_to_notify = [{
            'type': 'text',
            'content': msg
        }]

        return data_to_notify


if __name__ == '__main__':
    retriever = SongpaLibRetriever()
    print(retriever.retrieve())
