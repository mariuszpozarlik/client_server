import socket
import time

class EZclient:
    def __init__(self, server_IP, server_PORT = 5050, server_HEADER = 64, server_FORMAT = 'utf-8'):
        self.HEADER = server_HEADER
        self.PORT = server_PORT
        self.FORMAT = server_FORMAT
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = server_IP
        self.ADDR = (self.SERVER, self.PORT)          
        self.TIMEOUT = 3
        self.BLOCKING_MODE = False
        
    def connectToServer(self):
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
    def sendMessage(self, msg):
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
        
#         client.sendMessage("very long text to sent without any change of whatever I'm only writing without thinking bla blA BLAvery long text to sent withoutchange of whatever I'm only writing without thinking bla blA BLAvery long text to sent without any change of whatever I'm only writing without thinking bla blA BLAvery long text to sent without any change of whatever I'm only writing without thinking bla blA BLAvery long text to sent without any change of whatever I'm only writing without thinking bla blA BLA")
#      
#         client.sendMessage("shutdown -s -t 10")
#      
#         client.sendMessage(f"Hello test server!")
#  
#         client.sendMessage(str(cnt))
        
#         try:
#             print(client.client.recv(2048).decode('utf-8'))
#         except:
#             pass
#         print("asd")
#         cnt+=1
#         if cnt > 20: 
#             break

client.sendMessage(client.DISCONNECT_MESSAGE)