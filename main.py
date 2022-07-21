from bs4 import BeautifulSoup
import requests
import os
from threading import Thread
from threading import current_thread
import time
from urllib.parse import urlencode
import json
import dotenv

def get_proxy_url(url):
    API_KEY = os.getenv('API_KEY')
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

def main(x,y):
    url = "https://pagina12.com.ar/"
    bts = requests.get(url)
    soup = BeautifulSoup(bts.text, 'html.parser')
    urls = soup.find("div", {"class": "p12-dropdown-column"}).find_all('a', href=True)
    for link in urls[x:y]:
        r = requests.get(link.get('href'))
        time.sleep(1)
        s = BeautifulSoup(r.text, 'html.parser')
        title = s.find("title").text
        with open("links4.json", "a") as f:
            json.dump({'title':title,'thread': current_thread().getName()}, f, indent=4)

# start code
if __name__ == '__main__':
    dotenv.load_dotenv()
    t1 = Thread(target=main, args=(0,10))
    t2 = Thread(target=main, args=(10,20))
    t3 = Thread(target=main, args=(20,25))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print("Done!")