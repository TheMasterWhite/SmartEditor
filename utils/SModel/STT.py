from utils.Config.PMTProcess import *
from Config import *
from utils import Tools
import queue, threading, time, logging
from utils.SModel.TaskThread import *

fileSavePath = copy.deepcopy(GLOBAL_FileSavePath)

QuerySTTThread = TaskThread()
QuerySTTThread.start()


class STTInterface:  # 小模型应用接口类

    # 创建音频转写任务
    @staticmethod
    def CreateTask(FullFileName, Language = "Chinese"):

        try:
            fileExtension = Tools.GetExtension(FullFileName)
            fileName = Tools.GetFileName(FullFileName)
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


    @staticmethod
    def MainProcess(FullFileName, UserName, UUID, Language = "Chinese"):
        try:
            fileExtension = Tools.GetExtension(FullFileName)
            fileName = Tools.GetFileName(FullFileName)

            # 视频文件转wav再STT处理
            if fileExtension in ["mp4"]:
                FileProcess.ConvertToWav(UUID = UUID,
                                         FileExtension = fileExtension,
                                         UserName = UserName)
                # 发起STT服务调用
                fileName_Wav = os.path.join(fileSavePath, UserName, UUID + ".wav")
                taskId = STTInterface.CreateTask(FullFileName = fileName_Wav,
                                                 Language = Language)
                # 加入轮询队列
                QuerySTTThread.PutTaskId(FileName = FullFileName,
                                         TaskId = taskId,
                                         UserName = UserName,
                                         UUID = UUID)

            # 音频文件，直接转文字处理
            elif fileExtension in ["wav", "mp3", "pcm", "m4a", "amr"]:
                # 发起STT服务调用
                taskId = STTInterface.CreateTask(FullFileName = FullFileName,
                                                 Language = Language)
                # 加入轮询队列
                QuerySTTThread.PutTaskId(FileName = FullFileName,
                                         TaskId = taskId,
                                         UserName = UserName)

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[STT_MainProcess]" + str(e))
