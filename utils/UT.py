from utils.HeadFiles import *
from utils.SModel.OCR import *
from utils.SModel.TarDetect import *
from utils.SModel.STT import *
from LModel import *


def LModelTest():
    a = LLMInterface.Translate("我是雪狐！快夸我可爱！")
    b = LLMInterface.Correct("我是雪狐！快夸我可爱！")
    c = LLMInterface.Summary("我是雪狐！快夸我可爱！")
    d = LLMInterface.Polish("我是雪狐！快夸我可爱！")
    print(a)
    print(b)
    print(c)
    print(d)


def SModelTest():
    housePath = "resources/house.jpeg"
    posterPath = "resources/Poster.jpg"
    chineseSTTPath = "resources/沁园春雪.mp3"
    englishSTTPath = "resources/英文语音测试.mp3"
    pdfPath = "resources/作文.pdf"

    # a = TarInterface.GetResult(housePath)
    # b = OCRInterface.Raw(posterPath)
    # c = OCRInterface.Doc(posterPath)
    # d = OCRInterface.Doc(pdfPath,FileType = "PDF")
    e = STTInterface.GetResult(chineseSTTPath, Language = "Chinese", FileExtension = "mp3")
    f = STTInterface.GetResult(englishSTTPath, Language = "English", FileExtension = "mp3")

    # print("a = " + a)
    # print("b = " + b)
    # print("c = " + c)
    # print("d = " + d)
    print(e)
    print(f)


def Test():
    a = GetPrompt().Data()["FunctionPrompt"]["Translate"]
    print(a + '1')
    Parameter = [{"role": "user", "content": "知识库载入提示词(静态) + 用户知识库(动态)"},
                 {"role": "assistant", "content": "我是第一轮大模型回复内容"},
                 {"role": "user", "content": "功能提示词(静态) + 用户编辑器文本(动态)"},
                 {"role": "assistant", "content": "我是第二轮大模型回复内容"}]


def FileIterator():
    for i in range(1, 7):
        fileName = f"{''}{i}{'.jpg'}"
        abspath = FileProcess.AbsPath("resources/t")
        filePath = os.path.join(abspath, fileName)
        if os.path.isfile(filePath):
            yield filePath
        else:
            print(f" {filePath} 不存在。")


def SaveMoney():
    result = ""
    prompt = "你是一个聊天记录分析助手，下文冒号后面是一串由OCR识别到的微信聊天群消息，你需要将其内容尽可能详细地复述出来："
    for i in FileIterator():
        content = SModelInterface.GetRawOCRResult(FilePath = i)
        result += content
    prompt += result
    result = LLMInterface.GetResponse_String(prompt)
    print(result)


if __name__ == '__main__':
    SModelTest()
