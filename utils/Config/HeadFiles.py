import os
from configparser import ConfigParser
import erniebot
import asyncio
import base64
import pathlib
import json
from pathlib import Path


class HeadFiles:

    @staticmethod
    def AbsPath(FilePath):  # 传入相对路径返回绝对路径
        currentPath = Path(__file__).resolve()
        currentDir = currentPath.parent
        absPath = currentDir.parent / FilePath
        return absPath


    @staticmethod
    def ReadConfigFile():
        # 读取配置文件
        Config = ConfigParser()
        Config.optionxform = str
        cfgPath = "utils/Config/Config.cfg"
        Config.read(cfgPath)
        # 遍历配置文件中的所有选项，创建全局变量
        global_vars = dict(Config["TOKENS"])
        for key, value in global_vars.items():
            globals()[key] = value


    @staticmethod
    def InitToken():  # 初始化环境变量

        os.environ['OSS_ACCESS_KEY_ID'] = OSS_ACCESS_KEY_ID
        os.environ['OSS_ACCESS_KEY_SECRET'] = OSS_ACCESS_KEY_SECRET
        os.environ["EB_AGENT_ACCESS_TOKEN"] = GLOBAL_ERNIETOKEN
        erniebot.api_type = "aistudio"
        erniebot.access_token = GLOBAL_ERNIETOKEN


    @staticmethod
    def InitProcess():
        HeadFiles.ReadConfigFile()
        HeadFiles.InitToken()


HeadFiles.InitProcess()
