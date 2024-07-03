import json

from HeadFiles import *
from FileProcess import *


class SModelBasic:  # 小模型应用接口类

    @staticmethod
    def GetAccessToken():  # 百度智能云获取access_token

        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": GLOBAL_Baidu_AK, "client_secret": GLOBAL_Baidu_SK}
        return str(requests.post(url, params=params).json().get("access_token"))


    @staticmethod
    def GetDocOcrResult(FilePath, FileType="IMG", SavePath="Saves/OcrResult"):  # 获取文档抽取OCR模型识别内容，
        # 传入相对文件地址、文件类型和JSON文件保存地址，文件类型为"IMG"或"PDF",返回解析文本
        fileCode = {"PDF": 0, "IMG": 1}
        try:
            absPath = FileProcess.AbsPath(FilePath)
            base64File = FileProcess.Base64(absPath)
            headers = {
                "Authorization": f"token {GLOBAL_ERNIETOKEN}",
                "Content-Type": "application/json"
            }
            Payload = {
                "file": base64File,  # Base64编码的文件内容或者文件链接
                "fileType": fileCode[FileType],  # 本地文件类型，0:pdf,1:图片，此参数在上传本地文件时必须设置，使用文件链接时可省略
                "aistudioToken": GLOBAL_ERNIETOKEN,
                "inferenceParams": {
                    "maxLongSide": 960  # 文本检测长边的最大值，当大分辨率图片漏检严重时，可调大该值
                }
            }
            # 获取解析结果
            ocrResponse = requests.post(GLOBAL_DOC_OCRURL, json=Payload, headers=headers)
            ocrResponseData = ocrResponse.json()
            saveData = json.dumps(ocrResponseData, ensure_ascii=False, indent=4)

            # JSON文件操作
            text = ocrResponseData['result']['tableOcrResult']['text_result']
            tableText = ocrResponseData['result']['tableOcrResult']['table_text_rec']
            resultText = max(text, tableText)

            # 处理文件路径
            savePath = FileProcess.SaveWithTime(FileName="DocResult",
                                                TarPath=SavePath,
                                                FileExtension="json")
            with open(savePath, 'w', encoding='utf-8') as f:
                f.write(saveData)
            return resultText

        except Exception as e:
            raise e


    @staticmethod
    def GetSTTResult(FilePath, FileExtension, Language="Chinese", SavePath="Saves/SttResult"):  # Chinese或English
        # 获取语音转文字结果，传入相对路径、扩展名和语言，返回转写结果String并保存到SavePath

        AbsPath = FileProcess.AbsPath(FilePath)
        OSSPath = OSSProcess.UploadFile(AbsPath, FileExtension)
        CreatUrl = "https://aip.baidubce.com/rpc/2.0/aasr/v1/create?access_token=" + SModelBasic.GetAccessToken()
        QueryUrl = "https://aip.baidubce.com/rpc/2.0/aasr/v1/query?access_token=" + SModelBasic.GetAccessToken()

        Code = {"Chinese": 80006, "English": 1737}
        # 请求头
        payload = json.dumps({
            "speech_url": OSSPath,
            "format": FileExtension,
            "pid": Code[Language],
            "rate": 16000,
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        CreateResponse = requests.request("POST", CreatUrl, headers=headers, data=payload)
        # print(Response.text)

        # 上传信息
        CreateData = json.loads(CreateResponse.text)
        CreateTask = CreateData["task_id"]
        # print("task id:" + task)
        QuertPayload = json.dumps({"task_ids": [CreateTask]})

        while (1):
            queryResponse = requests.request("POST", QueryUrl, headers=headers, data=QuertPayload)
            queryData = queryResponse.json()
            saveData = json.dumps(queryData, ensure_ascii=False, indent=4)
            # 获取状态
            status = queryData['tasks_info'][0]['task_status']

            if (status == "Success"):

                savePath = FileProcess.SaveWithTime(FileName="Result",
                                                    TarPath=SavePath,
                                                    FileExtension="json")
                with open(savePath, "w") as f:
                    f.write(saveData)
                return queryData['tasks_info'][0]['task_result']['result']

            elif (status == "Failed"):
                return "Failed!"


    @staticmethod
    def GetTarDetectResult(FilePath, SavePath="Saves/TarResult"):
        # 获取目标检测结果，传入文件地址返回结果String并保存json到SavePath

        API_URL = "https://mas5g0dfrereq9ta.aistudio-hub.baidu.com/objectdetection"
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
            response = requests.post(API_URL, json=payload, headers=headers)
            responseData = response.json()
            saveData = json.dumps(responseData, ensure_ascii=False, indent=4)

            # 保存预测结果json文件
            savePath = FileProcess.SaveWithTime(FileName="Result",
                                                TarPath=SavePath,
                                                FileExtension="json")
            with open(savePath, "w") as f:
                f.write(saveData)

            # 处理识别结果图片并保存
            savePath = FileProcess.SaveWithTime(FileName="Result",
                                                TarPath=SavePath,
                                                FileExtension="jpg")
            imageBase64 = responseData["result"]["image"]
            imageBytes = base64.b64decode(imageBase64)
            imageArray = np.frombuffer(imageBytes, dtype=np.uint8)
            predictedImage = cv2.imdecode(imageArray, flags=cv2.IMREAD_COLOR)
            cv2.imwrite(savePath, predictedImage)
            return "Need to be added json function"

        except Exception as e:
            raise e


    @staticmethod
    def GetRawOcrResult(FilePath, SavePath="Saves/OcrResult"):
        # 获取RawOCR识别结果，传入文件地址返回结果String并保存json到SavePath

        try:
            absPath = FileProcess.AbsPath(FilePath)
            base64File = FileProcess.Base64(absPath)
            headers = {
                "Authorization": f"token {GLOBAL_ERNIETOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "image": base64File  # Base64编码的文件内容或者文件链接
            }
            savePath = FileProcess.SaveWithTime(FileName="RawResult",
                                                TarPath=SavePath,
                                                FileExtension="json")
            response = requests.post(url=GLOBAL_RAW_OCRURL, json=payload, headers=headers)
            responseData = response.json()
            saveData = json.dumps(responseData, ensure_ascii=False, indent=4)
            result = [i['text'] for i in responseData['result']['texts']]
            resultText = "".join(result)

            with open(savePath, 'w') as f:
                f.write(saveData)
            return resultText

        except Exception as e:
            raise e


class SModelInterface(SModelBasic):

    def ProcessedOCR():
        pass


def test():
    path = "resources/house.jpeg"
    a = SModelBasic.GetTarDetectResult(FilePath=path)
    print(a)


if __name__ == '__main__':
    test()
