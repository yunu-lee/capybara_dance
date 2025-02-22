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
MYCHAT_ID = os.getenv('TELEGRAM_CHAT_ID_TEST')


async def bot(df: pd.DataFrame):
    bot = telegram.Bot(TOKEN)

    csv_name = f'{datetime.now().strftime("%Y-%m-%d")}.csv'
    df.to_csv(csv_name)

    async with bot:
        # print(await bot.get_me())
        msg = f'{datetime.now().strftime("%Y-%m-%d")} 24단지 매물\n\n'

        df_1 = df[df['floor_num'] == '1'].reset_index(drop=True)
        msg += f'24평 이상 1층 매물이 {len(df_1)}개 있습니다.\n\n'
        for idx, row in df_1.iterrows():
            msg += f"{idx + 1}) {row.get('areaName')} ({row.get('pyoung'):.1f}평) {row.get('buildingName')} {row.get('floorInfo')}층 {row.get('dealOrWarrantPrc')} {row.get('direction')} {row.get('articleFeatureDesc')} {row.get('realtorName')} {row.get('cpPcArticleUrl')}"
            msg += '\n\n'

        await bot.send_message(
            text=msg,
            chat_id=MYCHAT_ID
        )

        await bot.send_document(
            document=csv_name,
            caption='24평 이상 모든 매물 정보',
            chat_id=MYCHAT_ID
        )


if __name__ == '__main__':
    nr = NaverRealestate()
    apt = nr.get_data(apt_id=104126)
    apt = apt[apt['square_meter'] > 100].sort_values(by='square_meter').reset_index(drop=True)
    asyncio.run(bot(apt))
