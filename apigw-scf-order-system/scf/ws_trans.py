# -*- coding: utf8 -*-
import json
import requests
import datetime
import logging
import sys
import pytz
import os
import psycopg2


print('Start Transmission function')

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)

# The reverse push link for API gateway. API网关的反向推送链接 ,注意：该链接根据apigw的 回推地址
apiid = os.getenv('apiid')
sendbackHost = "http://set-websocket.cb-common.apigateway.tencentyun.com/"+apiid


Host = 'xxxx'
Port = xxx
User = 'xxxx'
Password = 'xxxx'
DB = 'xxx'



# Changing the time zone to Beijing. 更改时区为北京时区
tz = pytz.timezone('Asia/Shanghai')

def get_connection_id(connection_id):
    conn = psycopg2.connect(database=DB, user=User, password=Password, host=Host, port=Port)
    print "Opened database successfully"

    sql = 'select connection_id,shop_name from info_connectionid_shop_map where connection_id =\'%s\''%(connection_id)
    print sql
    cur = conn.cursor()
    cur.execute(sql)
    print "Table created successfully"

    rows = cur.fetchall()
    if len(rows) == 0:
        return None

    for row in rows:
        connection_id = row[0]
        shop_name = row[1]
    conn.commit()
    conn.close()
    return connection_id


def set_shop_name(connection_id, shop_name):
    conn = psycopg2.connect(database=DB, user=User, password=Password, host=Host, port=Port)
    print "Opened database successfully"
    sql = 'update  info_connectionid_shop_map set shop_name=\'%s\' where connection_id = \'%s\''%(shop_name,connection_id)
    print sql
    cur = conn.cursor()
    cur.execute(sql)
    print "Table created successfully"

    conn.commit()
    conn.close()


def send(connectionID, data):
    retmsg = {}
    retmsg['websocket'] = {}
    retmsg['websocket']['action'] = "data send"
    retmsg['websocket']['secConnectionID'] = connectionID
    retmsg['websocket']['dataType'] = 'text'
    retmsg['websocket']['data'] = data
    print("send %s to %s" % (json.dumps(data).decode('unicode-escape'), connectionID))
    r = requests.post(sendbackHost, json=retmsg)
    print(r.text)

def main_handler(event, context):
    print("event is %s" % event)
    if 'websocket' not in event.keys():
        return {"errNo": 102, "errMsg": "not found web socket"}
    # Sending message to client. 发送消息给客户端

    print("Start DB Request{%s}" % datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S    "))

    connection_id = event['websocket']['secConnectionID']

    connection_id_in_db = get_connection_id(connection_id)
    if connection_id_in_db is None:
        return "connection not regsiter"
    print("Finish DB Request {%s}" % datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"))

    data = event['websocket']['data'] + " " + " Online !!!"
    shop_name = event['websocket']['data']
    print(shop_name)
    set_shop_name(connection_id, shop_name)
    send(connection_id, data)

    return "send success"