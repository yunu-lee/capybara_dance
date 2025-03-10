import asyncio
import os
import time

import telegram

from Notifier import Notifier


class TelegramNotifier(Notifier):
    def __init__(self, config: dict):
        super().__init__(config)
        self.bot_token = config.get('bot_token')
        self.chat_id = config.get('chat_id')
        if not self.bot_token or not self.chat_id:
            raise AttributeError('invalid config')

    def notify(self, data: list):
        asyncio.run(self.bot_send(data))

    async def bot_send(self, data: list):
        bot = telegram.Bot(self.bot_token)

        for d in data:
            if d.get('type') == 'text':
                print('sending a text message')
                await bot.send_message(
                    text=d.get('content'),
                    chat_id=self.chat_id
                )
            elif d.get('type') == 'file':
                print('sending a file')
                await bot.send_document(
                    document=d.get('file_path'),
                    caption=d.get('caption'),
                    chat_id=self.chat_id
                )
            elif d.get('type') == 'image':
                print('sending a image')
                await bot.send_photo(
                    photo=d.get('file_path'),
                    caption=d.get('caption'),
                    chat_id=self.chat_id
                )
            else:
                print('unsupported type')

            time.sleep(1)

