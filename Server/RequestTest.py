import copy
import requests, json, os
from utils.LModel.ChatBot import BotInterface
from utils.LModel.Interface import LLMInterface
from utils.Config.FileProcess import *


# 用于单元测试

def UnitTest():
    url2 = 'http://8.148.25.61:8888/LLMInterface/'
    # url2 = 'http://localhost:8888/LLMInterface/'
    data = {
        "content": "生活就像海洋，只有意志坚强的人才能到达彼岸",
        "userId": "666"
    }
    headers = {'Content-Type': 'application/json'}

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

    url = url2 + "ChatBot"
    data2 = data.copy()
    data2["content"] = "你好，我是小王"
    response = requests.post(url, data = json.dumps(data2), headers = headers)
    print(response.json()["response"])


def UnitTestGen():
    url2 = 'http://8.148.25.61:8888/LLMInterface/'
    # url2 = 'http://localhost:8888/LLMInterface/'
    data = {
        "content": "生活就像海洋，只有意志坚强的人才能到达彼岸",
        "userId": "666"
    }
    headers = {'Content-Type': 'application/json'}

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

    url = copy.deepcopy(url2) + "ChatBotStream"
    data2 = data.copy()
    data2["content"] = "你好，我是小王"
    response = requests.post(url, data = json.dumps(data), headers = headers, stream = True)
    for i in response.iter_content(chunk_size = 1024):
        print(i.decode('utf-8'), end = "")
    print()


if __name__ == "__main__":
    # UnitTest()
    # print("666")
    # UnitTestGen()

    # url = 'http://8.148.25.61:8888/Server/UploadFile'
    # files = {"file": open("E:/Code/CodeLibrary/Python/SmartEditor/resources/Poster.jpg", "rb")}
    # response = requests.post(url, files = files)
    # print(response.json())

    url = 'http://8.148.25.61:8888/OCRInterface/Doc'
    data = {
        "fileName": "Poster.jpg",
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json())
