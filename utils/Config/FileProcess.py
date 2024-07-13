import os

from utils.Config.HeadFiles import *


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
    def AbsPath1(FilePath):  # 传入相对路径返回绝对路径

        try:
            currentPath = Path(__file__).resolve()
            currentDir = currentPath.parent
            absPath = currentDir.parent / FilePath
            return absPath
        except Exception as e:
            raise e

    @staticmethod
    def AbsPath(FilePath):
        currentPath = Path(__file__).resolve()
        currentDir = currentPath.parent
        projectRoot = currentDir
        projectName = Path.cwd().name
        while projectRoot.name != "SmartEditor":
            projectRoot = projectRoot.parent
        tarAbsPath = projectRoot / FilePath
        return tarAbsPath



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
    a = GetPrompt().Data()["FunctionPrompt"]["Translate"]
    print(a)


if __name__ == '__main__':
    test()
    print(a)
    print(b)
