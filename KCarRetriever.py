from datetime import datetime, timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from Retriever import Retriever
import requests
import json



class KCarRetriever(Retriever):
    def retrieve(self) -> pd.DataFrame():
        import requests

        cookies = {
            'grb_ck@cbd6aecb': '3e475220-7d00-c8ad-a1c2-ecda8694b5c3',
            'grb_ui@cbd6aecb': '7613a0a0-c8f7-a5b6-4d8b-7b7228a2e72e',
            '_gid': 'GA1.2.2147079486.1747549496',
            'grb_id_permission@cbd6aecb': 'fail',
            'grb_ip_permission@cbd6aecb': 'fail',
            '_fwb': '83EHBMgxqMNVjAAjc5x7zV.1747549496341',
            '_kmpid': 'km|kcar.com|1747549496349|66a4ca3f-e8d4-41dc-a7b3-44ce0f3ce000',
            'dmcself_fp': 'f58702c0f00fa4ec3a4cba0240a5087a',
            '_spfp': 'sp.1.f58702c0f00fa4ec3a4cba0240a5087a.1747549498',
            '_spfp_v2_2': 'sp.2.2.1747549498.113489',
            '_ga_N2QC9KJL32': 'GS2.1.s1747549495$o1$g1$t1747551038$j0$l0$h0',
            'ab.storage.deviceId.01813139-0733-4624-b7b9-97a6152d027a': '%7B%22g%22%3A%22d2f05979-c711-2317-a92e-6d79e4514714%22%2C%22c%22%3A1747551038610%2C%22l%22%3A1747551038610%7D',
            'WMONID': 'ZDmSX3tLI_1',
            'cto_bundle': 'j376IV91V0t6RzFEOVdiRUFqWjYlMkJleldTR0M1YUN1SE8zTWdoVUtta0VDb2JMazR4VnNMcUJNcVZZWklhTEJSdzlIMCUyQmR1UW5nWVRONjA2MnplazdnSiUyRm9KQSUyQmQ5VTFIMlVLbnVSWkVYbSUyRkdnSVJlQTcyQlJwY2hPSHI0bFlOVDJvWHBFN0ZpaUhYQktHUmduWTd0N3ZZMGVBJTNEJTNE',
            '_gcl_au': '1.1.397274289.1747549496.962443965.1747551040.1747551039',
            '_ga': 'GA1.2.605271136.1747549495',
            '_gat_UA-23566107-15': '1',
            '_dc_gtm_UA-23566107-15': '1',
            '_ga_12BKR6ZT1H': 'GS2.2.s1747549497$o1$g1$t1747551117$j4$l0$h0$d1BW2NrR0hT77yByOg_XviPRX63xw-QYDBg',
            '_ga_17DVLNK818': 'GS2.1.s1747549496$o1$g1$t1747551117$j42$l0$h0$dllqwYNI0esWxmPR1uZwaKAMxl5fJcWRYXw',
            'amplitude_id_86cd6422ba1c1dd78d122ad0b1158d6akcar.com': 'eyJkZXZpY2VJZCI6IjI1NGEzNjRlLWM0OWMtNGIyNC05ZWI4LTRlZmY2ODQ4NzVhM1IiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTc0NzU0OTQ5NTQ5OCwibGFzdEV2ZW50VGltZSI6MTc0NzU1MTExNzc1NSwiZXZlbnRJZCI6MTMsImlkZW50aWZ5SWQiOjQsInNlcXVlbmNlTnVtYmVyIjoxN30=',
            'ab.storage.sessionId.01813139-0733-4624-b7b9-97a6152d027a': '%7B%22g%22%3A%22ff4d3d64-e7cf-6ff9-ede9-63ea5342ceb2%22%2C%22e%22%3A1747552917757%2C%22c%22%3A1747551038621%2C%22l%22%3A1747551117757%7D',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ko,en;q=0.9,en-US;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://m.kcar.com',
            'priority': 'u=1, i',
            'referer': 'https://m.kcar.com/',
            'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
            # 'cookie': 'grb_ck@cbd6aecb=3e475220-7d00-c8ad-a1c2-ecda8694b5c3; grb_ui@cbd6aecb=7613a0a0-c8f7-a5b6-4d8b-7b7228a2e72e; _gid=GA1.2.2147079486.1747549496; grb_id_permission@cbd6aecb=fail; grb_ip_permission@cbd6aecb=fail; _fwb=83EHBMgxqMNVjAAjc5x7zV.1747549496341; _kmpid=km|kcar.com|1747549496349|66a4ca3f-e8d4-41dc-a7b3-44ce0f3ce000; dmcself_fp=f58702c0f00fa4ec3a4cba0240a5087a; _spfp=sp.1.f58702c0f00fa4ec3a4cba0240a5087a.1747549498; _spfp_v2_2=sp.2.2.1747549498.113489; _ga_N2QC9KJL32=GS2.1.s1747549495$o1$g1$t1747551038$j0$l0$h0; ab.storage.deviceId.01813139-0733-4624-b7b9-97a6152d027a=%7B%22g%22%3A%22d2f05979-c711-2317-a92e-6d79e4514714%22%2C%22c%22%3A1747551038610%2C%22l%22%3A1747551038610%7D; WMONID=ZDmSX3tLI_1; cto_bundle=j376IV91V0t6RzFEOVdiRUFqWjYlMkJleldTR0M1YUN1SE8zTWdoVUtta0VDb2JMazR4VnNMcUJNcVZZWklhTEJSdzlIMCUyQmR1UW5nWVRONjA2MnplazdnSiUyRm9KQSUyQmQ5VTFIMlVLbnVSWkVYbSUyRkdnSVJlQTcyQlJwY2hPSHI0bFlOVDJvWHBFN0ZpaUhYQktHUmduWTd0N3ZZMGVBJTNEJTNE; _gcl_au=1.1.397274289.1747549496.962443965.1747551040.1747551039; _ga=GA1.2.605271136.1747549495; _gat_UA-23566107-15=1; _dc_gtm_UA-23566107-15=1; _ga_12BKR6ZT1H=GS2.2.s1747549497$o1$g1$t1747551117$j4$l0$h0$d1BW2NrR0hT77yByOg_XviPRX63xw-QYDBg; _ga_17DVLNK818=GS2.1.s1747549496$o1$g1$t1747551117$j42$l0$h0$dllqwYNI0esWxmPR1uZwaKAMxl5fJcWRYXw; amplitude_id_86cd6422ba1c1dd78d122ad0b1158d6akcar.com=eyJkZXZpY2VJZCI6IjI1NGEzNjRlLWM0OWMtNGIyNC05ZWI4LTRlZmY2ODQ4NzVhM1IiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTc0NzU0OTQ5NTQ5OCwibGFzdEV2ZW50VGltZSI6MTc0NzU1MTExNzc1NSwiZXZlbnRJZCI6MTMsImlkZW50aWZ5SWQiOjQsInNlcXVlbmNlTnVtYmVyIjoxN30=; ab.storage.sessionId.01813139-0733-4624-b7b9-97a6152d027a=%7B%22g%22%3A%22ff4d3d64-e7cf-6ff9-ede9-63ea5342ceb2%22%2C%22e%22%3A1747552917757%2C%22c%22%3A1747551038621%2C%22l%22%3A1747551117757%7D',
        }

        json_data = {
            'enc': 'gEa/4VFh8fIVdgV57tSPemDQF6QbljIynqg9F6X9NotGCVjf3dWfiFeUCeUpR454m5oQjKo9QuxNie/eaPuLcleWt+f3XB+hWxS8KmrqHv4HaY32DXe8G8C3xzjVEdWlXh68Ckb5graX2rX7hmGco4bGSua1TptSk2dn9bIGENgAaytmTPBQ0HfpP22ABgydUve8TZg6qziqhx4orOxLwgBVzA++iCbRI2P1q2g5NSn8zoUof8OW1TF3NA9qCtuuJos/j2zwapYC+Q7CgliuzOkBT0i9TcfvBPb+6UqH4h/RqCRVPIFlrUrTaDP+dbRVjVeeKwcKFf8lwv0NOyfEhrqhVw4uzGSzF8fm4bchrpB9W5rYki0TkCZOUjWGw3z72yEzV8hxi/flX529Uny7Ow==',
        }

        response = requests.post('https://mapi.kcar.com/bc/search/list/drct', cookies=cookies, headers=headers,
                                 json=json_data)

        # Note: json_data will not be serialized by requests
        # exactly as it was in the original request.
        # data = '{"enc":"gEa/4VFh8fIVdgV57tSPemDQF6QbljIynqg9F6X9NotGCVjf3dWfiFeUCeUpR454m5oQjKo9QuxNie/eaPuLcleWt+f3XB+hWxS8KmrqHv4HaY32DXe8G8C3xzjVEdWlXh68Ckb5graX2rX7hmGco4bGSua1TptSk2dn9bIGENgAaytmTPBQ0HfpP22ABgydUve8TZg6qziqhx4orOxLwgBVzA++iCbRI2P1q2g5NSn8zoUof8OW1TF3NA9qCtuuJos/j2zwapYC+Q7CgliuzOkBT0i9TcfvBPb+6UqH4h/RqCRVPIFlrUrTaDP+dbRVjVeeKwcKFf8lwv0NOyfEhrqhVw4uzGSzF8fm4bchrpB9W5rYki0TkCZOUjWGw3z72yEzV8hxi/flX529Uny7Ow=="}'
        # response = requests.post('https://mapi.kcar.com/bc/search/list/drct', cookies=cookies, headers=headers, data=data)
        data = json.loads(response.text)

        return data

    def export(self):
        # msg = f'{datetime.now().strftime("%Y-%m-%d")} 송파런(위례)\n\n'
        #
        # df = self.retrieved_data[self.retrieved_data['register_end'] > (datetime.now() - timedelta(days=1))]
        #
        # if df.empty:
        #     msg += '모집중인 강좌가 없습니다.\n\n'
        # else:
        #     for key, group in df.groupby(by='host'):
        #         msg += f'{key}\n\n'
        #         for idx, row in group.iterrows():
        #             msg += (f"{idx + 1}) {row.get('title')}, "
        #                     # f"{row.get('audience')}, {row.get('price')}, "
        #                     f"일정({row.get('class_start').strftime('%Y-%m-%d')} ~ {row.get('class_end').strftime('%Y-%m-%d')}, "
        #                     # f"{row.get('class_day_time')}), "
        #                     f"등록({row.get('register_start').strftime('%Y-%m-%d')} ~ {row.get('register_end').strftime('%Y-%m-%d')})")
        #             msg += '\n\n'
        #
        # msg += 'https://www.songpa.go.kr/learn/youth/program/lecture_list.do'
        #
        # data_to_notify = [{
        #     'type': 'text',
        #     'content': msg
        # }]

        return data_to_notify


if __name__ == '__main__':
    r = KCarRetriever()
    r.retrieve()
