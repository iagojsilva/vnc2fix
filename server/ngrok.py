from pyngrok import ngrok

def thereIsTunnels():
    tunnels = ngrok.get_tunnels()
    return len(tunnels) > 1

def getTunnels():
    return ngrok.get_tunnels()

def createTunnel():
    #print("Creating tunnel..")
    vncTunnel = ngrok.connect(5900, "tcp")
    return vncTunnel.public_url

def deleteTunnel(tunnels):
    #print("Deleting Tunnels")
    for tunnel in tunnels:
        ngrok.disconnect(tunnel.public_url)

def setToken():
    ngrok.set_auth_token("1cSM5wr99ViurDfgyCWRGY00Ccc_2wPt8sChGiHZjbf14HgXL")

def builder():
    setToken()
    if thereIsTunnels():
       for tunnel in getTunnels():
           deleteTunnel(tunnel.public_url)

    return createTunnel()

if __name__ == '__main__':
    b = builder()
    print(b)