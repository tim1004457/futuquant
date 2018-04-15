from futuquant.open_context import *
from futuquant.timluo import Global
import math
import StockUtils


class DataPool:
    maPool = {}
    stockDataList = []
    volatityData = []
    ATR = {}

    def debug(self):
        for i in range(0, len(self.stockDataList)):
            print(self.stockDataList[i])

    def __init__(self, code=Global.TENCENT, start="2015-01-01"):
        self.quoteContext = OpenQuoteContext(Global.LOCAL_HOST, Global.LOCAL_PORT)
        _, ret_data = self.quoteContext.get_history_kline(code, start)
        for data in ret_data.itertuples():
            self.stockDataList.append(data)
            print(data)

    def findIndexByTime(self,time):
        for i in range(0,len(self.stockDataList)):
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

    def getATR(self, n):
        self.initVolatity()
        if (self.ATR.get(n, None) is None):
            self.ATR[n] = StockUtils.average(self.volatityData, n)
        return self.ATR[n]

    def ma(self, ma=5.0):
        if (ma <= 0):
            return
        if (self.maPool.get(ma, None) is None):
            list = []
            recentSum = 0.0
            for data in self.stockDataList:
                if (data.Index < ma - 1):
                    list.append(0)
                    recentSum += data.close
                    continue
                else:
                    recentSum += data.close
                    list.append(round(recentSum / ma, 3))
                    recentSum = recentSum - self.stockDataList[data.Index - (ma - 1)].close
            self.maPool[ma] = list
        return self.maPool.get(ma)
