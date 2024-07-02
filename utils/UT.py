from HeadFiles import *
from SModel import *
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
    # path = "resources/house.jpeg"
    # a = SModel.GetTarDetectResult(FilePath=path)
    ocrpath = "resources/Poster.jpg"
    # bb = SModel.GetOcrResult("resources/作文.pdf",0)
    # c = SModel.GetSTTResult("resources/英文语音测试.mp3",FileExtension="mp3",Language="English")
    d = SModel.GetSTTResult("resources/沁园春雪.mp3", FileExtension="mp3", Language="Chinese")
    # print(c)
    print(d)


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
        content = SModel.GetOcrResult(FilePath=i, FileType=1)
        result += content
    prompt += result
    result = LLMInterface.GetResponse_String(prompt)
    print(result)

if __name__ == '__main__':
    LModelTest()
