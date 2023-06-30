from bs4 import BeautifulSoup
import requests
import datetime

html = requests.get("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%85%BC%EC%82%B0+%EB%82%A0%EC%94%A8")

soup = BeautifulSoup(html.text, "html.parser")

temperature_soup = soup.find_all('div', 'cell_temperature')
rainfall_soup = soup.find_all('div', 'cell_weather')
date_soup = soup.find_all('div', 'cell_date')

date = []
low_temp = []
high_temp = []
rainfall_am = []
rainfall_pm = []

for day in date_soup:
    weather_day = day.find_all('span', 'date')
    weather_day = str(weather_day)
    weather_day = weather_day[20:25]
    date.append(weather_day)

for data in temperature_soup:
    lowest = data.find('span', 'lowest')
    lowest = str(lowest)
    l_start = lowest.find("최저기온</span>")
    l_finish = lowest.find("°</span>")
    low_temp.append(int(lowest[l_start + 11 :l_finish]))
    
    highest = data.find('span', 'highest')
    highest = str(highest)
    h_start = highest.find("최고기온</span>")
    h_finish = highest.find("°</span>")
    high_temp.append(int(highest[l_start + 12 : l_finish + 1]))

for rdata in rainfall_soup:
    rainfalls = rdata.find_all('span', 'rainfall')
    rf_am, rf_pm =  rainfalls[0], rainfalls[1]
    
    rf_am = str(rf_am)
    rf_am_start = rf_am.find('"rainfall">')
    rf_am_end = rf_am.find("%</span>")
    rainfall_am.append(int(rf_am[rf_am_start + 11:rf_am_end]))
    #print("AM:", rainfall_am)

    rf_pm = str(rf_pm)
    rf_pm_start = rf_pm.find('"rainfall">')
    rf_pm_end = rf_pm.find("%</span>")
    rainfall_pm.append(int(rf_pm[rf_pm_start + 11:rf_pm_end]))
    #print("PM:", rainfall_pm)


d = datetime.datetime.now()
write_type = str(d.year) + str(d.month).rjust(2, '0') + str(d.day).rjust(2, '0') + "_forecast"
f = open('{}.txt'.format(write_type), 'w')

today_str = str(d.year) + "년 " +  str(d.month).rjust(2, '0') + "월 " + str(d.day).rjust(2, '0') + "일"
time_str = str(d.hour).rjust(2, '0') + ":" + str(d.minute).rjust(2, '0') + ":" + str(d.second).rjust(2, '0')
f.write("아래 내용은 {} {}에 자동적으로 작성되었습니다.\n".format(today_str, time_str))
f.write(today_str)
f.write(" 기준 논산 일기예보입니다.\n")
for i in range(len(date)):
    f.write('{} 날씨를 알려드립니다.\n'.format(date[i][:-1]))
    f.write('최저기온은 {}도이며, 최고기온은 {}도입니다.\n'.format(low_temp[i], high_temp[i]))
    f.write('오전 강수확률은 {}%, 오후 강수확률은 {}%입니다\n'.format(rainfall_am[i], rainfall_pm[i]))
    
f.close()