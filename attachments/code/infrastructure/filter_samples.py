#!/usr/bin/env python3
# Filter files by specified file type
import os
import magic
import argparse


FILE="deletedFiles.txt"


class BaseFilter:
    """ Abstract base class """

    def __init__(self, dir, movedir):
        self.dir = dir
        self.movedir = movedir

    def filter(self):
        self.filesToDelete = [f for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir, f))]
        self.filterFilesToDelete()

    def filterFilesToDelete(self):
        pass

    def deleteFiles(self):
        try:
            os.remove(FILE)
        except OSError:
            pass
        for file in self.filesToDelete:
            print("file {} deleted".format(os.path.join(self.dir, file)))
            with open(FILE, 'a') as outFile:
                outFile.write("{}\t{}\n".format(file, magic.from_file(os.path.join(self.dir,file))))

class PortableExecutableFilter(BaseFilter):
    def filterFilesToDelete(self):
        toDelete = []
        for file in self.filesToDelete:
            metadata = magic.from_file(os.path.join(self.dir, file)).split(" ")
            if "PE32" in metadata or "PE32+" in metadata or "executable" in metadata or file.split(".")[-1] in ["acm", "ax", "cpl",
                                                                                                  "dll", "drv", "efi",
                                                                                                  "exe", "mui", "ocx",
                                                                                                  "scr", "sys",
                                                                                                  "tsp"]:  # list here https://en.wikipedia.org/wiki/Portable_Executable
                
                os.rename(os.path.join(self.dir, file), os.path.join(self.movedir, file))
        print("Overall {} / Deleted {}".format(len(self.filesToDelete), len(toDelete)))
        self.filesToDelete = toDelete


class ZipFilter(BaseFilter):
    def filterFilesToDelete(self):
        toDelete = []
        for file in self.filesToDelete:
            metadata = magic.from_file(os.path.join(self.dir, file)).split(" ")
            if "Zip" in metadata:
                os.rename(os.path.join(self.dir, file), os.path.join(self.movedir, file))
        self.filesToDelete = toDelete


if __name__ == '__main__':
    parser = argparse.ArgumentParser("description")
    parser.add_argument("dir", help="directory to be filtered in")
    parser.add_argument("movedir", help="directory where filtered files should be moved")
    parser.add_argument("type", choices=["exe", "zip"], help="type of files to be filtered from selected directory")
    args = parser.parse_args()
    
    if args.type == "exe":
        PortableExecutableFilter(args.dir, args.movedir).filter()
    if args.type == "zip":
        ZipFilter(args.dir, args.movedir).filter()
    else:
        print("Bad choice of file type")
    print("Filtering done")