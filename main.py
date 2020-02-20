from bs4 import BeautifulSoup
import requests
import os

class earth():
    def __init__(self):
        self.hdr = {'User-Agent': 'Mozilla/5.0'}

        self.script_dir = os.path.dirname(__file__)

        self.base_url = "https://earthview.withgoogle.com"

        self.newpath = os.path.join(self.script_dir, "assets")
        if not os.path.exists(self.newpath):
            os.makedirs(self.newpath)

    def main_page(self):
        req = requests.get(self.base_url, headers = self.hdr)

        soup = BeautifulSoup(req.content, "html.parser")

        self.next_link = soup.find("a", {"class": "button intro__explore"})["href"]
    
    def download(self, link):
        if (link + ".jpg") not in os.listdir(self.newpath):
            url = "https://www.gstatic.com/prettyearth/assets/full/" + link.split("-")[-1] + ".jpg"
            r = requests.get(url, allow_redirects=True)
            open(self.newpath + link + ".jpg", 'wb').write(r.content)

            print ("Downloaded " + link[1:])
        else:
            print (link, "already exists. Skipping download.")
    
    def get_next_link(self):
        req = requests.get(self.base_url + "/" + self.next_link, headers = self.hdr)

        soup = BeautifulSoup(req.content, "html.parser")

        self.next_link = soup.find("a", {"class": "pagination__link pagination__link--next"})["href"]

    def main_loop(self):
        while True:
            self.download(self.next_link)
            self.get_next_link()

obj = earth()
obj.main_page()
obj.main_loop()