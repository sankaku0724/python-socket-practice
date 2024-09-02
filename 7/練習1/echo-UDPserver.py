# -*- coding: utf-8 -*-
# モジュールのインポート
import socket
import datetime 

# グローバル変数
PORT = 50000      # ポート番号
BUFSIZE = 4096    # 受信バッファの大きさ
# メイン実行部
# ソケットの作成
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# アドレスの設定
server.bind(("",PORT))

# クライアントへの対応処理
try:
    while True:                                    # 対応の繰り返し
        data, client = server.recvfrom(BUFSIZE)    # 通信用ソケットの取得 
        msg = data         # メッセージの作成
        server.sendto(msg, client) # メッセージの送信
        print(msg, "接続要求あり")
        print(client)
        if msg.decode("UTF-8") == "quit":
            break
except KeyboardInterrupt:
    print("サーバーが停止しました。")