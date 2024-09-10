from utils.Config.PMTProcess import *
from Config import *
from utils import Tools
import queue, threading, time, logging
from threading import Thread

fileSavePath = GLOBAL_FileSavePath
logging.basicConfig(filename = "Server/Log.log",
                    filemode = 'a',
                    level = logging.INFO)


def GetAccessToken():  # 百度智能云获取access_token

    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": GLOBAL_Baidu_AK, "client_secret": GLOBAL_Baidu_SK}
    return str(requests.post(url, params = params).json().get("access_token"))


class TaskThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.taskQueue = queue.Queue()
        self.fileIdList = {}
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]TaskThread Started.")


    # 获取音频转写任务结果
    def QueryTask(self, TaskId) -> bool:
        queryUrl = "https://aip.baidubce.com/rpc/2.0/aasr/v1/query?access_token=" + GetAccessToken()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {"task_ids": [TaskId]}
        queryResponse = requests.request("POST", queryUrl, headers = headers, data = json.dumps(data))
        queryData = queryResponse.json()
        # 获取状态
        return queryData


    # 轮询任务列表
    def run(self):
        while True:
            if self.taskQueue.empty():
                time.sleep(1)
                continue

            taskId = self.taskQueue.get()
            responseData = self.QueryTask(taskId)
            status = responseData["tasks_info"][0]["task_status"]

            if (status == "Success"):
                fullFileName = self.fileIdList[taskId]
                fileName = Tools.GetFileName(fullFileName)
                content = responseData["tasks_info"][0]["task_result"]["result"][0]
                # 保存结果到txt
                FileProcess.SaveTxt(fileName, content)
                curTime = Tools.GetTime()
                logging.info(f"[{curTime}]Receive STT result successfully.")
                del self.fileIdList[taskId]

            elif (status == "Failed"):
                curTime = Tools.GetTime()
                logging.info(f"[{curTime}]STT task failed.")

            elif (status == "Running"):
                self.taskQueue.put(taskId)


    # 添加轮询任务id
    def PutTaskId(self, FileName, TaskId):
        self.taskQueue.put(TaskId)
        self.fileIdList[TaskId] = FileName


class STTInterface:  # 小模型应用接口类

    # 创建音频转写任务
    @staticmethod
    def CreateTask(FileName, Language = "Chinese"):

        try:
            fileExtension = Tools.GetExtension(FileName)
            fileName = Tools.GetFileName(FileName)
            # 将文件上传到阿里云并获取外链
            ossPath = OSSProcess.UploadFile(FileName = fileName,
                                            FileExtension = fileExtension)
            creatUrl = "https://aip.baidubce.com/rpc/2.0/aasr/v1/create?access_token=" + GetAccessToken()
            code = {"Chinese": 80006, "English": 1737}
            # 请求头
            payload = json.dumps({
                "speech_url": ossPath,
                "format": "wav",
                "pid": code[Language],
                "rate": 16000,
            })
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            createResponse = requests.request("POST", creatUrl, headers = headers, data = payload)
            createResponseData = createResponse.json()
            # 获取TaskID
            taskID = createResponseData["task_id"]

            curTime = Tools.GetTime()
            logging.info(f"[{curTime}]Created STT Task successfully, ID = {taskID}.")
            return taskID

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[CreateTask]" + str(e))
