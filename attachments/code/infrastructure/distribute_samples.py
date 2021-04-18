#!/usr/bin/env python3
import requests
import argparse
import os
import json
import urllib.parse
import hashlib
import time
from datetime import datetime
from collections import namedtuple
import logging

MINUTES_PER_TASK = 5
QUOTIENT = 2
PORT = 8000
TASK_SUBMIT_URL = "/api/tasks/create/file/"
TASK_EXISTS_URL = "/api/files/view/sha256/"
TYPES = ["nointernet", "internet"]

logging.basicConfig(format='%(asctime)s %(message)s', filename='send.log', level=logging.DEBUG)

class Sender():
    def __init__(self, path, cache, machines):
        self.path = path
        self.cache_file = cache
        self.machine_file = machines
        self._load_machines()
        self._load_cache()
        self._load_files_to_analyse()

    
    
    def _load_files_to_analyse(self):
        self.files = {}
        for type in TYPES:
            self.files[type] = list(filter(lambda file: file[1]["type_active"] == "", list(self.cache.items())))
            self.files[type] = list(filter(lambda file: type not in [item for sublist in list(map(lambda t: list(t.keys()),file[1]["types"])) for item in sublist], self.files[type]))
            if len(self.files[type]) < self.machines[type]["count"]:
                self.machines[type]["count"] = len(self.files[type])
                continue
            else:
                self.files[type] = self.files[type][:self.machines[type]["count"] -1]
            for key in self.files[type]:
                self.cache[key[0]]["type_active"] = type
   

    def _load_machines(self):
        machines = []
        self.machines = {}
        #load machines
        with open(self.machine_file, 'r') as file:
            machines = json.load(file)["machines"]
        #set number of files per type of analysis
        for type in TYPES:
            self.machines[type] = {}
            self.machines[type]["machines"] = list(filter(lambda machine:  machine["type"] == type, machines))
            machine_count = len([x['machine_count'] for x in self.machines[type]["machines"] if x['enabled']])
            self.machines[type]["count"] = QUOTIENT * ((60 // MINUTES_PER_TASK) * sum([x['machine_count'] for x in self.machines[type]["machines"] if x['enabled']]))
            if (self.machines[type]["count"] % machine_count) > 0:
                self.machines[type]["count"] = self.machines[type]["count"] + (machine_count - (self.machines[type]["count"] % machine_count))

    def send(self, file, ip):
        time.sleep(2) #better for sandbox api
        #using curl led us to expected result, python.requests does not, cause was not identified
        logging.info("curl -F file=@{} {}:{}{}".format(file, ip, PORT, TASK_SUBMIT_URL))
        os.system("curl -F file=@{} {}:{}{}".format(file, ip, PORT, TASK_SUBMIT_URL))
    
    def update_sent_db(index, type, machine):
        self.cache[self.files[type][index][0]]["last_submitted"] = "{}".format(datetime.now())
        self.cache[self.files[type][index][0]]["target_machine"] = machine["ip"]
        self.cache[self.files[type][index][0]]["type_active"] = type

    def distribute(self):
        if enough_available():
            for type in TYPES:
                logging.info("Sending to type: {} to send we have {} files and we have {} machine/s".format(type, self.machines[type]["count"], len(self.machines[type]["machines"])))
                index = 0
                for machine in self.machines[type]["machines"]:
                    if not machine["enabled"]: continue
                    for _ in range(self.machines[type]["count"] // len(self.machines[type]["machines"])):
                        logging.info(self.cache[self.files[type][index][0]])
                        self.send(self.files[type][index][1]["file"], machine["ip"])
                        self.update_sent_db(index, type, machine)
                        index += 1
                        if index == len(self.files[type]):
                            logging.info("All files were sent")
                            break

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as file:
                self.cache = json.load(file)
        else:
            self.cache = {}

    def _store_cache(self):
        with open(self.cache_file, 'w') as file:
            json.dump(self.cache, file)
        logging.info("Cache stored")

    def run(self):
        self.distribute()
        self._store_cache()
        self._log_stats()


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
    parser = argparse.ArgumentParser("distrubute specified number of malware samples to sandbox instances")
    parser.add_argument("--path", help="directory to get file from")
    parser.add_argument("--cache", help="db of files and details, json file")
    parser.add_argument("--machines", help="machines config file, json")
    args = parser.parse_args()
    a = Sender(args.path, args.cache, args.machines)
    a.run()