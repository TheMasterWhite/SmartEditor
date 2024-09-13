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
logging.basicConfig(filename = f"Server/[{curTime}]Log.log",
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


def InitToken():  # 初始化环境变量

    os.environ['OSS_ACCESS_KEY_ID'] = OSS_ACCESS_KEY_ID
    os.environ['OSS_ACCESS_KEY_SECRET'] = OSS_ACCESS_KEY_SECRET
    os.environ["EB_AGENT_ACCESS_TOKEN"] = GLOBAL_ERNIETOKEN
    erniebot.api_type = "aistudio"
    erniebot.access_token = GLOBAL_ERNIETOKEN


def InitServer():
    ReadConfigFile()
    InitToken()


InitServer()
