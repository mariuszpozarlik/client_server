import socket
import time
import services

class EZclient:

    """
    Client class to connect with server.
    """

    def __init__(self, server_IP, server_PORT = 5050, server_HEADER = 64):
        self.HEADER: int = server_HEADER
        self.PORT: int = server_PORT
        self.FORMAT: str = 'utf-8'        
        self.SERVER: int = server_IP
        self.ADDR: tuple = (self.SERVER, self.PORT)          
        self.TIMEOUT: int = 3
        self.BLOCKING_MODE: bool = False
        
    def connectToServer(self) -> bool:
        self.result = True
        while self.result:
            try:
                print(f"Attepmt to connect address {self.SERVER}")
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.setblocking(self.BLOCKING_MODE)
                self.client.settimeout(self.TIMEOUT)
                #time.sleep(1)
                self.client.connect(self.ADDR)
                self.result = False
            except ConnectionRefusedError as e:
                print(e.__class__)
            except Exception as e:
                print(e.__class__)
        return True
    
    def sendMessage(self, msg: str) -> str:
        try:
            long_resp = ""
            message = msg.encode(self.FORMAT)
            msg_length = len(message)
            if msg_length < 2000:
                send_length = str(msg_length).encode(self.FORMAT)
                send_length += b' ' * (self.HEADER - len(send_length))
                self.client.send(send_length)
                time.sleep(0.1)
                self.client.send(message)
                return self.client.recv(2048).decode(self.FORMAT)
            else: #send in chunks
                chunk_size = 2000
                list_chunks = [bytes(f"CHUNK #{int(i/chunk_size)}#: ", encoding='utf-8') + \
                               message[i:i+chunk_size] for i in range(0, msg_length, chunk_size)]
                for chunk in list_chunks:
                    send_length = str(len(chunk)).encode(self.FORMAT)
                    send_length += b' ' * (self.HEADER - len(chunk))
                    self.client.send(send_length)
                    time.sleep(0.1)
                    self.client.send(chunk)
                    long_resp += self.client.recv(2048).decode(self.FORMAT)
                return long_resp

        except ConnectionResetError as e:
            print(e.__class__)
            self.connectToServer()
        except ConnectionAbortedError as e:
            print(e.__class__)
            self.connectToServer()
        except socket.timeout as e:
            print(e.__class__)


if __name__ == "__main__":

    IP = f"192.168.0.253"
    client = EZclient(server_IP=IP)
    cnt = 0
    if(client.connectToServer()):
        print(f"[CONNECTED TO {IP}]")
    while(True):
        res = client.sendMessage(input())
        print(res)
        

