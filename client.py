import socket
import time
import Services

class EZclient:
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
        while(self.result):
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
            message = msg.encode(self.FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(self.FORMAT)
            send_length += b' ' * (self.HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
            #time.sleep(1)
            return self.client.recv(2048).decode(self.FORMAT)
        except ConnectionResetError as e:
            print(e.__class__)
            self.connectToServer()
        except ConnectionAbortedError as e:
            print(e.__class__)
            self.connectToServer()
        except socket.timeout as e:
            print(e.__class__)


if __name__ == "__main__":
    client = EZclient(server_IP = f"192.168.168.3")    
    cnt = 0
    if(client.connectToServer()):
        pass
    while(True):
        res = client.sendMessage(input())
        print(res)
        
#         res =client.sendMessage("very long text to sent without any change of whatever I'm only writing without thinking bla blA BLAvery long text to sent withoutchange of whatever I'm only writing without thinking bla blA BLAvery long text to sent without any change of whatever I'm only writing without thinking bla blA BLAvery long text to sent without any change of whatever I'm only writing without thinking bla blA BLAvery long text to sent without any change of whatever I'm only writing without thinking bla blA BLA")
#         print(res)
#         res =client.sendMessage("shutdown -s -t 10")
#         print(res)
#         res =client.sendMessage(f"Hello test server!")
#         print(res)
#         res =client.sendMessage(str(cnt))
#         print(res)
#         try:
#             print(client.client.recv(2048).decode('utf-8'))
#         except:
#             pass
#         print("asd")
#         cnt+=1
#         if cnt > 20: 
#             break

    client.sendMessage(client.DISCONNECT_MESSAGE)