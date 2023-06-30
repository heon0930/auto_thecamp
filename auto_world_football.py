import requests 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import re
import openai
#OPENAI_API_KEY = OPEN_API_KEY
wanted_text = ""

d = datetime.datetime.now() # 오늘 날짜 확인

popular_url_list = [] # 해외축구::최신뉴스::인기순 눌렀을 때 1페이지부터 10페이지까지의 url들
real_url_list = [] #진짜 기사로 가는 url들

#naver에서 date=20230628 같이 나와서 이에 맞춰서 formatting
today = str(d.year) + str(d.month).rjust(2, '0') + str(d.day-1).rjust(2, '0')

# 해외축구::최신뉴스::인기순 눌렀을 때 1페이지부터 10페이지까지의 url 넣기
for i in range(1, 2):
    popular_url_list.append("https://sports.news.naver.com/wfootball/news/index?date={}&isphoto=N&type=popular&page={}".format(today, i))

for popular_url in popular_url_list:
    response = urlopen(popular_url) #url open
    soup = BeautifulSoup(response, "html.parser")
    
    #아래는 html쪽은 잘 몰라서 수정 필요할지도
    #일단 a 들어가면 하이퍼링크 연결한다는 것만 알아서
    #a 들어가는 것들 전부 찾아서 넣기
    full_url_list = soup.find_all('a') 
    
    for url in full_url_list:
        url = url.get('href') #href 뒤에 있는 것들이 기사로 가는 url 인데 다른 것들도 있음
        
        #string type 아닌 것들도 있어서 예외 처리 해주기
        try:
            if url[:5] == "/news": #원하는 기사들 url은 "/news" 로 시작함
                real_url = "https://sports.news.naver.com" + url #원래 url로 만들어주기
                real_url_list.append(real_url)
        except:
            continue


test_url_list_1 = real_url_list[:5]
for url in test_url_list_1:
    response = urlopen(url)
    original_html = requests.get(url)
    html = BeautifulSoup(original_html.text, "html.parser")
    content = html.select("#newsEndContents")
    content = ''.join(str(content))


    pattern1 = '<[^>]*>'
    content = re.sub(pattern=pattern1, repl='', string=content)

    email_index = content.find('@')
    if(email_index != -1):
        content = content[:email_index]
        
    
    openai.api_key = OPENAI_API_KEY
    model = "gpt-3.5-turbo"
    query = content + "를 3줄 이내로 요약해줘"
    messages = [{"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    answer = response['choices'][0]['message']['content']
    wanted_text += answer

test_url_list_2 = real_url_list[5:5]
for url in test_url_list_2:
    response = urlopen(url)
    original_html = requests.get(url)
    html = BeautifulSoup(original_html.text, "html.parser")
    content = html.select("#newsEndContents")
    content = ''.join(str(content))


    pattern1 = '<[^>]*>'
    content = re.sub(pattern=pattern1, repl='', string=content)

    email_index = content.find('@')
    if(email_index != -1):
        content = content[:email_index]
        
    
    openai.api_key = OPENAI_API_KEY
    model = "gpt-3.5-turbo"
    query = content + "를 3줄 이내로 요약해줘"
    messages = [{"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    answer = response['choices'][0]['message']['content']
    wanted_text += answer
    wanted_text += '\n'

openai.api_key = OPENAI_API_KEY
model = "gpt-3.5-turbo"
query = wanted_text + "를 정확히 1350자 이내로 요약해줘"
messages = [{"role": "user", "content": query}]

write_type = today + "_" + str(d.hour).rjust(2, '0') +  str(d.minute).rjust(2, '0') +  str(d.second).rjust(2, '0')
f = open('{}.txt'.format(write_type), 'a')

today_str = str(d.year) + "년 " +  str(d.month).rjust(2, '0') + "월 " + str(d.day).rjust(2, '0') + "일"
time_str = str(d.hour).rjust(2, '0') + ":" + str(d.minute).rjust(2, '0') + ":" + str(d.second).rjust(2, '0')
f.write("아래 내용은 {} {}에 자동적으로 작성되었습니다.".format(today_str, time_str))
f.write("\n")
f.write("{} 네이버 해외축구 인기순 1~10위를 요약한 내용입니다.".format(today_str))
f.write("\n")
f.write(wanted_text)
f.close()
