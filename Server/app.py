import Tools, logging, json
from flask import Flask, request, jsonify
from wsgiref.simple_server import WSGIServer
from utils.LModel.Interface import LLMInterface

# 获取app.py的绝对路径
appPath = os.path.abspath(__file__)

# 获取app.py所在的目录
appDir = os.path.dirname(appPath)

# 获取项目根目录（假设Server是根目录的一个子目录）
rootPath = os.path.join(appDir, os.path.pardir)

# 将项目根目录添加到sys.path中
sys.path.append(rootPath)

app = Flask(__name__)
logging.basicConfig(filename = "Log.log",
                    filemode = 'a',
                    level = logging.INFO)


# 翻译功能接口
@app.route("/LLMInterface/Translate", methods = ["POST"])
def Translate():
    try:

        requestData = request.json
        language = requestData.get("language", "English")  # 目标语言
        content = requestData["content"]  # 待润色文本内容
        scene = requestData.get("scene", "General")  # 润色情境
        logging.info("reeive")
        response = LLMInterface.Translate(Tartext = "生活就像海洋，只有意志坚强的人才能到达彼岸。",
                                          Tarlanguage = language,
                                          Scene = scene)
        logging.info("6666")
        curTime = Tools.GetTime()
        retObj = {
            "status": "success",
            "requestTime": curTime,
            "response": response
        }
        logging.info(f"[{curTime}]Translate successed.")

    except Exception as e:
        curTime = Tools.GetTime()
        logging.error(f"[{curTime}]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
        return jsonify(retObj)


# 总结功能接口
@app.route("/LLMInterface/Summary", methods = ["POST"])
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
        logging.error(f"[{curTime}]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
        return jsonify(retObj)


# 润色功能接口
@app.route("/LLMInterface/Polish", methods = ["POST"])
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
        logging.error(f"[{curTime}]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
        return jsonify(retObj)


# 总结功能接口
@app.route("/LLMInterface/Correct", methods = ["POST"])
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
        logging.error(f"[{curTime}]" + str(e))
        retObj = {
            "status": "failed",
            "requestTime": curTime,
            "response": str(e)
        }

    finally:
        return jsonify(retObj)


def StartServer():
    app.run(host = "0.0.0.0", port = 8888)
    curTime = Tools.GetTime()
    logging.info(f"[{curTime}]Server Started!")


if __name__ == "__main__":
    StartServer()
