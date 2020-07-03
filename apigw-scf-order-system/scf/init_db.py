# -*- coding: utf-8 -*-

import sys
import logging
import psycopg2
print('Loading function')

logger = logging.getLogger()

def main_handler(event, context):
    logger.info("start main handler")

    host='xxxx'
    port= xxxx
    user='xxxx'
    password='xxxx'
    dbname='xxxx'
	
    conn = psycopg2.connect(database=dbname, user=user , password=password, host=host, port=port)
    print "Opened database successfully"

    cur = conn.cursor()

    cur.execute('''CREATE TABLE info_shop (
        shop_name VARCHAR(50) NOT NULL DEFAULT '0',
        dish VARCHAR(50) NOT NULL DEFAULT '0' ,
        price FLOAT NOT NULL DEFAULT '0' 
    );
    ''')
    print "Table info_shop created successfully"

    cur.execute("INSERT INTO info_shop (shop_name,dish,price) VALUES ('shop1', 'egg', 3),('shop2', 'egg', 3),('shop1', 'rice', 1)");

    
    cur.execute(''' CREATE TABLE info_bill (
	bill_id serial NOT NULL,
	userid INT NOT  NULL,
	shop_name VARCHAR(50) NULL ,
	dish VARCHAR(50) NULL,
	price FLOAT NULL 
    )
    ;   
    ''')
    print "Table info_bill created successfully"

    cur.execute(''' CREATE TABLE info_customer (
	userid serial  NOT NULL ,
	name VARCHAR(50) NOT NULL DEFAULT '0',
	addr VARCHAR(50) NOT NULL DEFAULT '0',
	telephone VARCHAR(50) NOT NULL DEFAULT '0'
    )
    ;
    ''')
    print "Table info_customer created successfully"

    cur.execute('''CREATE TABLE info_connectionid_shop_map (
	connection_id VARCHAR(50) NOT NULL ,
	shop_name VARCHAR(50) NOT NULL DEFAULT '' ,
	date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    ;
    ''')   
    print "Table info_connectionid_shop_map created successfully"

    conn.commit()
    conn.close()

    return "success"