from pyngrok import ngrok

def thereIsTunnels():
    tunnels = ngrok.get_tunnels()
    return len(tunnels) > 1
        
def createTunnel():
    #print("Creating tunnel..")
    vncTunnel = ngrok.connect(5900, "http")
    return vncTunnel.public_url

def deleteTunnel(tunnels):
    #print("Deleting Tunnels")
    for tunnel in tunnels:
        ngrok.disconnect(tunnel.public_url)

def builder():
    if thereIsTunnels():
       for tunnel in ngrok.get_tunnels():
           deleteTunnel(tunnel.public_url)

    return createTunnel()

if __name__ == '__main__':
    b = builder()
    print(b)