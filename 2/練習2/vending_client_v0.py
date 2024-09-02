# -*- coding: utf-8 -*-
# モジュールのインポート
import socket
import sys

args=sys.argv

# グローバル変数

BUFSIZE = 4096     # 受信バッファの大きさ

host = args[1]
PORT=int(args[2])

# メイン実行部
# ソケットの作成
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((host, PORT))
    while True:
        # サーバからのメッセージの受信
        data = client.recv(BUFSIZE)
        received_data = data.decode("UTF-8")
        print(received_data)  # 受信データを表示

        # サーバへのメッセージの送信
        selected_product_name = input("購入したい商品名を入力してください:")
        item = selected_product_name
        client.sendall(selected_product_name.encode("utf-8"))


        data = client.recv(BUFSIZE)
        received_data = data.decode("UTF-8")
        print(received_data)  # 受信データを表示

        if received_data == "OK":
            print("Thank you for your purchase ",item,"!")
        elif received_data == "NG":
            print("あなたが選んだ商品は購入できません!")
        break

except:
    print("接続できません")
    sys.exit()

# コネクションのクローズ
client.close()                             