import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import time

channel = "https://www.youtube.com/channel/UCHt_gfJhwWgFPE1HtG1Y-hA"
contentList = []

driver = webdriver.Chrome()
page = driver.page_source
driver.get(channel+"/videos")
driver.maximize_window()

soup = BeautifulSoup(page, 'lxml')


lsat_height = driver.execute_script(
    "return document.documentElement.scrollHeight")

while True:
    driver.execute_script(
        "window.scrollTo(0, document.documentElement.scrollHeight);")

    time.sleep(5)

    new_height = driver.execute_script(
        "return document.documentElement.scrollHeight")
    if new_height == lsat_height:
        break
    lsat_height = new_height

    for i in range(len(lsat_height)):

        title = soup.find_all(
            'a', 'yt-simple-endpoint style-scope ydt-grid-video-renderer')[i]['title']
        url = soup.find_all(
            'a', 'yt-simple-endpoint style-scope ydt-grid-video-renderer')[i]['href']

        contentList.append({
            "제목": title,
            "url": url,
            "업로드 날짜": 0,
            "조회수": 0,
            "댓글": 0
        })
        print(i, title, url)
