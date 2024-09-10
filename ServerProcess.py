import logging, os
from flask import Flask, Blueprint, request, jsonify, send_file
from utils import Tools
from utils.Config.FileProcess import *
from utils.SModel.OCR import OCRInterface
from utils.SModel.STT import *

logging.basicConfig(filename = "Server/Log.log",
                    filemode = 'a',
                    level = logging.INFO)

ServerProcessBlueprint = Blueprint("ServerProcessBlueprint", __name__, url_prefix = "/Server")
fileSavePath = GLOBAL_FileSavePath


# 从前端接收文件接口
@ServerProcessBlueprint.route("/UploadFile", methods = ["POST"])
def UploadFile():
    try:
        # 请求中不存在文件
        if "file" not in request.files:
            raise Exception("No file in the request.")

        # 获取文件并保存
        file = request.files["file"]
        fullFileName = file.filename
        file.save(os.path.join(fileSavePath, fullFileName))
        fileExtension = Tools.GetExtension(fullFileName)
        fileName = Tools.GetFileName(fullFileName)

        # 预处理音视频
        if fileExtension in ["mp4", "wav", "mp3", "pcm", "m4a", "amr"]:
            STTInterface.MainProcess(FullFileName = fullFileName,
                                     FileExtension = fileExtension)

        # 预处理图片
        elif fileExtension in ["pdf", "jpg", "jpeg", "png"]:
            if fileExtension == "pdf":
                filePath = os.path.join(fileSavePath, fullFileName)
                OCRResult = OCRInterface.Doc(FileName = filePath,
                                             FileType = "PDF")
                FileProcess.SaveTxt(FileName = fileName,
                                    Content = OCRResult)
            else:
                filePath = os.path.join(fileSavePath, fullFileName)
                OCRResult = OCRInterface.Doc(FilePath = filePath,
                                             FileType = "IMG")
                FileProcess.SaveTxt(FileName = fileName,
                                    Content = OCRResult)

        elif fileExtension in ["txt"]:
            pass
        else:
            # 上传文件格式不支持
            raise ValueError("Unsupported file type.")

        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": "File uploaded successfully."
        }
        return jsonify(retObj)

    # 文件不符合格式规范
    except ValueError as e:
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)

    # AI Studio服务未启动
    except TypeError as e:
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": "AI Studio service did not started."
        }
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[UploadFile]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 文件下载接口
@ServerProcessBlueprint.route("/DownloadFile/<fileName>", methods = ["GET"])
def DownloadFile(fileName):
    try:
        filePath = os.path.join(fileSavePath, fileName)
        # 文件不存在
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"File {fileName} does not exist.")

        return send_file(filePath, as_attachment = True)

    except FileNotFoundError as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[DownloadFile]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj), 404

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[DownloadFile]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj), 500
