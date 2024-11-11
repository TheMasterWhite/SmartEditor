import os
import erniebot
import asyncio
import base64
import pathlib
import json
import requests, logging
import copy
from pathlib import Path
from utils import Tools
import jwt

curTime = Tools.GetTime()
curData = Tools.GetDate()
os.makedirs("Logs", exist_ok = True)
logging.basicConfig(filename = f"Logs/[{curData}][{curTime}].log",
                    filemode = 'w',
                    level = logging.INFO)


# 验证JWT并返回结果
def ValidToken(Token):
    try:
        payload = jwt.decode(Token, GLOBAL_RSA_PUBLIC_KEY, algorithms = ["RS256"])
        username = payload["username"]
        retObj = {
            "status": True,
            "msg": "OK",
            "username": username,
        }
        return retObj

    except jwt.ExpiredSignatureError:
        retObj = {
            "status": False,
            "msg": "登录过期，请重新登录！",
        }
        return retObj

    except jwt.InvalidTokenError:
        retObj = {
            "status": False,
            "msg": "验证失败，请重试！",
        }
        return retObj

    except Exception as e:
        retObj = {
            "status": False,
            "msg": str(e),
        }
        return retObj


# 读取配置文件
def ReadConfigFile():
    filePath = "/Server/SmartEditor/config.json"  # linux
    # filePath = "E:/Code/CodeLibrary/Python/SmartEditor/config.json"  # windows

    with open(filePath, "r", encoding = "utf-8") as f:
        configData = json.load(f)

    for key, value in configData.items():
        globals()[key] = value
        if key == "GLOBAL_RSA_PUBLIC_KEY":
            with open("/Server/RSA公钥.pem", "r", encoding = "utf-8") as f:
                globals()[key] = f.read()
        if key == "GLOBAL_RSA_PRIVATE_KEY":
            with open("/Server/RSA私钥.pem", "r", encoding = "utf-8") as f:
                globals()[key] = f.read()


# 初始化环境变量
def InitToken():
    os.environ["OSS_ACCESS_KEY_ID"] = OSS_ACCESS_KEY_ID
    os.environ["OSS_ACCESS_KEY_SECRET"] = OSS_ACCESS_KEY_SECRET
    os.environ["EB_AGENT_ACCESS_TOKEN"] = GLOBAL_ERNIETOKEN
    os.environ["GLOBAL_RSA_PRIVATE_KEY"] = GLOBAL_RSA_PRIVATE_KEY
    os.environ["GLOBAL_RSA_PUBLIC_KEY"] = GLOBAL_RSA_PUBLIC_KEY
    erniebot.api_type = "aistudio"
    erniebot.access_token = GLOBAL_ERNIETOKEN


def InitServer():
    ReadConfigFile()
    InitToken()


InitServer()
