from utils.Config.FileProcess import FileProcess, OSSProcess, JsonOperator
from utils.Config.HeadFiles import *


class GetPrompt:  # 获取Prompt的单例模式类

    instance = None  # 存储实例
    data = None  # 存储数据


    def __new__(cls, *args, **kwargs):  # 创建实例
        if not cls.instance:
            cls.instance = super(GetPrompt, cls).__new__(cls, *args, **kwargs)
            absPath = FileProcess.AbsPath("utils/Config/Prompts.json")
            with open(absPath, "r", encoding = "utf-8") as f:
                cls.data = json.load(f)
        return cls.instance


    def Data(self):  # 返回存储Prompt的json字典
        return self.data


class KnowledgeLib:  # 用于维护用户知识库

    @staticmethod
    def InitList_String(KnowledgeText):  # 载入用户知识库，传入知识库字符串返回初始化后的列表

        prompt = GetPrompt().Data()["FunctionPrompt"]["InputKnowledge"]
        prompt += KnowledgeText
        parameter = [{"role": "user", "content": prompt},
                     {"role": "assistant", "content": "明白"}]

        return parameter


    @staticmethod
    def InitList_Path(KnowledgePath):  # 载入用户知识库，传入知识库文件路径返回初始化后的列表

        prompt = GetPrompt().Data()["FunctionPrompt"]["InputKnowledge"]
        absPath = FileProcess.AbsPath(KnowledgePath)
        print(absPath)
        content = FileProcess.ReadTxt(absPath)
        parameter = [{"role": "user", "content": content},
                     {"role": "assistant", "content": "明白"}]

        return parameter
    