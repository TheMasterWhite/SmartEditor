from utils.Config.PMTProcess import *
from utils.LModel.Interface import LLMBasic
from utils.Config.FileProcess import *
import copy, erniebot, json


class BotBasic():  # 聊天机器人基本接口

    def __init__(self):
        self.Parameter = {}  # 初始化存储记录的空列表


    def AddMessage(self, Role, content, UserId):
        if UserId not in self.Parameter:
            self.Parameter[UserId] = []

        # 向对象添加交互内容，如果添加的是用户信息则会返回结果，否则返回Lambda表达式
        self.Parameter[UserId].append({"role": Role, "content": content})


        def GetResponseOrAdd():  # 判断添加聊天记录还是发送请求函数
            if Role == "user":
                # 控制对话轮数在25轮内
                if len(self.Parameter[UserId]) >= 50:
                    del self.Parameter[UserId][2]
                    del self.Parameter[UserId][3]
                return LLMBasic.GetResponse_List(self.Parameter[UserId])
            else:
                return lambda Content: self.AddMessage(Role, Content, UserId)


        return GetResponseOrAdd()


    def AddMessageStream(self, Role, content, UserId):
        if UserId not in self.Parameter:
            self.Parameter[UserId] = []
        # 与上条函数相似，返回迭代器
        self.Parameter[UserId].append({"role": Role, "content": content})


        def GetResponseOrAdd():
            if Role == "user":
                if len(self.Parameter[UserId]) >= 30:
                    del self.Parameter[UserId][2]
                    del self.Parameter[UserId][3]
                for i in LLMBasic.GetResponseStream_List(self.Parameter[UserId]):
                    yield i
            else:
                return lambda Content: self.AddMessageStream(Role, Content, UserId)


        return GetResponseOrAdd()


# 聊天机器人功能接口类
class BotInterface(BotBasic):

    def __init__(self):
        super().__init__()


    # 获取机器人问答结果，传入内容
    def GetResponse(self, Content, UserId):
        try:
            result = self.AddMessage("user", Content, UserId)
            self.AddMessage("assistant", result, UserId)
            return result
        except Exception as e:
            raise e


    # 流式获取机器人回复内容，传入输入内容返回迭代器
    def GetResponseStream(self, Content, UserId):
        try:

            tmp = ""
            result = self.AddMessageStream("user", Content, UserId)
            for i in result:
                tmp += i
                yield i
            self.AddMessageStream("assistant", tmp, UserId)
        except Exception as e:
            raise e


    # 载入知识库，传入知识库文本
    def LoadKnowledgeLib_String(self, KnowledgeText, UserId):
        try:
            InitedList = KnowledgeLib.InitList_String(KnowledgeText)
            self.Parameter[UserId] = InitedList
        except Exception as e:
            raise e


    # 载入知识库，传入知识库路径
    def LoadKnowledgeLib_Path(self, KnowledgePath, UserId):
        try:
            initedUserId = "Lib" + UserId
            InitedList = KnowledgeLib.InitList_Path(KnowledgePath)
            self.Parameter[initedUserId] = InitedList
        except Exception as e:
            raise e


    # 清除对话历史记录
    def ClearHistory(self, UserId):
        self.Parameter[UserId] = []


# 实例化一个全局对象
bot = BotInterface()
