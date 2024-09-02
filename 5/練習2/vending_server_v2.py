# -*- coding: utf-8 -*-
# モジュールのインポート
import socket
import datetime 
import sys
import threading

args=sys.argv

lock = threading.Lock()

# グローバル変数

BUFSIZE = 4096    # 受信バッファの大きさ
PORT=int(args[1])

# メイン実行部
# ソケットの作成
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# アドレスの設定
server.bind(("",PORT))
# 接続の待ち受け
server.listen()

class Drink:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
    def __str__(self): # 文字列化メソッド
        return "Drink: " + self.name + " " + str(self.price) + " " + str(self.stock)


# 商品リストをファイルから読み込む関数
def load_drink_list(filename):
    drink_list = []
    SalesList = []
    try:
        with open(filename, 'r',encoding = "utf-8-sig") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    name, price, stock = parts
                    drink = Drink(name, int(price), int(stock))
                    drink_list.append(drink)
                    salesdrink = Drink(name, 0, 0)
                    SalesList.append(salesdrink)
    except FileNotFoundError:
        print("商品リストファイルが見つかりません。")
    return drink_list,SalesList

# 商品リストファイル名
drink_list_filename = "商品リスト.csv"
DrinkList,SalesList = load_drink_list(drink_list_filename)

# 売り上げを管理
sales = 0


def stock_handler(lock, client,DrinkList,SalesList):  
    purchase = ""
    global sales
    while True:
        print("send drinks start")
        # クライアントに商品リストを送信
        drink_info = ""
        for drink in DrinkList:
            drink_info += 'Drink: {} Price: {} Stock: {}\n'.format(drink.name,drink.price,drink.stock)
        client.sendall(drink_info.encode("utf-8"))
        # クライアントから商品を受信
        data = client.recv(BUFSIZE)
        received_data = data.decode("UTF-8")
        print("商品名",received_data)

        # クライアントに商品が存在するかどうかを送信
        result = "NG"
        choose_drink = False
        for drink in DrinkList:
            if drink.name == received_data:
                choose_drink = drink
                if choose_drink.stock>0:
                    result = "OK"
                else:
                    result = received_data

        
        client.sendall(result.encode("utf-8"))
        if result != "OK":
            continue
        
        while True:
            #クライアントにその代金で購入できるかどうかを送信
            data = client.recv(BUFSIZE)
            received_data = data.decode("UTF-8")
            print("支払われた代金",received_data,"\n")

            if int(received_data) - choose_drink.price == 0 and choose_drink.stock > 0:
                lock.acquire()
                choose_drink.stock -= 1
                for i in SalesList:
                    if choose_drink.name == i.name:
                        i.stock += 1
                sales += choose_drink.price
                lock.release()
                purchase = "OK"
                client.sendall(purchase.encode("utf-8"))
                result_msg()
                client.close()
                break
            elif int(received_data) - choose_drink.price > 0 and choose_drink.stock > 0:
                lock.acquire()
                choose_drink.stock -= 1
                for i in SalesList:
                    if choose_drink.name == i.name:
                        i.stock += 1
                sales += choose_drink.price
                lock.release()
                Change = int(received_data) - choose_drink.price
                client.sendall(str(Change).encode("utf-8"))
                result_msg()
                client.close()
                break
            elif int(received_data) - choose_drink.price < 0 and choose_drink.stock > 0:
                purchase = "代金が足りません"
                client.sendall(purchase.encode("utf-8"))
                continue
            else:
                purchase = "NG"
                client.sendall(purchase.encode("utf-8"))
                break
        if purchase == "NG":
            continue
        break

def result_msg():
        #売上の表示
        print("現在の売り上げ",sales,"\n")

        #販売数の表示
        sales_info = ""
        print("販売数")
        for i in SalesList:
            sales_info += '{}:{}\n'.format(i.name,i.stock)
        print(sales_info)

        #在庫切れの商品の表示
        zaiko_info = ""
        print("在庫切れの商品")
        for i in DrinkList:
            if i.stock <= 0:
                zaiko_info += '{}\n'.format(i.name)
        print(zaiko_info)


# クライアントへの対応処理
try:
    while True:
        client, addr = server.accept()
        p = threading.Thread(target = stock_handler,args = (lock,client,DrinkList,SalesList))
        p.start()
        print(p)
except KeyboardInterrupt:
    print("サーバーが停止しました。")
    client.close()