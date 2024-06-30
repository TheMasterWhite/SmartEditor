from HeadFiles import *
from SModel import *
from LModel import *


def LModelTest():
    a = LModel.Translate("我是雪狐！快夸我可爱！")
    b = LModel.Correct("我是雪狐！快夸我可爱！")
    c = LModel.Summary("我是雪狐！快夸我可爱！")
    d = LModel.Polish("我是雪狐！快夸我可爱！")
    print(a)
    print(b)
    print(c)
    print(d)

def SModelTest():
    # path = "resources/house.jpeg"
    # a = SModel.GetTarDetectResult(FilePath=path)
    ocrpath = "resources/Poster.jpg"
    # b = SModel.GetOcrResult(ocrpath)
    # bb = SModel.GetOcrResult("resources/作文.pdf",0)
    #c = SModel.GetSTTResult("resources/英文语音测试.mp3",FileExtension="mp3",Language="English")
    d = SModel.GetSTTResult("resources/沁园春雪.mp3",FileExtension="mp3",Language="Chinese")
    #print(c)
    print(d)

if __name__ == '__main__':
    SModelTest()
