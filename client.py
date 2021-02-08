import subprocess

class VNC():
    def __init__(self):
        self.__clientIP = "192.168.1.32"

    def runOnCmd(self, cmd):
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output = output.communicate()[0].decode('utf-8')
        return output

    def connect(self):
        cmd = ["cd","server/UltraVNC","&","vncviewer.exe", self.__clientIP, "-password", "kF2rX8"]
        output = self.runOnCmd(cmd)
        print(output)

vnc = VNC()
vnc.connect()