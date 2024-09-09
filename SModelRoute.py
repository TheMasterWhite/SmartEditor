import logging, json, os, sys, requests
from flask import Flask, Blueprint, jsonify, request
from Config import *
from utils import Tools
from utils.SModel.OCR import *
from utils.SModel.TarDetect import *
from utils.SModel.STT import *

OCRBlueprint = Blueprint("OCRBlueprint", __name__, url_prefix = "/OCRInterface")
fileSavePath = GLOBAL_FileSavePath


@OCRBlueprint.route("/Doc", methods = ["POST"])
def GetDocOCR():
    try:
        requestData = request.json
        logging.info(f"Received request from OCR API,{requestData}")
        fileName = requestData["fileName"]
        filePath = os.path.join(fileSavePath, fileName)
        # 文件不存在
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"File {fileName} does not exist.")

        fileExtension = Tools.GetExtension(fileName)
        fileType = "IMG"
        if fileExtension == "pdf":
            fileType = "PDF"
        elif (fileExtension == "jpg" or
              fileExtension == "jpeg" or
              fileExtension == "png"):
            fileType = "IMG"
        else:
            raise ValueError("Unsupported file type.")

        OCR_ResultString = OCRInterface.Doc(FilePath = filePath,
                                            FileType = fileType)
        savePath = os.path.join(fileSavePath, fileName)

        with open(savePath, "rb") as f:
            f.write(OCR_ResultString)

        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": "OCR result saved successfully."
        }
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]OCR success.")
        return jsonify(retObj)

    except FileNotFoundError as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[GetDocOCR]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj), 404

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[GetDocOCR]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj), 500
