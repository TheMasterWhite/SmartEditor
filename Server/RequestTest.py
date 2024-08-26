import requests, json, os
from utils.LModel.Interface import LLMInterface
from utils.Config.FileProcess import *


def test():
    url = 'http://8.148.25.61:8888/LLMInterface/Translate'
    data = {
        "content": "你说你不想在这里"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json())


if __name__ == "__main__":
    test()
    #print(LLMInterface.Translate("生活就像海洋，只有意志坚强的人才能到达彼岸。"))
    #print(LLMInterface.Translate("你好"))