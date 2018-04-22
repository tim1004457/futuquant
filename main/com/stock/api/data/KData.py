import talib


class KData:

    def __init__(self, code, high, low, open, close, volume, starTime, endTime):
        self.stockCode = code
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.volume = volume
        self.startTime = starTime
        self.endTime = endTime
