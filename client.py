import socket
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
suffix = 3
SERVER = f"192.168.168.4"
ADDR = (SERVER, PORT)
result = True

global client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while(result):
    try:
        print(f"Attepmt to connect address {SERVER}")
        client.connect(ADDR)
        result = False
    except Exception as e:
        print(e.__class__)

def send(msg):
    global client
    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        #time.sleep(1)
        print(client.recv(2048).decode(FORMAT))
    except Exception as e:
        print(e.__class__)
        del client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = True
        while (result):
            try:
                print(f"Attepmt to re-connect address {SERVER}")
                client.connect(ADDR)
                result = False
            except Exception as e:
                print(e.__class__)

cnt = 0
while(True):
    send("very long text to sent without any change of whatever I'm only writing without thinking bla blA BLAvery long text to sent withoutchange of whatever I'm only writing without thinking bla blA BLAvery long text to sent without any change of whatever I'm only writing without thinking bla blA BLAvery long text to sent without any change of whatever I'm only writing without thinking bla blA BLAvery long text to sent without any change of whatever I'm only writing without thinking bla blA BLA")

    send("shutdown -s -t 10")

    send(f"Hello test server!")

    send(str(cnt))
    cnt+=1

send(DISCONNECT_MESSAGE)