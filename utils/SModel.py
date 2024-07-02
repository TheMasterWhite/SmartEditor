from HeadFiles import *
from FileProcess import *


class SModel:  # 小模型应用接口类

    @staticmethod
    def GetAccessToken():  # 百度智能云获取access_token

        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": GLOBAL_Baidu_AK, "client_secret": GLOBAL_Baidu_SK}
        return str(requests.post(url, params=params).json().get("access_token"))

    @staticmethod
    def GetOcrResult(FilePath, FileType=1, SavePath="Saves/OcrResult"):
        # 获取OCR识别内容，传入相对文件地址、文件类型和JSON文件保存地址，0为PDF，1为图片,返回解析文本
        try:
            ABSPath = FileProcess.AbsPath(FilePath)
            Base64File = FileProcess.Base64(ABSPath)
            headers = {
                "Authorization": f"token {GLOBAL_ERNIETOKEN}",
                "Content-Type": "application/json"
            }
            Payload = {
                "file": Base64File,  # Base64编码的文件内容或者文件链接
                "fileType": FileType,  # 本地文件类型，0:pdf,1:图片，此参数在上传本地文件时必须设置，使用文件链接时可省略
                "aistudioToken": GLOBAL_ERNIETOKEN,
                "inferenceParams": {
                    "maxLongSide": 960  # 文本检测长边的最大值，当大分辨率图片漏检严重时，可调大该值
                }
            }
            # 获取解析结果
            OcrResponse = requests.post(GLOBAL_OCRURL, json=Payload, headers=headers)
            OcrResponseData = OcrResponse.json()

            # JSON文件操作
            text = OcrResponseData['result']['tableOcrResult']['text_result']
            tableText = OcrResponseData['result']['tableOcrResult']['table_text_rec']
            resultText = max(text,tableText)

            # 处理文件路径
            savePath = FileProcess.SaveWithTime(FileName="Result",
                                                TarPath=SavePath,
                                                FileExtension="json")
            print(savePath)
            with open(savePath, 'w', encoding='utf-8') as f:
                json.dump(OcrResponseData, f, ensure_ascii=False, indent=4)

            return resultText
        except Exception as e:
            return str(e)

    @staticmethod
    def GetSTTResult(FilePath, FileExtension, Language="Chinese", SavePath="Saves/SttResult"):  # Chinese或English
        # 获取语音转文字结果，传入相对路径、扩展名和语言，返回转写结果

        AbsPath = FileProcess.AbsPath(FilePath)
        OSSPath = OSSProcess.UploadFile(AbsPath, FileExtension)
        CreatUrl = "https://aip.baidubce.com/rpc/2.0/aasr/v1/create?access_token=" + SModel.GetAccessToken()
        QueryUrl = "https://aip.baidubce.com/rpc/2.0/aasr/v1/query?access_token=" + SModel.GetAccessToken()

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
        print(CreateData)
        CreateTask = CreateData["task_id"]
        # print("task id:" + task)
        QuertPayload = json.dumps({"task_ids": [CreateTask]})

        while (1):
            queryResponse = requests.request("POST", QueryUrl, headers=headers, data=QuertPayload)
            queryData = json.loads(queryResponse.text)
            # 获取状态
            status = queryData['tasks_info'][0]['task_status']

            if (status == "Success"):
                savePath = FileProcess.SaveWithTime(FileName="Result",
                                                    TarPath=SavePath,
                                                    FileExtension="json")
                with open(savePath, "w") as f:
                    json.dump(queryData, f)
                return queryData['tasks_info'][0]['task_result']['result']
            elif (status == "Failed"):
                return "Failed!"

    @staticmethod
    def GetTarDetectResult(FilePath, SavePath="Saves/TarResult"):
        # 获取目标检测结果
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
            responseData = json.loads(response.content)
            boxResult = responseData["result"]["bboxResult"]

            # 保存预测结果json文件
            savePath = FileProcess.SaveWithTime(FileName="Result",
                                                TarPath=SavePath,
                                                FileExtension="json")
            with open(savePath, "w") as f:
                json.dump(boxResult, f)

            # 处理识别结果图片并保存
            savePath = FileProcess.SaveWithTime(FileName="Result",
                                                TarPath=SavePath,
                                                FileExtension="jpg")
            imageBase64 = responseData["result"]["image"]
            imageBytes = base64.b64decode(imageBase64)
            imageArray = np.frombuffer(imageBytes, dtype=np.uint8)
            predictedImage = cv2.imdecode(imageArray, flags=cv2.IMREAD_COLOR)
            cv2.imwrite(savePath, predictedImage)

            return boxResult
        except Exception as e:
            return str(e)


def test():
    path = "resources/house.jpeg"
    a = SModel.GetTarDetectResult(FilePath=path)
    print(a)


if __name__ == '__main__':
    test()
