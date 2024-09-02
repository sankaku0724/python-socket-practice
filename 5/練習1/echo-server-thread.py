# -*- coding: utf-8 -*-
# モジュールのインポート
import socket
import datetime 
import sys

import threading

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

def stock_handler(client):
    while True:
        data = client.recv(BUFSIZE)
        if not data:
            break
        print(data.decode("UTF-8"))                # 受信内容の出力
        client.sendall(data)  # メッセージの送信
        if data.decode("UTF-8") == "quit":
            break        
    client.close()  

# クライアントへの対応処理
try:
    while True:                                    # 対応の繰り返し
        client, addr = server.accept()             # 通信用ソケットの取得
        p = threading.Thread(target = stock_handler,args = (client,))
        p.start()
        print(p)
except KeyboardInterrupt:
    print("サーバーが停止しました。")