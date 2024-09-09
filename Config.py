import os
from configparser import ConfigParser
import erniebot
import asyncio
import base64
import pathlib
import json
from pathlib import Path


def ReadConfigFile():
    # 读取配置文件
    Config = ConfigParser()
    Config.optionxform = str
    cfgPath = "Config.cfg"
    Config.read(cfgPath)
    # 遍历配置文件中的所有选项，创建全局变量
    global_vars = dict(Config["TOKENS"])
    for key, value in global_vars.items():
        globals()[key] = value


def InitToken():  # 初始化环境变量

    os.environ['OSS_ACCESS_KEY_ID'] = OSS_ACCESS_KEY_ID
    os.environ['OSS_ACCESS_KEY_SECRET'] = OSS_ACCESS_KEY_SECRET
    os.environ["EB_AGENT_ACCESS_TOKEN"] = GLOBAL_ERNIETOKEN
    erniebot.api_type = "aistudio"
    erniebot.access_token = GLOBAL_ERNIETOKEN


ReadConfigFile()
InitToken()

print(GLOBAL_ERNIETOKEN)
