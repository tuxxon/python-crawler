#!/usr/bin/python3


# 내장함수
from urllib.request import urlopen
# 명령행 파싱 모듈 argparse 모듈 사용
import argparse
# request => 요청하는거를 웹에 요청한 결과값을 얻어올수 있는 모듈
import requests as req
#!/usr/bin/python3

# 웹에 요청한 결과를 보내주는 모듈
from bs4 import BeautifulSoup

import os

parser = argparse.ArgumentParser()
#argparse 모듈 에 ArgumentParse() 함수 사용하여 parser 생성

#parser.add_argument("-name", "--people", required=True)
#  명령행 옵션을 지정하기 위해 사용합니다 명령행 옵션 인자는 -name으로 지정

args = parser.parse_args()
#parse에 add_argument()함수 사용해 args 인스턴스생성

#people = args.people
# 명령행에서 받은 인자값을 people에 값을 넘겨줌

male = {
    "cat" : ["황민현", "시우민", "강동원", "이종석", "이준기"],
    "dog" : ["강다니엘", "백현", "박보검", "송중기"],
    "rabbit": ["정국", "바비", "박지훈", "수호"],
    "dinosaur" : ["윤두준", "이민기", "김우빈", "육성재", "공유"],
    "bear" : ["마동석", "조진웅", "조세호", "안재홍"]
}

female = {
    "dog" : ["박보영", "아이유", "윤승아", "민아", "한지민"],
    "cat" : ["안소희", "오연서", "한예슬", "이성경", "이효리"],
    "rabbit": ["수지", "나연", "예린", "한승연", "문채원"],
    "deer": ["윤아", "이연희", "고아라", "문근영", "정유미"],
    "fox": ["경리", "예지", "한혜진", "헤이즈", "지연"],
}

def google_image_extractor(sex=None, classKey=None,people=None):

    if classKey is None or people is None:
        return

    # 사용한 구글 url https://www.google.co.kr/search?q=%EB%B2%A4&tbm=isch
    url_info = "https://www.google.co.kr/search?"
    #params에 딕션을 넣어줌

    params = {
        #명령행에서 받은 인자값을 people로 넣어줌
        "q" : people,
        "tbm":"isch"
    }
    #url 요청 파싱값
    html_object = req.get(url_info,params) #html_object html source 값

    if html_object.status_code == 200:
        #페이지 status_code 가 200 일때 2XX 는 성공을 이야기함
        bs_object = BeautifulSoup(html_object.text,"html.parser")
        #인스턴스 생성
        img_data = bs_object.find_all("img")
        #인스턴스의 find_all 이라는 함수에 img 태그가 있으면 img_data에 넣어줌

        for i in enumerate(img_data[1:]):
            #딕셔너리를 순서대로 넣어줌
            dirPath = "{sex}/{classKey}/{people}".format(
                sex=sex,
                classKey=classKey,
                people=people
            )

            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            t = urlopen(i[1].attrs['src']).read()
            filename = "{dirPath}/{seq}".format(
                dirPath=dirPath, 
                seq=str(i[0]+1)+'.jpg'
            )

            with open(filename,"wb") as f:
                f.write(t)
            print("Img Save Success")

def main():

    ''' Fetch images for male from Google'''
    for classKey in male.keys():
        for people in male[classKey]:
            print("===> Fetching {} / {}".format(classKey, people))
            google_image_extractor("male",classKey, people);

    ''' Fetch images for female from Google'''
    for classKey in female.keys():
        for people in female[classKey]:
            print("===> Fetching {} / {}".format(classKey, people))
            google_image_extractor("female",classKey, people);

if __name__=="__main__":
    main()