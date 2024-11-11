from Config import *
from utils import Tools
import queue, threading, time, logging
from threading import Thread
from utils.Config.FileProcess import *
from utils.LModel.Interface import *


def GetAccessToken():  # 百度智能云获取access_token
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": GLOBAL_Baidu_AK, "client_secret": GLOBAL_Baidu_SK}
    token = str(requests.post(url, params = params).json().get("access_token"))
    print(token)
    return token


class TaskThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.taskQueue = queue.Queue()
        self.fileInfoDict = {}
        curTime = Tools.GetTime()
        logging.info(f"[{curTime}]TaskThread Started.")


    # 获取音频转写任务结果
    def QueryTask(self, TaskId):
        queryUrl = "https://aip.baidubce.com/rpc/2.0/aasr/v1/query?access_token=" + GetAccessToken()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {"task_ids": [TaskId]}
        queryResponse = requests.request("POST", queryUrl, headers = headers, data = json.dumps(data))
        queryData = queryResponse.json()
        return queryData


    # 轮询任务列表
    def run(self):
        while True:
            if self.taskQueue.empty():
                time.sleep(2)
                continue
            else:
                time.sleep(1)

            taskId = self.taskQueue.get()
            responseData = self.QueryTask(taskId)
            status = responseData["tasks_info"][0]["task_status"]

            if (status == "Success"):
                fullFileName = self.fileInfoDict[taskId]["fileName"]  # 多媒体文件名
                userName = self.fileInfoDict[taskId]["userName"]
                fileUUID = self.fileInfoDict[taskId]["UUID"]  # 文件UUID
                content = responseData["tasks_info"][0]["task_result"]["result"][0]
                # 保存结果到txt
                FileProcess.SaveTxt(UUID = fileUUID,
                                    Content = content,
                                    UserName = userName)
                curTime = Tools.GetTime()
                logging.info(f"[{curTime}]Receive STT result successfully.")
                # 将文件信息保存到数据库中
                summaryText = LLMInterface.FileSummary(content)
                saveTime = Tools.GetSaveTime()
                FileProcess.SaveFileInfo(FileName = fullFileName,
                                         Description = summaryText,
                                         SaveTime = saveTime,
                                         UserName = userName,
                                         UUID = fileUUID)
                del self.fileInfoDict[taskId]

            elif (status == "Failed"):
                curTime = Tools.GetTime()
                errorMsg = responseData["tasks_info"][0]["task_result"]["err_msg"]
                logging.info(f"[{curTime}]STT task failed : {errorMsg}.")

            elif (status == "Running"):
                self.taskQueue.put(taskId)


    # 添加轮询任务id
    def PutTaskId(self, FileName, TaskId, UserName, UUID):
        self.taskQueue.put(TaskId)
        self.fileInfoDict[TaskId] = {
            "fileName": FileName,
            "userName": UserName,
            "UUID": UUID
        }
