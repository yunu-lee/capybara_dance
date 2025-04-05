from datetime import datetime, timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from Retriever import Retriever


class SongpaLearnRetriever(Retriever):
    def retrieve(self, **kwargs) -> pd.DataFrame():
        cookies = {
            'JSESSIONID': '0uURPfVNodBq955AzJJCOouFnc0wz0VURORnGpxPYV2JYJC6vpCvqHM9a3K3TIgu.amV1c19kb21haW4vc3NlbXdhc18x',
            'WMONID': 'm7sqAGgQ330',
            '_pk_id.songpa': '5829e1d3-c92a-1d7e-6bcc-741416160082.1741416160082.b01e9480-b487-0ecc-85ed-741416160082.1741416160082.1741416686538.21',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko,en;q=0.9,en-US;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.songpa.go.kr',
            'Referer': 'https://www.songpa.go.kr/learn/youth/program/lecture_list.do',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            # 'Cookie': 'JSESSIONID=0uURPfVNodBq955AzJJCOouFnc0wz0VURORnGpxPYV2JYJC6vpCvqHM9a3K3TIgu.amV1c19kb21haW4vc3NlbXdhc18x; WMONID=m7sqAGgQ330; _pk_id.songpa=5829e1d3-c92a-1d7e-6bcc-741416160082.1741416160082.b01e9480-b487-0ecc-85ed-741416160082.1741416160082.1741416686538.21',
        }

        now = datetime.now()
        search_date_start = now.strftime('%Y-%m-%d')
        search_date_end = (now + timedelta(days=90)).strftime('%Y-%m-%d')

        data = {
            'page': '1',
            'page_grid_yn': 'Y',
            'searchKind4': '127',
            'searchVal8': '',
            'searchVal2': '',
            'searchVal5': '',
            'searchVal6': '',
            'searchVal7': '',
            'searchKind2': '',
            'searchSDate': search_date_start,
            'searchEDate': search_date_end,
            'searchVal': '',
        }

        all_program = []
        hosts = [
            {'id': '127', 'name': '송파런 위례 교육센터'},
            {'id': '28', 'name': '위례동 자치회관'},
            {'id': '47', 'name': '위례동 전산교육장'},
        ]

        for host in hosts:
            data['searchKind4'] = host.get('id')
            for i in range(1, 3):
                data['page'] = f'{i}'
                response = requests.post(
                    'https://www.songpa.go.kr/learn/youth/program/lecture_list.do',
                    cookies=cookies,
                    headers=headers,
                    data=data,
                )
                try:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    article = soup.select_one('#contents > section > div > section > div > div').text.splitlines()
                    article = [x.strip() for x in article if x][3:]

                    for k in range(0, len(article), 4):
                        try:
                            chunk = article[k:k + 4]

                            dates = re.findall(r'\d{4}-\d{2}-\d{2}', chunk[3])

                            program = {
                                'host': chunk[2].replace('/', ''),
                                'title': chunk[1],
                                'class_start': datetime.strptime(dates[2], "%Y-%m-%d"),
                                'class_end': datetime.strptime(dates[3], "%Y-%m-%d"),
                                'register_start': datetime.strptime(dates[0], "%Y-%m-%d"),
                                'register_end': datetime.strptime(dates[1], "%Y-%m-%d"),
                            }
                            all_program.append(program)
                        except Exception as e:
                            print('1', e)
                            break
                except Exception as e:
                    print('2', e)
                    break

        df = pd.DataFrame(all_program)
        df['class_start'] = pd.to_datetime(df['class_start'])
        df['class_end'] = pd.to_datetime(df['class_end'])
        df['register_start'] = pd.to_datetime(df['register_start'])
        df['register_end'] = pd.to_datetime(df['register_end'])
        self.retrieved_data = df
        return df

    def export(self):
        msg = f'{datetime.now().strftime("%Y-%m-%d")} 송파런(위례)\n\n'

        df = self.retrieved_data[self.retrieved_data['register_end'] > (datetime.now() - timedelta(days=1))]

        if df.empty:
            msg += '모집중인 강좌가 없습니다.\n\n'
        else:
            for key, group in df.groupby(by='host'):
                msg += f'{key}\n\n'
                for idx, row in group.iterrows():
                    msg += (f"{idx + 1}) {row.get('title')}, "
                            # f"{row.get('audience')}, {row.get('price')}, "
                            f"일정({row.get('class_start').strftime('%Y-%m-%d')} ~ {row.get('class_end').strftime('%Y-%m-%d')}, "
                            # f"{row.get('class_day_time')}), "
                            f"등록({row.get('register_start').strftime('%Y-%m-%d')} ~ {row.get('register_end').strftime('%Y-%m-%d')})")
                    msg += '\n\n'

        msg += 'https://www.songpa.go.kr/learn/youth/program/lecture_list.do'

        data_to_notify = [{
            'type': 'text',
            'content': msg
        }]

        return data_to_notify


if __name__ == '__main__':
    r = SongpaLearnRetriever()
    r.retrieve()
