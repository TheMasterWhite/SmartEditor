from utils.Config.PMTProcess import *
from utils.Config.HeadFiles import *
from utils.LModel.Interface import LLMBasic
from utils.Config.FileProcess import *


class BotBasic():  # 聊天机器人基本接口

    def __init__(self):
        self.Parameter = []  # 初始化存储记录的空列表


    def AddMessage(self, role, content):
        # 向对象添加交互内容，如果添加的是用户信息则会返回结果，否则返回Lambda表达式
        self.Parameter.append({"role": role, "content": content})


        def GetResponseOrAdd():  # 判断添加聊天记录还是发送请求函数
            if role == "user":
                return LLMBasic.GetResponse_List(self.Parameter)
            else:
                return lambda content: self.AddMessage(role, content)


        return GetResponseOrAdd()


    def AddMessageStream(self, role, content):
        # 与上条函数相似，返回迭代器
        self.Parameter.append({"role": role, "content": content})


        def GetResponseOrAdd():
            if role == "user":
                for i in LLMBasic.GetResponseStream_List(self.Parameter):
                    yield i
            else:
                return lambda content: self.AddMessageStream(role, content)


        return GetResponseOrAdd()


class BotInterface(BotBasic):  # 聊天机器人功能接口类

    def __init__(self):
        super().__init__()


    def GetResponse(self, Content):  # 获取机器人问答结果，传入内容
        result = self.AddMessage("user", Content)
        self.AddMessage("assistant", result)
        return result


    def GetResponseStream(self, Content):
        # 流式获取机器人回复内容，传入输入内容返回迭代器
        tmp = ""
        result = self.AddMessageStream("user", Content)
        for i in result:
            tmp += i
            yield i
        self.AddMessage("assistant", tmp)


    def LoadKnowledgeLib_String(self, KnowledgeText):  # 载入知识库，传入知识库文本
        InitedList = KnowledgeLib.InitList_String(KnowledgeText)
        self.Parameter += InitedList


    def LoadKnowledgeLib_Path(self, KnowledgePath):  # 载入知识库，传入知识库路径
        InitedList = KnowledgeLib.InitList_Path(KnowledgePath)
        self.Parameter += InitedList


    def ClearHistory(self):  # 清除历史记录
        self.Parameter = []


if __name__ == '__main__':
    bot = BotInterface()