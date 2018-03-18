import requests
from bs4 import BeautifulSoup
import sqlite3
import time


# html 페이지 크롤링
def crawlHtml(url):
    r = requests.get(url)
    print("url :: {0}\nstatCode :: {1}".format(url, r.status_code))
    return BeautifulSoup(r.text,'html.parser')

# 당첨번호 파싱
def parseWinNums(html):
    winNumTags = html.select('div.lotto_win_number p.number > img')
    winNums = []
    for tag in winNumTags:
        winNums.append(tag['alt'])
    return winNums

# 보너스번호 파싱
def parseBonusNum(html):
    bonusNumTag = html.select('div.lotto_win_number p.number span.number_bonus > img')[0]
    return bonusNumTag['alt']


# DB연결
def dbConnection():
    # connection :: lotto.db
    # table :: CREATE TABLE lotto_win_num ( no INTEGER, win_num INTEGER, bonus_flag VARCHAR(1), PRIMARY KEY (no, win_num));
    return sqlite3.connect('lotto.db')

# 당첨번호 insert
def insertWinNum(conn, no, winNums, bonusNum):
    cur = conn.cursor()
    insertWinNumSql = "INSERT INTO lotto_win_num VALUES "
    insertWinNumSql += "(?, ?, ?)"
    insertWinNumSql += ",(?, ?, ?)"
    insertWinNumSql += ",(?, ?, ?)"
    insertWinNumSql += ",(?, ?, ?)"
    insertWinNumSql += ",(?, ?, ?)"
    insertWinNumSql += ",(?, ?, ?)"
    insertWinNumSql += ",(?, ?, ?)"

    insertDateArray = []
    for winNum in winNums:
        insertDateArray.append(no)
        insertDateArray.append(winNum)
        insertDateArray.append('N')
    insertDateArray.append(no)
    insertDateArray.append(bonusNum)
    insertDateArray.append('Y')

    cur.execute(insertWinNumSql, insertDateArray)
    conn.commit()


# 회차별 로또 당첨번호 수집
def collectLottoWinNum(no):
    baseUrl = 'http://nlotto.co.kr/gameResult.do?method=byWin&drwNo='
    url = baseUrl + str(no)

    # 크롤링 html
    soupHtml = crawlHtml(url)

    # 담청번호 파싱
    winNums = parseWinNums(soupHtml)
    bonusNum = parseBonusNum(soupHtml)

    # DB 연결 및 담첨번호 insert
    conn = dbConnection()
    insertWinNum(conn, no, winNums, bonusNum)
    conn.close()


#796회
startNo = 797
lastNo = 797
for no in range(startNo,lastNo+1):
    print("{0}회차".format(str(no)))
    collectLottoWinNum(no)
    time.sleep(0.5)
