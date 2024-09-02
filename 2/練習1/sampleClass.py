class Food:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def __str__(self): # 文字列化メソッド
        return "Food: " + self.name + " " + str(self.price)

x = Food('milk', 150)
print(x.name, x.price)
print(x)

## 練習問題の回答は以下に記すこと

# 問1：変数yを使って，品名：egg, 価格：200で初期化したデータを作成せよ
y = Food('egg', 200)
# 問2：milkの価格を300円に変更せよ
x.price = 300
# 例：リストを使って，Food情報を複数個管理する
foodList = [] # foodリストの設定

f = Food('milk', 300)
foodList.append(f)
print(foodList[0])
f = Food('coffee', 150)
foodList.append(f)
print(foodList[1])

# 問3：for文を使って，全てのFood情報を表示せよ
for x in foodList:
    print(x)

# 例：milkの商品名を変更する
foodList[0].name = 'coffeeMilk'

# 問4：coffeeMilkの価格を250円へ変更せよ
foodList[0].price = 250

# 問5：三つ目の商品を追加せよ（商品名と価格はなんでもよい）
f = Food('caramel macchiato',1000)
foodList.append(f)
# 問6：for文を使って，全てのFood情報を表示せよ．ただし，文字列化メソッドを使用しないこと．
for x in foodList:
    print('Food: {} {}'.format(x.name,x.price))