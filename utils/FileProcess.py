from utils.HeadFiles import *


class FileProcess:  # 文件处理类

    @classmethod
    def ReadTxt(cls, FilePath):  # 打开txt文件并返回内容，传参为文件地址
        File = open(FilePath, 'r', encoding='utf-8')
        Content = File.read()
        File.close()
        return Content

    @classmethod
    def Base64(cls, InputFilePath):  # 对文件进行Base64编码，返回编码内容文件，传入文件路径
        FileBytes = pathlib.Path(InputFilePath).read_bytes()
        FileBase64 = base64.b64encode(FileBytes).decode('ascii')
        return FileBase64

    @classmethod
    def AbsPath(cls, FilePath):  # 传入相对路径返回绝对路径
        CurrentPath = Path(__file__).resolve()
        CurrentDir = CurrentPath.parent
        AbsPath = CurrentDir.parent / FilePath
        return AbsPath

    @classmethod
    def SaveWithTime(cls, FileName, FileFolder, FileExtension):
        pass


class OSSProcess:  # OSS云服务处理类

    @staticmethod
    def UploadFile(FilePath, FileExtension, BucketName="masterwhite"):  # 上传文件到阿里云，传入相对路径和文件扩展名,返回OSS文件路径
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


if __name__ == '__main__':
    OSSProcess.UploadFile("resources/zh.wav", "wav")
