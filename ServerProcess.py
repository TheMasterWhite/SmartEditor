import logging
from flask import Flask, Blueprint, request, jsonify, send_file
from utils import Tools
from utils.Config.FileProcess import *
from utils.SModel.STT import *
import os
from utils.SModel.STT import TaskThread

logging.basicConfig(filename = "Server/Log.log",
                    filemode = 'a',
                    level = logging.INFO)

QuerySTTThread = TaskThread()
QuerySTTThread.start()

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
        curTime = Tools.GetTime()

        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": "File uploaded successfully."
        }

        # 如果是音视频文件那就预处理成wav
        fileExtension = Tools.GetExtension(fullFileName)
        if fileExtension in ["mp3", "mp4"]:
            FileProcess.ConvertToWav(FileName = fullFileName,
                                     FileExtension = fileExtension)
            # 发起STT服务调用
            taskId = STTInterface.CreateTask(FileName = fullFileName)
            # 加入轮询队列
            QuerySTTThread.PutTaskId(FileName = fullFileName,
                                     TaskId = taskId)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[UploadFile]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
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
