# -*- coding: utf-8 -*- 主要是查詢網路股價 提醒價錢到了設定的金額
"""
Created on Tus Oct 05 11:00:10 2021

@author: jiangyifu
"""

from __future__ import print_function
import time
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import schedule
from pymongo import MongoClient
import urllib.parse
import datetime
import requests
from bs4 import BeautifulSoup

# Authentication Database認證資料庫
Authdb='jiangyifu_1'

line_bot_api = LineBotApi('RuiuVWm3xf/F4AxQlVUdVCLa4LKZI96gz1hRN+tK+HNF74tDqxggMspmSJzg8/ISJBT9aPbJR2eobHKoC9vYDPmLdHGA9aX0rBnrTKytPeiQwvYj229m1OznRN7U6RzGUpZNhqvRB/VqKR4I85NSLwdB04t89/1O/w1cDnyilFU=')
yourid='Ucefc5a091d5126136b4016420451ae49'
##### 資料庫連接 #####
def constructor():
    client = MongoClient('mongodb+srv://jiangyifu_1:bobby5994@cluster0.d9alp.mongodb.net/mystock?retryWrites=true&w=majority')
    db = client[Authdb]
    return db

# 抓你的股票
def show_user_stock_fountion():  
    db=constructor()
    collect = db['mystock']
    cel=list(collect.find({"data": 'care_stock'}))
    return cel

def job():
    data = show_user_stock_fountion()
    for i in data:
        stock=i['stock']
        bs=i['bs']
        price=i['price']
        
        url = 'https://tw.stock.yahoo.com/q/q?s=' + stock 
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.content, "html.parser")
        getstock= soup.find('b').text #裡面所有文字內容
        if float(getstock):
            if bs == '<':
                if float(getstock) < price:
                    get=stock + '的價格：' + getstock
                    line_bot_api.push_message(yourid, TextSendMessage(text=get))
            else:
                if float(getstock) > price:
                    get=stock + '的價格：' + getstock
                    line_bot_api.push_message(yourid, TextSendMessage(text=get))
        else:
            line_bot_api.push_message(yourid, TextSendMessage(text='這個有問題'))
second_5_j = schedule.every(10).seconds.do(job)

# 無窮迴圈
while True: 
    schedule.run_pending()
    time.sleep(1)
