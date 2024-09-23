from datetime import datetime
import os


# 获取格式化时间
def GetTime():
    curTime = datetime.now()
    formatTime = curTime.strftime("%H:%M:%S")
    return str(formatTime)


# 获取格式化日期
def GetDate():
    curDate = datetime.now()
    formatDate = curDate.strftime("%y.%m.%d")
    return str(formatDate)


# 获取文件扩展名
def GetExtension(FileName):
    fileName, extension = os.path.splitext(FileName)
    return extension[1:] if extension.startswith('.') else extension


# 获取文件名
def GetFileName(FileName):
    fileName, extension = os.path.splitext(FileName)
    return fileName
