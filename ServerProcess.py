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
QuerySTTThread = TaskThread()
QuerySTTThread.start()


# 从前端接收文件接口
@ServerProcessBlueprint.route("/UploadFile", methods = ["POST"])
def UploadFile():
    try:
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": "File uploaded successfully."
        }
        # 请求中不存在文件
        if "file" not in request.files:
            raise Exception("No file in the request.")

        # 获取文件并保存
        file = request.files["file"]
        fullFileName = file.filename
        file.save(os.path.join(fileSavePath, fullFileName))
        curTime = Tools.GetTime()

        fileExtension = Tools.GetExtension(fullFileName)
        fileName = Tools.GetFileName(fullFileName)

        # 视频文件转wav再STT处理
        if fileExtension in ["mp4"]:
            FileProcess.ConvertToWav(FileName = fullFileName,
                                     FileExtension = fileExtension)
            # 发起STT服务调用
            fileName_Wav = Tools.GetFileName(fullFileName) + ".wav"
            taskId = STTInterface.CreateTask(FileName = fileName_Wav)
            # 加入轮询队列
            QuerySTTThread.PutTaskId(FileName = fullFileName,
                                     TaskId = taskId)
        # 音频文件，直接转文字处理
        elif fileExtension in ["wav", "mp3", "pcm", "m4a", "amr"]:
            # 发起STT服务调用
            taskId = STTInterface.CreateTask(FileName = fullFileName)
            # 加入轮询队列
            QuerySTTThread.PutTaskId(FileName = fullFileName,
                                     TaskId = taskId)

        # 图片，OCR处理
        elif fileExtension in ["pdf", "jpg", "jpeg", "png"]:
            if fileExtension == "pdf":
                filePath = os.path.join(fileSavePath, fullFileName)
                OCRResult = OCRInterface.Doc(FileName = filePath,
                                             FileType = "PDF")
                FileProcess.SaveTxt(FileName = fileName,
                                    Content = OCRResult)
            else:
                filePath = os.path.join(fileSavePath, fullFileName)
                OCRResult = OCRInterface.Doc(FileName = filePath,
                                             FileType = "IMG")
                FileProcess.SaveTxt(FileName = fileName,
                                    Content = OCRResult)

        elif fileExtension in ["txt"]:
            pass
        else:
            raise ValueError("Unsupported file type.")

    except ValueError as e:
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
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
