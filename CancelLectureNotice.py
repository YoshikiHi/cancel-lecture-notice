# -*- coding: utf-8 -*-
import csv
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import chardet
import shutil
import filecmp
from requests_oauthlib import OAuth1Session
import json,config

def serch(url):
    html = requests.get(url)
    contents = BeautifulSoup(html.content,"html.parser")

    table = contents.findAll("table")[0]
    rows = table.findAll("tr")

    with open("cancel_list.csv","w",newline="",encoding="shift_jis") as file:
        writer = csv.writer(file)
        for row in rows:
            cancel_list = []
            for cell in row.findAll(['td']):
                cancel = cell.get_text().replace("\xa0","")
                cancel_list.append(cancel)
            if cancel_list[0] in ["IE-M","IE全専攻"]:
                writer.writerow(cancel_list)
        
    if filecmp.cmp("cancel_list.csv","cancel_list_old.csv",shallow=False):
        print("休講情報のサイトに変更点はありませんでした．")

    else: 
        shutil.copyfile("cancel_list.csv","cancel_list_old.csv")
        print("休講情報のサイトに更新がありました．")
        check_csv()

def check_csv():
    result = ""
    CK = config.CONSUMER_KEY
    CS = config.CONSUMER_SECRET
    AT = config.ACCESS_TOKEN
    ATS = config.ACCESS_TOKEN_SECRET
    twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理
    url = "https://api.twitter.com/1.1/statuses/update.json"
    twitter = OAuth1Session(CK, CS, AT, ATS)

    with open("cancel_list.csv","r") as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] in ["IE-M","IE全専攻"]:
                result += str(row[1])+": "+str(row[3])+"\r"
                print(str(row[1])+"の"+str(row[3])+"("+str(row[4])+"先生)"+"は休講です．")

        params = {"status": "【休講情報】\r休講情報のサイトの更新がありました．\r"+str(result)+"は休講です． #休講情報 #電通大"}
        req = twitter.post(url, params = params)
        if req.status_code == 200:
            print ("OK")
        else:
            print ("Error: %d" % req.status_code)

if __name__ == '__main__':
    url = "http://kyoumu.office.uec.ac.jp/kyuukou/kyuukou2.html"
    serch(url)
    
    