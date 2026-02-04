import requests
from bs4 import BeautifulSoup
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
            elif(link == "https://www.tunijobs.com/jobs?page="):
                res = scrapingTuniJob(soup, url, page)
            else:
                articles = soup.find_all("article")
                if articles:
                    a = articles.find("a")
                    if a:
                        lien = a.get("href")
                        if not lien:
                            continue
        
                        if not lien.startswith("http"):
                            lien = url.rstrip('/').replace("/?page="+str(page), "") + '/' + lien.lstrip('/')
        else:
            print(f"Erreur: {response.status_code}")
            return []
    return res
