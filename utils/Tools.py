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


# 获取文件保存时的格式化时间结构
def GetSaveTime():
    curDate = datetime.now().strftime("%y.%m.%d")
    curTime = datetime.now().strftime("%H:%M:%S")
    saveTime = f"{curDate} {curTime}"
    return saveTime


# 验证密码合法性
def ValidPassword(Password):
    if len(Password) < 8 or len(Password) > 16:
        return False

    has_upper = any(char.isupper() for char in Password)
    has_lower = any(char.islower() for char in Password)
    has_digit = any(char.isdigit() for char in Password)

    return has_upper and has_lower and has_digit and Password.isalnum()


# 验证用户名合法性
def ValidUsername(Username):
    if len(Username) < 3 or len(Username) > 10:
        return False

    has_upper = any(char.isupper() for char in Username)
    has_lower = any(char.islower() for char in Username)
    has_digit = any(char.isdigit() for char in Username)

    return has_upper and has_lower and has_digit and Username.isalnum()
