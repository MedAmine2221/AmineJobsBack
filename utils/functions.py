import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote

def scrapingTunisieTravail(soup, url):
    res = []
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
    return res

def scrapingTuniJob(soup, url, page):
    res = []
    title_elem = soup.find_all("h3")
    img_elem = soup.find_all("img")
    for h3, img in zip(title_elem, img_elem):
        a = h3.find_parent("a")
        if not a:
            continue
        
        lien = a.get("href")
        if not lien:
            continue
        
        if not lien.startswith("http"):
            lien = url.rstrip('/').replace("/jobs?page="+str(page), "") + '/' + lien.lstrip('/')
        title = h3.get_text(strip=True)
        img_link = img.get("src")
        try:
            link_response = requests.get(lien, timeout=5)
        except Exception as e:
            print("link error:", lien, e)
            continue
        
        if link_response.status_code == 200:
            link_soup = BeautifulSoup(link_response.text, "html.parser")
            svgs = link_soup.find_all("svg")
            if svgs:
                for s in svgs:
                    path = s.find_all("path")
                    if path:
                        for p in path:
                            if(p.get("d") == "M4 19V8h16v3.29c.72.22 1.4.54 2 .97V8c0-1.11-.89-2-2-2h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h7.68c-.3-.62-.5-1.29-.6-2H4zm6-15h4v2h-4V4z"):
                                exp = s.find_parent("div").find_parent("div").find("p", class_="font-semibold").get_text(strip=True)
                            elif(p.get("d") == "M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"):
                                contract = s.find_parent("div").find_parent("div").find("p", class_="font-semibold").get_text(strip=True)
                            elif(p.get("d") == "M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"):
                                working_type = s.find_parent("div").find_parent("div").find("p", class_="font-semibold").get_text(strip=True)
                            elif(p.get("d") == "M319.4 320.6L224 416l-95.4-95.4C57.1 323.7 0 382.2 0 454.4v9.6c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48v-9.6c0-72.2-57.1-130.7-128.6-133.8zM13.6 79.8l6.4 1.5v58.4c-7 4.2-12 11.5-12 20.3 0 8.4 4.6 15.4 11.1 19.7L3.5 242c-1.7 6.9 2.1 14 7.6 14h41.8c5.5 0 9.3-7.1 7.6-14l-15.6-62.3C51.4 175.4 56 168.4 56 160c0-8.8-5-16.1-12-20.3V87.1l66 15.9c-8.6 17.2-14 36.4-14 57 0 70.7 57.3 128 128 128s128-57.3 128-128c0-20.6-5.3-39.8-14-57l96.3-23.2c18.2-4.4 18.2-27.1 0-31.5l-190.4-46c-13-3.1-26.7-3.1-39.7 0L13.6 48.2c-18.1 4.4-18.1 27.2 0 31.6z"):
                                study_lvl = s.find_parent("div").find_parent("div").find("p", class_="font-medium text-gray-800").get_text(strip=True)
                            elif(p.get("d") == "M9 22v-4h6v4"):
                                company_desc = []
                                company = s.find_parent("div").find_parent("div").find_all("p")
                                if company:
                                    for i in company:
                                        company_desc.append(i.get_text(strip=True))
                            elif(p.get("d") == "M10.35 14.01C7.62 13.91 2 15.27 2 18v2h9.54c-2.47-2.76-1.23-5.89-1.19-5.99zM19.43 18.02c.36-.59.57-1.28.57-2.02 0-2.21-1.79-4-4-4s-4 1.79-4 4 1.79 4 4 4c.74 0 1.43-.22 2.02-.57L20.59 22 22 20.59l-2.57-2.57zM16 18c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"):
                                profil_searched = []
                                profil = s.find_parent("div").find_parent("div").find_all("p")
                                if profil:
                                    for i in profil:
                                        profil_searched.append(i.get_text(strip=True))
                            elif(p.get("d") == "M528.1 171.5L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6zM388.6 312.3l23.7 138.4L288 385.4l-124.3 65.3 23.7-138.4-100.6-98 139-20.2 62.2-126 62.2 126 139 20.2-100.6 98z"):
                                skills=[]
                                skill = s.find_parent("div").find_parent("div").find_all("div", class_= "inline-flex items-center rounded-md border transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent shadow bg-blue-50 text-blue-800 hover:bg-blue-200 px-3 py-1 text-xs font-medium")
                                if skill:
                                    for i in skill:
                                        skills.append(i.get_text(strip=True))
                            elif(p.get("d") == "M100,100a12,12,0,0,1,12-12h32a12,12,0,0,1,0,24H112A12,12,0,0,1,100,100ZM236,68V196a20,20,0,0,1-20,20H40a20,20,0,0,1-20-20V68A20,20,0,0,1,40,48H76V40a28,28,0,0,1,28-28h48a28,28,0,0,1,28,28v8h36A20,20,0,0,1,236,68ZM100,48h56V40a4,4,0,0,0-4-4H104a4,4,0,0,0-4,4ZM44,72v35.23A180.06,180.06,0,0,0,128,128a180,180,0,0,0,84-20.78V72ZM212,192V133.94A204.27,204.27,0,0,1,128,152a204.21,204.21,0,0,1-84-18.06V192Z"):
                                post_desc = []
                                post = s.find_parent("div").find_parent("div").find_all("p")
                                if post:
                                    for i in post:
                                        post_desc.append(i.get_text(strip=True))
                            
        res.append({
            # "link": lien,
            "experience": exp,
            "contract_type": contract,
            "working_type": working_type,
            "study_level": study_lvl,
            "profile": profil_searched,
            "company_desc": company_desc,
            "post_desc": post_desc,
            "skills": skills,
            "title": title,
            "image": unquote(img_link.replace("/_next/image?url=", "")) if img_link else None
        })
    return res