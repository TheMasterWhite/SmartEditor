from utils.HeadFiles import *


class FileProcess:  # 文件处理类

    @classmethod
    def ReadTxt(cls, filePath):  # 打开txt文件并返回内容，传参为文件地址
        try:
            File = open(filePath, 'r', encoding='utf-8')
            Content = File.read()
            File.close()
            return Content
        except:
            raise

    @classmethod
    def Base64(cls, inputFilePath):  # 对文件进行Base64编码，返回编码内容文件，传入文件路径
        try:
            FileBytes = pathlib.Path(inputFilePath).read_bytes()
            FileBase64 = base64.b64encode(FileBytes).decode('ascii')
            return FileBase64
        except:
            raise

    @classmethod
    def AbsPath(cls, filePath):  # 传入相对路径返回绝对路径
        try:
            CurrentPath = Path(__file__).resolve()
            CurrentDir = CurrentPath.parent
            AbsPath = CurrentDir.parent / filePath
            return AbsPath
        except:
            raise

    @classmethod
    def SaveWithTime(cls, fileName, tarPath, fileExtension):  # 将文件名赋予时间并返回绝对路径
        # 传入文件名，保存路径，文件扩展名
        try:
            folderPath = FileProcess.AbsPath(tarPath)
            Time = datetime.datetime.now()
            fileName += "_"
            saveFileName = fileName + Time.strftime("%Y_%m_%d_%H_%M_%S") + "." + fileExtension
            savePath = os.path.join(folderPath, saveFileName)
            return savePath
        except:
            raise


class OSSProcess:  # OSS云服务处理类

    @staticmethod
    def UploadFile(FilePath, FileExtension, BucketName="masterwhite"):  # 上传文件到阿里云，传入相对路径和文件扩展名,返回OSS文件路径
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


if __name__ == '__main__':
    OSSProcess.UploadFile("resources/zh.wav", "wav")
