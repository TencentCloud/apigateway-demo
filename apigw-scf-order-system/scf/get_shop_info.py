# -*- coding: utf-8 -*-

import sys
import logging
import psycopg2
print('Loading function')

logger = logging.getLogger()

def main_handler(event, context):
    logger.info("start main handler")

    Host = os.getenv('host')
    Port = os.getenv('port')
    User = os.getenv('user')
    Password = os.getenv('password')
    DB = os.getenv('dbname')
	
    conn = psycopg2.connect(database=DB, user=User, password=Password, host=Host, port=Port)
    print "Opened database successfully"

    cur = conn.cursor() 
    cur.execute("SELECT shop_name, dish, price  from info_shop")

    rows = cur.fetchall()
    shop_info = {}
    
    for row in rows:
        if shop_info.has_key(row[0]) is False:
            shop_info[row[0]] = []
        one = {}
        one["dish"] = row[1]
        one["price"] = row[2]

        print(row[0], row[1], row[2])
        print(one)
        shop_info[row[0]].append(one)


    print(shop_info)
    conn.commit()
    conn.close()

    return shop_info