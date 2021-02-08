import pygetwindow as gw
import time
from win32api import GetSystemMetrics

def getW():

    windows = gw.getAllWindows()
    
    return windows

def moveW(w):
    width = GetSystemMetrics(0)#int(input("X: "))

    w.move(-width, 0)

def moveAll():
    windows = getW()
    print("Movendo todas as janelas!")
    for window in windows:
        if window.title == "Lockscreen":
            pass
        else:
            moveW(window)



if __name__ == '__main__':

    moveAll()
    