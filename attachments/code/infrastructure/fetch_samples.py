#!/usr/bin/env python3

from lxml import html
import requests
import argparse
from os import path
import os
from urllib.request import urlretrieve
from zipfile import ZipFile, BadZipfile

# On scraping: https://docs.python-guide.org/scenarios/scrape/
# https://www.w3schools.com/xml/xpath_syntax.asp

FILE="downloaded.txt"

class Abusefetch():
    """ Fetches samples from abuse.ch
    """

    url = "https://mb-api.abuse.ch/downloads/"

    def __init__(self, downloadpath, samplepath, limit, newestFirst=False, deleteArchives=False):
        """
        :param downloadpath: Path to store downloaded files. Works as cache
        :param samplepath: Path to store samples after extraction
        """

        self.dir = None
        self.download_path = path.join(path.abspath(downloadpath), "abuse")
        self.sample_path = path.abspath(samplepath)
        self.mainpage = None
        self.limit = limit
        self.newestFirst = newestFirst
        self.deleteArchives = deleteArchives
        self.prepare()

    def prepare(self):
        """ Prepares paths and environment
        :return:
        """

        if not path.exists(self.download_path):
            os.makedirs(self.download_path)

        if not path.exists(self.sample_path):
            os.makedirs(self.sample_path)
        if os.path.exists(FILE):
            with open(FILE, 'r') as file:
                self.cached = file.read().splitlines()
        else: self.cached = []


    def fetch(self):
        self.mainpage = requests.get(self.url).content


    def get_bundles(self, content):
        """ Gets a list of zip paths from the content
        :param content: text content of the download page
        :return: a list of tuples: package path, download url
        """

        tree = html.fromstring(content)
        links = list(filter(lambda x: x.endswith(".zip"), tree.xpath("//a[@href]/text()")))

        links = list(map(lambda x: (os.path.join(self.download_path, x), self.url + x), links))
        
        if self.newestFirst:
            links.reverse()

        return links[:self.limit] if self.limit != 0 else links

    def download(self, packages):
        """ Downloads packages
        :param packages: a list of tuples: package path, download url
        :return:
        """

        for (dest, url) in packages:
            
            if dest in self.cached: 
                print("{} found in cache".format(dest))
                continue

            if not path.exists(dest):
                print("{}: {}".format(url, dest))
                urlretrieve(url, dest)
            else:
                print("Already have: {}".format(dest))

    def extract(self, packages):
        """ Extracts downloaded packages into samples
        :param packages: a list of tuples: package path, download url
        """

        for (dest, url) in packages:
            
            if dest in self.cached: 
                continue

            try:
                with ZipFile(dest) as myzip:
                    print("Extracting: {}".format(dest))
                    myzip.setpassword(b"infected")
                    myzip.extractall(self.sample_path)
                    with open(FILE, 'a') as file:
                        file.write("{}\n".format(dest))
                    if self.deleteArchives:
                        if os.path.exists(dest):
                            os.remove(dest)
            except BadZipfile:
                print("Skipping zip file, bad zipfile...")

    def delete(self, packages): 
        for (dest, url) in packages:
            if os.path.exists(dest):
                os.remove(dest)

    def run(self):
        self.fetch()
        packages = self.get_bundles(self.mainpage)
        self.download(packages)
        self.extract(packages)
        #if self.deleteArchives:
        #    self.delete(packages)   


if __name__ == '__main__':
    parser = argparse.ArgumentParser("description")
    parser.add_argument("--samplepath", help="target directory for the samples", default="samples")
    parser.add_argument("--downloadpath", help="download directory for the samples", default="downloads")
    parser.add_argument("--limit", help="number of downloaded archives, if zero so all archives are fetched", type=int, default=0)
    parser.add_argument("--newest", help="For downloading from newest to oldest set this flag", action="store_true")
    parser.add_argument("--deletearchives", help="downloaded archives are deleted after extraction if this flag is set", action="store_true")
    args = parser.parse_args()

    a = Abusefetch(args.downloadpath, args.samplepath, args.limit, args.newest, args.deletearchives)
    a.run()
    print("Done")
