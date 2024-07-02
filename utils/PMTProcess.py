from utils.HeadFiles import *
from utils.FileProcess import *


class GetPrompt:  # 获取Prompt的单例模式类

    instance = None  # 存储实例
    data = None  # 存储数据

    def __new__(cls, *args, **kwargs):  # 创建实例
        if not cls.instance:
            cls.instance = super(GetPrompt, cls).__new__(cls, *args, **kwargs)
            with open("Prompts.json", "r", encoding="utf-8") as f:
                cls.data = json.load(f)
        return cls.instance

    def Data(self):
        return self.data


class KnowledgeLib:

    @staticmethod
    def InitLib(KnowledgeText):  # 载入用户知识库，传入知识库字符串返回初始化后的列表

        prompt = GetPrompt().Data()["FunctionPrompt"]["InputKnowledge"]
        prompt += KnowledgeText
        parameter = [{"role": "user", "content": prompt},
                     {"role": "assistant", "content": "明白"}]
        return parameter
