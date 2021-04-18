import ftplib
import argparse
import requests
import json
import os
import zipfile
import shutil

#FTP storage
URL=""
USER=""
PASSWORD=""

SANDBOX_URL = "http://localhost:8000/api/tasks/list/50/?status=reported"
CACHE_FILE = "cache.txt"

class Collector:
    def __init__(self, dir, server = URL, user = USER, password = PASSWORD):
        self.server = server
        self.user = user
        self.password = password
        self.dir = dir

    def run(self):
        self.load_cache()
        self.load_analysis()
        self.zip_and_send()
        with open(CACHE_FILE, 'w') as file:
            json.dump(self.analyses_cache, file)            

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as file:
                self.analyses_cache = json.load(file)
        else:
            self.analyses_cache = {'data': []}

    def delete_sent(self):
        for a in (a for a in self.analyses_cache['data']):
            print(os.path.join(self.dir, str(a[0])))
            if os.path.exists(os.path.join(self.dir, str(a[0]))):
                os.rmdir(os.path.join(self.dir, str(a[0])))

    def load_analysis(self):
        analyses = requests.get(SANDBOX_URL).json()['data']
        analyses = {'data': list(map(lambda x: (x['id'], x['sample']['sha256']), analyses))}
        self.analyses_load = analyses

    def zip_and_send(self):
        q = 0
        for a in (a for a in self.analyses_load['data'] if list(a) not in self.analyses_cache['data']):
            if os.path.exists(os.path.join(os.path.join(self.dir, str(a[0])))):
                q+=1
                zip_name = "{}.zip".format(str(a[1]))
                zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
                path = os.path.join(self.dir, str(a[0]))
                zipdir(path, zipf)
                zipf.close()
                try:
                    shutil.rmtree(os.path.join(self.dir, str(a[0])))
                except:
                    print("ERR")
                with ftplib.FTP(self.server, self.user, self.password) as ftp:
                    ftp.cwd("samples/sandbox/")
                    with open(zip_name, 'rb') as file:
                        ftp.storbinary('STOR {}'.format(zip_name), file)
                self.analyses_cache['data'].append(a)
                os.remove(zip_name)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Upload zipped analysis results to master ftp server")
    parser.add_argument("--dir", help="Directory with analyses files", default="/opt/CAPEv2/storage/analyses/")
    args = parser.parse_args()
    collector = Collector(args.dir)
    collector.run()