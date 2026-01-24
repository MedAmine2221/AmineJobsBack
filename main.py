# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from scraping.scraper import scraping
app = FastAPI()


@app.get("/")
def home():
    return RedirectResponse(url= "/scraping/1")

@app.get("/scraping/{page}")
def scrape(page: str):
    res = scraping(page)
    return res
