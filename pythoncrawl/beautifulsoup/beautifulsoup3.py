from bs4 import BeautifulSoup
import requests

# 가상환경이기 때문에 실제 경로는 pythoncrawl
# 때문에 경로 줄 때 ./ 현재경로 밑에 beautifulsoup/ 안에 story.html로 줌
with open("./beautifulsoup/story.html", "r") as f:   
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
# print(soup.prettify())

# 타이틀 태그 출력
print("title >> {}".format(soup.title))
# 타이틀 태그 내용 출력
print("title >> {}".format(soup.title.string))
# h1 태그 출력
print("h1 >> {}".format(soup.body.h1))
# 첫번째 p 태그 출력
print("p >> {}".format(soup.body.p))
p1 = soup.p
print("p >> {}".format(p1))
print("p class value >> {}".format(p1["class"]))

### find
print("\n---- find() 함수 ----")
print("h1 : {}".format(soup.find("h1")))
print("p : {}".format(soup.find("p")))

## 두번째 p태그 가져오기
print("\n-- 두번째 p태그 --")
p2 = p1.next_sibling.next_sibling  # enter도 인식되기 때문에 next_sibling 두번 해줘야 함! (속성property으로 처리)
print(p2)
print()
p2 = p1.find_next_sibling()   # find는 공백 인식X 좀 더 편함!
print(p2.prettify())

print("\n-- 세번째 p태그 --")
p3 = p2.next_sibling.next_sibling
print(p3)
print()
p3 = p2.find_next_sibling()
print(p3.prettify())

print()
for v in p2.next_element:
    print(v, end="")

print()
# p3가 사용할 수 있는 함수/속성 확인
print(dir(p3))
