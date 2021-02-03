import random

def gerarPassword():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    caracters = alphabet + alphabet.upper() + '1234567890!@#$%&*()'
    
    password = []

    for i in range(0,6):
        index = random.randint(0, len(caracters)-i)
        
        password.append(caracters[index])


    return ''.join(password)

if __name__ == '__main__':

    for i in range(0,20):
        print(gerarPassword())