import asyncio
import telegram
import os
import time

loop = asyncio.get_event_loop()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MYCHAT_ID = os.getenv('TELEGRAM_CHAT_ID_TEST')

import asyncio
import telegram


async def main():
    bot = telegram.Bot("TOKEN")
    async with bot:
        print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main())
