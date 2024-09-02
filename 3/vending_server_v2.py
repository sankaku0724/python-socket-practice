# -*- coding: utf-8 -*-
# モジュールのインポート
import socket
import datetime 
import sys

args=sys.argv

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

DrinkList = [] # Drinkリストの設定

f = Drink('milk', 300, 5)
DrinkList.append(f)
print(DrinkList[0])
f = Drink('coffee', 150, 10)
DrinkList.append(f)
print(DrinkList[1])
f = Drink('tea', 1000000, 0)
DrinkList.append(f)
print(DrinkList[2])

# 売り上げを管理
sales = 0

# 販売数を管理
SalesList = [] # Drinkリストの設定

f = Drink('milk', 300, 0)
SalesList.append(f)
f = Drink('coffee', 150, 0)
SalesList.append(f)
f = Drink('tea', 1000000, 0)
SalesList.append(f)

# クライアントへの対応処理
try:
    while True:
        client, addr = server.accept()
        while True:
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
            index_number = 0
            for drink in DrinkList:
                if received_data == drink.name:
                    index_number = drink
                    if index_number.stock>0:
                        result = "OK"
                    else:
                        result = index_number.name
            client.sendall(result.encode("utf-8"))

            # クライアントから代金を受信
            data = client.recv(BUFSIZE)
            received_data = data.decode("UTF-8")
            if received_data == "NG":
                client.close()
                break
            else:
                print("支払われた代金",received_data)

            #クライアントにその代金で購入できるかどうかを送信
            purchase = "NG"
            if int(received_data) - index_number.price == 0:
                index_number.stock -= 1
                for i in SalesList:
                    if index_number.name == i.name:
                        i.stock += 1
                purchase = "OK"
                sales += index_number.price
                client.sendall(purchase.encode("utf-8"))
            elif int(received_data) - index_number.price > 0:
                index_number.stock -= 1
                for i in SalesList:
                    if index_number.name == i.name:
                        i.stock += 1
                Change = int(received_data) - index_number.price
                sales += index_number.price
                client.sendall(str(Change).encode("utf-8"))
            else:
                purchase = "代金が足りません"
                client.sendall(purchase.encode("utf-8"))
            print("現在の売り上げ",sales)
            sales_info = ""
            print("販売数")
            for i in SalesList:
                sales_info += 'Drink: {} Number of sales: {}\n'.format(i.name,i.stock)
            print(sales_info)

            zaiko_info = ""

            print("在庫切れの商品")
            for i in DrinkList:
                if i.stock <= 0:
                    zaiko_info += 'Drink: {}\n'.format(i.name)
            print(zaiko_info)

            client.close()
            break
except KeyboardInterrupt:
    print("サーバーが停止しました。")