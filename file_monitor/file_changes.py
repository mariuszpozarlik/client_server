from file_monitor.file_scaner import FileScanner
from threading import Thread
import os
import time

class FileChanges(FileScanner):

    """
    class with process to monitor file sync between server-storage and server-storage backup
    """

    def __init__(self, root: str = "", source_folder_name: str = "", destination_folder_name: str = ""):
        super().__init__(root, source_folder_name, destination_folder_name)
        self.file_list_save()
        self.file_change_background_task = Thread(target=self.__folder_change_monitor_background_job)

    def file_list_save(self):
        file_content = ""
        with open(file=os.path.join(self.src, "file list.txt"), mode='w') as file:  # save src
            [file.write(x+'\n') for x in self.scan_for_files()[0]]

        # with open(file=os.path.join(self.dst, "file list.txt"), mode='w') as file:  # save dst
        #     [file.write(x+'\n') for x in self.scan_for_files()[1]]

    def file_list_open(self):
        files_from_saved_list = []
        with open(file=os.path.join(self.src, "file list.txt"), mode='r') as file:
            for line in file:
                line = line[:-1]  # remove '\n'
                files_from_saved_list.append(line)
        return files_from_saved_list

    def run_file_change_monitor_thread(self):
        self.file_change_background_task.start()
        print("file change monitor Thread started")

    def __folder_change_monitor_background_job(self):
        while True:
            src_folder_content_current = sorted(self.scan_for_files()[0])
            src_folder_content_from_file = sorted(self.file_list_open())

            if src_folder_content_current != src_folder_content_from_file:
                self.file_list_save()
                print("updated list saved")

            time.sleep(60)

if __name__ == "__main__":
    fc = FileChanges(root="C:\\",
                     source_folder_name="server-storage",
                     destination_folder_name="server-storage-bckup")
    # fc.file_list_save()
    # fc.file_list_open()
    # fc.folder_change_monitor_backgound_job()
    fc.run_file_change_monitor_thread()

