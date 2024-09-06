import logging, json, os, sys
from flask import Flask, request, jsonify, Response, stream_with_context, Blueprint
from utils.LModel.Interface import LLMInterface
from utils.LModel.ChatBot import BotInterface
from utils import Tools

LLMBlueprint = Blueprint("LLMBlueprint", __name__, url_prefix = '/LLMInterface')


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
            "status": "success",
            "requestTime": curTime,
            "response": response
        }
        logging.info(f"[{curTime}]Translate successed.")

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Translate]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
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
            "status": "failed",
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
            "status": "success",
            "requestTime": curTime,
            "response": response
        }
        logging.info(f"[{curTime}]Summary successed.")

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Summary]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
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
            "status": "failed",
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
            "status": "success",
            "requestTime": curTime,
            "response": response
        }
        logging.info(f"[{curTime}]Polish successed.")

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Polish]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
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
            "status": "failed",
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
            "status": "success",
            "requestTime": curTime,
            "response": response
        }
        logging.info(f"[{curTime}]Correct successed.")

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[Correct]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
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
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }
        return jsonify(retObj)


# 对话机器人功能接口
@LLMBlueprint.route("/ChatBot", methods = ["POST"])
def ChatBot():
    try:
        bot = BotInterface()
        requestData = request.json
        content = requestData["content"]
        userId = requestData.get("userId", "user")

        response = bot.GetResponse(content, userId)
        curTime = Tools.GetTime()
        retObj = {
            "status": "success",
            "requestTime": curTime,
            "response": response
        }
        logging.info(f"[{curTime}]Chatbot request successed.")

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[ChatBot]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
        return jsonify(retObj)


# 对话机器人功能接口，返回迭代器
@LLMBlueprint.route("/ChatBotStream", methods = ["POST"])
def ChatBotStream():
    try:
        bot = BotInterface()
        requestData = request.json
        content = requestData["content"]
        userId = requestData.get("userId", "user")

        responseStream = bot.GetResponseStream(content, userId)
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]ChatbotStream request successed.")



    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[ChatBotStream]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }
