from utils.Config.PMTProcess import GetPrompt, KnowledgeLib
from utils.Config.HeadFiles import *
from utils.Config.FileProcess import FileProcess, OSSProcess, JsonOperator


class LLMBasic:  # 大模型基本通信接口类

    @staticmethod
    def GetResponse_String(Prompt):  # 获取推理结果，传入字符串，返回String

        try:
            Parameter = [{"role": "user", "content": Prompt}]
            Response = erniebot.ChatCompletion.create(
                model = "ernie-4.0",
                messages = Parameter
            )
            return Response.get_result()

        except Exception as e:
            raise e


    @staticmethod
    def GetResponseStream_String(Prompt):  # 流式获取推理结果，传入字符串，返回迭代器

        try:
            Parameter = [{"role": "user", "content": Prompt}]
            Response = erniebot.ChatCompletion.create(
                model = "ernie-4.0",
                messages = Parameter,
                stream = True
            )
            for i in Response:
                yield i.get_result()

        except Exception as e:
            raise e


    @staticmethod
    def GetResponse_List(ListPrompt):  # 获取推理结果，传入List，返回String

        try:
            Response = erniebot.ChatCompletion.create(
                model = "ernie-4.0",
                messages = ListPrompt,
            )
            return Response.get_result()

        except Exception as e:
            raise e


    @staticmethod
    def GetResponseStream_List(ListPrompt):  # 流式获取推理结果，传入List，返回迭代器

        try:
            Response = erniebot.ChatCompletion.create(
                model = "ernie-4.0",
                messages = ListPrompt,
                stream = True
            )
            for i in Response:
                yield i.get_result()

        except Exception as e:
            raise e


class LLMInterface(LLMBasic):  # 大模型高级功能接口类

    @staticmethod
    def Translate(Tartext, Tarlanguage = "英语",
                  Scene = "General"):  # 翻译，Tartext传入翻译目标字符串，TarLanguage传入目标语言,返回String

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Translate"]
            prompt = prompt.replace("@Replace@", Tarlanguage)
            prompt += Tartext
            return LLMBasic.GetResponse_String(prompt)

        except Exception as e:
            raise e


    @staticmethod
    def TranslateStream(Tartext, Tarlanguage = "英语",
                        Scene = "General"):  # 翻译，Tartext传入翻译目标字符串，TarLanguage传入目标语言,返回迭代器

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Translate"]
            prompt = prompt.replace("@Replace@", Tarlanguage)
            prompt += Tartext
            for i in LLMBasic.GetResponseStream_String(prompt):
                yield i

        except Exception as e:
            raise e


    @staticmethod
    def Summary(Tartext, Scene = "General"):  # 精炼语言，，Tartext传入目标字符串,返回String

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Summary"]
            prompt += Tartext
            return LLMBasic.GetResponse_String(prompt)

        except Exception as e:
            raise e


    @staticmethod
    def SummaryStream(Tartext, Scene = "General"):  # 精炼语言，，Tartext传入目标字符串,返回迭代器

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Summary"]
            prompt += Tartext
            for i in LLMBasic.GetResponseStream_String(prompt):
                yield i

        except Exception as e:
            raise e


    @staticmethod
    def Correct(Tartext, Scene = "General"):  # 句子纠错，Tartext传入目标字符串,返回String

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Correct"]
            prompt += Tartext
            return LLMBasic.GetResponse_String(prompt)

        except Exception as e:
            raise e


    @staticmethod
    def CorrectStream(Tartext, Scene = "General"):  # 句子纠错，Tartext传入目标字符串,返回迭代器

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Correct"]
            prompt += Tartext
            for i in LLMBasic.GetResponseStream_String(prompt):
                yield i

        except Exception as e:
            raise e


    @staticmethod
    def Polish(Tartext, Scene = "General"):  # 文章润色，Tartext传入目标字符串,返回String

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Polish"]
            prompt += Tartext
            return LLMBasic.GetResponse_String(prompt)

        except Exception as e:
            raise e


    @staticmethod
    def PolishStream(Tartext, Scene = "General"):  # 文章润色，Tartext传入目标字符串,返回迭代器

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Polish"]
            prompt += Tartext
            for i in LLMBasic.GetResponseStream_String(prompt):
                yield i

        except Exception as e:
            raise e


    @staticmethod
    def Check_String(Tartext, KnowledgeContent):  # 检查输入内容与知识库的差异，传入目标文本和用户知识库字符串

        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["Check"]
            promptText += Tartext
            initedList = KnowledgeLib.InitList_String(KnowledgeContent)
            initedList.append({"role": "user", "content": promptText})
            return LLMBasic.GetResponse_List(initedList)

        except Exception as e:
            raise e


    @staticmethod
    def CheckStream_String(Tartext, KnowledgeContent):  # 检查输入内容与知识库的差异，传入目标文本和用户知识库文本，返回迭代器

        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["Check"]
            promptText += Tartext
            initedList = KnowledgeLib.InitList_String(KnowledgeContent)
            initedList.append({"role": "user", "content": promptText})
            for i in LLMBasic.GetResponseStream_List(initedList):
                yield i

        except Exception as e:
            raise e


    @staticmethod
    def Check_List(Tartext, KnowledgeList):  # 检查输入内容与知识库的差异，传入目标文本和初始化之后的列表

        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["Check"]
            promptText += Tartext
            KnowledgeList.append({"role": "user", "content": promptText})
            return LLMBasic.GetResponse_List(KnowledgeList)

        except Exception as e:
            raise e


    @staticmethod
    def CheckStream_List(Tartext, KnowledgeList):  # 检查输入内容与知识库的差异，传入目标文本和初始化之后的列表，返回迭代器

        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["Check"]
            promptText += Tartext
            KnowledgeList.append({"role": "user", "content": promptText})
            for i in LLMBasic.GetResponseStream_List(KnowledgeList):
                yield i

        except Exception as e:
            raise e


def UnitTest():
    a = LLMBasic.GetResponse_String("我是雪狐！快夸我可爱！")


if __name__ == '__main__':
    pass
