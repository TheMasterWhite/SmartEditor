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

curTime = Tools.GetTime()
curData = Tools.GetDate()
os.makedirs("Logs", exist_ok = True)
logging.basicConfig(filename = f"Logs/[{curData}][{curTime}].log",
                    filemode = 'w',
                    level = logging.INFO)


def ReadConfigFile():
    # 读取配置文件
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


def InitToken():  # 初始化环境变量

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
