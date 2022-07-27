import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import math

# https://www.youtube.com/channel/UCHt_gfJhwWgFPE1HtG1Y-hA
channel_videos = "/videos"
driver = webdriver.Chrome()


def getChannelInfo():
    print("Input Youtube URL.")
    channel = input('Channel : ')
    print("Input Video counts. ")
    videos = int(input('Videos : '))
    countNum = math.ceil(videos / 30)
    openYoutube(channel)


def openYoutube(channel):
    channel = channel + channel_videos
    driver.maximize_window()
    driver.get(channel)


getChannelInfo()


def main():

    # 스크롤 내리기 => 한 번 당 영상 30개
    j = 0
    while j <= 13:
        driver.execute_script(
            "window.scrollTo(0,document.documentElement.scrollHeight);")
        time.sleep(1)
        j = j + 1
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    video_data = soup.find_all(
        'ytd-grid-video-renderer', {'class': 'style-scope ytd-grid-renderer'})
    print('start crawling')
    getInfo(video_data)


def getInfo(video_data):
    contentList = []

    print("let's go")
    for i in range(len(video_data)):
        if i % 10 == 0:
            print('휴식')
            time.sleep(4)
        # 동영상 제목, 개별 URL
        name = video_data[i].find('a', {'id': 'video-title'}).text
        temp_url = youtube_url + \
            video_data[i].find('a', {'id': 'thumbnail'})['href']
        # shorts 영상 형식 통일
        url = temp_url.replace('shorts/', 'watch?v=')
        driver.get(url)
        time.sleep(2)
        driver.execute_script(
            "window.scrollTo(0,document.documentElement.scrollHeight);")
        time.sleep(0.5)
        each_page = driver.page_source
        each_soup = BeautifulSoup(each_page, 'lxml')
        print(f'정보 수집 중 {i+1} / {len(video_data)}')
        # 조회수
        temp_view = each_soup.find(
            'span', {'class': 'view-count style-scope ytd-video-view-count-renderer'}).string
        view = temp_view.replace('조회수 ', '').replace('회', '')
        # 좋아요
        temp_like = each_soup.find_all(
            'yt-formatted-string', {'id': 'text'})
        like = temp_like[2].string

        # 데이터 저장
        contentList.append({
            "제목": name,
            "조회수": view,
            "좋아요": like,
            "URL": url
        })
        if i + 1 == len(video_data):
            print("수집 완료")
            contentList = pd.DataFrame(contentList)
            contentList.to_excel('youtube.xlsx')
            break
