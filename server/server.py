import subprocess, socket, time, sys, os
from pwdgen import gerarPassword
from threading import Thread

class VNC():
    
    def __init__(self):
        self.__vncServerPath = "UltraVNC"
        self.ip = socket.gethostbyname(socket.gethostname())

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
        Thread(target=self.testServer()).start()
    
        

        print(f"Server UP: {self.ip}")


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
            #self.criar2Monitor()
            self.setPWD()
            self.pararServer()
            time.sleep(3)
            self.rodarServer()
  
            
            #self.criarTela()
    
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    def criarTela(self):
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

    def verificarSeCriou(self, qtdMonitor):
        cmd = ["cd", "./dc/", "&", "dc64cmd.exe", "-listmonitors"]
        output = self.runOnCmd(cmd)
        qtd2 = output.count("Adapter:")
        print(qtd2)
        return qtd2-1 == qtdMonitor
            

    def criar2Monitor(self):
        cmd = ["cd", "./usbmmidd/", "&", "usbmmidd.bat"]
        qtdMonitor = 1
        output = self.runOnCmd(cmd)
        if self.verificarSeCriou(qtdMonitor):
            print("Monitor Virtual criado com sucesso!")
        else:
            print("Houve um erro ao criar o Monitor!")
            print(output)
        
v = VNC()
v.runServer()

