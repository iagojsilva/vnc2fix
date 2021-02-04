import subprocess, socket, time, sys, os, platform, pygame
from pwdgen import gerarPassword
from threading import Thread

class VNC():
    
    def __init__(self):
        self.__vncServerPath = "UltraVNC"
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

    def runServer(self):
        
        try:
            self.criar2Monitor()
            self.setPWD()
            self.pararServer()
            time.sleep(3)
            self.rodarServer()
            time.sleep(5)
            self.setMonitorToExtend()
            self.lockScreen()
    
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    def lockScreen(self):
        pygame.init()
        tela = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        
        screenWidth, screenHeight = tela.get_size();
        imagem = pygame.image.load('./down.png')
        imagem = pygame.transform.scale(imagem, [screenWidth, screenHeight])
        corBranca = pygame.color.Color("#abcddd")
        
        rodando = True
        while rodando:
            
            tela.fill(corBranca)
            tela.blit(imagem,(0,0))
            pygame.display.update()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_l:
                        rodando = False  # Set running to False to end the while 
        pygame.quit()

    def verificarSeCriouMonitor(self, device):
        cmd = ["cd", "./usbmmidd/", "&", device, 'status', 'usbmmidd']
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
            cmd = ["cd", "./usbmmidd/", "&", device, 'status', 'usbmmidd']

            output= self.runOnCmd(cmd)
            if 'No matching devices found.' in output:
                cmd = ["cd", "./usbmmidd/", "&", device, 'install' , 'usbmmidd.inf', 'usbmmidd']
                output = self.runOnCmd(cmd)
                if self.verificarSeCriouMonitor(device):
                    print('ativando monitor')
                    cmd = ["cd", "./usbmmidd/", "&", device, 'enableidd' , '1']
                    self.runOnCmd(cmd)
            else:
                print('Monitor virtual já existe!\nAtivando monitor\nMonitor Ativado!')
                cmd = ["cd", "./usbmmidd/", "&", device, 'enableidd' , '1']
                self.runOnCmd(cmd)

        except Exception as e:
            print(f'Ocorreu um erro {e}')

    def setMonitorToExtend(self):
        cmd = ["DisplaySwitch.exe", "/extend"]
        self.runOnCmd(cmd)

v = VNC()
v.runServer()

