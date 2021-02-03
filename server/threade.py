from threading import Thread
import time

def a():
    print("estou na a")
    time.sleep(10)
def b():
    print("estou na b")

def myfunc():
    a()
    b()

Thread(target=a).start()
time.sleep(3)
Thread(target=b).start()