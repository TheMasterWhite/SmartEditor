from utils.Config.FileProcess import FileProcess, OSSProcess, JsonOperator
from utils.Config.HeadFiles import *
from utils.Config.PMTProcess import GetPrompt, KnowledgeLib
from utils.LModel.ChatBot import BotInterface
from utils.LModel.Interface import LLMInterface
from utils.SModel.OCR import *
from utils.SModel.STT import *
from utils.SModel.TarDetect import *


def LModelExample():
    # General情景
    Translate = LLMInterface.Translate(Tartext = "生活就像海洋，只有意志坚强的人才能到达彼岸",
                                       Tarlanguage = "英语")
    print(Translate)
    Summary = LLMInterface.Summary(Tartext = "生活就像海洋，只有意志坚强的人才能到达彼岸")
    print(Summary)
    Correct = LLMInterface.Correct(Tartext = "好你，今天天气很错")
    print(Correct)
    Polish = LLMInterface.Polish(Tartext = "今天天气真好")
    print(Polish)


def LModelExample2():
    Translate = LLMInterface.TranslateStream(Tartext = "生活就像海洋，只有意志坚强的人才能到达彼岸",
                                             Tarlanguage = "英语")
    for i in Translate:
        print(i, end = "")
    print()
    Summary = LLMInterface.SummaryStream(
        Tartext = "生活就像海洋，只有意志坚强的人才能到达彼岸，生活就像海洋，只有意志坚强的人才能到达彼岸")
    for i in Summary:
        print(i, end = "")
    print()
    Correct = LLMInterface.CorrectStream(Tartext = "好你，今天天气很错")
    for i in Correct:
        print(i, end = "")
    print()
    Polish = LLMInterface.PolishStream(
        Tartext = "今天天气真好,今天天气真好，今天天气真好，今天天气真好,今天天气真好,今天天气真好，今天天气真好，今天天气真好,今天天气真好,今天天气真好，今天天气真好，今天天气真好")
    for i in Polish:
        print(i, end = "")
    print()


def BotExample():
    bot = BotInterface()
    bot2 = BotInterface()
    response = bot.GetResponse("我是小王")
    print(response)
    response = bot.GetResponse("我是谁")
    print(response)

if __name__ == '__main__':
    BotExample()


