from flask import Flask, Blueprint, request, jsonify
from utils import Tools
from werkzeug.utils import secure_filename
import os

ServerProcessBlueprint = Blueprint("ServerProcessBlueprint", __name__, url_prefix = "/ServerProcess")


# 从前端接收文件接口
@ServerProcessBlueprint.route("/UploadFile", methods = ["POST"])
def UploadFile():
    try:
        curTime = Tools.GetTime()
        # 请求中不存在文件
        if "file" not in request.files:
            raise Exception("No file in the request.")

        # 获取文件并保存
        file = request.files["file"]
        fileName = secure_filename(file.filename)
        file.save(os.path.join(GLOBAL_UploadFileFolder, fileName))

        retObj = {
            "status": "success",
            "requestTime": curTime,
            "response": "File uploaded successfully"
        }

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]Module:[UploadFile]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
        return jsonify(retObj)
