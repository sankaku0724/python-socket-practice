# -*- coding: utf-8 -*-
# モジュールのインポート
import socket
import threading
import sys

# グローバル変数
PORT = 50000     # ポート番号
BUFSIZE = 4096   # 受信バッファの大きさ

#下請け関数の定義
#server_handler()関数
def server_handler(client):
    """
    サーバとの接続処理スレッド
    """
    while True:
        try:
            data = client.recv(BUFSIZE)   # サーバより受信 
            print(data.decode("UTF-8"))   # 受信内容の出力
        except:                           # エラー対応
            sys.exit()
    client.close()                        # コネクションのクローズ
#server_handler()関数の終わり

# メイン実行部
# ソケットの作成
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# サーバの設定
host = input("接続先サーバ：")
if host == "":        # デフォルト設定
    host = "localhost" 
# 送受信処理
# スレッドの設定
p = threading.Thread(target = server_handler,
                     args = (client,))
p.setDaemon(True)

#ユーザ名の入力
while True:
    user = input("ユーザ名を入力してください:")
    if "@" in user:
        print("「@」は名前に入れることができません！")
        print("別のユーザ名にしてください")
        continue
    client.sendto(user.encode("UTF-8"), (host, PORT))
    data, server = client.recvfrom(BUFSIZE)
    if data.decode("UTF-8") == "重複しています":
        print("別のユーザ名にしてください")
        continue
    else:
        print(data.decode("UTF-8"))
        break

#メッセージの送信
while True:
    msg = input("入力してください(quitで終了)")
    client.sendto(msg.encode("UTF-8"), (host, PORT))
    if msg == "quit":    # quit
        break         # 接続終了
    # スレッドの起動
    if not p.is_alive():
        p.start()     # 未起動の場合、一回だけ起動する
client.close()