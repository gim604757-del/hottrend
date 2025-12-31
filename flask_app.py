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

########################################
# GOOGLE 트렌드 (한국 기준, 최근 인기)
########################################
def get_google_trends():
    url = "https://trends.google.com/trending?geo=KR"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, timeout=8)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    keywords = []
    titles = soup.find_all("span")

    for t in titles:
        txt = t.get_text(strip=True)
        if len(txt) > 1:
            keywords.append(txt)

    # 중복 제거 + 30개 제한
    return list(dict.fromkeys(keywords))[:30]
########################################
# 공통 키워드 20개 추출
########################################
def get_hot_keywords():
    google = set(get_google_trends())
    naver = set(get_naver_trends())

    # 공통 키워드
    common = list(google & naver)

    # 20개 이하일 경우 추가 보충
    if len(common) < 20:
        extra = list((google | naver) - set(common))
        common.extend(extra)

    return common[:20]
########################################
# HTML
########################################
HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>한국 실시간 트렌드</title>

<style>
body { font-family: Arial; background:#111; color:white; text-align:center }
.box { width:70%; margin:auto; padding:20px; }
.keyword {
  background:#222;
  padding:15px;
  margin:8px;
  border-radius:10px;
  font-size:20px;
}
a { color:#00ff90; text-decoration:none }
</style>

</head>
<body>

<h1>🇰🇷 한국 실시간 공통 인기 키워드</h1>
<h3>Google + Naver 기준 (최근 트렌드)</h3>

<div class="box">
{% for k in keywords %}
<div class="keyword">
  {{ loop.index }}위 :
  <a target="_blank" href="https://www.google.com/search?q={{k}}">
    {{ k }}
  </a>
</div>
{% endfor %}
</div>

</body>
</html>
"""
