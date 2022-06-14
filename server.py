import socket
import threading

class EZServer:
    def __init__(self, server_HEADER = 64, server_PORT = 5050):
        self.HEADER = server_HEADER
        self.PORT = server_PORT
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.BLOCKING_MODE = False
        self.TIMEOUT = 5
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.server.setblocking(self.BLOCKING_MODE)
        self.server.settimeout(self.TIMEOUT)
        self.msg = ''

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            try:                
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:
                    print(f"[MESSAGE SIZE] -> {msg_length}")
                    msg_length = int(msg_length)
                    self.msg = conn.recv(msg_length).decode(self.FORMAT)
                    if self.msg == self.DISCONNECT_MESSAGE:
                        conn.send(f"[RESPONSE FROM SERVER]-> Disconnected!".encode(self.FORMAT))
                        connected = False                        
                    print(f"[INCOMMING MESSAGE FROM] {addr} -> {self.msg}")

                    # process message

                    conn.send(f"[RESPONSE FROM SERVER]-> message <<{self.msg}>> processed with status {0}".encode(self.FORMAT))
            except ConnectionResetError as exc:
                connected = False
                print(exc.__class__)
            except Exception as e:
                print(e.__class__)
        conn.close()

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            try:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
            except Exception as e: 
                pass
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")      

if __name__ == "__main__":
    s = EZServer()
    s.start()