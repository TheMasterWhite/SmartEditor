from utils.HeadFiles import *
from utils.FileProcess import *

prevmsg = []

class LModel:  # 大模型处理类

    @staticmethod
    def GetResponse_String(Prompt):  # 获取推理结果，传入字符串，返回String
        try:
            Parameter = [{"role": "user", "content": Prompt}]
            Response = erniebot.ChatCompletion.create(
                model="ernie-4.0",
                messages=Parameter
            )
            return Response.get_result()
        except Exception as e:
            return str(e)


    @staticmethod
    def GetResponseStream_String(Prompt):  # 流式获取推理结果，传入字符串，返回迭代器
        try:
            Parameter = [{"role": "user", "content": Prompt}]
            Response = erniebot.ChatCompletion.create(
                model="ernie-4.0",
                messages=Parameter,
                stream=True
            )
            for i in Response:
                yield i
        except Exception as e:
                return str(e)

    @staticmethod
    def GetResponse_List(ListPrompt):  # 获取推理结果，传入List，返回String
        try:
            Response = erniebot.ChatCompletion.create(
                model="ernie-4.0",
                messages=ListPrompt,
            )
            return Response.get_result()
        except Exception as e:
            return str(e)

    @staticmethod
    def GetResponseStream_List(ListPrompt):  # 流式获取推理结果，传入List，返回迭代器
        try:
            Response = erniebot.ChatCompletion.create(
                model="ernie-4.0",
                messages=ListPrompt,
                stream=True
            )
            for i in Response.get_result():
                yield i
        except Exception as e:
                return str(e)

    @staticmethod
    def Translate(Tartext, LanCode=2):  # Tartext传入翻译目标字符串，TarLanguage传入int型目标语言代号,返回String

        try:
            AbsPromptPath = FileProcess.AbsPath(Global_TranslationPath)
            Prompt = FileProcess.ReadTxt(AbsPromptPath)
            Code = {1: "中文", 2: "英语", 3: "日语", 4: "俄语", 5: "法语"}
            TarLanguage = Code.get(LanCode, "ErrorCode")

            if TarLanguage == "ErrorCode":
                return "Invalid Language Code!"

            Prompt = Prompt.replace("@Replace@", TarLanguage)
            Prompt += Tartext

            return LModel.GetResponse_String(Prompt)
        except Exception as e:
            return str(e)


    @staticmethod
    def Summary(Tartext):  # 精炼语言，传入目标句子，返回String
        try:
            AbsPromptPath = FileProcess.AbsPath(Global_SummaryPath)
            Prompt = FileProcess.ReadTxt(AbsPromptPath)
            Prompt += Tartext
            return LModel.GetResponse_String(Prompt)
        except Exception as e:
            return str(e)

    @staticmethod
    def Correct(Tartext):  # 句子纠错，Tartext传入目标字符串，OpeartionCode传入操作代码(int),返回String

        try:
            AbsPromptPath = FileProcess.AbsPath(Global_CorrectPath)
            Prompt = FileProcess.ReadTxt(AbsPromptPath)
            Prompt += Tartext
            return LModel.GetResponse_String(Prompt)
        except Exception as e:
            return str(e)

    @staticmethod
    def Polish(Tartext):  # 文章润色
        try:
            AbsPromptPath = FileProcess.AbsPath(Global_PolishPath)
            Prompt = FileProcess.ReadTxt(AbsPromptPath)
            Prompt += Tartext
            return LModel.GetResponse_String(Prompt)
        except Exception as e:
            return str(e)

    @staticmethod
    def AgentInit():  # 初始化聊天助手
        Prompt = FileProcess.ReadTxt(AgentURL)
        Dialogue = [{
            "role": "user",
            "content": Prompt
        }]
        Result = LModel.GetResponse_List(Dialogue)
        Dialogue.append({
            "role": "assistant",
            "content": Result
        })
        return Dialogue

def Test():
    LModel.GetResponse_String("我是一只雪狐！我要吃浆果！")

if __name__ == '__main__':
    Test()
