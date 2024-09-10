import logging, json, os, sys, requests
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from wsgiref.simple_server import WSGIServer
from Config import *
from LLMRoute import LLMBlueprint
from SModelRoute import SModelBlueprint
from ServerProcess import ServerProcessBlueprint
from utils.SModel.STT import TaskThread, SModelBlueprint
from utils import Tools

app = Flask(__name__)
QuerySTTThread = TaskThread()
QuerySTTThread.start()
CORS(app, resources = {r"/*": {"origins": "*"}})

logging.basicConfig(filename = "Server/Log.log",
                    filemode = 'a',
                    level = logging.INFO)

# 大模型注册蓝图
app.register_blueprint(LLMBlueprint)
# OCR注册蓝图
app.register_blueprint(SModelBlueprint)
# 服务业务注册蓝图
app.register_blueprint(ServerProcessBlueprint)


def StartServer():
    curTime = Tools.GetTime()
    logging.info(f"[{curTime}]Server Started!")
    app.run(host = "0.0.0.0", port = 8888)


if __name__ == "__main__":
    StartServer()
