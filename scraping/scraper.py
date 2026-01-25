import requests
from bs4 import BeautifulSoup
import re
from constants.const import links
from utils.functions import scrapingTunisieTravail, scrapingTuniJob
def scraping(page: str):
    res = []
    for link in links:
        url = link+str(page)
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find all articles/offers
            if(link == "https://www.tunisietravail.net/page/"):
                res = scrapingTunisieTravail(soup, url)
            else:
                res = scrapingTuniJob(soup, url, page)
        else:
            print(f"Erreur: {response.status_code}")
            return []
    return res
