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
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def __str__(self): # 文字列化メソッド
        return "Drink: " + self.name + " " + str(self.price)

DrinkList = [] # Drinkリストの設定

f = Drink('milk', 300)
DrinkList.append(f)
print(DrinkList[0])
f = Drink('coffee', 150)
DrinkList.append(f)
print(DrinkList[1])

# クライアントへの対応処理
try:
    while True:
        client, addr = server.accept()
        while True:
            # クライアントに商品リストを送信
            drink_info = ""
            for drink in DrinkList:
                drink_info += 'Drink: {} {}\n'.format(drink.name,drink.price)
            client.sendall(drink_info.encode("utf-8"))
            # クライアントから商品を受信
            data = client.recv(BUFSIZE)
            received_data = data.decode("UTF-8")
            print(received_data)
            
            result = "NG"
            for drink in DrinkList:
                if received_data == drink.name:
                    result = "OK"
            client.sendall(result.encode("utf-8"))
            client.close()
            break
except KeyboardInterrupt:
    print("サーバーが停止しました。")