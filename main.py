from bs4 import BeautifulSoup
import requests
import os
import time

class earth():
    def __init__(self):
        self.hdr = {'User-Agent': 'Mozilla/5.0'}

        self.script_dir = os.path.dirname(__file__)

        self.base_url = "https://earthview.withgoogle.com"

        self.newpath = os.path.join(self.script_dir, "assets")
        if not os.path.exists(self.newpath):
            os.makedirs(self.newpath)

        self.now = time.time()
        self.count = 0

        self.timeout = 200 #seconds
        
        print ("Recommend running multiple parallel jobs")

    def main_page(self):
        req = requests.get(self.base_url, headers = self.hdr)

        soup = BeautifulSoup(req.content, "html.parser")

        self.next_link = soup.find("a", {"class": "button intro__explore"})["href"]
    
    def download(self, link):
        self.count += 1
        if (link[1:] + ".jpg") not in os.listdir(self.newpath):
            self.now = time.time()
            url = "https://www.gstatic.com/prettyearth/assets/full/" + link.split("-")[-1] + ".jpg"
            r = requests.get(url, allow_redirects=True)
            open(self.newpath + link + ".jpg", 'wb').write(r.content)

            print ("Downloaded " + link[1:])
        else:
            print ("Skipping", link[1:])
    
    def get_next_link(self):
        req = requests.get(self.base_url + "/" + self.next_link, headers = self.hdr)

        soup = BeautifulSoup(req.content, "html.parser")

        self.next_link = soup.find("a", {"class": "pagination__link pagination__link--next"})["href"]

    def main_loop(self):
        while time.time() - self.now < self.timeout:
            self.download(self.next_link)
            self.get_next_link()
        print ("Done")
        print (self.count)

obj = earth()
obj.main_page()
obj.main_loop()
input()