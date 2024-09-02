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
        data, client = server.recvfrom(BUFSIZE)
        if data.decode("UTF-8") in ulist and not (client in clist):
            server.sendto("重複しています".encode("UTF-8"), client)
            continue
        if not (client in clist):
            clist.append(client)
            ulist.append(data.decode("UTF-8"))
            server.sendto("ユーザ名を登録しました".encode("UTF-8"), client)
        if data.decode("UTF-8") == 'quit':
            username = ulist[clist.index(client)]
            clist.remove(client)
            ulist.remove(username)
        else:
            sender_username = ulist[clist.index(client)]
            data2 = data.decode('UTF-8')
            message = f"{sender_username}> {data.decode('UTF-8')}"  # 発信元を付加
            print(message) # 受信内容の出力

            
            # ダイレクトメッセージの形式: "recipient_username@send_message"
            if '@' in data2:
                recipient_username, send_message = data2.split('@', 1)
                recipient_username = recipient_username.strip()
                send_message = send_message.strip()

                # 対象のクライアントにのみメッセージを送信
                recipient_found = False
                for i, u in enumerate(ulist):
                    if u == recipient_username:
                        recipient_found = True
                        message = f"{sender_username}からのダイレクトメッセージ> {send_message}"  # 発信元を付加
                        server.sendto(message.encode("UTF-8"), clist[i])

                # 対象のクライアントが存在しない場合の処理                
                if not recipient_found:
                    server.sendto("そのユーザは存在しません".encode("UTF-8"), client)
            else:
                # 通常のメッセージは全クライアントに送信
                for c in clist:
                    server.sendto(message.encode("UTF-8"), c)


except KeyboardInterrupt:
    print("サーバが停止しました")