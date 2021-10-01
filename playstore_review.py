from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    loop = 0

    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                content = browser.find_element_by_class_name("RveJvd snByac")
                browser.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(SCROLL_PAUSE_TIME)
                new_height = browser.execute_script("return document.body.scrollHeight")
            except NoSuchElementException as e:
                print(e)
                break
        last_height = new_height
    html = browser.page_source

    soup = BeautifulSoup(html, "html.parser")
    #users
    users = soup.select('span.X43Kjb')
    user_list = list()
    for user in users:
        if user.text != 'Petdoc':
            user_list.append(user.text)

    #stars
    star_list = list()
    stars = soup.select('span.nt2C1d > div > div')
    for star in stars:
        tmp = star['aria-label'].replace("별표 5개 만점에", "").replace("개를 받았습니다.", "")
        star_list.append(tmp)
    print(star_list)
    print(len(star_list),len(user_list))

    #reviews
    reviews = soup.select('div.UD7Dzf > span:nth-child(1)')
    review_list = list()
    for review in reviews:
        review_list.append(review.text)
    print(review_list)

    #date
    dates = soup.select('div.bAhLNe.kx8XBd > div > span.p2TkOb')
    date_list = list()
    for date in dates:
        date_list.append(date.text)

    res_dict = list()
    for u, s, r, d in zip(user_list, star_list, review_list, date_list):
        res_dict.append(
            {
                'USER': u,
                'STAR': s,
                'REVIEW': r,
                'DATE': d
            }
        )
    res_df = pd.DataFrame(res_dict)
    # res_df['DATE'] = pd.to_datetime(res_df['DATE'], format='%Y-%m-%d')
    res_df.to_csv('./test.csv', index=False, encoding='utf-8-sig')

    browser.quit()

if __name__ == "__main__":
    play_store_crawling()
