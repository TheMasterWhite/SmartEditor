import requests, json, os
from utils.LModel.Interface import LLMInterface
from utils.Config.FileProcess import *


def test():
    url = 'http://127.0.0.1:8888/LLMInterface/Summary'
    data = {
        "content": "生活就像海洋，只有意志坚强的人才能到达彼岸。"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json())


if __name__ == "__main__":
    test()
    #print(LLMInterface.Translate("你好"))