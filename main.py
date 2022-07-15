import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time

channel = "https://www.youtube.com/channel/UCHt_gfJhwWgFPE1HtG1Y-hA/videos"
youtube_url = "https://www.youtube.com"
contentList = []

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(channel)


lsat_height = driver.execute_script(
    "return document.documentElement.scrollHeight")

last_element = []
video_url_list = []

while True:
    driver.execute_script(
        "window.scrollTo(0,document.documentElement.scrollHeight);")

    time.sleep(2)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')

    video_data = soup.find_all(
        'ytd-grid-video-renderer', {'class': 'style-scope ytd-grid-renderer'})

    for i in range(5):
        # for i in range(len(video_data)) :
        # 동영상 제목, 개별 URL
        name = video_data[i].find('a', {'id': 'video-title'}).text
        temp_url = youtube_url + \
            video_data[i].find('a', {'id': 'thumbnail'})['href']

        # shorts 영상 형식 통일
        url = temp_url.replace('shorts/', 'watch?v=')

        driver.get(url)
        time.sleep(3)

        driver.execute_script(
            "window.scrollTo(0,document.documentElement.scrollHeight);")

        time.sleep(1)

        each_page = driver.page_source
        each_soup = BeautifulSoup(each_page, 'lxml')

        # 조회수
        temp_view = each_soup.find(
            'span', {'class': 'view-count style-scope ytd-video-view-count-renderer'}).string
        view = temp_view.replace('조회수 ', '').replace('회', '')

        # 좋아요
        temp_like = each_soup.find_all(
            'yt-formatted-string', {'id': 'text'})
        like = temp_like[2].string

        # 댓글 ing
        temp_comments = each_soup.find_all(
            'ytd-comments', {'id': 'comments', 'class': 'style-scope ytd-watch-flexy'})
        ble = each_soup.find_all(
            'ytd-item-section-renderer', {'id': 'sections'})

        # 데이터 저장
        contentList.append({
            "제목": name,
            "조회수": view,
            "좋아요": like,
            "URL": url
        })
