import asyncio
import telegram
import os
import time

loop = asyncio.get_event_loop()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MYCHAT_ID = os.getenv('TELEGRAM_CHAT_ID_TEST')

# 메시지 보내는 함수
async def send_message(text):
    bot = telegram.Bot(TOKEN)
    async with bot:
        await bot.send_message(text=text, chat_id=MYCHAT_ID)

if __name__ == "__main__":
    print('gogo')
    loop.create_task(send_message('action test'))
    time.sleep(20)
