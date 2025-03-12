import os

from dotenv import load_dotenv

from SongpaLearnRetriever import SongpaLearnRetriever
from SongpaLibRetriever import SongpaLibRetriever
from TelegramNotifier import TelegramNotifier

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MYCHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if __name__ == '__main__':
    notifier = TelegramNotifier(config={
        'bot_token': TOKEN,
        'chat_id': MYCHAT_ID
    })

    # songpa lib
    retriever = SongpaLibRetriever()
    _ = retriever.retrieve()
    data_to_notify = retriever.export()
    notifier.notify(data=data_to_notify)

    # songpa learn
    retriever = SongpaLearnRetriever()
    _ = retriever.retrieve()
    data_to_notify = retriever.export()
    notifier.notify(data=data_to_notify)
