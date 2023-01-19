'''
Created on 14 cze 2022

@author: Mariusz
'''

import os
import socket
from file_monitor.file_manager import FileManager

class Service:
    PowerServices = {"SHUTDOWN_SERVICE" : "!SHUTDOWN",
    "SHUTDOWN_SERVICE_FORCED" : "!F_SHUTDOWN",
    "RESTART_SERVICE" : "!RESTART",
    "RESTART_SERVICE_FORCED" : "!F_RESTART" ,
    "ABORT_POWER_SERVICE" : "!ABORT",
    "DISCONNECT_SERVICE" : "!DISCONNECT"}

    HelpServices = {"HELP_SERVICE" : "?HELP"}

    BackupServices = {"BACKUP_FOLDER_FULL_COPY": "!GLOBAL_BACKUP",
    "BACKUP_FOLDER_SYNC_STATUS": "?GLOBAL_BACKUP_STATUS",
    "RESYNC_BACKUP_FOLDER": "!RESYNC_BACKUP"}

    @classmethod
    def processPowerService(cls, serv: str) -> None:
        if(serv == Service.PowerServices["SHUTDOWN_SERVICE"]):
            os.system("shutdown -s -t 60")

        if(serv == Service.PowerServices["SHUTDOWN_SERVICE_FORCED"]):
            os.system("shutdown -s -f -t 60")

        if(serv == Service.PowerServices["RESTART_SERVICE"]):
            os.system("shutdown -r -t 60")

        if(serv == Service.PowerServices["RESTART_SERVICE_FORCED"]):
            os.system("shutdown -r -f -t 60")

        if(serv == Service.PowerServices["ABORT_POWER_SERVICE"]):
            os.system("shutdown -a")

        if(serv in Service.PowerServices.values()):
            return True
        return False

    @classmethod
    def processHelpService(cls, serv: str) -> None:
        if(serv == Service.HelpServices["HELP_SERVICE"]):
            return (True, "Available options:\n" \
                    "!SHUTDOWN              -> Shutdown server\n" \
                    "!F_SHUTDOWN            -> Force shutdown server\n" \
                    "!RESTART               -> Restart server\n" \
                    "!F_RESTART             -> Force restart server\n" \
                    "!ABORT                 -> abort scheduled actions\n" \
                    "!DISCONNECT            -> disconnect from the server\n" \
                    "!GLOBAL_BACKUP         -> backup all files from server-storage")
        return False, ""

    @classmethod
    def processBackupServices(cls, serv: str) -> None:
        if(serv == Service.BackupServices["BACKUP_FOLDER_FULL_COPY"]):
            fm = FileManager(root="C:\\", source_folder_name="server-storage", destination_folder_name="server-storage-bckup")
            fm.run_copy_all_from_src_to_dst_thread()
            return fm.is_copying

        if(serv == Service.BackupServices["RESYNC_BACKUP_FOLDER"]):
            fm = FileManager(root="C:\\", source_folder_name="server-storage", destination_folder_name="server-storage-bckup")
            fm.run_diff_copy_from_src_to_dst_thread()
            return fm.is_copying #TODO
