import requests
from bs4 import BeautifulSoup
import re
from constants.const import links
from urllib.parse import urlparse, parse_qs, unquote

def scraping(page: str):
    res = []
    for link in links:
        url = link+str(page)
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find all articles/offers
            if(link == "https://www.tunisietravail.net/page/"):
                articles = soup.find_all("article") # or the appropriate container
                for article in articles:
                    # Extract title
                    titre_elem = article.find("h2")
                    titre = titre_elem.get_text(strip=True) if titre_elem else "Pas de titre"
                    
                    # Extract the link from the "Details" button
                    bouton_detail = article.find("a", string=lambda text: text and "Détail" in text)
                    # Or, if the button has a specific class:
                    # button_detail = article.find("a", class_="btn-detail")
                    
                    lien = bouton_detail.get("href") if bouton_detail else None
                    
                    # If the link is relative, complete it
                    if lien and not lien.startswith("http"):
                        lien = url.rstrip('/') + '/' + lien.lstrip('/')
                    
                    noscript = article.find("noscript")
                    if(noscript):
                        img = noscript.find("img")

                    response_details = requests.get(lien)
                    if response_details.status_code == 200:
                        detail_info = []
                        details = BeautifulSoup(response_details.text, "html.parser")
                        post = details.find("div",class_="PostContent")
                        post_infos = post.find_all("p")
                        for p in post_infos:
                            send_cv_button = p.find("button")
                            detail_info.append(p.get_text(strip=True))                                              
                            if(send_cv_button):
                                onclick = send_cv_button.get("onclick")
                                link = re.search(r"'([^']+)'", onclick).group(1)
                                res.append({
                                    "title": titre,
                                    "image": img["src"],
                                    "post_infos": {
                                        "send_cv": link,
                                        "detail_info": detail_info
                                    }
                                })
            else:
                title_elem = soup.find_all("h3")
                img_elem = soup.find_all("img")
                for h3, img in zip(title_elem, img_elem):
                    title = ""
                    lien = ""
                    a = h3.find_parent("a")
                    if a:
                        lien = a.get("href")
                    if lien and not lien.startswith("http"):
                        lien = url.rstrip('/').replace("/jobs?page=1", "") + '/' + lien.lstrip('/')
                    title = h3.get_text(strip=True)
                    img_link = img.get("src")
                    res.append({
                        "link": lien,
                        "title": title,
                        "image": img_link.replace("/_next/image?url=", "")
                    })                    
            
        else:
            print(f"Erreur: {response.status_code}")
            return []
    return res
