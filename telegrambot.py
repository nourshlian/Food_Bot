from config import TELEGRAM_SEND_MESSAGE_URL
import requests
import time
import json
import sqlfood

food_list = ["pizza", "falafel", "tost"]


class TelegramBot:

    def __init__(self):

        self._chat_id = None  # chat id for specific conversation
        self._text = None  # incoming message
        self._name = None  # the name of the user that had sent the message
        self._orders = []

    def parse_webhook_data(self, data):

        message = data.get('message')
        if message is None:
            message = data.get('edited_message')

        # parsing the data
        chatid = message['chat']['id']
        in_msg = message.get('text')  # if it have one
        name = message['from']['first_name']

        self._chat_id = chatid
        if in_msg is None:
            self.incoming_message_text = ""
        else:
            self.incoming_message_text = in_msg.lower()
        self._name = name

    # what to replay to the message parsing specific messages and send the message to the telegram servers
    def replay(self):

        if self.incoming_message_text == '/start':
            self.outgoing_message_text = "Hello I see you are new, you need to register first.\nif you what to become " \
                                         "one of our clients please replay with /register. "

        elif self.incoming_message_text == '/register':
            try:
                sqlfood.register(self._chat_id, self._name)
                self.outgoing_message_text = 'wellcome {}\nif you want to order replay with /order \nreplay with /help to ' \
                                             'see available commands.'.format(self._name)
            except:
                self.outgoing_message_text = "your all ready in"

        elif self.incoming_message_text == '/order':
            self.outgoing_message_text = "what do you want to order?\nPizza\nfalafel\ntost"

        elif self.incoming_message_text in food_list:
            order = self.incoming_message_text
            ans = sqlfood.makeOrder(self._chat_id, order)
            if ans:
                self.outgoing_message_text = "you'r {} will be ready in 30 minutes\nThanks for you'r patient".format(
                    order)
            else:
                self.outgoing_message_text = "dear {} you can order only one time a day.".format(self._name)

        elif self.incoming_message_text == '/order_history':
            history = sqlfood.orders_history(self._chat_id)
            msg = ""
            for order in history.split(","):
                msg += order.strip() + "\n"
            self.outgoing_message_text = msg

        elif self.incoming_message_text == '/setmeasadmin':
            self.outgoing_message_text = "please enter admin password"

        elif self.incoming_message_text == 'thisistheadminpassword':
            sqlfood.setadmin(self._chat_id)
            self.outgoing_message_text = "your an Admin now"

        elif self.incoming_message_text == '/allordershistory':
            ans = history = sqlfood.allorders(self._chat_id)
            if ans == None:
                self.outgoing_message_text = "your not an Admin"
            else:
                msg = ""
                for user, orders in history.items():
                    msg += "user : " + user + " \nordered : " + orders + "\n\n"
                self.outgoing_message_text = msg


        elif self.incoming_message_text == '/help':
            self.outgoing_message_text = "/order -> make an order\n/order_history -> your order " \
                                         "history\n/setMeAsAdmin -> set you as admin (password " \
                                         "needed)\n/allOrdersHistory -> see the history of all users (admin only) "

        else:
            self.outgoing_message_text = "/order -> make an order\n/order_history -> your order " \
                                         "history\n/setMeAsAdmin -> set you as admin (password " \
                                         "needed)\n/allOrdersHistory -> see the history of all users (admin only) "

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self._chat_id, self.outgoing_message_text))

        if_answerd = (res.status_code == 200)

        return if_answerd
