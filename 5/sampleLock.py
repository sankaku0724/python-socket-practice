import threading
import time

class Food:
    def __init__(self, name, stock):
        self.name = name
        self.stock = stock
    def __str__(self): # 文字列化メソッド
        return "Food: " + self.name + " " + str(self.stock)

foodList = [] # foodリストの設定

f = Food('milk', 100)
foodList.append(f)
print(foodList[0])
f = Food('coffee', 150)
foodList.append(f)
print(foodList[1])

lock = threading.Lock()

def stock_handler(lock, foodList, i):
    for n in range(20):
        #lock.acquire()
        foodList[0].stock -=1
        print("thread:",i, " stock=", foodList[0].stock)
        #lock.release()
        time.sleep((i+1) * 0.1)     
        
threads = []
for i in range(20):
    p = threading.Thread(target = stock_handler,
                         args = (lock, foodList, i))
    threads.append(p)
    p.start()
    print(p)

for thread in threads:
    thread.join()
    print(thread)