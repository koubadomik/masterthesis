#!/usr/bin/env python3

# Get meta data about samples from online services. Uses abuse.ch, metadefender and virustotal

import argparse
import os
import requests
import json
import hashlib
from time import sleep

#ABUSE
ABUSECH_URL = "https://mb-api.abuse.ch/api/v1/"
ABUSE_KEY = ""

#VIRUSTOTAL
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/files/"
VIRUSTOTAL_KEY = ""

#METADEFENDER
METADEFENDER_URL = "https://api.metadefender.com/v4/hash/"
METADEFENDER_KEY = ""

class BaseGetMeta():
    """ Abstract base class """
    def __init__(self, name, store=False, dir="."):
        self.store = store
        self.dir = dir
        self.engineName = name
        self.exceeded = False

    def storeResult(self, hash, data):
        if not os.path.exists(os.path.join(self.dir, hash)): os.mkdir(os.path.join(self.dir, hash))
        with open(os.path.join(self.dir, hash, self.engineName + "." + "json"), 'w') as f:
            json.dump(data, f)

    def fetchJsonMetadataByHash(self, hash):
        if self.fileExists(hash):
            print("File already exists, delete it if you want to regenerate")
            return
        status, result = self._fetchJsonMetadataByHash(hash)
        
        if int(status) == 200:
            if self.exceeded: self.exceeded = False
            print("OK")
            if self.store:
                self.storeResult(hash, result)
            else:
                print("Output for file {}:\n{}\n".format(hash, result))
            return
        
        elif int(status) == 404:
            if self.exceeded: self.exceeded = False
            print("Not found")
            with open("NotFound_{}.txt".format(self.engineName), 'a') as file:
                file.write("{}\n".format(hash))
            return
        
        elif int(status) == 429:
            print("Quota exceeded")
            if not self.exceeded:
                print("Sleep for a while...")
                self.exceeded = True
                sleep(1800)
                self.fetchJsonMetadataByHash(hash)
                return
            else:
                print("Sleep did not work, {} suspended".format(self.engineName))
                return
        else:
            print("Unknown status code: {}".format(status))

    def fileExists(self, hash):
        return os.path.exists(os.path.join(self.dir, hash, self.engineName + "." + "json"))

    def _fetchJsonMetadataByHash(self, hash):
        pass



class AbuseGetMeta(BaseGetMeta):

    def _fetchJsonMetadataByHash(self, hash):
        headers = {'API-KEY': ABUSE_KEY}
        data = {'query': 'get_info', 'hash': hash}
        r = requests.post(ABUSECH_URL, headers=headers, data=data)
        #print(r.status_code)
        return (r.status_code, r.json())





class VirustotalGetMeta(BaseGetMeta):
    def _fetchJsonMetadataByHash(self, hash):
        headers = {'x-apikey': VIRUSTOTAL_KEY}
        r = requests.get(requests.compat.urljoin(VIRUSTOTAL_URL, hash), headers=headers)
        #print(r.status_code)
        return (r.status_code, r.json())


    


class MetaDefenderGetMeta(BaseGetMeta):
    def _fetchJsonMetadataByHash(self, hash):
        headers = {'apikey': METADEFENDER_KEY}
        r = requests.get(requests.compat.urljoin(METADEFENDER_URL, hash), headers=headers)
        #print(r.status_code)
        return (r.status_code, r.json())



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
    parser = argparse.ArgumentParser("Get Meta information from online sources (VirusTotal, Abusech, Metadafender) for a specific file")
    parser.add_argument("--store_result_dir", help="Store the result in specified directory (name of file is <hash>.json), file is in its own directory named after hash")
    parser.add_argument("--file", help="File to get info for")
    parser.add_argument("--hash", help="Hash of file to get info for")
    parser.add_argument("--dir", help="Directory with files to get info for, according to hashes of files")
    parser.add_argument("--engines", help="comma-separated list of used engines, see their list in description, for all just type 'all'", default="all")
    args = parser.parse_args()
    
    store = args.store_result_dir is not None
    storeDir = args.store_result_dir

    fetchers = {'abusech': AbuseGetMeta("abusech", store=store, dir=storeDir ),
                'virustotal': VirustotalGetMeta("virustotal", store=store, dir=storeDir),
                'metadefender': MetaDefenderGetMeta("metadefender", store=store, dir=storeDir)}

    #choose metadata engines    
    chosen = []
    if args.engines == "all":
        chosen = list(fetchers.values())
    else:
        engines = [e.strip() for e in args.engines.split(",")]
        chosen = [fetchers[x] for x in engines if x in list(fetchers.keys())]
    
    #load input files
    toProcess = {'files':[], 'hashes':[]}
    if args.file is not None:
        toProcess['files'].append(args.file)
    if args.hash is not None:
        toProcess['hashes'].append(args.hash) #TODO check it is valid hash
    if args.dir is not None:
        for file in [x for x in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, x))]:
            toProcess['hashes'].append(hashFile(os.path.join(args.dir, file)))

    # fetch metadata for each file
    for engine in chosen:
        print("ENGINE: {} processing".format(engine.engineName))
        print("Processing files...")
        for file in toProcess['files']:
            pass
        print("Files processed.")
        print("Processing hashes...")
        for hash in toProcess['hashes']:
            print("Fetching info for: {}".format(hash))
            engine.fetchJsonMetadataByHash(hash)
            if engine.exceeded: break
        print("Hashes processed.")