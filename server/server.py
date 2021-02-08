import subprocess, socket, time, sys, os, platform
from pwdgen import gerarPassword
from threading import Thread
from webviewLock import builderWebView
from windowsManager import moveAll

class VNC():
    
    def __init__(self):
        self.__vncServerPath = os.path.dirname(os.path.abspath(__file__)) + "/UltraVNC"
        self.__usbmmiddPath = os.path.dirname(os.path.abspath(__file__)) + "/usbmmidd/"
        self.__displayPath = os.path.dirname(os.path.abspath(__file__))+ "/DisplaySwitch.exe"

        self.ip = socket.gethostbyname(socket.gethostname())
        self.desktopName = socket.gethostname()

    def runOnCmd(self, cmd):
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output = output.communicate()[0].decode('utf-8')
        return output
        

    def testServer(self):
        print(f'verificando o server...')
        
        pass

    def rodarServer(self):
        print(f'Rodando o server!')
        
        startServerCMD = ["cd", self.__vncServerPath, "&", "winvnc"]
        
        Thread(target=self.runOnCmd, args=[startServerCMD]).start()
        time.sleep(5)
        Thread(target=self.testServer).start()
    
        
        
        print(f"Desktop Name: {self.desktopName}\nServer UP: {self.ip}")


    def pararServer(self):
        print(f'Derrubando qualquer instacia de VNC!')

        stopServerCMD = ["cd", self.__vncServerPath, "&", "winvnc", "-kill"]
        self.runOnCmd(stopServerCMD)



    def setPWD(self):
        loginPWD = gerarPassword()
        viewPWD = gerarPassword()

        print(f'configurando password: {loginPWD}')
        
        setPwdCMD = ["cd", self.__vncServerPath, "&", "setpasswd.exe", f'{loginPWD}', f'{viewPWD}']

        self.runOnCmd(setPwdCMD)


    def lockScreen(self):
        builderWebView('https://pywebview.flowrl.com/hello')

    def verificarSeCriouMonitor(self, device):
        cmd = ["cd", self.__usbmmiddPath, "&", device, 'status', 'usbmmidd']
        output = self.runOnCmd(cmd)
        if 'Driver is running' in output:
            print('monitor criado com sucesso!')
            return True
        else:
            print('Monitor não foi criado!')
            return False
            
    def getArch(self):
        try:
            arch = platform.processor()
            if '32' in arch:
                bits = 32
                return bits
            else:
                bits = 64
                return bits
        except Exception as e:
            print(f'Ocorreu um erro: {e}')


    def selectDevice(self, bits):
        if bits == 32:
            return 'deviceinstaller'
        else:
            return 'deviceinstaller64'

    def criar2Monitor(self):

        try:
            bits = self.getArch()
            device = self.selectDevice(bits)
            cmd = ["cd", self.__usbmmiddPath, "&", device, 'status', 'usbmmidd']

            output= self.runOnCmd(cmd)
            if 'No matching devices found.' in output:
                cmd = ["cd", self.__usbmmiddPath, "&", device, 'install' , 'usbmmidd.inf', 'usbmmidd']
                output = self.runOnCmd(cmd)
                if self.verificarSeCriouMonitor(device):
                    print('ativando monitor')
                    cmd = ["cd", self.__usbmmiddPath, "&", device, 'enableidd' , '1']
                    self.runOnCmd(cmd)
            else:
                print('Monitor virtual já existe!\nAtivando monitor\nMonitor Ativado!')
                cmd = ["cd", self.__usbmmiddPath, "&", device, 'enableidd' , '1']
                self.runOnCmd(cmd)

        except Exception as e:
            print(f'Ocorreu um erro {e}')

    def setMonitorToExtend(self):
        cmd = [self.__displayPath, "/extend"]
        self.runOnCmd(cmd)

    def builder(self):
        try:
            self.criar2Monitor()
            self.setPWD()
            self.pararServer()
            Thread(target=self.setMonitorToExtend).start()
            self.rodarServer()
            time.sleep(10)
            moveAll()
            self.lockScreen()
    
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

if __name__ == '__main__':
    v = VNC()
    v.builder()
