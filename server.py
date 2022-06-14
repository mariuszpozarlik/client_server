import socket
import threading
from Services import PowerService
import os

class EZServer:
    def __init__(self, server_HEADER: int = 64, server_PORT: int = 5050):
        self.HEADER: int = server_HEADER
        self.PORT: int = server_PORT
        self.SERVER: str = socket.gethostbyname(socket.gethostname())
        self.ADDR: tuple = (self.SERVER, self.PORT)
        self.FORMAT: str = 'utf-8'
        self.BLOCKING_MODE: bool = False
        self.TIMEOUT: int = 5
        self.server: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.server.setblocking(self.BLOCKING_MODE)
        self.server.settimeout(self.TIMEOUT)
        self.msg: str = ''    

    def handleClient(self, conn: socket, addr: socket.AddressInfo) -> None:
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            try:                
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:
                    #print(f"[MESSAGE SIZE] -> {msg_length}")
                    msg_length = int(msg_length)
                    self.msg = conn.recv(msg_length).decode(self.FORMAT)
                    if self.msg == PowerService.DISCONNECT_SERVICE:
                        conn.send(f"[RESPONSE FROM SERVER]-> Disconnected!".encode(self.FORMAT))
                        connected = False                        
                    #print(f"[INCOMMING MESSAGE FROM] {addr} -> {self.msg}")

                    PowerService.processService(self.msg, conn)

                    conn.send(f"[RESPONSE FROM SERVER]-> message <<{self.msg}>> processed with status {0}".encode(self.FORMAT))
            except ConnectionResetError as exc:
                connected = False
                print(exc.__class__)
            except Exception as e:
                connected = False
                print(e.__class__)
        conn.close()

    def start(self) -> None:
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            try:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handleClient, args=(conn, addr))
                thread.start()
            except Exception as e: 
                pass
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")      

if __name__ == "__main__":
    s = EZServer()
    s.start()