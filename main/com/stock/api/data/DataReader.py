# -*- coding: utf-8 -*-

from path import Path


def readFileData(file):
    fileName = file.name
    split = str.split(fileName, "#")
    stockCode = split[1]
    if split[2].find("1d") >= 0:
        time = 60 * 24
    elif (split[2].find("5m") >= 0):
        time = 5
    read = file.text(encoding="ISO-8859-1")
    print(read)


d = Path("/Users/xiaot/workspace/futuquant/data")
for file in d.files("*.txt"):
    if file.find("00700#1d") >= 0:
        readFileData(file)
        break
