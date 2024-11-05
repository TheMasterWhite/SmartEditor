import copy
import json
import logging, os
from flask import Flask, Blueprint, request, jsonify, send_file
from utils.Config.FileProcess import *
from utils.SModel.OCR import OCRInterface
from utils.SModel.STT import *
from utils.LModel.Interface import *
from utils import Tools
import jwt
import hashlib
import sqlite3
import datetime

ServiceProcessBlueprint = Blueprint("ServiceProcessBlueprint", __name__, url_prefix = "/Service")
fileSavePath = copy.deepcopy(GLOBAL_FileSavePath)
resourceSavePath = copy.deepcopy(GLOBAL_ResourcesSavePath)


# 从前端接收文件接口
@ServiceProcessBlueprint.route("/UploadFile", methods = ["POST"])
def UploadFile():
    try:
        # 鉴权认证
        valInfo = Tools.ValidToken(request.headers)
        if valInfo["status"] is False:
            raise Exception(valInfo["msg"])
        else:
            userName = valInfo["username"]

        # 请求中不存在文件
        if "file" not in request.files:
            raise Exception("No file in the request.")

        # 获取文件，并保存到用户文件夹中
        file = request.files["file"]
        fullFileName = file.filename
        os.makedirs(userName, exist_ok = True)
        file.save(os.path.join(os.path.join(fileSavePath, userName), fullFileName))
        fileExtension = Tools.GetExtension(fullFileName)
        fileName = Tools.GetFileName(fullFileName)
        curTime = Tools.GetTime()
        # 预处理音视频
        if fileExtension in ["mp4", "wav", "mp3", "pcm", "m4a", "amr"]:
            STTInterface.MainProcess(FullFileName = fullFileName, UserName = userName)

        # 预处理图片
        elif fileExtension in ["pdf", "jpg", "jpeg", "png"]:
            if fileExtension == "pdf":
                filePath = os.path.join(fileSavePath, fullFileName)
                OCRResult = OCRInterface.Doc(FilePath = filePath,
                                             FileType = "PDF")
                FileProcess.SaveTxt(FileName = fileName,
                                    Content = OCRResult)
                # 将文件信息保存到数据库中
                saveTime = Tools.GetSaveTime()
                summaryText = LLMInterface.FileSummary(OCRResult)
                FileProcess.SaveFileInfo(FileName = fullFileName,
                                         Description = summaryText,
                                         SaveTime = saveTime,
                                         UserName = userName)

            else:
                filePath = os.path.join(fileSavePath, fullFileName)
                OCRResult = OCRInterface.Doc(FilePath = filePath,
                                             FileType = "IMG")
                FileProcess.SaveTxt(FileName = fileName,
                                    Content = OCRResult)
                # 将文件信息保存到数据库中
                summaryText = LLMInterface.FileSummary(OCRResult)
                saveTime = Tools.GetSaveTime()
                FileProcess.SaveFileInfo(FileName = fullFileName,
                                         Description = summaryText,
                                         SaveTime = saveTime,
                                         UserName = userName)

        elif fileExtension in ["txt"]:
            text = FileProcess.ReadTxt(os.path.join(fileSavePath, fullFileName))
            # 将文件信息保存到数据库中
            summaryText = LLMInterface.FileSummary(text)
            saveTime = Tools.GetSaveTime()
            FileProcess.SaveFileInfo(FileName = fullFileName,
                                     Description = summaryText,
                                     SaveTime = saveTime,
                                     UserName = userName)

        elif fileExtension in ["doc", "docx"]:
            docFile = os.path.join(fileSavePath, fullFileName)
            doc = Document(docFile)
            txtSavePath = os.path.join(fileSavePath, fileName + ".txt")
            with open(txtSavePath, 'w', encoding = 'utf-8') as f:
                # 遍历文档中的每个段落
                for para in doc.paragraphs:
                    # 将段落文本写入txt文件
                    f.write(para.text + '\n')

            text = FileProcess.ReadTxt(txtSavePath)
            # 将文件信息保存到数据库中
            summaryText = LLMInterface.FileSummary(text)
            saveTime = Tools.GetSaveTime()
            FileProcess.SaveFileInfo(FileName = fullFileName,
                                     Description = summaryText,
                                     SaveTime = saveTime,
                                     UserName = userName)

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
        # 鉴权验证
        valInfo = Tools.ValidToken(request.headers)
        if valInfo["status"] is False:
            raise Exception(valInfo["msg"])
        else:
            userName = valInfo["username"]

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
        # 鉴权验证
        valInfo = Tools.ValidToken(request.headers)
        if valInfo["status"] is False:
            raise Exception(valInfo["msg"])
        else:
            userName = valInfo["username"]

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
        # 鉴权验证
        valInfo = Tools.ValidToken(request.headers)
        if valInfo["status"] is False:
            raise Exception(valInfo["msg"])
        else:
            userName = valInfo["username"]

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
            filePath = os.path.join(os.path.join(fileSavePath, userName), fullFileName)

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

    except FileNotFoundError as e:
        pass

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
        # 鉴权验证
        valInfo = Tools.ValidToken(request.headers)
        if valInfo["status"] is False:
            raise Exception(valInfo["msg"])
        else:
            userName = valInfo["username"]

        requestData = request.json
        content = requestData["content"]
        if len(content) <= 5:
            raise ValueError("File content is empty.")

        prompt = "根据下面这段文字生成一个文件名，字数10个字以内，如果无实质内容就回答“空文件”，只回答文件名不要回复多余的内容，不需要扩展名:\n" + content
        fileName = LLMInterface.GetResponse_String(prompt)
        txtFileName = fileName + ".txt"
        savePath = os.path.join(fileSavePath, txtFileName)
        with open(savePath, "w") as f:
            f.write(content)

        saveTime = Tools.GetSaveTime()
        fileSummary = LLMInterface.FileSummary(content)
        FileProcess.SaveFileInfo(FileName = fullFileName,
                                 Description = summaryText,
                                 SaveTime = saveTime,
                                 UserName = userName)

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
@ServiceProcessBlueprint.route("/GetFileInfo", methods = ["GET"])
def GetFileList():
    try:
        # 鉴权验证
        valInfo = Tools.ValidToken(request.headers)
        if valInfo["status"] is False:
            raise Exception(valInfo["msg"])
        else:
            userName = valInfo["username"]

        # 从请求头中获取username
        userName = Tools.GetUsername(request.headers)
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


# 登录
@ServiceProcessBlueprint.route("/Login", methods = ["POST"])
def Login():
    try:
        requestData = request.json
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        conn = sqlite3.connect("UserInfo.db")
        cursor = conn.cursor()

        if Tools.ValidUsername(username) is False:
            raise Exception("用户名长度限制3-10，只允许大小写字母和数字！")
        if Tools.ValidPassword(password) is False:
            raise Exception("密码长度限制8-16，只允许大小写字母和数字！")
        if username is None:
            raise Exception("请输入用户名！")
        if password is None:
            raise Exception("请输入密码！")

        cursor.execute("SELECT passwordHash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()

        # 验证用户名和密码
        if user is None:
            raise Exception("用户名不存在！")
        elif hashedPassword != user[0]:
            raise Exception("密码错误！")

        # 生成JWT
        token = jwt.encode({
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours = 24)  # 设置token过期时间为24小时
        }, GLOBAL_RSA_PRIVATE_KEY, algorithm = "RS256")
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": "登录成功！",
            "token": token
        }
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Login]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)

    finally:
        conn.close()


# 注册
@ServiceProcessBlueprint.route('/Register', methods = ['POST'])
def Register():
    try:
        # 获取用户名和密码
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        # 连接到SQLite数据库
        conn = sqlite3.connect("UserInfo.db")
        cursor = conn.cursor()

        if Tools.ValidUsername(username) is False:
            raise Exception("用户名长度限制3-10，只允许大小写字母和数字！")
        if Tools.ValidPassword(password) is False:
            raise Exception("密码长度限制8-16，至少需要一个大小写字母和数字！")
        if username is None:
            raise Exception("请输入用户名！")
        if password is None:
            raise Exception("请输入密码！")

        # 加密密码
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()

        # 插入新用户
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            userName TEXT PRIMARY KEY,
            passwordHash TEXT
            userFiles TEXT
        )
        ''')
        userFiles = json.dumps({"fileList": []})
        cursor.execute("INSERT INTO users (userName, passwordHash, userFiles) VALUES (?, ?, ?)",
                       (username, hashedPassword, userFiles))
        conn.commit()
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": "注册成功，请返回登录！"
        }
        return jsonify(retObj)


    except sqlite3.IntegrityError:
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": "此用户已存在!"
        }
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[register]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)

    finally:
        conn.close()


# test
@ServiceProcessBlueprint.route('/protected', methods = ["POST"])
def protected():
    try:
        # 从请求头中获取username
        token = request.headers.get("Authorization").split(" ")[1]
        result = Tools.ValidToken(token)

        if result[0] == True:
            curTime = Tools.GetTime()
            retObj = {
                "statusCode": 1,
                "requestTime": curTime,
                "response": [GLOBAL_RSA_PRIVATE_KEY, GLOBAL_RSA_PUBLIC_KEY]
            }
            return jsonify(retObj)
        else:
            raise result[1]

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[protected]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)
