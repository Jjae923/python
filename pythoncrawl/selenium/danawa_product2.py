# 다나와 사이트에서 노트북 정보 가져오기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

# 파싱 라이브러리
from bs4 import BeautifulSoup

# 엑셀 저장
import openpyxl
# 이미지를 저장
import requests
from io import BytesIO

# excel 기본 작업
workbook = openpyxl.Workbook()
sheet1 = workbook.active
sheet1.column_dimensions['A'].width = 52
sheet1.column_dimensions['B'].width = 18
sheet1.column_dimensions['C'].width = 10
sheet1.append(['제품명','가격','이미지'])

options = webdriver.ChromeOptions()
# 브라우저 안 띄우기
# options.add_argument("headless")
# 그래픽 카드 사용 안하기
options.add_argument("disable-gpu")
# 브라우저 크기 지정
options.add_argument("window-size=1920,1080")
# user-agent 지정
options.add_argument(
    "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
)

driver = webdriver.Chrome("d:/webdriver/chromedriver.exe", options=options)

# 크롬 브라우저 내부 대기
driver.implicitly_wait(3)
driver.get("http://prod.danawa.com/list/?cate=112758")

# 테스트 코드
# print(driver.title)
assert "Danawa.com" in driver.title

# 현재 페이지
cur_page = 1
# 크롤링 페이지 수
target_crawl_num = 6

try:

    # 제조사별 더 보기 클릭
    # //*[@id="dlMaker_simple"]/dd/div[2]/button[1]
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@id='dlMaker_simple']/dd/div[2]/button[1]")
        )
    ).click()

    # 제조사에서 apple 클릭하기
    # //*[@id="selectMaker_simple_priceCompare_A"]/li[13]
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@id='selectMaker_simple_priceCompare_A']/li[13]")
        )
    ).click()

    time.sleep(2)
    
    # 엑셀 행 수 지정
    ins_cnt = 1

    # 제품 목록 확인하기
    while cur_page <= target_crawl_num:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # print(soup.prettify())

        # 실제 제품 리스트 목록 가져오기
        product_list = soup.select(
            "div.main_prodlist.main_prodlist_list > ul > li"
        )
        # print(product_list[0])

        # 현재 페이지 출력
        print("***** current page ***** {}".format(cur_page))

        for item in product_list:
            if not item.find("div", class_="ad_header"):
                # 상품명
                prod_name = item.select("p.prod_name > a")[0].text.strip()
                # 가격
                prod_price = item.select("p.price_sect > a")[0].text.strip()
                # 제품이미지
                img = item.select("a.thumb_link > img")[0]
                if img.get("data-original"):
                    url = img["data-original"]
                else:
                    url = img["src"]
                
                # 이미지 다운로드 하기
                res = requests.get(url)
                prod_img = BytesIO(res.content)

                # 수집된 정보를 엑셀에 저장
                sheet1.append([prod_name, prod_price])
                # 이미지 저장
                img = openpyxl.drawing.image.Image(prod_img)
                img.width = 30
                img.height = 20
                sheet1.add_image(img, "C"+str(ins_cnt+1))
                
                ins_cnt += 1

        # 엑셀 저장
        workbook.save("./resorces/danawa_product.xlsx")

        # 현재 페이지 번호 변경
        cur_page += 1

        if cur_page > target_crawl_num:
            print("crawling 성공")
            break

        # 다음 페이지 번호 클릭하기
        element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div.number_wrap > a:nth-child({})".format(cur_page),
                )
            )
        )
        element.click()

        # soup 인스턴스 삭제
        del soup
        time.sleep(3)

except Exception as e:
    print(e)


time.sleep(3)
driver.quit()
