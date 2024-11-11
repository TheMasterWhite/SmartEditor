import logging, json, os, sys, requests
from flask import Flask, Blueprint, jsonify, request
from Config import *
from utils import Tools
from utils.SModel.OCR import *
from utils.SModel.TarDetect import *
from utils.SModel.STT import *
import erniebot

SModelBlueprint = Blueprint("SModelBlueprint", __name__, url_prefix = "/SModelInterface")
fileSavePath = copy.deepcopy(GLOBAL_FileSavePath)


def GetAccessToken_Image():  # 百度智能云获取access_token
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials",
              "client_id": GLOBAL_Baidu_Image_AK,
              "client_secret": GLOBAL_Baidu_Image_SK}
    return str(requests.post(url, params = params).json().get("access_token"))


@SModelBlueprint.route("/OCR", methods = ["POST"])
def GetDocOCR():
    try:
        requestData = request.json
        fileNameList = requestData["fileName"]

        for fileName in fileNameList:

            filePath = os.path.join(fileSavePath, fileName)
            # 文件不存在
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"File {fileName} does not exist.")

            saveFileName = Tools.GetFileName(FileName = fileName)
            fileExtension = Tools.GetExtension(FileName = fileName)
            fileType = "IMG"
            if fileExtension == "pdf":
                fileType = "PDF"
            elif fileExtension in ["jpg", "jpeg", "png"]:
                fileType = "IMG"
            else:
                raise ValueError("Unsupported file type.")

            # 发起OCR调用
            OCR_ResultString = OCRInterface.Doc(FilePath = filePath,
                                                FileType = fileType)
            curTime = Tools.GetTime()
            logging.info(f"[{curTime}]Get OCR result successfully.")

            # 写入OCR识别结果
            saveFileName += ".txt"
            savePath = os.path.join(fileSavePath, saveFileName)
            with open(savePath, "w") as f:
                f.write(OCR_ResultString)

        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": "OCR results saved successfully."
        }
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]Write OCR results successfully.")
        return jsonify(retObj)

    # 没找到本地文件
    except FileNotFoundError as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[GetDocOCR]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj), 404

    # AI Studio服务未启动
    except TypeError as e:
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": "AI Studio service did not started."
        }
        return jsonify(retObj), 503

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[GetDocOCR]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj), 500


@SModelBlueprint.route("/STT", methods = ["POST"])
def GetSTTResult():
    try:
        requestData = request.json
        fileData = requestData["fileData"]

        # 处理数据列表
        for file in fileData:
            fullFileName = file["name"]
            language = file.get("language", "Chinese")

            filePath = os.path.join(fileSavePath, fullFileName)
            # 文件不存在
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"File {fullFileName} does not exist.")

            STTInterface.MainProcess(FullFileName = fullFileName,
                                     Language = language)

        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": "Send STT request successfully."
        }
        return jsonify(retObj)

    except FileNotFoundError as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[GetSTTResult]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj), 404

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[GetSTTResult]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


@SModelBlueprint.route("/Image", methods = ["POST"])
def Image():
    try:
        # 鉴权验证
        token = request.headers.get("Authorization", None)
        if token is None:
            raise Exception("Unauthorized request.")
        token = token.split(" ")[1]
        valInfo = ValidToken(token)
        if valInfo["status"] is False:
            raise Exception(valInfo["msg"])
        else:
            userName = valInfo["username"]

        requestData = request.json
        prompt = requestData["prompt"]

        # 临时切换erniebot api类型
        erniebot.api_type = "yinian"
        erniebot.access_token = GetAccessToken_Image()
        response = erniebot.Image.create(model = "ernie-vilg-v2",
                                         prompt = prompt,
                                         width = 2048,
                                         height = 2048,
                                         version = "v2",
                                         image_num = 1)
        url = response.get_result()[0]
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": url
        }
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Image]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)

    finally:
        erniebot.api_type = "aistudio"
