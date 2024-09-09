from utils.LModel.Interface import *
from utils.Config.PMTProcess import *
import base64, os, pathlib, json, Config
from pathlib import Path


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
            raise e


    @staticmethod
    def GetRawJson(FilePath):  # 获取RawOCR识别结果，传入文件地址返回Json对象

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
            response = requests.post(url = GLOBAL_RAW_OCRURL, json = payload, headers = headers)
            responseData = response.json()
            return responseData

        except Exception as e:
            raise e


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
            raise e


    @staticmethod
    def Raw(FilePath, SavePath = "Saves/OcrResult"):  # 获取RawOCR结果，返回String

        try:
            response = super(OCRInterface, OCRInterface).GetRawJson(FilePath)
            result = [i['text'] for i in response['result']['texts']]
            resultText = "".join(result)
            return resultText

        except Exception as e:
            raise e


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
    def ProcessRaw(FilePath, SavePath = "Saves/RawResult", ResultType = "General"):
        # 使用大模型处理OCR识别结果，传入字符串和结果类型对应的Prompt名字，返回字符串
        try:
            ocrResult = OCRInterface.Raw(FilePath, FileType, SavePath)
            prompt = GetPrompt().Data()["OCRPrompt"][ResultType]
            prompt += ocrResult
            content = LLMInterface.GetResponse_String(prompt)
            return content

        except Exception as e:
            raise e

print(GLOBAL_ERNIETOKEN)