TOKEN = '1689696012:AAFkyT5k6VLjivBu5bBLIBq4UPq5Al_Pe2w'
NGROK_URL = 'https://ece648e89433.ngrok.io'
NGROK_PORT = 9999

BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)
LOCAL_WEBHOOK_ENDPOINT = '{}/webhook'.format(NGROK_URL)

TELEGRAM_INIT_WEBHOOK_URL = '{}/setWebhook?url={}'.format(BASE_TELEGRAM_URL, LOCAL_WEBHOOK_ENDPOINT)
TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + '/sendMessage?chat_id={}&text={}'


#bot name : lhvfood