import subprocess, socket, time, pygame

class VNC():
    
    def __init__(self):
        self.__vncServerPath = ""
        self.ip = socket.gethostbyname(socket.gethostname())
        self.getVNCPath()
        
    def getVNCPath(self):
        
        cmd = ["cd", "C:/", "&", "dir", "vncserver.exe", "/S"]
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        
        start = output.find("C:")
        end = output.find("RealVNC")

        if start == -1 or end == -1:
            print("PATH: NÃO ENCONTREI\nSaindo...")
        else:
            print("PATH: OK")
        self.__vncServerPath = output[start:end+18]

    def runServer(self):
        self.criar2Monitor()

        startServerCMD = ["cd", self.__vncServerPath, "&", "vncserver.exe"]
        stopServerCMD = ["cd", self.__vncServerPath, "&", "vncserver.exe", "-stop"]

        try:
            output = subprocess.Popen(stopServerCMD, stdout=subprocess.PIPE, shell=True)
            time.sleep(3)
            output = subprocess.Popen(startServerCMD, stdout=subprocess.PIPE, shell=True)
            print(f"Server UP: {self.ip}")
            self.criarTela()
    
            print(output.communicate()[0].decode('utf-8'))
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

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
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output = output.communicate()[0].decode('utf-8')
        qtd2 = output.count("Adapter:")
        print(qtd2)
        return qtd2-1 == qtdMonitor
            

    def criar2Monitor(self):
        cmd = ["cd", "./usbmmidd/", "&", "usbmmidd.bat"]
        qtdMonitor = 1
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        if self.verificarSeCriou(qtdMonitor):
            print("Monitor Virtual criado com sucesso!")
        else:
            print("Houve um erro ao criar o Monitor!")
        
v = VNC()
s = v.runServer()

