from utils.Config.PMTProcess import GetPrompt, KnowledgeLib
from utils.Config.FileProcess import FileProcess, OSSProcess, JsonOperator
import erniebot


class LLMBasic:  # 大模型基本通信接口类

    # 获取推理结果，传入字符串，返回String
    @staticmethod
    def GetResponse_String(Prompt):

        try:
            Parameter = [{"role": "user", "content": Prompt}]
            Response = erniebot.ChatCompletion.create(
                model = "ernie-4.0",
                messages = Parameter
            )
            return Response.get_result()

        except Exception as e:
            raise e


    # 流式获取推理结果，传入字符串，返回迭代器
    @staticmethod
    def GetResponseStream_String(Prompt):

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


    # 获取推理结果，传入List，返回String
    @staticmethod
    def GetResponse_List(ListPrompt):

        try:
            Response = erniebot.ChatCompletion.create(
                model = "ernie-4.0",
                messages = ListPrompt,
            )
            return Response.get_result()

        except Exception as e:
            raise e


    # 流式获取推理结果，传入List，返回迭代器
    @staticmethod
    def GetResponseStream_List(ListPrompt):

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

    # 翻译，Tartext传入翻译目标字符串，TarLanguage传入目标语言,返回String
    @staticmethod
    def Translate(Tartext, Tarlanguage = "英语",
                  Scene = "General"):

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Translate"]
            prompt = prompt.replace("@Replace@", Tarlanguage)
            prompt += Tartext
            return LLMBasic.GetResponse_String(prompt)

        except Exception as e:
            raise e


    # 翻译，Tartext传入翻译目标字符串，TarLanguage传入目标语言,返回迭代器
    @staticmethod
    def TranslateStream(Tartext, Tarlanguage = "英语",
                        Scene = "General"):

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Translate"]
            prompt = prompt.replace("@Replace@", Tarlanguage)
            prompt += Tartext
            for i in LLMBasic.GetResponseStream_String(prompt):
                yield i

        except Exception as e:
            raise e


    # 精炼语言，，Tartext传入目标字符串,返回String
    @staticmethod
    def Summary(Tartext, Scene = "General"):

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Summary"]
            prompt += Tartext
            return LLMBasic.GetResponse_String(prompt)

        except Exception as e:
            raise e


    # 精炼语言，，Tartext传入目标字符串,返回迭代器
    @staticmethod
    def SummaryStream(Tartext, Scene = "General"):

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Summary"]
            prompt += Tartext
            for i in LLMBasic.GetResponseStream_String(prompt):
                yield i

        except Exception as e:
            raise e


    # 句子纠错，Tartext传入目标字符串,返回String
    @staticmethod
    def Correct(Tartext, Scene = "General"):

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Correct"]
            prompt += Tartext
            return LLMBasic.GetResponse_String(prompt)

        except Exception as e:
            raise e


    # 句子纠错，Tartext传入目标字符串,返回迭代器
    @staticmethod
    def CorrectStream(Tartext, Scene = "General"):

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Correct"]
            prompt += Tartext
            for i in LLMBasic.GetResponseStream_String(prompt):
                yield i

        except Exception as e:
            raise e


    # 文章润色，Tartext传入目标字符串,返回String
    @staticmethod
    def Polish(Tartext, Scene = "General"):

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Polish"]
            prompt += Tartext
            return LLMBasic.GetResponse_String(prompt)

        except Exception as e:
            raise e


    # 文章润色，Tartext传入目标字符串,返回迭代器
    @staticmethod
    def PolishStream(Tartext, Scene = "General"):

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Polish"]
            prompt += Tartext
            for i in LLMBasic.GetResponseStream_String(prompt):
                yield i

        except Exception as e:
            raise e


    # 检查输入内容与知识库的差异，传入目标文本和用户知识库字符串
    @staticmethod
    def Check_String(Tartext, KnowledgeContent):

        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["Check"]
            sepLib = "###知识库内容###\n"
            sepContent = "###用户输入文本###\n"
            promptText += sepLib + KnowledgeContent + sepContent + Tartext
            return LLMBasic.GetResponse_String(promptText)

        except Exception as e:
            raise e


    # 检查输入内容与知识库的差异，传入目标文本和用户知识库文本，返回迭代器
    @staticmethod
    def CheckStream_String(Tartext, KnowledgeContent):
        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["Check"]
            sepLib = "###知识库内容###\n"
            sepContent = "###用户输入文本###\n"
            promptText += sepLib + KnowledgeContent + sepContent + Tartext
            for i in LLMBasic.GetResponseStream_String(promptText):
                yield i

        except Exception as e:
            raise e


    # 检查输入内容与知识库的差异，传入目标文本和初始化之后的列表
    @staticmethod
    def Check_List(Tartext, KnowledgeList):

        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["Check"]
            promptText += Tartext
            KnowledgeList.append({"role": "user", "content": promptText})
            return LLMBasic.GetResponse_List(KnowledgeList)

        except Exception as e:
            raise e


    # 检查输入内容与知识库的差异，传入目标文本和初始化之后的列表，返回迭代器
    @staticmethod
    def CheckStream_List(Tartext, KnowledgeList):

        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["Check"]
            promptText += Tartext
            KnowledgeList.append({"role": "user", "content": promptText})
            for i in LLMBasic.GetResponseStream_List(KnowledgeList):
                yield i

        except Exception as e:
            raise e


    @staticmethod
    def CheckFile(Tartext):
        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["CheckFile"] + Tartext
            return LLMBasic.GetResponse_String(promptText)
        except Exception as e:
            raise e
