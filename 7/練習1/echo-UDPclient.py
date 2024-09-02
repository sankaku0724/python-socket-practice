# -*- coding: utf-8 -*-
# モジュールのインポート
import socket

# グローバル変数
HOST = "localhost"  # 接続先ホストの名前
#HOST = "127.0.0.1" # 接続先ホストの名前
PORT = 50000        # ポート番号
BUFSIZE = 4096      # 受信バッファの大きさ

while True:
    # メイン実行部
    # ソケットの作成
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # サーバへの情報の要求
    msg = input("入力してください(quitで終了):")
    client.sendto(msg.encode("UTF-8"), (HOST, PORT))
    # サーバからのメッセージの受信
    data = client.recv(BUFSIZE)
    print(data.decode("UTF-8"))
    if msg == "quit":
        break
# ソケットのクローズ
client.close()                             
