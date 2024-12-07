from utils import Tools
from utils.Config.PMTProcess import GetPrompt, KnowledgeLib
from utils.Config.FileProcess import FileProcess, OSSProcess, JsonOperator
from Config import *
import erniebot, copy

fileSavePath = copy.deepcopy(GLOBAL_FileSavePath)


class LLMBasic:  # 大模型基本通信接口类

    # 获取推理结果，传入字符串，返回String
    @staticmethod
    def GetResponse_String(Prompt, Model = "ernie-4.0"):

        try:
            erniebot.api_type = "aistudio"
            erniebot.access_token = GLOBAL_ERNIETOKEN
            Parameter = [{"role": "user", "content": Prompt}]
            Response = erniebot.ChatCompletion.create(
                model = Model,
                messages = Parameter
            )
            return Response.get_result()

        except Exception as e:
            raise e


    # 流式获取推理结果，传入字符串，返回迭代器
    @staticmethod
    def GetResponseStream_String(Prompt, Model = "ernie-4.0"):

        try:
            erniebot.api_type = "aistudio"
            erniebot.access_token = GLOBAL_ERNIETOKEN
            Parameter = [{"role": "user", "content": Prompt}]
            Response = erniebot.ChatCompletion.create(
                model = Model,
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
            erniebot.api_type = "aistudio"
            erniebot.access_token = GLOBAL_ERNIETOKEN
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
            erniebot.api_type = "aistudio"
            erniebot.access_token = GLOBAL_ERNIETOKEN
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
            return LLMBasic.GetResponse_String(Prompt = prompt)

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
            for i in LLMBasic.GetResponseStream_String(Prompt = prompt):
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
            return LLMBasic.GetResponse_String(Prompt = prompt, Model = "ernie-speed")

        except Exception as e:
            raise e


    # 精炼语言，，Tartext传入目标字符串,返回迭代器
    @staticmethod
    def SummaryStream(Tartext, Scene = "General"):

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Summary"]
            prompt += Tartext
            for i in LLMBasic.GetResponseStream_String(Prompt = prompt, Model = "ernie-speed"):
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
            return LLMBasic.GetResponse_String(Prompt = prompt)

        except Exception as e:
            raise e


    # 句子纠错，Tartext传入目标字符串,返回迭代器
    @staticmethod
    def CorrectStream(Tartext, Scene = "General"):

        try:
            sceneLocation = "ScenePrompt_" + Scene
            prompt = GetPrompt().Data()[sceneLocation]["Correct"]
            prompt += Tartext
            for i in LLMBasic.GetResponseStream_String(Prompt = prompt):
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


    # 文件内容联网检查
    @staticmethod
    def CheckFile(Tartext):
        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["CheckFile"] + Tartext
            return LLMBasic.GetResponse_String(promptText)
        except Exception as e:
            raise e


    # 文件内容总结
    @staticmethod
    def FileSummary(FileText):
        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["FileSummary"] + FileText
            return LLMBasic.GetResponse_String(promptText)
        except Exception as e:
            raise e


    # 生成文件名
    @staticmethod
    def GetFileName(FileText):
        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["GetFileName"] + FileText
            return LLMBasic.GetResponse_String(promptText)
        except Exception as e:
            raise e


    @staticmethod
    def AIWriting(Tartext):
        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["AIWriting"]
            promptText += Tartext
            return LLMBasic.GetResponse_String(Prompt = promptText, Model = "ernie-speed")

        except Exception as e:
            raise e


    @staticmethod
    def AIWriting_Stream(Tartext):
        try:
            promptText = GetPrompt().Data()["FunctionPrompt"]["AIWriting"]
            promptText += Tartext
            for i in LLMBasic.GetResponseStream_String(Prompt = prompt, Model = "ernie-speed"):
                yield i

        except Exception as e:
            raise e
