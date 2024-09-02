# -*- coding: utf-8 -*-
# モジュールのインポート
import socket
import datetime
import threading
import os

# グローバル変数
PORT = 50000      # ポート番号
BUFSIZE = 4096    # 受信バッファの大きさ

lock = threading.Lock()

def stock_handler(client):
    previous_time = datetime.datetime.now()
    fname = previous_time.strftime("%H%M%S") + ".txt"
    print(fname, "接続要求あり")
    print(client)
    fout = open(fname, "wt")

    try:
        while True:
            data = client.recv(BUFSIZE)
            if not data:
                break

            lock.acquire()
            print(data.decode("UTF-8"))
            print(data.decode("UTF-8"), file=fout)
            lock.release()

            current_time = datetime.datetime.now()
            elapsed_time = (current_time - previous_time).total_seconds()

            if elapsed_time >= 30:
                lock.acquire()
                fout.close()
                fname = current_time.strftime("%H%M%S") + ".txt"
                print(fname, "接続要求あり")
                print(client)
                fout = open(fname, "wt")
                previous_time = current_time
                lock.release()

    finally:
        client.close()
        fout.close()
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
    threads = []
    try:
        while True:                                  # 対応の繰り返し
            client, addr = server.accept()           # 通信用ソケットの取得
            p = threading.Thread(target=stock_handler, args=(client,))
            threads.append(p)
            p.start()
            print(p)
    except KeyboardInterrupt:
        print("サーバーが停止しました。")
    except Exception as e:  # エラーへの対応
        print("エラーが発生しました:", e)

    for t in threads:
        t.join()
        print(t)
