"""
Created on 16 sty 2023

@author: Mariusz
"""

import os
from shutil import copy2, rmtree, copytree
from file_monitor.file_scaner import FileScanner
from threading import Thread
from time import sleep

class FileManager(FileScanner):

    """
    Class that copies from source folder do destination folder.
    It implements two functionalities:
    1. Copy all in separate thread
    2. Copy only differences in separate thread. This method cycles in the loop
    """

    def __init__(self, root: str = "", source_folder_name: str = "", destination_folder_name: str = ""):
        super().__init__(root, source_folder_name, destination_folder_name)
        self.full_copy_thread = Thread(target=self.__copy_all_from_src_to_dst)
        self.diff_copy_thread = Thread(target=self.__copy_update_missing_from_src_to_dst)
        self.is_copying = False

    def run_copy_all_from_src_to_dst_thread(self):
        if self.is_copying:
            return
        self.full_copy_thread.start()
        self.is_copying = True
        print("full copy Thread started")

    def run_diff_copy_from_src_to_dst_thread(self):
        if self.is_copying:
            return
        self.diff_copy_thread.start()
        print("update copy Thread started")

    def __copy_all_from_src_to_dst(self):
        rmtree(self.dst)
        copytree(self.src, self.dst)
        self.is_copying = False
        print("Copying done")

    def __copy_update_missing_from_src_to_dst(self):
        while True:
            diff_list = self.search_for_differences()
            # diff_list.reverse()  # reverse is required because list starts from the deepest path
            for file in diff_list:
                self.is_copying = True
                file_dir = file.split("\\")[0:-1]
                file_dir[0] += '\\'
                p = os.path.join(*file_dir).replace(self.src, self.dst)
                p_ = p.split('\\')
                p_[0] += '\\'
                try:
                    if not os.path.exists(p):  # destination path doesn't exist
                        temp_dir = os.path.join(p_[0])
                        for dir_part in p_[1:]:  # building destination path
                            temp_dir = os.path.join(temp_dir, dir_part)
                            if not os.path.exists(temp_dir):
                                os.mkdir(temp_dir)
                    copy2(file, p)
                except Exception as e:
                    print(e.__cause__)
                    print(e.__class__)
                finally:
                    print(f"copied {file}, to {p}")
            self.is_copying = False
            sleep(60)
            pass  # TODO


if __name__ == "__main__":
    filemng = FileManager(root="C:\\",
                          source_folder_name="server-storage",
                          destination_folder_name="server-storage-bckup")
    # filemng.run_copy_all_from_src_to_dst_thread()
    # filemng.run_copy_all_from_src_to_dst_thread()
    filemng.run_diff_copy_from_src_to_dst_thread()

