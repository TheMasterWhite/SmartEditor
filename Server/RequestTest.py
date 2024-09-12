import copy
import requests, json, os


# 用于单元测试

def UnitTest():
    url2 = 'http://8.148.25.61:8888/LLMInterface/'
    # url2 = 'http://localhost:8888/LLMInterface/'
    data = {
        "content": "生活就像海洋，只有意志坚强的人才能到达彼岸",
        "userId": "Test"
    }
    headers = {'Content-Type': 'application/json'}

    # url = url2 + "Translate"
    # response = requests.post(url, data = json.dumps(data), headers = headers)
    # print(response.json()["response"])
    #
    # url = url2 + "Summary"
    # response = requests.post(url, data = json.dumps(data), headers = headers)
    # print(response.json()["response"])
    #
    # url = url2 + "Correct"
    # response = requests.post(url, data = json.dumps(data), headers = headers)
    # print(response.json()["response"])
    #
    # url = url2 + "Polish"
    # response = requests.post(url, data = json.dumps(data), headers = headers)
    # print(response.json()["response"])

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
    response = requests.post(url, data = json.dumps(data2), headers = headers, stream = True)
    for i in response.iter_content(chunk_size = 1024):
        print(i.decode('utf-8'), end = "")
    print()


def UploadFile():
    url = 'http://8.148.25.61:8888/Service/UploadFile'
    files = {"file": open("E:/Code/CodeLibrary/Python/SmartEditor/resources/作文.pdf", "rb")}
    response = requests.post(url, files = files)
    print(response.json())

    # files = {"file": open("E:/Code/CodeLibrary/Python/SmartEditor/resources/沁园春雪.mp3", "rb")}
    # response = requests.post(url, files = files)
    # print(response.json())
    #
    # files = {"file": open("E:/Code/CodeLibrary/Python/SmartEditor/resources/沁园春长沙.mp4", "rb")}
    # response = requests.post(url, files = files)
    # print(response.json())


def SModelTest():
    # url = "http://8.148.25.61:8888/SModelInterface/OCR"
    # headers = {'Content-Type': 'application/json'}
    # data = {
    #     "fileName": ["作文.pdf", "Poster.jpg"]
    # }
    # response = requests.post(url, data = json.dumps(data), headers = headers)
    # print(response.json())

    url2 = "http://8.148.25.61:8888/SModelInterface/STT"
    data = {
        "fileData": [{"name": "沁园春雪.mp3", "language": "Chinese"},
                     {"name": "沁园春长沙.mp4", "language": "Chinese"}]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url2, data = json.dumps(data), headers = headers)
    print(response.json())


def LibTest():
    url = "http://8.148.25.61:8888/LLMInterface/Check"
    data = {
        "content": "亚托莉是一个人类。男性",
        "fileName": ["亚托莉.txt"],
        "userId": "Test"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])


def ChatBotLib():
    url = "http://8.148.25.61:8888/LLMInterface/ChatBot"
    headers = {'Content-Type': 'application/json'}

    data = {
        "content": "亚托莉是谁",
        "fileName": ["作文.txt"],
        "userId": "Test"
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])

    data = {
        "content": "亚托莉需要刷牙吗",
        "userId": "Test"
    }
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json()["response"])


if __name__ == "__main__":
    UploadFile()
    #ChatBotLib()
