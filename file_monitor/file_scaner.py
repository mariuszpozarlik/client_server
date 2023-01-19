'''
Created on 16 sty 2023

@author: Mariusz-Laptop
'''

import os

class FileScanner(object):
    """
    class to implement functionality for differences in folder contents
    """

    def __init__(self, root: str = "", source_folder_name: str = "", destination_folder_name: str = ""):
        self.src_folder_name = source_folder_name
        self.dst_folder_name = destination_folder_name
        self.src = os.path.join(root, source_folder_name)
        self.dst = os.path.join(root, destination_folder_name)
        self.paths_ok = False
        if os.path.exists(self.src) and os.path.exists(self.dst):
            print("paths exits")
            self.paths_ok = True
        else:
            print("path doesnt exist")
            try:
                os.mkdir(self.dst)
                self.paths_ok = True
            except Exception as e:
                print(e.__class__)
                print(e.__cause__)

    def is_paths_ok(self):
        return self.paths_ok
    
    def scan_for_files(self):
        files_in_src = []
        files_in_dst = []

        if self.is_paths_ok():
            for root, dirs, files in os.walk(top=self.src, topdown=False):
                for name in files:
                    files_in_src.append(os.path.join(root, name))

            for root, dirs, files in os.walk(top=self.dst, topdown=False):
                for name in files:
                    files_in_dst.append(os.path.join(root, name))
        return files_in_src, files_in_dst

    def search_for_differences(self):
        diff = []
        fsrc, fdst = self.scan_for_files()
        try:
            for fs in fsrc:
                #  temporarly replace source path to destination only for content comparision
                check = fs.replace(self.src, self.dst)
                if check not in fdst:
                    diff.append(fs)
                    print(fs.encode(encoding="utf-8"))
        except Exception as e:
            print(e.__class__)
        return diff

if __name__ == "__main__":
    scan = FileScanner(root=r"C:\Users\Mariusz-Laptop\Desktop",
                       source_folder_name="s1",
                       destination_folder_name="s2")
    scan.search_for_differences()