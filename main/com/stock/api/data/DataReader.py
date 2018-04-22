# -*- coding: utf-8 -*-
from datetime import datetime

from path import Path
from main.com.stock import Global
from main.com.stock.api import DataPool
from main.com.stock.api.data.KData import KData


def readFileData(file, stockCode):
    fileName = file.name
    split = str.split(fileName, "#")
    stockCode = split[1]
    if split[2].find("1d") >= 0:
        time = 60 * 24
    elif (split[2].find("5m") >= 0):
        time = 5
    read = file.text(encoding="ISO-8859-1")
    allString = str.split(read, "\n")
    list = []
    for i in range(2, len(allString) - 1):
        k = str.split(allString[i], "\t")
        if (len(k) == 7):
            list.append(getKDay(k, stockCode))
    pool = DataPool.DataPool(kData=list)
    return pool


def getKDay(k, code):
    starTime = datetime.strptime(str(k[0]), "%Y/%m/%d")
    endTime = datetime.strptime(str(k[0]) + str("23:59:59"), "%Y/%m/%d%H:%M:%S")
    open = float(k[1])
    high = float(k[2])
    low = float(k[3])
    close = float(k[4])
    volume = float(k[5])
    return KData(code=code, open=open, high=high, low=low, close=close, starTime=starTime,
                 endTime=endTime, volume=volume)


#
def macdTest(dataPoll):
    buyDate = []
    sellDate = []
    upCount = 0
    downCount = 0
    max = 1
    print(dataPoll.startTime[0])
    for i in range(1, dataPoll.len - max):
        if (dataPoll.hist[i - 1] <= 0 and dataPoll.hist[i] >= 0):
            buyDate.append(i)
            if (dataPoll.close[i + max] > dataPoll.close[i]):
                upCount = upCount + 1
            else:
                downCount = downCount + 1
                print(dataPoll.startTime[i])
        if (dataPoll.hist[i - 1] >= 0 and dataPoll.hist[i] <= 0):
            sellDate.append(i)
    print(upCount)
    print(downCount)


def testBolling(dataPoll):
    sum = 0
    count = 0
    value = 0
    sValue = 0
    winCount = 0
    failCount = 0
    for i in range(1, dataPoll.len):
        if dataPoll.lower[i] >= dataPoll.low[i]:
            subValue = (dataPoll.lower[i] - dataPoll.low[i]) * 100 / dataPoll.close[i - 1]
            count = count + 1
            sum = sum + subValue
            if (subValue > 1):
                if (dataPoll.close[i + 1] > dataPoll.low[i]):
                    winCount += 1
                else:
                    failCount += 1
                print(str(dataPoll.startTime[i]) + " " + str(subValue))
    print("%s %s" % (winCount, failCount))
    # print(value)
    # print(sValue)
    # print(sum / count)


d = Path("/Users/xiaot/workspace/futuquant/data")
for file in d.files("*.txt"):
    if file.find("00700#1d") >= 0:
        dataPoll = readFileData(file, Global.TENCENT)
        break
# print(dataPoll.debug())
# strptime = datetime.strptime("2014/12/31", "%Y/%m/%d")
# print(strptime)
# macdTest(dataPoll)
testBolling(dataPoll)
