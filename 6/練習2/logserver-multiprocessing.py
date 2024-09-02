# -*- coding: utf-8 -*-
# モジュールのインポート
import socket
import datetime
from multiprocessing import Process
import os

# グローバル変数
PORT = 50000      # ポート番号
BUFSIZE = 4096    # 受信バッファの大きさ

def stock_handler(client):
    d = datetime.datetime.now()              # 現在時刻の取得
    fname = d.strftime("%m%d%H%M%S%f")       # 文字列へ変換
    print(fname, "接続要求あり")               # 接続先を端末に表示
    print(client)
    fout = open(fname + ".txt", "wt")        # 書き込みファイルオープン
    try:
        while True:
            data = client.recv(BUFSIZE)      # クライアントより受信 
            if not data:                     # 受信するものがないなら
                break                         # 受信終了
            print(data.decode("UTF-8"))      # 受信内容の出力
            print(data.decode("UTF-8"), file=fout)  # ファイルへの書き込み
    finally:
        client.close()  # コネクションのクローズ
        fout.close()    # ファイルのクローズ
        print("接続処理終了（", fname, ")")

if __name__ == '__main__':
    # メイン実行部
    # ソケットの作成
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # アドレスの設定
    server.bind(("", PORT))
    # 接続の待ち受け
    server.listen()

    # クライアントへの対応処理
    processes = []
    try:
        while True:                                  # 対応の繰り返し
            client, addr = server.accept()           # 通信用ソケットの取得
            p = Process(target=stock_handler, args=(client,))
            processes.append(p)
            p.start()
            print(p)
    except KeyboardInterrupt:
        print("サーバーが停止しました。")
    except Exception as e:  # エラーへの対応
        print("エラーが発生しました:", e)

    for i in processes:
        i.join()
        print(i)
