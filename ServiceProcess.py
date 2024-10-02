import copy
import logging, os
from flask import Flask, Blueprint, request, jsonify, send_file
from utils import Tools
from utils.Config.FileProcess import *
from utils.SModel.OCR import OCRInterface
from utils.SModel.STT import *
from utils.LModel.Interface import *

ServiceProcessBlueprint = Blueprint("ServiceProcessBlueprint", __name__, url_prefix = "/Service")
fileSavePath = copy.deepcopy(GLOBAL_FileSavePath)
resourceSavePath = copy.deepcopy(GLOBAL_ResourcesSavePath)


# 从前端接收文件接口
@ServiceProcessBlueprint.route("/UploadFile", methods = ["POST"])
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
        curTime = Tools.GetTime()
        # 预处理音视频
        if fileExtension in ["mp4", "wav", "mp3", "pcm", "m4a", "amr"]:
            STTInterface.MainProcess(FullFileName = fullFileName)

        # 预处理图片
        elif fileExtension in ["pdf", "jpg", "jpeg", "png"]:
            if fileExtension == "pdf":
                filePath = os.path.join(fileSavePath, fullFileName)
                OCRResult = OCRInterface.Doc(FilePath = filePath,
                                             FileType = "PDF")
                FileProcess.SaveTxt(FileName = fileName,
                                    Content = OCRResult)
                # 将文件信息保存到数据库中
                saveTime = f"{Tools.GetDate()} {Tools.GetTime()}"
                summaryText = LLMInterface.FileSummary(text)
                FileProcess.SaveFileInfo(FileName = fullFileName,
                                         Description = summaryText,
                                         SaveTime = saveTime)

            else:
                filePath = os.path.join(fileSavePath, fullFileName)
                OCRResult = OCRInterface.Doc(FilePath = filePath,
                                             FileType = "IMG")
                FileProcess.SaveTxt(FileName = fileName,
                                    Content = OCRResult)
                # 将文件信息保存到数据库中
                summaryText = LLMInterface.FileSummary(text)
                saveTime = f"{Tools.GetDate()} {Tools.GetTime()}"
                FileProcess.SaveFileInfo(FileName = fullFileName,
                                         Description = summaryText,
                                         SaveTime = saveTime)

        elif fileExtension in ["txt"]:
            text = FileProcess.ReadTxt(os.path.join(fileSavePath, fullFileName))
            # 将文件信息保存到数据库中
            summaryText = LLMInterface.FileSummary(text)
            saveTime = f"{Tools.GetDate()} {Tools.GetTime()}"
            FileProcess.SaveFileInfo(FileName = fullFileName,
                                     Description = summaryText,
                                     SaveTime = saveTime)

        else:
            # 上传文件格式不支持
            raise ValueError("Unsupported file type.")

        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": f"File [{fullFileName}] uploaded successfully."
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
@ServiceProcessBlueprint.route("/DownloadFile/<fileName>", methods = ["GET"])
def DownloadFile(fileName):
    try:
        filePath = os.path.join(fileSavePath, fileName)
        # 文件不存在
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"File [{fileName}] does not exist.")

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


# 读取用户知识库文本
@ServiceProcessBlueprint.route("/ReadFile", methods = ["POST"])
def ReadFile():
    try:
        requestData = request.json
        fullFileName = requestData.get("fileName", None)
        if fullFileName is None:
            raise ValueError("Parameter cannot be empty.")

        filePath = os.path.join(fileSavePath, fullFileName)
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"File [{fullFileName}] does not exist.")

        fileName = Tools.GetFileName(fullFileName) + ".txt"
        filePath = os.path.join(fileSavePath, fileName)
        fileContent = FileProcess.ReadTxt(FilePath = filePath)

        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": fileContent
        }
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[ReadFile]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 删除用户知识库文件
@ServiceProcessBlueprint.route("/DeleteFile", methods = ["POST"])
def DeleteFile():
    try:
        requestData = request.json
        fullFileNameList = requestData.get("fileName", None)
        curTime = Tools.GetTime()
        if fullFileNameList is None:
            raise ValueError("Parameter cannot be empty.")

        # fileName是列表
        if isinstance(fullFileNameList, list):

            deletedFileList = []
            unknownFileList = []
            for fullFileName in fullFileNameList:
                filePath = os.path.join(fileSavePath, fullFileName)
                fileName = Tools.GetFileName(fullFileName)
                fileExtension = Tools.GetExtension(fullFileName)
                # 判断文件是否存在
                if not os.path.exists(filePath):
                    unknownFileList.append(fullFileName)
                    continue

                else:
                    # 目标文件是txt
                    if fileExtension == ".txt":
                        os.remove(filePath)
                        FileProcess.DeleteFileInfo(fullFileName)
                        logging.info(f"[{curTime}]\"{fileName}\" deleted successfully.")
                        deletedFileList.append(fullFileName)

                    # 目标文件是多媒体
                    else:
                        os.remove(filePath)
                        FileProcess.DeleteFileInfo(fullFileName)
                        txtFilePath = os.path.join(fileSavePath, fileName) + ".txt"
                        os.remove(txtFilePath)
                        logging.info(f"[{curTime}]\"{fullFileName}\" deleted successfully.")
                        deletedFileList.append(fullFileName)

            retObj = {
                "statusCode": 1,
                "requestTime": curTime,
                "response": f"{deletedFileList} were successfully deleted, but {unknownFileList} were not found."
            }
            return jsonify(retObj)

        # fileName不是列表
        else:
            fullFileName = fullFileNameList
            retObj = {
                "statusCode": 1,
                "requestTime": curTime,
                "response": f"File \"{fullFileName}\" were successfully deleted"
            }
            fileExtension = Tools.GetExtension(fullFileName)
            rawFileName = Tools.GetFileName(fullFileName)
            filePath = os.path.join(fileSavePath, fullFileName)

            # 判断文件存不存在
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"File [{fullFileName}] does not exist.")
            else:
                # 目标文件是txt
                if fileExtension == ".txt":
                    os.remove(filePath)
                    logging.info(f"[{curTime}]\"{fullFileName}\" deleted successfully.")
                    os.remove(filePath)

                # 目标文件是多媒体文件
                else:
                    os.remove(filePath)
                    txtFilePath = os.path.join(fileSavePath, rawFileName) + ".txt"
                    os.remove(txtFilePath)
                    logging.info(f"[{curTime}]\"{fullFileName}\" deleted successfully.")

            return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[DeleteFile]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 将用户编辑器内容保存到文件中
@ServiceProcessBlueprint.route("/Save", methods = ["POST"])
def Save():
    try:
        requestData = request.json
        fileName = requestData["fileName"]
        content = requestData["content"]

        rawFileName = Tools.GetFileName(fileName)
        txtFileName = rawFileName + ".txt"
        savePath = os.path.join(fileSavePath, txtFileName)
        with open(savePath, "w") as f:
            f.write(content)

        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]User txt file [{txtFileName}] saved successfully.")
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": f"Document content saved successfully."
        }
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Save]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 大模型联网纠错
@ServiceProcessBlueprint.route("/CheckFile", methods = ["POST"])
def CheckFile():
    try:
        requestData = request.json
        fullfileName = requestData["fileName"]
        filePath = os.path.join(fileSavePath, fullfileName)
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"File [{fullfileName}] does not exist.")

        fileName = Tools.GetFileName(fullfileName)
        txtfileName = fileName + ".txt"
        filePath = os.path.join(fileSavePath, txtfileName)
        fileContent = FileProcess.ReadTxt(FilePath = filePath)

        checkResult = LLMInterface.CheckFile(Tartext = fileContent)
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": checkResult
        }
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Save]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 上传资源文件，开发者接口不对用户开放
@ServiceProcessBlueprint.route("/UploadResource", methods = ["POST"])
def UploadResource():
    try:
        # 请求中不存在文件
        if "file" not in request.files:
            raise Exception("No file in the request.")

        # 获取文件并保存
        file = request.files["file"]
        fullFileName = file.filename
        file.save(os.path.join(resourceSavePath, fullFileName))

        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": f"File [{fullFileName}] uploaded successfully."
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


# 获取文件列表
@ServiceProcessBlueprint.route("/GetFileList", methods = ["GET"])
def GetFileList():
    try:
        fileList = []
        for fullFileName in os.listdir(fileSavePath):
            fileInfo = FileProcess.GetFileInfo(FileName = fullFileName)
            if fileInfo is None:
                continue
            else:
                distObj = {
                    "name": fullFileName,
                    "description": fileInfo[0],
                    "time": fileInfo[1],
                }
                fileList.append(distObj)

        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]Send file list successed.")
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": fileList,
        }
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[GetFileList]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)
