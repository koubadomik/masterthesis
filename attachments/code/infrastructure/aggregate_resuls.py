import argparse
import os
import json
import logging

TYPES = ["nointernet", "internet"]
logging.basicConfig(format='%(asctime)s %(message)s', filename='aggregate.log', level=logging.DEBUG)

class Aggregator():
    def __init__(self, source, target, cache):
        self.source = source
        self.target = target
        self.cache_file = cache
        self._load_files_from_source()
        self._load_cache()

    
    def _load_files_from_source(self):
        self.files = [x for x in os.listdir(self.source) if x.split(".")[1] == 'zip' ]

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as file:
                self.cache = json.load(file)
        else:
            self.cache = {}

    def _store_cache(self):
        with open(self.cache_file, 'w') as file:
            json.dump(self.cache, file)
        logging.info("Cache stored ok")
    
    def update_db_received(hash, last_type):
        self.cache[hash]["type_active"] = "invalid"
        self.cache[hash]["type_active"] = ""
        self.cache[hash]["types"].append({last_type: 1})

    def move_files_to_target(self):
        for file in self.files:
            count = 0
            hash = file.split(".")[0]
            last_type = self.cache[hash]["type_active"]
            logging.info('receive: {} info: {}'.format(hash, self.cache[hash]))
            if not os.path.exists(os.path.join(self.target, last_type, hash)):
                os.mkdir(os.path.join(self.target, last_type,  hash))
            else:
                count = len([x for x in os.listdir(os.path.join(self.target, last_type, hash))])
            os.mkdir(os.path.join(self.target, last_type, hash, str(count)))
            os.system("zip -d {} opt/CAPEv2/storage/analyses/*/binary".format(os.path.join(self.source, file)))
            os.system("mv {} {}".format(os.path.join(self.source, file), os.path.join(self.target, last_type, hash, str(count))))
            self.update_db_received(hash, last_type)
            

    def run(self):
        self.move_files_to_target()
        self._store_cache()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("move analysis results from one directory to another, place particular file in own directory and ensure deduplication")
    parser.add_argument("--source", help="directory to get result analyses from")
    parser.add_argument("--target", help="directory to store final results")
    parser.add_argument("--cache", help="file where db of hashes is stored")
    args = parser.parse_args()
    a = Aggregator(args.source, args.target, args.cache)
    a.run()