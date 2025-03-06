import os
from datetime import datetime

from dotenv import load_dotenv

from NaverRealestate import NaverRealestate
from TelegramNotifier import TelegramNotifier

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MYCHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if __name__ == '__main__':
    nr = NaverRealestate()
    apt = nr.get_data(apt_id=104126)
    apt = apt[apt['square_meter'] > 100].sort_values(by='square_meter').reset_index(drop=True)

    csv_path = f'{datetime.now().strftime("%Y-%m-%d")}.csv'
    apt.to_csv(csv_path, index=False)

    msg = f'{datetime.now().strftime("%Y-%m-%d")} 24단지 매물\n\n'

    df_1 = apt[apt['floor_num'] == '1'].reset_index(drop=True)
    msg += f'24평 이상 1층 매물이 {len(df_1)}개 있습니다.\n\n'
    for idx, row in df_1.iterrows():
        msg += f"{idx + 1}) {row.get('areaName')} ({row.get('pyoung'):.1f}평) {row.get('buildingName')} {row.get('floorInfo')}층 {row.get('dealOrWarrantPrcNum'):.1f}억 {row.get('direction')} {row.get('articleFeatureDesc')} {row.get('realtorName')} {row.get('cpPcArticleUrl')}"
        msg += '\n\n'

    notifier = TelegramNotifier(config={
        'bot_token': TOKEN,
        'chat_id': MYCHAT_ID
    })

    notifier.notify(data=[
        {
            'type': 'text',
            'content': msg
        },
        {
            'type': 'file',
            'file_path': csv_path,
            'caption': '24평 이상 모든 매물 정보'
        }
    ])
