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

    time.sleep(5)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')

    video_data = soup.find_all(
        'ytd-grid-video-renderer', {'class': 'style-scope ytd-grid-renderer'})

    # for i in range(len(video_data)):
    #     url = youtube_url + \
    #         video_data[i].find('a', {'id': 'thumbnail'})['href']
    #     video_url_list.append(url)

    for i in range(5):
        name = video_data[i].find('a', {'id': 'video-title'}).text
        url = youtube_url + \
            video_data[i].find('a', {'id': 'thumbnail'})['href']
        driver.get(url)

        time.sleep(3)

        each_page = driver.page_source
        each_soup = BeautifulSoup(each_page, 'lxml')

        try:
            container = each_soup.find(
                'span', {'class': 'view-count style-scope ytd-video-view-count-renderer'}).string
            print(name, container)
        except:
            print(name, "short")
