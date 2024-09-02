# -*- coding: utf-8 -*-
"""
echo-server.pyプログラム
Pythonによるサーバソケットの利用法を示すプログラム
50000番ポートで接続を待ち受けます
クライアントからの入力後、時刻を返します
接続時にコンソールにメッセージを出力します
Ctrl+Breakで終了します
使いかた　c:\>python3 echo-server.py
"""

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

# クライアントへの対応処理
while True:                                    # 対応の繰り返し
    client, addr = server.accept()             # 通信用ソケットの取得
    while True:
        # msg = str(datetime.datetime.now())         # メッセージの作成
        # print(msg,"接続要求あり")
        # print(client)
        data = client.recv(BUFSIZE)                # クライアントより受信 
        print(data.decode("UTF-8"))                # 受信内容の出力
        if data.decode("UTF-8") == "quit":
            client.close()
            break
      
        client.sendall(data)      
    client.close()                             # コネクションのクローズ
# echo-server.pyの終わり
