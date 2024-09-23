import copy
import requests, json, os

# 用于单元测试
headers = {'Content-Type': 'application/json'}


def ClearBotHistory(UserId):
    url2 = "http://8.148.25.61:8888/LLMInterface/ClearBotHistory"
    data = {
        "userId": UserId
    }
    response = requests.post(url2, data = json.dumps(data), headers = headers)
    print(response.json())


def LLMTest():
    url2 = 'http://8.148.25.61:8888/LLMInterface/'
    data = {
        "content": "生活就像海洋，只有意志坚强的人才能到达彼岸"
    }
    # "userId": "Test"
    url = url2 + "Translate"
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])

    url = url2 + "Summary"
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])

    url = url2 + "Correct"
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])

    url = url2 + "Polish"
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])

    url = url2 + "Check"
    data = {
        "content": "亚托莉是一个人类。男性",
        "fileName": ["亚托莉.txt"]
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])


def LLMTestStream():
    url2 = 'http://8.148.25.61:8888/LLMInterface/'
    data = {
        "content": "生活就像海洋，只有意志坚强的人才能到达彼岸",
        "userId": "666"
    }

    url = copy.deepcopy(url2) + "TranslateStream"
    response = requests.post(url, data = json.dumps(data), headers = headers, stream = True)
    for i in response.iter_content(chunk_size = 1024):
        print(i.decode('utf-8'), end = "")
    print()

    url = copy.deepcopy(url2) + "PolishStream"
    response = requests.post(url, data = json.dumps(data), headers = headers, stream = True)
    for i in response.iter_content(chunk_size = 1024):
        print(i.decode('utf-8'), end = "")
    print()

    url = copy.deepcopy(url2) + "CorrectStream"
    response = requests.post(url, data = json.dumps(data), headers = headers, stream = True)
    for i in response.iter_content(chunk_size = 1024):
        print(i.decode('utf-8'), end = "")
    print()

    url = copy.deepcopy(url2) + "SummaryStream"
    response = requests.post(url, data = json.dumps(data), headers = headers, stream = True)
    for i in response.iter_content(chunk_size = 1024):
        print(i.decode('utf-8'), end = "")
    print()

    url = copy.deepcopy(url2) + "CheckStream"
    data = {
        "content": "亚托莉是一个人类",
        "fileName": ["亚托莉.txt"]
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    for i in response.iter_content(chunk_size = 1024):
        print(i.decode('utf-8'), end = "")


def UploadFile(FileName):
    url = "http://8.148.25.61:8888/Service/UploadFile"
    # files = {"file": open("E:/Code/CodeLibrary/Python/SmartEditor/resources/作文.pdf", "rb")}
    # response = requests.post(url, files = files)
    # print(response.json())
    #
    files = {"file": open(f"E:/Code/CodeLibrary/Python/SmartEditor/resources/{FileName}", "rb")}
    response = requests.post(url, files = files)
    print(response.json())

    # files = {"file": open("E:/Code/CodeLibrary/Python/SmartEditor/resources/沁园春长沙.mp4", "rb")}
    # response = requests.post(url, files = files)
    # print(response.json())
    #
    # files = {"file": open("E:/Code/CodeLibrary/Python/SmartEditor/resources/文心一言wrong.txt", "rb")}
    # response = requests.post(url, files = files)
    # print(response.json())

    # files = {"file": open("E:/Code/CodeLibrary/Python/SmartEditor/resources/Poster.jpg", "rb")}
    # response = requests.post(url, files = files)
    # print(response.json())


def SModelTest():
    url = "http://8.148.25.61:8888/SModelInterface/OCR"
    data = {
        "fileName": ["作文.pdf", "Poster.jpg"]
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json())

    url2 = "http://8.148.25.61:8888/SModelInterface/STT"
    data = {
        "fileData": [{"name": "沁园春雪.mp3", "language": "Chinese"},
                     {"name": "沁园春长沙.mp4", "language": "Chinese"}]
    }
    response = requests.post(url2, data = json.dumps(data), headers = headers)
    print(response.json())


def ChatBot():
    ClearBotHistory("Test")

    url = "http://8.148.25.61:8888/LLMInterface/ChatBot"
    data = {
        "content": "亚托莉需要刷牙吗",
        "fileName": ["亚托莉.txt"],
        "userId": "Test"
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])

    data2 = {
        "content": "亚托莉需要刷牙吗",
        "userId": "Test2"
    }
    response = requests.post(url, data = json.dumps(data2), headers = headers)
    print(response.json()["response"])

    ClearBotHistory("Test")

    data = {
        "content": "亚托莉喜欢吃东西吗",
        "userId": "Test"
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])


def ChatBotStream():
    url = "http://8.148.25.61:8888/LLMInterface/ChatBotStream"
    ClearBotHistory("Test")
    data = {
        "content": "亚托莉需要刷牙吗",
        "fileName": ["亚托莉.txt"],
        "userId": "Test"
    }
    response = requests.post(url, data = json.dumps(data), headers = headers, stream = True)
    for i in response.iter_content(chunk_size = 1024):
        print(i.decode('utf-8'), end = "")
    print()

    data2 = {
        "content": "亚托莉需要刷牙吗",
        "userId": "Test2"
    }
    response = requests.post(url, data = json.dumps(data2), headers = headers)
    for i in response.iter_content(chunk_size = 1024):
        print(i.decode('utf-8'), end = "")
    print()

    ClearBotHistory("Test")

    data = {
        "content": "亚托莉喜欢吃东西吗",
        "userId": "Test"
    }
    response = requests.post(url, data = json.dumps(data), headers = headers, stream = True)
    for i in response.iter_content(chunk_size = 1024):
        print(i.decode('utf-8'), end = "")
    print()


def CheckFile():
    url = "http://8.148.25.61:8888/Service/CheckFile"
    data = {
        "fileName": "文心一言wrong.txt"
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json())


def Delete():
    url = "http://8.148.25.61:8888/Service/DeleteFile"
    data = {
        "fileName": "Poster.jpg"
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json())


def Read():
    url = "http://8.148.25.61:8888/Service/Save"
    data = {
        "fileName": "test.txt",
        "content": "666"
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json())


def UploadResource(FileName):
    url = "http://8.148.25.61:8888/Service/UploadResource"
    files = {"file": open(f"E:/Code/CodeLibrary/Python/SmartEditor/resources/models/{FileName}", "rb")}
    response = requests.post(url, files = files)
    print(response.json())


def TextGen():
    url = "http://8.148.25.61:8888/LLMInterface/TextGen"
    data = {
        "content": "写一个介绍演讲稿",
        "template": "演讲稿",
        "materialFiles": ["亚托莉.txt", "亚托莉剧情.txt"]
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])


def main():
    # print("-UploadFile-")

    # print()
    # print("-LLMTest-")
    LLMTest()
    # print()
    # print("-LLMTestStream-")
    # LLMTestStream()
    # print()
    # print("-SModelTest-")
    # SModelTest()
    # print()
    # print("-ChatBot-")
    # ChatBot()
    # print()
    # print("-ChatBotStream-")
    # ChatBotStream()


if __name__ == "__main__":
    TextGen()
