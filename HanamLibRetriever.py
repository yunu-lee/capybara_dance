from datetime import datetime, timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup

from Retriever import Retriever


class HanamLibRetriever(Retriever):
    def retrieve(self) -> pd.DataFrame():
        cookies = {
            'JSESSIONID': '0204E6E172FAC3E895CD36E9A86E3757',
            '_fwb': '234p2RRXB2ljOPNUJbK8Kce.1741842462506',
            'wcs_bt': '178b3b477112c9:1741844348',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko,en;q=0.9,en-US;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://www.hanamlib.go.kr/wilib/selectSchedule.do?key=874&sYear=2025&sMonth=3',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            # 'Cookie': 'JSESSIONID=0204E6E172FAC3E895CD36E9A86E3757; _fwb=234p2RRXB2ljOPNUJbK8Kce.1741842462506; wcs_bt=178b3b477112c9:1741844348',
        }

        params = {
            'key': '975',
        }

        response = requests.get(
            'https://www.hanamlib.go.kr/wilib/selectWebEdcLctreList.do',
            params=params,
            cookies=cookies,
            headers=headers,
        )

        soup = BeautifulSoup(response.text, 'html.parser')

        all_programs = []

        article = soup.select_one('#contents > table > tbody').text.splitlines()
        article = [x.strip() for x in article if x]
        for k in range(0, len(article), 7):
            try:
                chunk = article[k:k + 7]
                class_date = chunk[3].replace(' ', '').split('~')
                regi_date = chunk[4].replace(' ', '').split('~')
                program = {
                    'host': '하남위례도서관',
                    'title': chunk[2],
                    'audience': chunk[1],
                    'class_start': datetime.strptime(class_date[0], '%Y-%m-%d'),
                    'class_end': datetime.strptime(class_date[1], '%Y-%m-%d'),
                    # 'class_day_time': chunk[13],
                    # 'place': chunk[14],
                    'register_start': datetime.strptime(regi_date[0], '%Y-%m-%d%H:%M'),
                    'register_end': datetime.strptime(regi_date[1], '%Y-%m-%d%H:%M'),
                }
                all_programs.append(program)
            except Exception as e:
                print(e)

        df = pd.DataFrame(all_programs)
        self.retrieved_data = df
        return df

    def export(self):
        msg = f'{datetime.now().strftime("%Y-%m-%d")} 하남위례도서관\n\n'

        df = self.retrieved_data[self.retrieved_data['register_end'] > (datetime.now() - timedelta(days=1))]

        if df.empty:
            msg += '모집중인 강좌가 없습니다.\n\n'
        else:
            for idx, row in df.iterrows():
                msg += (f"{idx + 1}) {row.get('title')}, {row.get('audience')}, "
                        f"일정({row.get('class_start').strftime('%Y-%m-%d')} ~ {row.get('class_end').strftime('%Y-%m-%d')}, "
                        f"등록({row.get('register_start')} ~ {row.get('register_end')})")
                msg += '\n\n'

        msg += 'https://www.hanamlib.go.kr/wilib/selectWebEdcLctreList.do?key=874'

        data_to_notify = [{
            'type': 'text',
            'content': msg
        }]

        return data_to_notify


if __name__ == '__main__':
    retriever = HanamLibRetriever()
    print(retriever.retrieve())
