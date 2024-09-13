import logging, json, os, sys, requests
from flask import Flask, Blueprint, jsonify, request
from Config import *
from utils import Tools
from utils.SModel.OCR import *
from utils.SModel.TarDetect import *
from utils.SModel.STT import *

SModelBlueprint = Blueprint("SModelBlueprint", __name__, url_prefix = "/SModelInterface")
fileSavePath = copy.deepcopy(GLOBAL_FileSavePath)


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
        return jsonify(retObj), 500
