from utils.Config.PMTProcess import *


class STTBasic:  # 小模型应用接口类

    @staticmethod
    def GetAccessToken():  # 百度智能云获取access_token

        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": GLOBAL_Baidu_AK, "client_secret": GLOBAL_Baidu_SK}
        return str(requests.post(url, params = params).json().get("access_token"))


    @staticmethod
    def CreateTask(FilePath, FileExtension, Language = "Chinese"):  # 创建音频转写任务

        try:
            absPath = FileProcess.AbsPath(FilePath)
            # 将文件上传到阿里云并获取外链
            ossPath = OSSProcess.UploadFile(absPath, FileExtension)
            creatUrl = "https://aip.baidubce.com/rpc/2.0/aasr/v1/create?access_token=" + STTBasic.GetAccessToken()
            code = {"Chinese": 80006, "English": 1737}
            # 请求头
            payload = json.dumps({
                "speech_url": ossPath,
                "format": FileExtension,
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
            return taskID

        except Exception as e:
            raise e


    @staticmethod
    def QueryTask(TaskID):  # 获取音频转写任务结果

        queryUrl = "https://aip.baidubce.com/rpc/2.0/aasr/v1/query?access_token=" + STTBasic.GetAccessToken()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        quertPayload = json.dumps({"task_ids": [TaskID]})
        while (1):
            queryResponse = requests.request("POST", queryUrl, headers = headers, data = quertPayload)
            queryData = queryResponse.json()
            # 获取状态
            status = queryData['tasks_info'][0]['task_status']

            if (status == "Success"):
                return queryData
            elif (status == "Failed"):
                raise Exception("Failed!")


class STTInterface(STTBasic):

    @staticmethod
    def GetResult(FilePath, FileExtension, Language = "Chinese", SavePath = "Saves/SttResult"):  # 获取语音转文字结果，返回String

        try:
            createTaskId = super(STTInterface, STTInterface).CreateTask(FilePath, FileExtension, Language)
            response = super(STTInterface, STTInterface).QueryTask(createTaskId)
            JsonOperator.Save(response, SavePath, "Result")
            return response['tasks_info'][0]['task_result']['result'][0]

        except Exception as e:
            raise e


def test():
    pass


if __name__ == '__main__':
    test()
