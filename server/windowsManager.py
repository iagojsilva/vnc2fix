import pygetwindow as gw
import time
from win32api import GetSystemMetrics

def getW():
    windows = gw.getAllWindows()
    return windows

def moveW(w):
    width = GetSystemMetrics(0)#int(input("X: "))

    w.move(-width, 0)

def getWindowsName():
    janelas = []
    for i in getW():
        janelas.append(i.title)
    return janelas

def moveAll():
    windows = getW()
    print("Movendo todas as janelas!")
    for window in windows:
        if window.title == "Lockscreen":
            pass
        else:
            moveW(window)
    moveContinuos(windows)

def moveContinuos(windows):
    while True:
        for i in getW():
            if i not in windows and len(i.title)>1:
                print(f"Nova janela detectada: {i.title} Movendo..")
                moveW(i)

            elif getW().count(i) > 1:
                print(f"Nova janela detectada: {i.title} Movendo..")
                moveW(i)
                
        windows = getW()
        time.sleep(.7)
        

if __name__ == '__main__':

    moveContinuos(getW())
    