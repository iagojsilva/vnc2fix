import webview, sys, time
from ctypes import *
from threading import Thread


def lockPerifericos():
    windll.user32.BlockInput(True)
    time.sleep(30)
    windll.user32.BlockInput(False)

def webViewScreen(link):
    try:
        webview.create_window(title='', url=link , fullscreen=True)
        webview.start()
    except KeyboardInterrupt:
        sys.exit(0)

def builderWebView(link):
    Thread(target=lockPerifericos).start()
    webViewScreen(link)


if __name__ == '__main__':
    builderWebView('https://pywebview.flowrl.com/hello')