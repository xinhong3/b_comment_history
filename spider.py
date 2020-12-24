import time
from datetime import datetime
from pytz import timezone

import csv
import sys

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# from selenium import JavascriptExecutor

class CommentCrawler(object):
    """docstring for CommentCrawler."""

    def __init__(self, videoSpace, crawlTime, runTime):
        super(CommentCrawler, self).__init__()
        self.videoSpace = videoSpace
        self.crawlTime = crawlTime
        self.runTime = runTime
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def main(self):

        driver = self.driver

        driver.get(self.videoSpace)

        # print(spaceWindow)

        lastestVideoPath = "//*[@id=\"page-index\"]/div[1]/div[1]/div/div[1]/a[2]"

        # lastestVideo = driver.find_element_by_xpath(lastestVideoPath)

        lastestVideo = WebDriverWait(driver,10).until(
        			EC.presence_of_element_located((By.XPATH, lastestVideoPath))
        		)

        lastestVideoLink = lastestVideo.get_attribute('href')

        last = "https://www.bilibili.com/video/BV1ny4y1D7F9"
        
        print(lastestVideoLink)




        while lastestVideoLink == last:
        	driver.refresh()
        	lastestVideo = WebDriverWait(driver,10).until(
        			EC.presence_of_element_located((By.XPATH, lastestVideoPath))
        		)
        	# lastestVideo = driver.find_element_by_xpath("//*[@id=\"page-index\"]/div[1]/div[1]/div/div[1]/a[2]")
        	lastestVideoLink = lastestVideo.get_attribute('href')
        	# spaceWindow = driver.current_window_handle
        	# print(spaceWindow)
        	print(lastestVideoLink)
        	time.sleep(5)

        spaceWindow = driver.current_window_handle

        ActionChains(driver).move_to_element(lastestVideo).click().perform()

        all_handles = driver.window_handles

        for handle in all_handles:
        	if handle != spaceWindow:
        		driver.switch_to.window(handle)


        c = open("data1.csv", "a")

        writer = csv.writer(c)

        fmt = '%Y-%m-%d %H:%M'
        china = timezone('Asia/Shanghai')

        # iter = 60*self.runTime//self.crawlTime


        # for i in range(0,iter):
        while True:

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

            try:
                # print(1)
                # load comments
                commentElement = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "page-jump"))
                )
                currTime = datetime.now(china).strftime(fmt)
                commentPath = "//*[@id=\"comment\"]/div/div[1]/span[1]"
                comment = driver.find_element_by_xpath(commentPath)
                writer.writerow([currTime, comment.text])
                print("time: {} \r comment: {} \r".format(currTime, comment.text))
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

    # old video
    website = "https://www.bilibili.com/video/BV1ny4y1D7F9"
    # video space
    space = "https://space.bilibili.com/390461123"

    # pause time(s)
    crawlTime = 10

    # run time(m)
    runTime = 5*60

    CommentCrawler(space, crawlTime, runTime).main()