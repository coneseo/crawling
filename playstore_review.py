from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd


def play_store_crawling():
    url = 'https://play.google.com/store/apps/details?id=kr.co.petdoc.petdoc&hl=ko&gl=US&showAllReviews=true'
    option = Options()
    option.add_argument("disable-infobars")
    option.add_argument("disable-extensions")
    option.add_argument('disable-gpu')
    option.add_argument('headless')

    browser = webdriver.Chrome('./chromedriver', options=option)
    browser.get(url)

    SCROLL_PAUSE_TIME = 1
    SCROLL_MAX_NUM = 0
    last_height = browser.execute_script("return document.body.scrollHeight")
    print(last_height)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    loop = 0
    # while loop < last_height:
    #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     sleep(SCROLL_PAUSE_TIME)
    #
    #     try:
    #         browser.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
    #     except:
    #         pass
    #
    #     loop += 1

    html = browser.page_source

    soup = BeautifulSoup(html, "html.parser")
    users = soup.select('span.X43Kjb')
    user_list = list()
    for user in users:
        # print(user, user.text)
        if user.text != 'Petdoc':
            user_list.append(user.text)
    print(user_list)
    star_list = list()
    stars = soup.select('span.nt2C1d > div > div')
    for star in stars:
        tmp = star['aria-label'].replace("별표 5개 만점에", "").replace("개를 받았습니다.", "")
        star_list.append(tmp)
    print(star_list)
    print(len(star_list),len(user_list))
    # fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > div > div.W4P4ne > div:nth-child(2) > div:nth-child(3) > div:nth-child(54) > div > div.d15Mdf.bAhLNe > div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > span
    # fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > div > div.W4P4ne > div:nth-child(2) > div > div:nth-child(1) > div > div.d15Mdf.bAhLNe > div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > span
    # fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > div > div.W4P4ne > div:nth-child(2) > div > div:nth-child(1) > div > div.d15Mdf.bAhLNe > div.xKpxId.zc7KVe > div.bAhLNe.kx8XBd > div > span.nt2C1d > div > div



if __name__ == "__main__":
    play_store_crawling()
