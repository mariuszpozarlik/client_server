'''
Created on 14 cze 2022

@author: Mariusz
'''

import os
import socket

class PowerService:
    SHUTDOWN_SERVICE: str = "!SHUTDOWN"
    SHUTDOWN_SERVICE_FORCED: str ="!F_SHUTDOWN"
    RESTART_SERVICE: str = "!RESTART"
    RESTART_SERVICE_FORCED: str = "!F_RESTART" 
    ABORT_POWER_SERVICE: str = "!ABORT"
    DISCONNECT_SERVICE: str = "!DISCONNECT"    

    @classmethod
    def processService(cls, serv: str, conn: socket) -> None:
        if(serv == PowerService.SHUTDOWN_SERVICE):
            os.system("shutdown -s -t 60")
            conn.send(f"[RESPONSE FROM SERVER]-> server shutdown in 60s".encode('utf-8'))
            
        if(serv == PowerService.SHUTDOWN_SERVICE_FORCED):
            os.system("shutdown -s -f -t 60")
            conn.send(f"[RESPONSE FROM SERVER]-> server force shutdown in 60s".encode('utf-8'))
            
        if(serv == PowerService.RESTART_SERVICE):
            os.system("shutdown -r -t 60")
            conn.send(f"[RESPONSE FROM SERVER]-> server restart in 60s".encode('utf-8'))
            
        if(serv == PowerService.RESTART_SERVICE_FORCED):
            os.system("shutdown -r -f -t 60")
            conn.send(f"[RESPONSE FROM SERVER]-> server force restart in 60s".encode('utf-8'))
            
        if(serv == PowerService.ABORT_POWER_SERVICE):
            os.system("shutdown -a")
            conn.send(f"[RESPONSE FROM SERVER]-> server power service aborted".encode('utf-8'))

            
            
            