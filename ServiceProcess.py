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
from docx import Document

ServiceProcessBlueprint = Blueprint("ServiceProcessBlueprint", __name__, url_prefix = "/Service")
fileSavePath = copy.deepcopy(GLOBAL_FileSavePath)
resourceSavePath = copy.deepcopy(GLOBAL_ResourcesSavePath)


# 验证JWT并返回结果
def ValidToken(Token):
    try:
        payload = jwt.decode(Token, GLOBAL_RSA_PUBLIC_KEY, algorithms = ["RS256"])
        username = payload["username"]
        retObj = {
            "status": True,
            "msg": "OK",
            "username": username,
        }
        return retObj

    except jwt.ExpiredSignatureError:
        retObj = {
            "status": False,
            "msg": "登录过期，请重新登录！",
        }
        return retObj

    except jwt.InvalidTokenError:
        retObj = {
            "status": False,
            "msg": "验证失败，请重试！",
        }
        return retObj

    except Exception as e:
        retObj = {
            "status": False,
            "msg": str(e),
        }
        return retObj


# 从前端接收文件接口
@ServiceProcessBlueprint.route("/UploadFile", methods = ["POST"])
def UploadFile():
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

        # 请求中不存在文件
        if "file" not in request.files:
            raise Exception("No file in the request.")

        # 获取文件，并保存到用户文件夹中
        file = request.files["file"]
        fullFileName = file.filename  # 文件全名
        userFolderPath = os.path.join(fileSavePath, userName)  # 用户文件夹路径
        os.makedirs(userFolderPath, exist_ok = True)
        fileExtension = Tools.GetExtension(fullFileName)  # 文件扩展名
        fileName = Tools.GetFileName(fullFileName)  # 纯文件名
        fileUUID = Tools.GetUUID()
        fullFileSavePath = os.path.join(userFolderPath, fileUUID + "." + fileExtension)  # 用户文件保存路径
        file.save(fullFileSavePath)  # 保存

        curTime = Tools.GetTime()
        # 预处理音视频
        if fileExtension in ["mp4", "wav", "mp3", "pcm", "m4a", "amr"]:
            STTInterface.MainProcess(FullFileName = fullFileName,
                                     UserName = userName,
                                     UUID = fileUUID)

        # 预处理图片
        elif fileExtension in ["pdf", "jpg", "jpeg", "png"]:
            if fileExtension == "pdf":
                OCRResult = OCRInterface.Doc(FilePath = fullFileSavePath,
                                             FileType = "PDF")
                FileProcess.SaveTxt(UUID = fileUUID,
                                    Content = OCRResult,
                                    UserName = userName)
                # 将文件信息保存到数据库中
                saveTime = Tools.GetSaveTime()
                summaryText = LLMInterface.FileSummary(OCRResult)
                FileProcess.SaveFileInfo(FileName = fullFileName,
                                         Description = summaryText,
                                         SaveTime = saveTime,
                                         UserName = userName,
                                         UUID = fileUUID)

            else:
                filePath = os.path.join(fullFileSavePath)
                OCRResult = OCRInterface.Doc(FilePath = fullFileSavePath,
                                             FileType = "IMG")
                FileProcess.SaveTxt(UUID = fileUUID,
                                    Content = OCRResult,
                                    UserName = userName)
                # 将文件信息保存到数据库中
                summaryText = LLMInterface.FileSummary(OCRResult)
                saveTime = Tools.GetSaveTime()
                FileProcess.SaveFileInfo(FileName = fullFileName,
                                         Description = summaryText,
                                         SaveTime = saveTime,
                                         UserName = userName,
                                         UUID = fileUUID)

        elif fileExtension in ["txt"]:
            text = FileProcess.ReadTxt(fullFileSavePath)
            # 将文件信息保存到数据库中
            summaryText = LLMInterface.FileSummary(text)
            saveTime = Tools.GetSaveTime()
            fileId = FileProcess.SaveFileInfo(FileName = fullFileName,
                                              Description = summaryText,
                                              SaveTime = saveTime,
                                              UserName = userName,
                                              UUID = fileUUID)

        elif fileExtension in ["doc", "docx"]:
            doc = Document(fullFileSavePath)
            txtSavePath = os.path.join(userFolderPath, fileUUID + ".txt")
            text = ""
            with open(txtSavePath, 'w', encoding = 'utf-8') as f:
                # 遍历文档中的每个段落
                for para in doc.paragraphs:
                    # 将段落文本写入txt文件
                    f.write(para.text + '\n')
                    text += para.text + "\n"

            # 将文件信息保存到数据库中
            summaryText = LLMInterface.FileSummary(text)
            saveTime = Tools.GetSaveTime()
            FileProcess.SaveFileInfo(FileName = fullFileName,
                                     Description = summaryText,
                                     SaveTime = saveTime,
                                     UserName = userName,
                                     UUID = fileUUID)

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
@ServiceProcessBlueprint.route("/DownloadFile", methods = ["GET"])
def DownloadFile():
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
        fileUUID = requestData["uuid"]
        fullFileName = FileProcess.GetFileInfo(UUID = fileUUID, UserName = userName)
        # 文件不存在
        if fullFileName is None:
            raise FileNotFoundError(f"The file does not exist.")
        else:
            fileExtension = Tools.GetExtension(fullFileName)
            retFileName = fileUUID + "." + fileExtension
            filePath = os.path.join(fileSavePath, userName, retFileName)
            return send_file(filePath, as_attachment = True)

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
        UUID = requestData.get("uuid", None)
        if UUID is None:
            raise ValueError("Parameter cannot be empty.")

        filePath = os.path.join(fileSavePath, userName, UUID + ".txt")
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"File does not exist.")

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
        fileUUID = requestData.get("uuid", None)

        if fileUUID is None:
            raise ValueError("Parameter cannot be empty.")

        # # fileName是列表
        # if isinstance(fullFileNameList, list):
        #
        #     deletedFileList = []
        #     unknownFileList = []
        #     for fullFileName in fullFileNameList:
        #         filePath = os.path.join(fileSavePath, fullFileName)
        #         fileName = Tools.GetFileName(fullFileName)
        #         fileExtension = Tools.GetExtension(fullFileName)
        #         # 判断文件是否存在
        #         if not os.path.exists(filePath):
        #             unknownFileList.append(fullFileName)
        #             continue
        #
        #         else:
        #             # 目标文件是txt
        #             if fileExtension == ".txt":
        #                 os.remove(filePath)
        #                 FileProcess.DeleteFileInfo(fullFileName)
        #                 logging.info(f"[{curTime}]\"{fileName}\" deleted successfully.")
        #                 deletedFileList.append(fullFileName)
        #
        #             # 目标文件是多媒体
        #             else:
        #                 os.remove(filePath)
        #                 FileProcess.DeleteFileInfo(fullFileName)
        #                 txtFilePath = os.path.join(fileSavePath, fileName) + ".txt"
        #                 os.remove(txtFilePath)
        #                 logging.info(f"[{curTime}]\"{fullFileName}\" deleted successfully.")
        #                 deletedFileList.append(fullFileName)
        #
        #     curTime = Tools.GetTime()
        #     retObj = {
        #         "statusCode": 1,
        #         "requestTime": curTime,
        #         "response": f"{deletedFileList} were successfully deleted, but {unknownFileList} were not found."
        #     }
        #     return jsonify(retObj)

        filePath = os.path.join(fileSavePath, userName, fileUUID + ".txt")

        # 判断文件存不存在
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"File does not exist.")

        else:
            fullFileName = FileProcess.GetFileInfo(UUID = fileUUID, UserName = userName)
            fileExtension = Tools.GetExtension(fullFileName)
            # 目标文件是txt
            if fileExtension == "txt":
                os.remove(filePath)

            # 目标文件是多媒体文件
            else:
                fileName = Tools.GetFileName(fullFileName)
                if fileExtension in ["mp4"]:
                    wavPath = os.path.join(fileSavePath, userName, fileUUID + ".wav")
                    os.remove(wavPath)

                oriFilePath = os.path.join(fileSavePath, userName, fileUUID + "." + fileExtension)
                os.remove(filePath)
                os.remove(oriFilePath)

        curTime = Tools.GetTime()
        FileProcess.DeleteFileInfo(UserName = userName, UUID = fileUUID)
        logging.info(f"[{curTime}]\"{fullFileName}\" deleted successfully.")
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": f"File [{fullFileName}] were successfully deleted"
        }
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
        content = requestData["content"]
        if len(content) <= 5:
            raise ValueError("File content is empty.")

        prompt = "根据下面这段文字生成一个文件名，字数10个字以内，如果无实质内容就回答“空文件”，只回答文件名不要回复多余的内容，不需要扩展名:\n" + content
        fileName = LLMInterface.GetResponse_String(prompt)
        fullFileName = fileName + ".docx"
        fileUUID = Tools.GetUUID()
        docFileName = fileUUID + ".docx"
        userFolderPath = os.path.join(fileSavePath, userName)  # 用户文件夹路径
        os.makedirs(userFolderPath, exist_ok = True)
        savePath = os.path.join(userFolderPath, docFileName)

        Tools.SaveDocx(Title = fileName, Content = content, SavePath = savePath)
        saveTime = Tools.GetSaveTime()
        summaryText = LLMInterface.FileSummary(content)
        FileProcess.SaveFileInfo(FileName = fullFileName,
                                 Description = summaryText,
                                 SaveTime = saveTime,
                                 UserName = userName,
                                 UUID = fileUUID)

        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]User txt file [{fullFileName}] saved successfully.")
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
        fullfileName = requestData["fileName"]
        userFolderPath = os.path.join(fileSavePath, userName)
        filePath = os.path.join(userFolderPath, fullfileName)
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
        token = request.headers.get("Authorization", None)
        if token is None:
            raise Exception("Unauthorized request.")
        token = token.split(" ")[1]
        valInfo = ValidToken(token)
        if valInfo["status"] is False:
            raise Exception(valInfo["msg"])
        else:
            userName = valInfo["username"]

        fileInfo = FileProcess.GetFileList(UserName = userName)
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]Send file list successed.")
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": fileInfo,
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

        if username is None:
            raise Exception("请输入用户名！")
        if password is None:
            raise Exception("请输入密码！")
        if Tools.ValidUsername(username) is False:
            raise Exception("用户名长度限制3-10，只允许大小写字母和数字！")
        if Tools.ValidPassword(password) is False:
            raise Exception("密码长度限制8-16，只允许大小写字母和数字！")

        cursor.execute("SELECT passwordHash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        # 验证用户名和密码
        if user is None:
            raise Exception("用户名不存在！")

        hashedPassword = hashlib.sha256(password.encode()).hexdigest()

        if hashedPassword != user[0]:
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
            "response": str(e),
            "token": None
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
            passwordHash TEXT,
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
