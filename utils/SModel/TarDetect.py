from utils.HeadFiles import *
from utils.FileProcess import *
from utils.LModel import *
from utils.PMTProcess import *


class TarDetectBasic:

    @staticmethod
    def GetJson(FilePath):
        # 获取目标检测结果，传入文件地址返回结果String并保存json到SavePath
        headers = {
            "Authorization": f"token {GLOBAL_ERNIETOKEN}",
            "Content-Type": "application/json"
        }
        try:
            # 获取文件对路径并转码
            absPath = FileProcess.AbsPath(FilePath)
            base64File = FileProcess.Base64(absPath)

            payload = {
                "image": base64File
            }
            # 请求结果并解析
            response = requests.post(GLOBAL_TarDetectURL, json = payload, headers = headers)
            responseData = response.json()
            return responseData

        except Exception as e:
            raise e


class TarInterface(TarDetectBasic):

    @staticmethod
    def GetResult(FilePath, SavePath = "Saves/TarResult"):  # 获取目标检测结果

        try:
            result = super(TarInterface, TarInterface).GetJson(FilePath)
            JsonOperator.Save(result, SavePath, "Result")

            # 处理图像数据并保存
            imageBase64 = result["result"]["image"]
            imageBytes = base64.b64decode(imageBase64)
            imageArray = np.frombuffer(imageBytes, dtype = np.uint8)
            predictedImage = cv2.imdecode(imageArray, flags = cv2.IMREAD_COLOR)
            savePath = FileProcess.GetFileTimePath(FileName = "Result",
                                                   TarPath = SavePath,
                                                   FileExtension = "jpg")
            cv2.imwrite(savePath, predictedImage)
            return "Need to be added json function"

        except Exception as e:
            raise e
