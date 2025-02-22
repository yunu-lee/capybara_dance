import json
import re

import pandas as pd
import requests


class NaverRealestate:
    def __init__(self):
        pass

    def get_data(self, apt_id: int):
        cookies = {
            'NAC': '89DJBUwys8Bd',
            'NNB': 'S7CRYINPWEGWO',
            'ASID': 'deeee25a00000192e31a4cbe00000048',
            'tooltipDisplayed': 'true',
            'nhn.realestate.article.rlet_type_cd': 'A01',
            'nhn.realestate.article.trade_type_cd': '""',
            'nhn.realestate.article.ipaddress_city': '1100000000',
            '_fwb': '2mcS9G7eaCBuLEev7leX4.1740151266212',
            'NACT': '1',
            'landHomeFlashUseYn': 'Y',
            'SRT30': '1740151267',
            '_fwb': '2mcS9G7eaCBuLEev7leX4.1740151266212',
            'nid_inf': '1999580738',
            'NID_AUT': 'H0OlYPE1Ibplovq8Vr0yZZ7HA+exn1eGk4FeWyHW9oZdU1LjniOy6mgxLgwFivnP',
            'NID_SES': 'AAABrBd6+J5QeHkdroDfZFdYh/pUUY0nOt44PAn0ywfxqSFfFXsPcBQ9CYrH2T7s//gjnIX1QeoyGExxQWFwSvID/lmeOfiJEPW3zNLlpsJiD4gEMPYlvYC73kuBfzURDArbZsWgVFg+PT/8EDO24YRw9nR2LSqYVmR3vjsmCzYajQXJ/OeZBAxIIodbtI5dx9++MOb2tsxXsVd40Y+S8t3y/lQj18VuqnTL4IPPLkN5RFHVwzr9Z4xrTiv3V+T+1ao4gBKlGRdKrh8ALrTeam1KwaPXpp+ZV01O/26Kgh3rQJJgS1sVnoWZyZN6zIjMXKrCo7mHBdmpezd0UXU3LZ8y5DwSijz2/e19dj1EbtB5HLZHiSiwwv3t2AWkv9Sn5eUarXb54khisk9mXu9qbSpeX3BjBjPBJHfx0JrJSEGs3GdxhcllZXHSG4AqGLSsAFE82D19XhYiVLu9AkTPkZexZcfGcjA1PkbmnG73zLP0n3BHjCctCc+WV8jdorZiZnw6Qaqsa276sKQOgMFKhvr9foSIZi4TWeJKQK9bx5irDzPn5Hk3XOoQ3+j30+JW/cDB7Q==',
            'NID_JKL': 'zKYvCUYa4tlSgi3SN04Yus1d7vrlr1Ew6xMkYltEbuI=',
            'realestate.beta.lastclick.cortar': '1171000000',
            'REALESTATE': 'Sat%20Feb%2022%202025%2000%3A21%3A30%20GMT%2B0900%20(Korean%20Standard%20Time)',
            'BUC': 'vgjeZTmblDd_Moc7zv-ckICJ_wL5zYqkd9bhmZ1Z6bc=',
        }

        headers = {
            'accept': '*/*',
            'accept-language': 'ko,en;q=0.9,en-US;q=0.8',
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NDAxNTEyOTAsImV4cCI6MTc0MDE2MjA5MH0.PNq9iW5xFKBUo-1hJYOc7ZgivS5iMQCJd9yrw9TgaGE',
            'priority': 'u=1, i',
            'referer': 'https://new.land.naver.com/complexes/104126?ms=37.4757163,127.1375238,16&a=APT&e=RETAIL&ad=true',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
            # 'cookie': 'NAC=89DJBUwys8Bd; NNB=S7CRYINPWEGWO; ASID=deeee25a00000192e31a4cbe00000048; tooltipDisplayed=true; nhn.realestate.article.rlet_type_cd=A01; nhn.realestate.article.trade_type_cd=""; nhn.realestate.article.ipaddress_city=1100000000; _fwb=2mcS9G7eaCBuLEev7leX4.1740151266212; NACT=1; landHomeFlashUseYn=Y; SRT30=1740151267; _fwb=2mcS9G7eaCBuLEev7leX4.1740151266212; nid_inf=1999580738; NID_AUT=H0OlYPE1Ibplovq8Vr0yZZ7HA+exn1eGk4FeWyHW9oZdU1LjniOy6mgxLgwFivnP; NID_SES=AAABrBd6+J5QeHkdroDfZFdYh/pUUY0nOt44PAn0ywfxqSFfFXsPcBQ9CYrH2T7s//gjnIX1QeoyGExxQWFwSvID/lmeOfiJEPW3zNLlpsJiD4gEMPYlvYC73kuBfzURDArbZsWgVFg+PT/8EDO24YRw9nR2LSqYVmR3vjsmCzYajQXJ/OeZBAxIIodbtI5dx9++MOb2tsxXsVd40Y+S8t3y/lQj18VuqnTL4IPPLkN5RFHVwzr9Z4xrTiv3V+T+1ao4gBKlGRdKrh8ALrTeam1KwaPXpp+ZV01O/26Kgh3rQJJgS1sVnoWZyZN6zIjMXKrCo7mHBdmpezd0UXU3LZ8y5DwSijz2/e19dj1EbtB5HLZHiSiwwv3t2AWkv9Sn5eUarXb54khisk9mXu9qbSpeX3BjBjPBJHfx0JrJSEGs3GdxhcllZXHSG4AqGLSsAFE82D19XhYiVLu9AkTPkZexZcfGcjA1PkbmnG73zLP0n3BHjCctCc+WV8jdorZiZnw6Qaqsa276sKQOgMFKhvr9foSIZi4TWeJKQK9bx5irDzPn5Hk3XOoQ3+j30+JW/cDB7Q==; NID_JKL=zKYvCUYa4tlSgi3SN04Yus1d7vrlr1Ew6xMkYltEbuI=; realestate.beta.lastclick.cortar=1171000000; REALESTATE=Sat%20Feb%2022%202025%2000%3A21%3A30%20GMT%2B0900%20(Korean%20Standard%20Time); BUC=vgjeZTmblDd_Moc7zv-ckICJ_wL5zYqkd9bhmZ1Z6bc=',
        }
        all_df = pd.DataFrame()
        for page in range(1, 100):
            response = requests.get(
                f'https://new.land.naver.com/api/articles/complex/{apt_id}?realEstateType=APT&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=104126&buildingNos=&areaNos=&type=list&order=rank',
                cookies=cookies,
                headers=headers,
            )

            print(page, response.text)
            data = json.loads(response.text)
            df = pd.DataFrame(data.get('articleList'))
            all_df = pd.concat([all_df, df])
            if data.get('isMoreData') is False:
                break
        if all_df.empty:
            return all_df

        apt_df = all_df[[
            # 'articleNo',
            # 'articleName',
            # 'articleStatus', 'realEstateTypeCode',       'realEstateTypeName', 'articleRealEstateTypeCode',       'articleRealEstateTypeName', 'tradeTypeCode',
            # 'tradeTypeName',
            # 'verificationTypeCode',
            'floorInfo',
            # 'priceChangeState', 'isPriceModification',
            'dealOrWarrantPrc', 'areaName',
            # 'area1', 'area2',
            'direction',
            # 'articleConfirmYmd',
            # 'siteImageCount',
            'articleFeatureDesc',
            # 'tagList',
            'buildingName',
            # 'sameAddrCnt', 'sameAddrDirectCnt', 'sameAddrMaxPrc', 'sameAddrMinPrc', 'cpid', 'cpName',
            'cpPcArticleUrl',
            # 'cpPcArticleBridgeUrl',
            # 'cpPcArticleLinkUseAtArticleTitleYn', 'cpPcArticleLinkUseAtCpNameYn',
            # 'cpMobileArticleUrl', 'cpMobileArticleLinkUseAtArticleTitleYn',
            # 'cpMobileArticleLinkUseAtCpNameYn', 'latitude', 'longitude', 'isLocationShow',
            'realtorName',
            # 'realtorId', 'tradeCheckedByOwner',
            # 'isDirectTrade', 'isInterest', 'isComplex', 'detailAddress',
            # 'detailAddressYn', 'isVrExposed', 'representativeImgUrl',
            # 'representativeImgTypeCode', 'representativeImgThumb'
        ]].reset_index(drop=True)

        apt_df['floor_num'] = apt_df['floorInfo'].apply(lambda x: x.split('/')[0])
        apt_df['square_meter'] = apt_df['areaName'].apply(
            lambda x: int(re.match(r'\d+', x).group()) if re.match(r'\d+', x) else None)
        apt_df['pyoung'] = apt_df['square_meter'].apply(lambda x: x * 0.3025 if x else x)
        return apt_df


if __name__ == '__main__':
    nr = NaverRealestate()
    print(nr.get_data(apt_id=104126))
