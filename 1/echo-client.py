# -*- coding: utf-8 -*-
"""
echo-client.pyプログラム
Pythonによるクライアントソケットの利用法を示すプログラム
50000番ポートで、指定したサーバに接続します
接続後、サーバにメッセージを送ります
その後、サーバからのメッセージを取得して表示します
使いかた　c:\>python3 echo-client.py
"""

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
        # サーバへのメッセージの送信
        msg = input("メッセージを入力：")
        client.sendall(msg.encode("utf-8"))
        if msg == "quit":
            break
        # サーバからのメッセージの受信
        data = client.recv(BUFSIZE)
        print("サーバからのメッセージ："+data.decode("UTF-8"))
except:
    print("接続できません")
    sys.exit()

# コネクションのクローズ
client.close()                             
# echo-client.pyの終わり
