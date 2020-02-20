from bs4 import BeautifulSoup
import requests
import os

class earth():
    def __init__(self):
        self.script_dir = os.path.dirname(__file__)

        self.base_url = "https://earthview.withgoogle.com"

    def main_page(self):
        hdr = {'User-Agent': 'Mozilla/5.0'}

        req = requests.get(self.base_url, headers = hdr)

        soup = BeautifulSoup(req.content, "html.parser")

        self.next_link = soup.find("a", {"class": "button intro__explore"})["href"]

        self.download(self.next_link)
    
    def download(self, link):
        if (link + ".jpg") not in os.listdir():
            url = "https://www.gstatic.com/prettyearth/assets/full/" + link[-5:] + ".jpg"
            r = requests.get(url, allow_redirects=True)
            open(self.script_dir + "/" + link + ".jpg", 'wb').write(r.content)

            print ("Downloaded " + link)
        else:
            print (link, "already exists. Skipping download.")

obj = earth()
obj.main_page()