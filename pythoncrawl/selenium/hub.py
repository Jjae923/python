from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# blog.scrapinghub.com 사이트에서 검색어를 넣고
# 검색결과 중 타이틀 추출하기
driver = webdriver.Chrome("d:/webdriver/chromedriver.exe")

driver.get("https://blog.scrapinghub.com/")
driver.maximize_window()
driver.implicitly_wait(3)

assert "SCRAPINGHUB" in driver.title

# 검색창 창기
element = driver.find_element_by_name("term")
# 검색어 넣기
element.send_keys("scraping")
# 엔터
element.send_keys(Keys.RETURN)

titles = driver.find_elements_by_css_selector("div.hs-search-results > ul > li > a")
# titles = driver.find_elements_by_css_selector("ul#hsresults > li > a")

for title in titles:
    print(title.text)

time.sleep(3)

driver.quit()
