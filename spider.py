import time
from datetime import datetime
from pytz import timezone

import csv
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium import JavascriptExecutor

class CommentCrawler(object):
    """docstring for CommentCrawler."""

    def __init__(self, website, crawlTime, runTime):
        super(CommentCrawler, self).__init__()
        self.website = website
        self.crawlTime = crawlTime
        self.runTime = runTime
        self.driver = webdriver.Chrome()


    def main(self):
        c = open("data.csv", "w")

        writer = csv.writer(c)

        writer.writerow(['time', 'totalComment'])

        fmt = '%Y-%m-%d %H:%M'
        china = timezone('Asia/Shanghai')


        driver = self.driver

        driver.get(self.website)
        # self.assertIn("武汉", driver.title)
        # print(driver.title)

        iter = 60*self.runTime//self.crawlTime


        for i in range(0,iter):

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

            try:
                # print(1)
                # 加载评论区
                commentElement = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "page-jump"))
                )
                currTime = datetime.now(china).strftime(fmt)
                commentPath = "//*[@id=\"comment\"]/div/div[1]/span[1]"
                comment = driver.find_element_by_xpath(commentPath)
                writer.writerow([currTime, comment.text])
                # print(comment.text)
                driver.refresh()
                # print(2)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                pass

        #     className = "b-head-t"
        #     xPath = "//*[@id=\"comment\"]/div/div[1]/span[1]"
        # #
        #     comment = driver.find_element_by_xpath(xPath)
        #     # title = driver.find_element_by_xpath("/html/head/title")
        #     print(comment.text)

            # driver.refresh()
        # # print(title)
        #
            time.sleep(crawlTime)


if __name__ == '__main__':

    # 页面
    website = "https://www.bilibili.com/video/BV1ny4y1D7F9"

    # 抓取时间间隔(s)
    crawlTime = 60

    # 运行时间(m)
    runTime = 60

    CommentCrawler(website, crawlTime, runTime).main()
