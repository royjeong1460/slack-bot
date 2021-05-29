from bs4 import BeautifulSoup
import requests
import schedule
import time


a = ' '
b = ' '
token = 'xoxb-2072308502805-2113961576835-7ALWjlEe2MHn07fMh9eO9UP0'

# 조코딩님 해결책 사용
# slack 봇에 메세지 전달 함수
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)


# coinGecko 신규코인 크롤링 함수
def coingecko_recent():
    global a
    global b
    url = 'https://www.coingecko.com/ko/%EC%BD%94%EC%9D%B8/recently_added'
    coinurl = 'https://www.coingecko.com/ko/%EC%BD%94%EC%9D%B8/'
    response = requests.get(url)
    
    # bs 크롤링
    if response.status_code == 200:
        dom = BeautifulSoup(response.text,'html.parser')
        # 코인 풀네임
        fullname = dom.select_one('div.center a.tw-hidden').text.strip()
        fullnameUrl = dom.select_one('div.center a.tw-hidden').text.strip().lower().replace(' ','-')
        # 코인 이름
        a = dom.select_one('div.center a.d-lg-none').text.strip()
        # 코인 크롤링 시 가격
        price = dom.select_one('td.td-price span').text.strip()
        # 신규 코인 주소
        text = f'코인게코-신규코인\n\
                    전체이름 : {fullname}  이름 : {a}  가격 : {price}\n\
                    상세정보 : {coinurl}{fullnameUrl}' 
        if  a !=  b:
            post_message(token,"#coingecko_recent",text)
            b = a


schedule.every(1).minutes.do(coingecko_recent)

while True: 
    schedule.run_pending() 
    time.sleep(1)