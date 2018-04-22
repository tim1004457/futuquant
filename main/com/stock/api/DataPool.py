import math
from datetime import time

import numpy
import talib
from talib._ta_lib import MA_Type

from main.com.stock import Global


class DataPool:
    maPool = {}
    bollPool = {}
    stockDataList = []
    volatityData = []
    ATR = {}
    low = []
    high = []
    open = []
    close = []
    volume = []
    startTime = []

    def __init__(self, kData, period=Global.KEY_DAY, atrTimePeriod=14):
        self.period = period
        self.atrTimePeriod = atrTimePeriod
        self.addKData(kData)

    def addKData(self, kData):
        lowList = []
        highList = []
        openList = []
        closeList = []
        volumeList = []
        for item in kData:
            self.stockCode = item.stockCode
            lowList.append(item.low)
            highList.append(item.high)
            openList.append(item.open)
            closeList.append(float(item.close))
            volumeList.append(item.volume)
            self.startTime.append(item.startTime)
        self.len = len(kData)
        self.low = numpy.asarray(lowList)
        self.high = numpy.asarray(highList)
        self.open = numpy.asarray(openList)
        self.close = numpy.asarray(closeList)
        self.volume = numpy.asarray(volumeList)
        self.upper, self.middle, self.lower = talib.BBANDS(self.close, timeperiod=20)
        self.macd, self.signal, self.hist = talib.MACD(self.close, 12, 26, 9)
        self.hist = self.hist * 2
        # self.ATR = talib.ATR(self.high,self.low,self.close,self.atrTimePeriod)

    def isRed(self, i):
        return self.open[i] < self.close[i]

    def findIndexByTime(self, time):
        for i in range(0, len(self.stockDataList)):
            if self.stockDataList[i].time_key == time:
                return i
        return 0

    def initVolatity(self):
        if (len(self.volatityData) > 0):
            return
        self.volatityData.append(0)
        for i in range(1, len(self.stockDataList)):
            dayVolatility = math.fabs(self.stockDataList[i].high - self.stockDataList[i].low)
            highVolatility = math.fabs(self.stockDataList[i - 1].close - self.stockDataList[i].high)
            lowVolatility = math.fabs(self.stockDataList[i - 1].close - self.stockDataList[i].low)
            self.volatityData.append(round(max(dayVolatility, highVolatility, lowVolatility), 3))

    def ma(self, ma=5.0):
        if (ma <= 0):
            return
        if (self.maPool.get(ma, None) is None):
            self.maPool[ma] = talib.SMA(self.close, ma)
        return self.maPool.get(ma)

    def rString(self, f):
        return str(round(f, 3))

    def debug(self):
        print(self.stockCode)
        atr = talib.ATR((self.high), self.low,
                        (self.close), 10)
        ma5 = self.ma(5)
        for i in range(self.len - 5, self.len):
            print(str(self.startTime[i]) + " " + self.rString(self.open[i]) + " " + self.rString(
                self.close[i])
                  + " " + self.rString(self.high[i]) + " " + self.rString(self.low[i])
                  + " " + self.rString(self.volume[i]) + " " + self.rString(
                atr[i]) + " " + self.rString(ma5[i]) + " " + self.rString(
                self.upper[i]) + " " + self.rString(self.middle[i]) + " " + self.rString(
                self.lower[i]))
            print(self.rString(self.macd[i]) + " " + self.rString(
                self.signal[i]) + " " + self.rString(self.hist[i]))
