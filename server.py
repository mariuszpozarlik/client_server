import socket
import threading
from services import Service
from file_monitor import file_changes, file_manager, file_scaner


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

    def handle_client(self, conn: socket, addr: socket.AddressInfo) -> None:
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            try:
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:

                    msg_length = int(msg_length)
                    print(f"[MESSAGE SIZE] -> {msg_length}")
                    self.msg = conn.recv(msg_length).decode(self.FORMAT)
                    if self.msg == Service.PowerServices["DISCONNECT_SERVICE"]:
                        connected = False
                    print(f"[INCOMMING MESSAGE FROM] {addr} -> {self.msg}")

                    if Service.processPowerService(str(self.msg)):
                        conn.send(f"[RESPONSE FROM SERVER]-> message <<{self.msg}>> processed with status 1".encode(
                            self.FORMAT))

                    elif Service.processHelpService(str(self.msg))[0]:
                        conn.send(Service.processHelpService(str(self.msg))[1].encode(self.FORMAT))

                    elif Service.processBackupServices(str(self.msg)):
                        conn.send(
                            f"[RESPONSE FROM SERVER]-> message <<backup server-storage data>>".encode(self.FORMAT))

                    else:
                        conn.send(f"[RESPONSE FROM SERVER]-> message <<OK>>".encode(self.FORMAT))
                print(f"[RESPONDED MESSAGE TO] {addr} -> OK")
            except ConnectionError:
                connected = False
            except ConnectionAbortedError:
                connected = False
            except:
                pass
        conn.close()

    def start(self) -> None:
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            try:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
            except Exception as e:
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 3}")


if __name__ == "__main__":
    root_pth = "C:\\"
    source_folder = r"server-storage"
    destination_folder = r"server-storage-bckup"

    fc = file_changes.FileChanges(root=root_pth,
                                  source_folder_name=source_folder,
                                  destination_folder_name=destination_folder)
    fc.run_file_change_monitor_thread()

    fm = file_manager.FileManager(root=root_pth,
                                  source_folder_name=source_folder,
                                  destination_folder_name=destination_folder)
    fm.run_diff_copy_from_src_to_dst_thread()

    s = EZServer()
    s.start()

