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
        if received_data == "OK":
            print("商品が存在するかどうか:",received_data)  # 受信データを表示
            print("あなたが選んだ商品は購入可能です")
            
            
        elif received_data == "NG":
            print("商品が存在するかどうか:",received_data)  # 受信データを表示
            print("あなたが選んだ商品は商品リストに存在しません!")
            continue
        else:
            print("すみません！在庫切れです！")
            continue
        

        while True:
            try:
                pay_money = input("お金を支払ってください: ")
                integer_value = int(pay_money)
                if integer_value < 0:
                    print("無効な金額です。正の整数を入力してください。")
                    continue
            except ValueError:
                print("無効な金額です。整数を入力してください。")
                continue
            
            client.sendall(pay_money.encode("utf-8"))
            data = client.recv(BUFSIZE)
            received_data = data.decode("UTF-8")
            if received_data == "OK":
                print("ピッタリ代金をいただきました！")
                print(item,"の購入ありがとうございます！")
                break
            elif received_data == "代金が足りません":
                print("代金が足りません")
                continue
            else:
                print(item,"の購入ありがとうございます！")
                print("お釣りは",received_data,"です!")
                break
        break

except:
    print("接続できません")
    sys.exit()

# コネクションのクローズ
client.close() 
