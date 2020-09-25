from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

search_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&"

param = {"query" : "영화"}

param = urlencode(param)

search_url += param

try:
    contents = urlopen(search_url).read().decode("utf-8")
    print(contents[150000:200000])
except HTTPError as e:
    print("에러 발생", e.code)
