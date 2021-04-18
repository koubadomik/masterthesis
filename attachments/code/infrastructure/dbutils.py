#!/usr/bin/env python3

import requests
import argparse
import os
import json
import urllib.parse
import hashlib
import time
from datetime import datetime
import copy
import logging


logging.basicConfig(format='%(asctime)s %(message)s', filename='statistics.log', level=logging.DEBUG)


class Util():
    def __init__(self, cache, directory, add, delete_active, clean_type):
        self.cache_file = cache
        self._load_cache()
        self.directory = directory
        self.add = add
        self.delete = delete_active
        self.clean_type = clean_type

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as file:
                self.cache = json.load(file)
        else:
            self.cache = {}

    def _store_cache(self):
        with open(self.cache_file, 'w') as file:
            json.dump(self.cache, file)

    def delete_active(self):
        cache = copy.deepcopy(self.cache)
        for k, v in self.cache.items():
            if cache[k]["type_active"] !="":
                cache[k]["type_active"] = ""
        self.cache = cache

    def clean_type_f(self, type):
        for item in self.cache.items():
            item[1]["types"] = [k for k in item[1]["types"] if k != {type: 1}]

    def add_new_files_to_db(self):
        cache = copy.deepcopy(self.cache)
        choose = [os.path.join(self.directory, x) for x in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, x))]
        for file in choose:
            hash = hashFile(file)
            if hash in cache:
                print("already in DB")
            else:
                report = {"file": file, "last_submitted": "", "target_machine": "", "type_active": "", "types": []}
                cache[hash] = report
        self.cache = cache

    def run(self):
        if self.add:
            self.add_new_files_to_db()
            self._store_cache()
            return
        if self.delete_active:
            self.delete_active()
            self._store_cache()
            return
        if self.clean_type is not None:
            self.clean_type_f(self.clean_type)
            self._store_cache()
            return

####UTILS#####
def hashFile(filePath):
    BLOCK_SIZE = 65536
    file_hash = hashlib.sha256()
    with open(filePath, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("file database utils")
    parser.add_argument("--cache", help="db of files and details, json file")
    parser.add_argument("--dir", help="file storage")
    parser.add_argument('--add', help="add new files from `dir`", action='store_true')
    parser.add_argument('--delete', help="delete `type_active` from each file in db", action='store_true')
    parser.add_argument("--clean_type")
    args = parser.parse_args()
    a = Util(args.cache, args.dir, add=args.add, delete_active=args.delete, clean_type=args.clean_type)
    a.run()