import requests
from requests.auth import HTTPBasicAuth

class HTTP():
    def __init__(self):
        self.__url = "https://api-vnc.herokuapp.com/dados/"

    def getPCs(self):
        r = requests.get(self.__url, auth=HTTPBasicAuth('u34726', 'kQPxp0^UG77&'))
        if r.status_code == 200:
            return r.json()

    def getPCByID(self, id):
        r = requests.get(self.__url+str(id), auth=HTTPBasicAuth('u34726', 'kQPxp0^UG77&'))
        if r.status_code == 200:
            return r.json()

    def postPC(self, pcDATA):
        data = {
            "pcName": pcDATA["pcName"],
            "ip": pcDATA["ip"],
            "password": pcDATA["password"],
            "htmlURL": pcDATA["htmlURL"],
            "isLocked": pcDATA["isLocked"]
        }
        r = requests.post(self.__url, data=data, auth=HTTPBasicAuth('u34726', 'kQPxp0^UG77&'))
        if r.status_code == 201:
            print("[+] API ok")
        else:
            print(r)

if __name__ == '__main__':
    h = HTTP()
    data = h.getPCs()
    print(data)