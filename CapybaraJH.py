import asyncio
import os

import pandas as pd
import telegram
from dotenv import load_dotenv
from datetime import datetime

from NaverRealestate import NaverRealestate

load_dotenv()
loop = asyncio.get_event_loop()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MYCHAT_ID = os.getenv('TELEGRAM_CHAT_ID_JH')


async def bot(df: pd.DataFrame):
    bot = telegram.Bot(TOKEN)

    csv_name = f'{datetime.now().strftime("%Y-%m-%d")}.csv'
    df.to_csv(csv_name, index=False)

    async with bot:
        # print(await bot.get_me())
        df = df[(df['pyoung'] > 20) & (df['pyoung'] < 30)]
        result = df.groupby(['articleName', 'pyoung']).apply(
            lambda x: x.nsmallest(2, 'dealOrWarrantPrcNum')).reset_index(drop=True)

        msg = f'{datetime.now().strftime("%Y-%m-%d")} 부동산 정보 (20평대, 평수별 최저가 2개씩)\n\n\n'
        for key, group in result.groupby(by='articleName'):
            msg += f'# {key}\n\n'
            for idx, row in group.reset_index(drop=True).iterrows():
                msg += f"{idx + 1}) {row.get('areaName')} ({row.get('pyoung'):.1f}평) {row.get('buildingName')} {row.get('floorInfo')}층 {row.get('dealOrWarrantPrcNum'):.1f}억 {row.get('direction')} {row.get('realtorName')} {row.get('cpPcArticleUrl')}"
                msg += '\n\n'
            msg += '\n'

        print('sending a message')
        await bot.send_message(
            text=msg,
            chat_id=MYCHAT_ID
        )

        print('sending a document')
        await bot.send_document(
            document=csv_name,
            caption='모든 매물 정보',
            chat_id=MYCHAT_ID
        )


if __name__ == '__main__':
    apt_id = [
        117329,  # 목동 센트럴아이파크위브
        127424,  # 철산역 롯데캐슬&SK VIEW 클래스티지
        109524,  # 광명역써밋플레이스(주상복합)
        109177,  # 광명역파크자이(주상복합)
        174562,  # 이문아이파크자이(3-1BL)
    ]
    nr = NaverRealestate()
    all_apt = pd.DataFrame()
    for a in apt_id:
        apt = nr.get_data(apt_id=a)
        all_apt = pd.concat([all_apt, apt], ignore_index=True)

    asyncio.run(bot(all_apt))
