import os

def main():
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    print(f"My secret key is {TELEGRAM_BOT_TOKEN}")

if __name__ == "__main__":
    main()
