import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
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
while True:
    driver.execute_script(
        "window.scrollTo(0,document.documentElement.scrollHeight);")

    time.sleep(5)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')

    video_data = soup.find_all(
        'ytd-grid-video-renderer', {'class': 'style-scope ytd-grid-renderer'})

    video_url_list = []
    for i in range(len(video_data)):

        url = youtube_url + \
            video_data[i].find('a', {'id': 'thumbnail'})['href']
        video_url_list.append(url)
    print(video_url_list)

    dataframe = pd.DataFrame(
        {'name': [], 'view_count': [], 'youtube_url': [], 'date': [], 'desc': []})
