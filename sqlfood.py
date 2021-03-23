import mysql.connector
from datetime import datetime

db = mysql.connector.connect(host="127.0.0.1",user="root",passwd="1234",database="lhvfood")

q = db.cursor(buffered=True)



def register(chat_id,name):
    q.execute('INSERT INTO foodOrders (id,name,credit,admin) VALUES (%s,%s,%s,%s)',(chat_id,name,1,0))
    db.commit()

def makeOrder(chat_id,order):
    quere = "select credit, food_order from foodOrders where id = {}".format(chat_id)
    q.execute(quere)
    history = ""
    for x in q:
        if x[1] is not None:
            history = history + x[1]
        if x[0] == 0:
            return False
    date = datetime.today().strftime('%Y-%m-%d')
    orderinfo = date +" "+ order +", "
    history += orderinfo
    quere = "UPDATE foodOrders SET food_order = '{}', credit = 0 where id = {}".format(history,chat_id)
    q.execute(quere)
    db.commit()
    return True



def orders_history(chat_id):
    q.execute("select food_order from foodOrders where id = {}".format(chat_id))
    history = ""
    for x in q:
        history = x[0]
    return history

def setadmin(chat_id):
    quere = "UPDATE foodOrders SET admin = 1 where id = {}".format(chat_id)
    q.execute(quere)
    db.commit()


def allorders(chat_id):
    q.execute("select admin from foodOrders where id = {}".format(chat_id))
    for x in q:
        if x[0] == 0:
            return None
    else:
        q.execute("select name,food_order from foodOrders")
        ans = {}
        for x in q:
            ans[x[0]] = x[1][:-2]

        return ans

def inc_credit():
    print("done")
    q.execute("UPDATE foodOrders SET credit=1")
    db.commit()


