# -*- coding: utf8 -*-
import json
import requests
import datetime
import psycopg2
import logging
import sys
import pytz
import os


print('Start Register function')

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


Host = os.getenv('host')
Port = os.getenv('port')
User = os.getenv('user')
Password = os.getenv('password')
DB = os.getenv('dbname')



#Changing the time zone to Beijing. 更改时区为北京时区
tz = pytz.timezone('Asia/Shanghai')

def record_connectionID(connectionID):
    print('Start record_connectionID function')
    print("connectionID is %s " % connectionID)

    conn = psycopg2.connect(database=DB, user=User, password=Password, host=Host, port=Port)
    print "Opened database successfully"
    cur = conn.cursor()
    time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    sql = 'INSERT INTO info_connectionid_shop_map(connection_id, date) VALUES(\'%s\',\'%s\')'%(connectionID, time)
    print(sql)
    cur.execute( sql )
    conn.commit()
    conn.close()

def main_handler(event, context):
    print("event is %s" % event)
    if 'requestContext' not in event.keys():
        return {"errNo": 101, "errMsg": "not found request context"}
    if 'websocket' not in event.keys():
        return {"errNo": 102, "errMsg": "not found web socket"}

    connectionID = event['websocket']['secConnectionID']
    retmsg = {}
    retmsg['errNo'] = 0
    retmsg['errMsg'] = "ok"
    retmsg['websocket'] = {
        "action": "connecting",
        "secConnectionID": connectionID
    }

    if "secWebSocketProtocol" in event['websocket'].keys():
        retmsg['websocket']['secWebSocketProtocol'] = event['websocket']['secWebSocketProtocol']
    if "secWebSocketExtensions" in event['websocket'].keys():
        ext = event['websocket']['secWebSocketExtensions']
        retext = []
        exts = ext.split(";")
        print(exts)
        for e in exts:
            e = e.strip(" ")
            if e == "permessage-deflate":
                # retext.append(e)
                pass
            if e == "client_max_window_bits":
                # retext.append(e+"=15")
                pass
        retmsg['websocket']['secWebSocketExtensions'] = ";".join(retext)

    # Recording the new 'connectionID' in database. 在数据库中记录新的connectionID
    print("Start DB Request {%s}" %datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"))
    record_connectionID(connectionID)
    print("Finish DB Request {%s}" % datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"))

    print("connecting: connection id:%s" % event['websocket']['secConnectionID'])
    return retmsg
