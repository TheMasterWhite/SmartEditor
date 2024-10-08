import copy
import logging, json, os, sys, requests
from flask import Flask, request, jsonify, Response, stream_with_context, Blueprint
from utils.LModel.Interface import LLMInterface
from utils.LModel.ChatBot import BotInterface, bot
from utils.Config.FileProcess import *
from utils import Tools

LLMBlueprint = Blueprint("LLMBlueprint", __name__, url_prefix = '/LLMInterface')
fileSavePath = copy.deepcopy(GLOBAL_FileSavePath)
resourceSavePath = copy.deepcopy(GLOBAL_ResourcesSavePath)


# 翻译功能接口
@LLMBlueprint.route("/Translate", methods = ["POST"])
def Translate():
    try:

        requestData = request.json
        language = requestData.get("language", "English")  # 目标语言
        content = requestData["content"]  # 待润色文本内容
        scene = requestData.get("scene", "General")  # 润色情境
        response = LLMInterface.Translate(Tartext = content,
                                          Tarlanguage = language,
                                          Scene = scene)
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": response
        }
        logging.info(f"[{curTime}]Translate successed.")
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Translate]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 翻译功能接口
@LLMBlueprint.route("/TranslateStream", methods = ["POST"])
def TranslateStream():
    try:

        requestData = request.json
        language = requestData.get("language", "English")  # 目标语言
        content = requestData["content"]  # 待润色文本内容
        scene = requestData.get("scene", "General")  # 润色情境
        responseStream = LLMInterface.TranslateStream(Tartext = content,
                                                      Tarlanguage = language,
                                                      Scene = scene)
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]Translate_Stream successed.")
        return Response(stream_with_context(responseStream))

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[TranslateStream]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 总结功能接口
@LLMBlueprint.route("/Summary", methods = ["POST"])
def Summary():
    try:
        requestData = request.json
        content = requestData["content"]  # 待润色文本内容
        scene = requestData.get("scene", "General")

        response = LLMInterface.Summary(Tartext = content,
                                        Scene = scene)
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": response
        }
        logging.info(f"[{curTime}]Summary successed.")
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Summary]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 总结功能接口，返回迭代器
@LLMBlueprint.route("/SummaryStream", methods = ["POST"])
def SummaryStream():
    try:
        requestData = request.json
        content = requestData["content"]  # 待润色文本内容
        scene = requestData.get("scene", "General")

        responseStream = LLMInterface.SummaryStream(Tartext = content,
                                                    Scene = scene)
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]Summary_Stream successed.")
        return Response(stream_with_context(responseStream))

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[SummaryStream]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 润色功能接口
@LLMBlueprint.route("/Polish", methods = ["POST"])
def Polish():
    try:
        requestData = request.json
        content = requestData["content"]  # 待润色文本内容
        scene = requestData.get("scene", "General")

        response = LLMInterface.Polish(Tartext = content,
                                       Scene = scene)
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": response
        }
        logging.info(f"[{curTime}]Polish successed.")
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Polish]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
    return jsonify(retObj)


# 润色功能接口，返回迭代器
@LLMBlueprint.route("/PolishStream", methods = ["POST"])
def PolishStream():
    try:
        requestData = request.json
        content = requestData["content"]  # 待润色文本内容
        scene = requestData.get("scene", "General")

        responseStream = LLMInterface.PolishStream(Tartext = content,
                                                   Scene = scene)
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]Polish successed.")
        return Response(stream_with_context(responseStream))

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Polish]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 纠错功能接口
@LLMBlueprint.route("/Correct", methods = ["POST"])
def Correct():
    try:
        requestData = request.json
        content = requestData["content"]  # 待润色文本内容
        scene = requestData.get("scene", "General")

        response = LLMInterface.Correct(Tartext = content,
                                        Scene = scene)
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": response
        }
        logging.info(f"[{curTime}]Correct successed.")
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Correct]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 纠错功能接口，返回迭代器
@LLMBlueprint.route("/CorrectStream", methods = ["POST"])
def CorrectStream():
    try:
        requestData = request.json
        content = requestData["content"]  # 待润色文本内容
        scene = requestData.get("scene", "General")

        responseStream = LLMInterface.CorrectStream(Tartext = content,
                                                    Scene = scene)
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]Correct_Stream successed.")
        return Response(stream_with_context(responseStream))

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[CorrectStream]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 知识库检查编辑器文本内容接口
@LLMBlueprint.route("/Check", methods = ["POST"])
def Check():
    try:
        requestData = request.json
        userContent = requestData["content"]
        userFileList = requestData.get("fileName", None)

        # 没传文件
        if userFileList is None:
            raise FileExistsError("Which file do you want to check?")

        # 限制文件数量
        if len(userFileList) > 5:
            raise FileNotFoundError("The number of files could not be more than 5.")

        knowledgeContent = ""
        # 获取知识库中txt
        for fileName in userFileList:
            rawName = Tools.GetFileName(fileName)
            TarName = rawName + '.txt'
            filePath = os.path.join(fileSavePath, TarName)
            # 文件不存在
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"File {fileName} does not exist.")

            tmpContent = FileProcess.ReadTxt(FilePath = filePath)
            knowledgeContent += tmpContent + "\n"

        response = LLMInterface.Check_String(Tartext = userContent,
                                             KnowledgeContent = knowledgeContent)
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": response
        }
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Check]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 知识库检查编辑器文本，返回迭代器
@LLMBlueprint.route("/CheckStream", methods = ["POST"])
def CheckStream():
    try:
        requestData = request.json
        userContent = requestData["content"]
        userFileList = requestData.get("fileName", None)

        # 没传文件
        if userFileList is None:
            raise FileExistsError("Which file do you want to check?")

        # 限制文件数量
        if len(userFileList) > 5:
            raise FileNotFoundError("The number of files could not be more than 5.")

        knowledgeContent = ""
        # 获取知识库中txt
        for fileName in userFileList:
            rawName = Tools.GetFileName(fileName)
            TarName = rawName + '.txt'
            filePath = os.path.join(fileSavePath, TarName)
            # 文件不存在
            if not os.path.exists(filePath):
                raise FileNotFoundError(f"File {fileName} does not exist.")

            tmpContent = FileProcess.ReadTxt(FilePath = filePath)
            knowledgeContent += tmpContent + "\n"

        responseStream = LLMInterface.CheckStream_String(Tartext = userContent,
                                                         KnowledgeContent = knowledgeContent)
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]Check_Stream successed.")
        return Response(stream_with_context(responseStream))

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[CheckStream]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 对话机器人功能接口
@LLMBlueprint.route("/ChatBot", methods = ["POST"])
def ChatBot():
    try:
        requestData = request.json
        content = requestData["content"]
        userId = requestData.get("userId", "user")
        userFileList = requestData.get("fileName", None)

        # 不传入文件情况下调用聊天机器人
        if userFileList is None:
            if userId not in bot.Parameter:
                prompt = GetPrompt().Data()["ScenePrompt_General"]["Agent"]
                content = prompt + content
            response = bot.GetResponse(content, userId)
            curTime = Tools.GetTime()
            retObj = {
                "statusCode": 1,
                "requestTime": curTime,
                "response": response
            }
            logging.info(f"[{curTime}]Chatbot request successed.")
            return jsonify(retObj)

        # 传入文件情况下调用机器人
        else:
            # 存在历史记录，所以不进行文件操作
            if userId in bot.Parameter:
                response = bot.GetResponse(content, userId)
                curTime = Tools.GetTime()
                retObj = {
                    "statusCode": 1,
                    "requestTime": curTime,
                    "response": response
                }
                logging.info(f"[{curTime}]Chatbot request successed.")
                return jsonify(retObj)

            # 不存在历史记录
            else:
                # 限制文件数量
                if len(userFileList) > 5:
                    raise ValueError("The number of files could not be more than 5.")

                # 获取知识库中txt
                knowledgeContent = ""
                for fileName in userFileList:
                    rawName = Tools.GetFileName(fileName)
                    tarName = rawName + '.txt'
                    filePath = os.path.join(fileSavePath, tarName)
                    # 文件不存在
                    if not os.path.exists(filePath):
                        raise FileNotFoundError(f"File {fileName} does not exist.")

                    tmpContent = FileProcess.ReadTxt(FilePath = filePath)
                    knowledgeContent += tmpContent + "\n"

                # 限制Token数
                if len(knowledgeContent) > 3000:
                    knowledgeContent = knowledgeContent[:3000]
                bot.LoadKnowledgeLib_String(KnowledgeText = knowledgeContent,
                                            UserId = userId)

                response = bot.GetResponse(content, userId)
                curTime = Tools.GetTime()
                retObj = {
                    "statusCode": 1,
                    "requestTime": curTime,
                    "response": response
                }
                return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[ChatBot]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 对话机器人功能接口，返回迭代器
@LLMBlueprint.route("/ChatBotStream", methods = ["POST"])
def ChatBotStream():
    try:
        requestData = request.json
        content = requestData["content"]
        userId = requestData.get("userId", "user")
        userFileList = requestData.get("fileName", None)

        # 不传入文件情况下调用聊天机器人
        if userFileList is None:
            if userId not in bot.Parameter:
                prompt = GetPrompt().Data()["ScenePrompt_General"]["Agent"]
                content = prompt + content
            responseStream = bot.GetResponseStream(content, userId)
            curTime = Tools.GetTime()
            logging.info(f"[{curTime}]ChatbotStream request successed.")
            return Response(stream_with_context(responseStream))

        # 传入文件情况下调用机器人
        else:
            # 存在历史记录，所以不进行文件操作
            if userId in bot.Parameter:
                responseStream = bot.GetResponseStream(content, userId)
                curTime = Tools.GetTime()
                logging.info(f"[{curTime}]ChatbotStream request successed.")

            # 不存在历史记录
            else:
                # 限制文件数量
                if len(userFileList) > 5:
                    raise ValueError("The number of files could not be more than 5.")

                knowledgeContent = ""
                # 获取知识库中txt
                for fileName in userFileList:
                    rawName = Tools.GetFileName(fileName)
                    TarName = rawName + '.txt'
                    filePath = os.path.join(fileSavePath, TarName)
                    # 文件不存在
                    if not os.path.exists(filePath):
                        raise FileNotFoundError(f"File {fileName} does not exist.")

                    tmpContent = FileProcess.ReadTxt(FilePath = filePath)
                    knowledgeContent += tmpContent + "\n"

                # 限制Token数
                if len(knowledgeContent) > 3000:
                    knowledgeContent = knowledgeContent[:3000]

                bot.LoadKnowledgeLib_String(KnowledgeText = knowledgeContent,
                                            UserId = userId)
                responseStream = bot.GetResponseStream(content, userId)
                curTime = Tools.GetTime()
                logging.info(f"[{curTime}]ChatbotStream request successed.")
                return Response(stream_with_context(responseStream))

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[ChatBotStream]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 清除机器人对话历史记录
@LLMBlueprint.route("/ClearBotHistory", methods = ["POST"])
def ClearBotHistory():
    try:
        requestData = request.json
        userId = requestData.get("userId", "user")
        bot.ClearHistory(userId)
        curTime = Tools.GetTime()
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": f"Successfully clear Bot history, userId = {userId}"
        }
        return jsonify(retObj)

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[ClearBotHistory]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 格式化文本生成接口
@LLMBlueprint.route("/TextGen", methods = ["POST"])
def TextGen():
    try:
        # 获取请求数据
        requestData = request.json
        userContent = requestData["content"]
        PromptFile = requestData["template"]
        materialFileList = requestData.get("materialFiles", None)
        sepLib = "####知识库内容####\n"
        sepContent = "####用户输入文本####\n"
        knowledgeContent = ""

        # 传入素材文件
        if materialFileList is not None:
            # 限制文件数量
            if len(materialFileList) > 5:
                raise ValueError("The number of files could not be more than 5.")

            # 获取知识库文本
            for fileName in materialFileList:
                rawName = Tools.GetFileName(fileName)
                txtName = rawName + ".txt"
                filePath = os.path.join(fileSavePath, txtName)
                # 文件不存在
                if not os.path.exists(filePath):
                    raise FileNotFoundError(f"File [{fileName}] dose not exist.")
                knowledgeContent += FileProcess.ReadTxt(filePath) + "\n"

            # 限制Token数
            if len(knowledgeContent) > 3500:
                knowledgeContent = knowledgeContent[:3500]

        # 获取文本生成提示词
        rawName = Tools.GetFileName(PromptFile)
        txtFileName = rawName + ".txt"
        filePath = os.path.join(resourceSavePath, txtFileName)
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"Template [{rawName}] dose not exist.")
        prompt = FileProcess.ReadTxt(filePath)
        prompt += sepLib + knowledgeContent + sepContent + userContent

        response = LLMInterface.GetResponse_String(prompt)

        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]TextGen request successed.")
        retObj = {
            "statusCode": 1,
            "requestTime": curTime,
            "response": response
        }
        return retObj

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Textgen]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 格式化文本生成接口，返回迭代器
@LLMBlueprint.route("/TextGenStream", methods = ["POST"])
def TextGenStream():
    try:
        # 获取请求数据
        requestData = request.json
        userContent = requestData["content"]
        PromptFile = requestData["template"]
        materialFileList = requestData.get("materialFiles", None)
        sepLib = "####知识库内容####\n"
        sepContent = "####用户输入文本####\n"
        knowledgeContent = ""

        # 传入素材文件
        if materialFileList is not None:
            # 限制文件数量
            if len(materialFileList) > 5:
                raise ValueError("The number of files could not be more than 5.")

            # 获取知识库文本
            for fileName in materialFileList:
                rawName = Tools.GetFileName(fileName)
                txtName = rawName + ".txt"
                filePath = os.path.join(fileSavePath, txtName)
                # 文件不存在
                if not os.path.exists(filePath):
                    raise FileNotFoundError(f"File [{fileName}] dose not exist.")
                knowledgeContent += FileProcess.ReadTxt(filePath) + "\n"

            # 限制Token数
            if len(knowledgeContent) > 3500:
                knowledgeContent = knowledgeContent[:3500]

        # 获取文本生成提示词
        rawName = Tools.GetFileName(PromptFile)
        txtFileName = rawName + ".txt"
        filePath = os.path.join(resourceSavePath, txtFileName)
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"Template [{rawName}] dose not exist.")
        prompt = FileProcess.ReadTxt(filePath)
        prompt += sepLib + knowledgeContent + sepContent + userContent

        responseStream = LLMInterface.GetResponseStream_String(prompt)

        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]TextGen_Stream request successed.")
        return Response(stream_with_context(responseStream))

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[TextgenStream]" + str(e))
        retObj = {
            "statusCode": 0,
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)
