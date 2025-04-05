from datetime import datetime, timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup

from Retriever import Retriever


class SungnamLibRetriever(Retriever):
    def retrieve(self, **kwargs) -> pd.DataFrame():
        cookies = {
            'SCOUTER': 'x53s7vn3c6933q',
            'JSESSIONID': '27FF26E9662DAC9BFBF02F983DE1CF4A.tomcat11',
            'wcCookie': '775a0310b91c848b0bb17c3c12edf9ad3d6a938c9f396313c272c431e3c9951a',
            '_fwb': '45xZGUcG9AKFeiarCTYENG.1742188418424',
            'wcs_bt': '8dbe8a27324cf8:1742188505',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko,en;q=0.9,en-US;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://sugang.seongnam.go.kr',
            'Referer': 'https://sugang.seongnam.go.kr/ilms/learning/learningList.do',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            # 'Cookie': 'SCOUTER=x53s7vn3c6933q; JSESSIONID=27FF26E9662DAC9BFBF02F983DE1CF4A.tomcat11; wcCookie=775a0310b91c848b0bb17c3c12edf9ad3d6a938c9f396313c272c431e3c9951a; _fwb=45xZGUcG9AKFeiarCTYENG.1742188418424; wcs_bt=8dbe8a27324cf8:1742188505',
        }

        data = {
            'office_id': '',
            'searchUseYn': 'Y',
            'searchCondition3': 'OFFICE_00001530',
            'searchCondition': '0',
            'searchKeyword': '위례도서관',
            'office_area_gu': '',
            'office_area_dong': '',
            '_office_type_arr': [
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
                'on',
            ],
            'a_search_ch': '',
            'b_search_arr': '',
            'c_search_ch': '',
            'h_search_ch': '',
            'd_search_ch': '',
            'i_search_ch': '',
            'e_search_arr': '',
            'f_search_arr': '',
            '_learning_recruitment_method_arr': [
                'on',
                'on',
                'on',
            ],
            '_learning_on_off_type_arr': [
                'on',
                'on',
                'on',
            ],
            'search_sort_by': '',
            'search_sort_order': '',
            'pageUnit': '50',
            'pageIndex': '1',
        }

        response = requests.post(
            'https://sugang.seongnam.go.kr/ilms/learning/learningList.do',
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False
        )
        soup = BeautifulSoup(response.text, 'html.parser')

        all_programs = []

        article = soup.select_one(f'#bbsList > tbody').text.splitlines()
        article = [x.strip() for x in article if x]
        article = [x for x in article if x != '']
        col_len = 16
        for k in range(0, len(article), col_len):
            try:
                chunk = article[k:k + col_len]
                program = {
                    'host': '성남위례도서관',
                    'title': chunk[1],
                    'class_start': datetime.strptime(chunk[6].replace('교육기간', ''), '%y.%m.%d'),
                    'class_end': datetime.strptime(chunk[8], '%y.%m.%d'),
                    'class_type': chunk[10],
                    'register_member': chunk[12],
                    'register_status': chunk[14],
                }
                all_programs.append(program)
            except Exception as e:
                print(e)

        df = pd.DataFrame(all_programs)
        self.retrieved_data = df
        return df

    def export(self):
        msg = f'{datetime.now().strftime("%Y-%m-%d")} 성남위례도서관\n\n'

        df = self.retrieved_data[self.retrieved_data['class_start'] > (datetime.now() - timedelta(days=1))]

        if df.empty:
            msg += '모집중인 강좌가 없습니다.\n\n'
        else:
            for idx, row in df.iterrows():
                msg += (f"{idx + 1}) {row.get('title')}, 일정({row.get('class_start').strftime('%Y-%m-%d')} ~ {row.get('class_end').strftime('%Y-%m-%d')}), "
                        f"{row.get('register_status')}, {row.get('register_member')}")
                msg += '\n\n'

        msg += 'https://sugang.seongnam.go.kr/ilms/learning/learningList.do'

        data_to_notify = [{
            'type': 'text',
            'content': msg
        }]

        return data_to_notify


if __name__ == '__main__':
    retriever = SungnamLibRetriever()
    print(retriever.retrieve())
