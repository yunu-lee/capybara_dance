import os

import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def get_chat_id():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url)
    data = response.json()
    print(data)

    # if data['ok'] and data['result']:
    #     # 가장 최근 메시지의 채팅 ID를 가져옵니다.
    #     chat_id = data['result'][-1]['message']['chat']['id']
    #     print(f"Chat ID: {chat_id}")
    #     return chat_id
    # else:
    #     print("Failed to get chat ID.")
    #     return None


if __name__ == '__main__':
    get_chat_id()
