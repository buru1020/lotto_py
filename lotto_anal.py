# 회차별 많이 나온 숫자와 적게 나온 숫자가 다음회차에 또 출연할 확율 계산
# - 회차별 많이 나온 숫자 1~3순위 추출
# - 적게나온 숫자 1~3순위 추출
# - 다음회사 당첨번호와 대조

import sqlite3
import pydash

# DBConnection
def getDbConnection():
    return sqlite3.connect('lotto.db')


# 회차별 만이 나온 순으로 정렬된 리스트 가져오기
def selectWinNumCountList(no):
    conn = getDbConnection()
    cur = conn.cursor()
    sql = "SELECT win_num, count "
    sql += "FROM ( "
    sql += "        SELECT win_num, count(win_num) as count "
    sql += "        FROM lotto_win_num WHERE no <= :no "
    sql += "        GROUP BY win_num ) "
    sql += "ORDER BY count DESC "
    cur.execute(sql, {'no': no})
    rows = cur.fetchall();
    cur.close()
    conn.close()
    return rows

# 해당 회차 당첨번호 조회
def selectWinNum(no):
    conn = getDbConnection()
    cur = conn.cursor()
    sql = "SELECT win_num, bonus_flag FROM lotto_win_num WHERE no = :no"
    cur.execute(sql, {'no': no})
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# N번째 까지 최대,최소값 리스트 추출
def getNthListFromWinNumCountList(list, n):
    result = []
    for i in range(0,len(list)):
        if (len(result) < n or i > 0 and result[len(result)-1][1] == list[i][1]):
            result.append(list[i])
    return result

# 당첨번호와 비교
def compareWinNums(no, diffTarget):
    winNums = selectWinNum(no)
    matchList = []
    for winNum in winNums:
        for diffNum in diffTarget:
            if (winNum[0] == diffNum[0]):
                matchList.append(diffNum + winNum[1:])
    # print("일치하는 번호 :: {0}".format(matchList))
    return matchList


# 최다 1~3개씩만 다음회차에 나오는지 비교
def analisysMaxDiff(no, maxMinRange):
    winNumCountList = selectWinNumCountList(no-1);
    maxList = getNthListFromWinNumCountList(winNumCountList, maxMinRange)
    return compareWinNums(no, maxList)

# 최소 1~3개씩만 다음회차에 나오는지 비교
def analisysMinDiff(no, maxMinRange):
    winNumCountList = selectWinNumCountList(no-1);
    winNumCountList.reverse()
    minList = getNthListFromWinNumCountList(winNumCountList, maxMinRange)
    return compareWinNums(no, minList)

# 최다,최소 1~3개씩만 다음회차에 나오는지 비교
def analisysMaxMinDiff(no, maxMinRange):
    winNumCountList = selectWinNumCountList(no-1);
    maxList = getNthListFromWinNumCountList(winNumCountList, maxMinRange)
    winNumCountList.reverse()
    minList = getNthListFromWinNumCountList(winNumCountList, maxMinRange)
    return compareWinNums(no, pydash.arrays.concat(maxList, minList))


# 100~797회까지 다음회차 매치 여부 수집
def collectMaxMatchedResult(endNo, maxRange):
    # Max, Min 1개 결과 확인
    matchedNoInfoList = []
    matchedList = []
    matchedFlag = False
    matchedNoCount = 0
    for i in range(100,endNo+1):
        matchedList = analisysMaxDiff(i, maxRange)
        matchedFlag = len(matchedList) > (maxRange - 1) * 2
        matchedNoInfoList.append((i, matchedFlag, matchedList))
        if (matchedFlag):
            matchedNoCount += 1
    # print("매치된 회차 정보 :: {0}".format(matchedNoInfoList))
    print("----- Max {0}개 매치 결과".format(maxRange))
    print("매치된 횟수/전체 :: {0}/{1}".format(matchedNoCount, endNo+1-100))
    print("매치된 확률 :: {0}".format( (matchedNoCount / (endNo+1-100)) * 100 ))

# 100~797회까지 다음회차 매치 여부 수집
def collectMinMatchedResult(endNo, minRange):
    # Max, Min 1개 결과 확인
    matchedNoInfoList = []
    matchedList = []
    matchedFlag = False
    matchedNoCount = 0
    for i in range(100,endNo+1):
        matchedList = analisysMinDiff(i, minRange)
        matchedFlag = len(matchedList) > (minRange - 1) * 2
        matchedNoInfoList.append((i, matchedFlag, matchedList))
        if (matchedFlag):
            matchedNoCount += 1
    # print("매치된 회차 정보 :: {0}".format(matchedNoInfoList))
    print("----- Min {0}개 매치 결과".format(minRange))
    print("매치된 횟수/전체 :: {0}/{1}".format(matchedNoCount, endNo+1-100))
    print("매치된 확률 :: {0}".format( (matchedNoCount / (endNo+1-100)) * 100 ))

# 100~797회까지 다음회차 매치 여부 수집
def collectMaxMinMatchedResult(endNo, maxMinRange):
    # Max, Min 1개 결과 확인
    matchedNoInfoList = []
    matchedList = []
    matchedFlag = False
    matchedNoCount = 0
    for i in range(100,endNo+1):
        matchedList = analisysMaxMinDiff(i, maxMinRange)
        matchedFlag = len(matchedList) >= maxMinRange * 2
        matchedNoInfoList.append((i, matchedFlag, matchedList))
        if (matchedFlag):
            matchedNoCount += 1
    # print("매치된 회차 정보 :: {0}".format(matchedNoInfoList))
    print("----- MaxMin {0}개 매치 결과".format(maxMinRange))
    print("매치된 횟수/전체 :: {0}/{1}".format(matchedNoCount, endNo+1-100))
    print("매치된 확률 :: {0}".format( (matchedNoCount / (endNo+1-100)) * 100 ))

# selectWinNumCountList(10)
# selectWinNum(10)
# analisysMaxMinDiff(100, 1)
collectMaxMatchedResult(797, 1)
collectMaxMatchedResult(797, 2)
collectMaxMatchedResult(797, 3)
collectMinMatchedResult(797, 1)
collectMinMatchedResult(797, 2)
collectMinMatchedResult(797, 3)
collectMaxMinMatchedResult(797, 1)
collectMaxMinMatchedResult(797, 2)
collectMaxMinMatchedResult(797, 3)
