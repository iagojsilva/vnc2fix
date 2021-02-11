import subprocess, sys
sys.path.append('../httpC')
from httpClient import HTTP
class VNC():
    def __init__(self):
        self.__h = HTTP()

    def runOnCmd(self, cmd):
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output = output.communicate()[0].decode('utf-8')
        return output

    def connect(self, PCData):
        print(f"Conectando a máquina: {PCData['pcName']}")
        cmd = ["vncviewer.exe", PCData['ip'][7:], "-password", f"{PCData['password']}"]
        output = self.runOnCmd(cmd)
        print(output)

    def choose(self):
        print(f'-'*10, 'Escolha uma Máquina para se conectar!','-'*10,)
        for i in self.__h.getPCs():
            print(f"[+] ID: {i['id']} \nPC: {i['pcName']}\nIP: {i['ip'][7:]}")
        machine = int(input('Escolha por ID: '))
        self.connect(self.__h.getPCByID(machine))

vnc = VNC()
vnc.choose()