import logging
import os
import base64
import pathlib
import json
from pathlib import Path
from pydub import AudioSegment
from utils import Tools
from Config import *
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
import sqlite3

fileSavePath = copy.deepcopy(GLOBAL_FileSavePath)


# 文件处理类
class FileProcess:

    # 打开txt文件并返回内容，传参为文件地址
    @staticmethod
    def ReadTxt(FilePath):

        try:
            with open(FilePath, 'r', encoding = 'utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            raise e


    # 将字符串文本保存到txt中
    @staticmethod
    def SaveTxt(UUID, Content, UserName):
        try:
            fullFileName = UUID + ".txt"
            filePath = os.path.join(fileSavePath, UserName, fullFileName)
            with open(filePath, 'w', encoding = 'utf-8') as f:
                f.write(Content)
        except Exception as e:
            raise e


    # 对文件进行Base64编码，返回编码内容文件，传入文件路径
    @staticmethod
    def Base64(FilePath):
        try:
            fileBytes = pathlib.Path(FilePath).read_bytes()
            fileBase64 = base64.b64encode(fileBytes).decode('ascii')
            return fileBase64
        except Exception as e:
            raise e


    # 将文件名赋予时间并返回绝对路径
    @staticmethod
    def GetFileTimePath(FileName, TarPath, FileExtension):
        # 传入文件名，保存路径，文件扩展名
        try:
            Time = datetime.datetime.now()
            FileName += "_"
            saveFileName = FileName + Time.strftime("%Y_%m_%d_%H_%M_%S") + "." + FileExtension
            savePath = os.path.join(fileSavePath, saveFileName)
            return savePath

        except Exception as e:
            raise e


    # 将多媒体文件转换成wav格式
    @staticmethod
    def ConvertToWav(FileName, UUID, FileExtension, UserName):
        try:
            filePath = os.path.join(fileSavePath, UserName, UUID + f".{FileExtension}")
            # 文件不存在
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"File {FileName} does not exist.")
            # 音频处理
            audio = AudioSegment.from_file(filePath, format = FileExtension)
            savePath = os.path.join(fileSavePath, UserName, UUID + ".wav")
            audio.export(savePath, format = "wav")
            curTime = Tools.GetTime()
            logging.info(f"[{curTime}]File {FileName} converted successfully.")

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[ConvertToWav]" + str(e))


    # 保存文件信息到数据库
    @staticmethod
    def SaveFileInfo(FileName, SaveTime, Description, UserName, UUID):
        try:
            # 连接到SQLite数据库
            with sqlite3.connect("UserInfo.db") as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT userFiles FROM users WHERE userName = ?", (UserName,))
                userFileList = json.loads(cursor.fetchone()[0])["fileList"]
                data = {
                    "fileName": FileName,
                    "saveTime": SaveTime,
                    "description": Description,
                    "uuid": UUID
                }
                userFileList.append(data)
                userFiles = json.dumps({"fileList": userFileList})
                cursor.execute("UPDATE users SET userFiles = ? WHERE userName = ?", (userFiles, UserName))
                conn.commit()

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[SaveFileInfo]" + str(e))
            raise e


    # 根据用户名查询文件上传时间和描述
    @staticmethod
    def GetFileList(UserName):
        try:
            # 连接到SQLite数据库
            with sqlite3.connect("UserInfo.db") as conn:
                cursor = conn.cursor()
                # 查询文件描述和时间
                cursor.execute("SELECT userFiles FROM users WHERE userName = ?", (UserName,))
                userFileList = json.loads(cursor.fetchone()[0])["fileList"]
            return userFileList

        except Exception as e:
            raise e


    # 根据UUID获得全文件名
    @staticmethod
    def GetFileInfo(UUID, UserName):
        try:
            # 连接到SQLite数据库
            with sqlite3.connect("UserInfo.db") as conn:
                cursor = conn.cursor()
                # 查询文件描述和时间
                cursor.execute("SELECT userFiles FROM users WHERE userName = ?", (UserName,))
                userFileList = json.loads(cursor.fetchone()[0])["fileList"]

            for data in userFileList:
                if data["uuid"] == UUID:
                    return data["fileName"]
            return None

        except Exception as e:
            raise e


    # 删除数据库中的文件信息
    @staticmethod
    def DeleteFileInfo(UserName, FileUUID):
        try:
            conn = sqlite3.connect("UserInfo.db")
            cursor = conn.cursor()
            cursor.execute("SELECT ", (UserName,))
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            raise e


class OSSProcess:  # OSS云服务处理类

    @staticmethod
    def UploadFile(FileName, FileExtension, UserName, BucketName = "smart-editor"):
        # 上传文件到阿里云，传入文件名和文件扩展名,返回OSS文件路径

        try:
            # 获取鉴权
            endPoint = OSS_ENDPOINT
            auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
            # 设置Bucket信息
            bucket = oss2.Bucket(auth = auth, endpoint = endPoint,
                                 bucket_name = BucketName)
            fullFileName = FileName + '.' + FileExtension
            filePath = os.path.join(fileSavePath, UserName, fullFileName)
            with open(filePath, 'rb') as fileobj:
                # Tell方法用于返回当前位置。
                current = fileobj.tell()
                bucket.put_object(key = fullFileName, data = fileobj)

            # 字符串处理获取OSS文件外链
            ossPath = endPoint[:8] + BucketName + "." + endPoint[8:] + "/" + fullFileName
            return ossPath

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[OSS_UploadFile]" + str(e))


class JsonOperator:

    # 保存Json文件至指定目录，传入Json对象、保存路径与文件名
    @staticmethod
    def Save(JsonObject, Path, FileName):

        try:
            saveData = json.dumps(JsonObject, ensure_ascii = False, indent = 4)
            savePath = FileProcess.GetFileTimePath(FileName = FileName,
                                                   TarPath = Path,
                                                   FileExtension = "json")
            with open(savePath, "w", encoding = 'utf-8') as f:
                f.write(saveData)
            pass

        except Exception as e:
            raise e


def test():
    a = GetPrompt().Data()["ScenePrompt_General"]["Translate"]
    print(a)


if __name__ == '__main__':
    test()
    userFiles = {
        "fileList": [
            {
                "fileName": "a",
                "saveTime": "a",
                "description": "a",
                "uuid": "1234"
            }
        ]
    }
