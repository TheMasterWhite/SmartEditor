import logging
import os
import base64
import pathlib
import json
from pathlib import Path
from pydub import AudioSegment
from utils import Tools

fileSavePath = GLOBAL_FileSavePath


class FileProcess:  # 文件处理类

    @staticmethod
    def ReadTxt(FilePath):  # 打开txt文件并返回内容，传参为文件地址

        try:
            file = open(FilePath, 'r', encoding = 'utf-8')
            Content = file.read()
            file.close()
            return Content
        except Exception as e:
            raise e


    @staticmethod
    def Base64(FilePath):  # 对文件进行Base64编码，返回编码内容文件，传入文件路径

        try:
            fileBytes = pathlib.Path(FilePath).read_bytes()
            fileBase64 = base64.b64encode(fileBytes).decode('ascii')
            return fileBase64
        except Exception as e:
            raise e


    @staticmethod
    def AbsPath(PackageName, RelativePath):  # 获取绝对路径
        # PackageName: 包名
        # RelativePath: 相对于包目录的文件或目录路径

        packagePath = os.path.dirname(os.path.abspath(__import__(PackageName).__file__))
        return os.path.join(packagePath, RelativePath)


    @staticmethod
    def GetFileTimePath(FileName, TarPath, FileExtension):  # 将文件名赋予时间并返回绝对路径
        # 传入文件名，保存路径，文件扩展名

        try:
            folderPath = FileProcess.AbsPath(TarPath)
            Time = datetime.datetime.now()
            FileName += "_"
            saveFileName = FileName + Time.strftime("%Y_%m_%d_%H_%M_%S") + "." + FileExtension
            savePath = os.path.join(folderPath, saveFileName)
            return savePath

        except Exception as e:
            raise e


    # 将多媒体文件转换成wav格式
    @staticmethod
    def ConvertToWav(FileName):
        try:
            filePath = os.path.join(fileSavePath, FileName)
            fileExtension = Tools.GetExtension(FileName)
            fileName = Tools.GetFileName(FileName)
            # 文件不存在
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"File {fileName} does not exist.")
            # 音频处理
            audio = AudioSegment.from_file(filePath, format = fileExtension)
            savePath = fileSavePath + ".wav"
            audio.export(savePath, format = "wav")
            curTime = Tools.GetTime()
            logging.info(f"[{curTime}]File {FileName} converted successfully.")

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[ConvertToWav]" + str(e))


class OSSProcess:  # OSS云服务处理类

    @staticmethod
    def UploadFile(FilePath, FileExtension, BucketName = "smart-editor"):  # 上传文件到阿里云，传入相对路径和文件扩展名,返回OSS文件路径

        try:
            # 获取鉴权
            endPoint = OSS_ENDPOINT
            auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
            # 设置Bucket信息
            bucket = oss2.Bucket(auth = auth, endpoint = endPoint,
                                 bucket_name = BucketName)

            fileName = os.path.basename(FilePath)
            absPath = FileProcess.AbsPath(FilePath)
            with open(absPath, 'rb') as fileobj:
                # Tell方法用于返回当前位置。
                current = fileobj.tell()
                bucket.put_object(key = fileName, data = fileobj)

            # 字符串处理获取OSS文件外链
            ossPath = endPoint[:8] + BucketName + "." + endPoint[8:] + "/" + fileName
            return ossPath

        except Exception as e:
            raise e


class JsonOperator:

    @staticmethod
    def Save(JsonObject, Path, FileName):  # 保存Json文件至指定目录，传入Json对象、保存路径与文件名

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


    @staticmethod
    def Load(FilePath, FileName):  # 加载Json文件

        try:
            absPath = FileProcess.AbsPath(FilePath)
            jsonObject = json.loads(absPath)
            return jsonObject

        except Exception as e:
            raise e


def test():
    a = GetPrompt().Data()["ScenePrompt_General"]["Translate"]
    print(a)


if __name__ == '__main__':
    test()
