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
        # 商品リストの受信
        data = client.recv(BUFSIZE)
        received_data = data.decode("UTF-8")
        print(received_data)  # 受信データを表示

        # 商品名の送信
        selected_product_name = input("購入したい商品名を入力してください:")
        item = selected_product_name
        client.sendall(selected_product_name.encode("utf-8"))

        # 商品が存在するかどうかを受信
        data = client.recv(BUFSIZE)
        received_data = data.decode("UTF-8")

        # 商品が存在する場合、代金を送信
        NG = "NG"
        if received_data == "OK":
            print("商品が存在するかどうか:",received_data)  # 受信データを表示
            print("あなたが選んだ商品は購入可能です")
            pay_money = input("お金を支払ってください:")
            client.sendall(pay_money.encode("utf-8"))
        elif received_data == "NG":
            print("商品が存在するかどうか:",received_data)  # 受信データを表示
            print("あなたが選んだ商品は商品リストに存在しません!")
            client.sendall(NG.encode("utf-8"))
            break
        else:
            print("あなたが選んだ商品:",received_data)  # 受信データを表示
            print("すみません！",received_data,"は在庫切れです！")
            client.sendall(NG.encode("utf-8"))
            break
        
        #その代金で購入できるかどうかを受信
        data = client.recv(BUFSIZE)
        received_data = data.decode("UTF-8")
        print("購入できるかどうか:",received_data)  # 受信データを表示

        if received_data == "OK":
            print("ピッタリ代金をいただきました！")
            print(item,"の購入ありがとうございます！")
        elif received_data == "代金が足りません":
            print("代金が足りません")
        elif received_data == "NG":
            print("あなたが選んだ商品は購入できません!")
        else:
            print(item,"の購入ありがとうございます！")
            print("お釣りは",received_data,"です!")
        break

except:
    print("接続できません")
    sys.exit()

# コネクションのクローズ
client.close() 
