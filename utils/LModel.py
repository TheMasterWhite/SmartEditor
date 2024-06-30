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
    def Translate(Tartext, Tarlanguage="英语"):  # Tartext传入翻译目标字符串，TarLanguage传入目标语言,返回String

        try:
            prompt = GetPrompt().Data()["FunctionPrompt"]["Translate"]
            prompt = prompt.replace("@Replace@", Tarlanguage)
            prompt += Tartext

            return LModel.GetResponse_String(prompt)
        except Exception as e:
            return str(e)

    @staticmethod
    def Summary(Tartext):  # 精炼语言，传入目标句子，返回String
        try:
            prompt = GetPrompt().Data()["FunctionPrompt"]["Summary"]
            prompt += Tartext
            return LModel.GetResponse_String(prompt)
        except Exception as e:
            return str(e)

    @staticmethod
    def Correct(Tartext):  # 句子纠错，Tartext传入目标字符串,返回String

        try:
            prompt = GetPrompt().Data()["FunctionPrompt"]["Correct"]
            prompt += Tartext
            return LModel.GetResponse_String(prompt)
        except Exception as e:
            return str(e)

    @staticmethod
    def Polish(Tartext):  # 文章润色
        try:
            prompt = GetPrompt().Data()["FunctionPrompt"]["Polish"]
            prompt += Tartext
            return LModel.GetResponse_String(prompt)
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


class LModel2:
    pass


def UnitTest():
    a = LModel.GetResponse_String("我是雪狐！快夸我可爱！")
    print(a)

if __name__ == '__main__':
    UnitTest()