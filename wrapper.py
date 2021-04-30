from flask import Flask, request, jsonify
from telegrambot import TelegramBot
from config import TELEGRAM_INIT_WEBHOOK_URL, NGROK_PORT
import sqlfood
import requests
import threading
import schedule
import time

wrapper = Flask(__name__)
 
# the post message
requests.get(TELEGRAM_INIT_WEBHOOK_URL)
bot = TelegramBot()


@wrapper.route('/webhook', methods=['POST'])
def index():
    req = request.get_json()
    bot.parse_webhook_data(req)
    success = bot.replay()

    return jsonify(success=success)


def credit_inc():
    schedule.every(24).hours.do(sqlfood.inc_credit)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    t1 = threading.Thread(target=credit_inc, daemon=True).start()

    print("start listening")  # the main thread
    wrapper.run(port=NGROK_PORT)
