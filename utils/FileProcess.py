from utils.HeadFiles import *
from utils.PMTProcess import *


class FileProcess:  # 文件处理类

    @staticmethod
    def ReadTxt(FilePath):  # 打开txt文件并返回内容，传参为文件地址
        try:
            file = open(FilePath, 'r', encoding='utf-8')
            Content = file.read()
            file.close()
            return Content
        except:
            raise

    @staticmethod
    def Base64(FilePath):  # 对文件进行Base64编码，返回编码内容文件，传入文件路径
        try:
            fileBytes = pathlib.Path(FilePath).read_bytes()
            fileBase64 = base64.b64encode(fileBytes).decode('ascii')
            return fileBase64
        except:
            raise

    @staticmethod
    def AbsPath(FilePath):  # 传入相对路径返回绝对路径
        try:
            currentPath = Path(__file__).resolve()
            currentDir = currentPath.parent
            absPath = currentDir.parent / FilePath
            return absPath
        except:
            raise

    @staticmethod
    def SaveWithTime(FileName, TarPath, FileExtension):  # 将文件名赋予时间并返回绝对路径
        # 传入文件名，保存路径，文件扩展名
        try:
            folderPath = FileProcess.AbsPath(TarPath)
            Time = datetime.datetime.now()
            FileName += "_"
            saveFileName = FileName + Time.strftime("%Y_%m_%d_%H_%M_%S") + "." + FileExtension
            savePath = os.path.join(folderPath, saveFileName)
            return savePath
        except:
            raise


class OSSProcess:  # OSS云服务处理类

    @staticmethod
    def UploadFile(FilePath, FileExtension, BucketName="smart-editor"):  # 上传文件到阿里云，传入相对路径和文件扩展名,返回OSS文件路径
        try:
            # 获取鉴权
            Auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
            # 设置Bucket信息
            EndPoint = "https://oss-cn-guangzhou.aliyuncs.com"
            Bucket = oss2.Bucket(auth=Auth, endpoint=EndPoint,
                                 bucket_name=BucketName)

            FileName = os.path.basename(FilePath)
            AbsPath = FileProcess.AbsPath(FilePath)
            with open(AbsPath, 'rb') as fileobj:
                # Tell方法用于返回当前位置。
                current = fileobj.tell()
                Bucket.put_object(key=FileName, data=fileobj)
            OSSPath = EndPoint[:8] + BucketName + "." + EndPoint[8:] + "/" + FileName
            return OSSPath
        except:
            raise


def test():
    a = GetPrompt().Data()["FunctionPrompt"]["Translate"]
    print(a)


if __name__ == '__main__':
    test()
    print(a)
    print(b)
