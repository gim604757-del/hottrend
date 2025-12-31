from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
########################################
# NAVER 인기검색어 (대한민국 기준)
########################################
def get_naver_trends():
    url = "https://datalab.naver.com/keyword/realtimeList.naver?where=main"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, timeout=8)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    keywords = []
    ranks = soup.select(".list_group span.item_title")

    for r in ranks:
        keywords.append(r.text.strip())

    return keywords[:30]

