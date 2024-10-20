from utils.LModel.Interface import *
from utils.Config.PMTProcess import *
from utils.Config.FileProcess import *
import base64, os, pathlib, json, logging
from pathlib import Path
from Config import *
from utils import Tools
import urllib

fileSavePath = copy.deepcopy(GLOBAL_FileSavePath)


class OCRBasic:

    @staticmethod
    def GetDocJson(FilePath, FileCode):  # 获取文档抽取OCR模型识别内容，
        # 传入绝对文件地址、文件类型，文件类型为"IMG"或"PDF",返回解析json

        try:
            base64File = FileProcess.Base64(FilePath)
            headers = {
                "Authorization": f"token {GLOBAL_ERNIETOKEN}",
                "Content-Type": "application/json"
            }
            Payload = {
                "file": base64File,  # Base64编码的文件内容或者文件链接
                "fileType": FileCode,  # 本地文件类型，0:pdf,1:图片，此参数在上传本地文件时必须设置，使用文件链接时可省略
                "aistudioToken": GLOBAL_ERNIETOKEN,
                "inferenceParams": {
                    "maxLongSide": 960  # 文本检测长边的最大值，当大分辨率图片漏检严重时，可调大该值
                }
            }
            # 获取解析结果
            ocrResponse = requests.post(GLOBAL_DOC_OCRURL, json = Payload, headers = headers)
            ocrResponseData = ocrResponse.json()
            return ocrResponseData

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[GetDocJson]" + str(e))


class OCRInterface(OCRBasic):

    @staticmethod
    def Doc(FilePath, FileType):
        # 获取DocOCR识别结果，返回String

        try:
            fileCode = {"PDF": 0, "IMG": 1}
            code = fileCode[FileType]
            response = OCRBasic.GetDocJson(FilePath, code)
            text = response['result']['tableOcrResult']['text_result']
            tableText = response['result']['tableOcrResult']['table_text_rec']
            resultText = max(text, tableText)
            return resultText

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[Doc]" + str(e))


    @staticmethod
    def ProcessDoc(FilePath, FileType = "IMG", SavePath = "Saves/OcrResult", ResultType = "General"):
        # 使用大模型处理OCR识别结果，传入字符串和结果类型对应的Prompt名字，返回字符串

        try:
            ocrResult = OCRInterface.Doc(FilePath, FileType, SavePath)
            prompt = GetPrompt().Data()["OCRPrompt"][ResultType]
            prompt += ocrResult
            content = LLMInterface.GetResponse_String(prompt)
            return content

        except Exception as e:
            raise e


    @staticmethod
    def BaiDu(FilePath, FileType):
        try:

            # 获取鉴权
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {
                "grant_type": "client_credentials",
                "client_id": GLOBAL_Baidu_AK,
                "client_secret": GLOBAL_Baidu_SK
            }
            token = str(requests.post(url, params = params).json().get("access_token"))

            url = "https://aip.baidubce.com/rest/2.0/ocr/v1/doc_convert/request?access_token=" + token
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }

            base64File = ""
            data = ""
            with open(FilePath, "rb") as f:
                content = base64.b64encode(f.read()).decode("utf8")
                base64File = urllib.parse.quote_plus(content)

            if FileType == "IMG":
                data = "image=" + base64File
            else:
                data = "pdf_file=" + base64File
                
            response = requests.post(url, data = data, headers = headers)
            result = ""
            for results in response.json()["words_result"]:
                result += results["words"]
            return result

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[BaiDuOCR]" + str(e))
