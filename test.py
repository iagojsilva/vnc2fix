import pygetwindow as gw
import time
def getW():

    windows = gw.getAllWindows()

    


    return windows

def moveW(w):
    w.restore()



if __name__ == '__main__':
    from win32api import GetSystemMetrics

    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)

    windows = getW()

    window = windows[2]

    window.move(width,height)