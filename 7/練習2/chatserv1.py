# -*- coding: utf-8 -*-
# モジュールのインポート
import socket

# グローバル変数
PORT = 50000     # ポート番号
BUFSIZE = 4096   # 受信バッファの大きさ

# メイン実行部
# ソケットの作成
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# アドレスの設定
server.bind(("", PORT))

# クライアントへの対応処理
clist = []       # クライアントのリスト
ulist = []       # ユーザのリスト

# 対応の繰り返し
try:
    while True:
        data, client = server.recvfrom(BUFSIZE) # 通信用ソケットの取得
        if not (client in clist):
            clist.append(client)                # クライアントの追加
            ulist.append(data.decode("UTF-8"))  # ユーザ名の追加
        if data.decode("UTF-8") == 'quit':      # quit
            # 対応するユーザ名を取得
            username = ulist[clist.index(client)]
            clist.remove(client)                     # クライアントをリストから取り除く
            ulist.remove(username)                    # クライアントに対応するユーザ名をリストから取り除く
            # print(clist)
            # print(ulist)
        else:
            # 対応するユーザ名を取得
            username = ulist[clist.index(client)]
            msg = f"{username}> {data.decode('UTF-8')}"  # 発信元を付加
            print(msg)                          # 受信内容の出力
            # print(clist)
            # print(ulist)
            for c in clist:                     # クライアントに配信
                server.sendto(msg.encode("UTF-8"), c)
except KeyboardInterrupt:
    print("サーバが停止しました")