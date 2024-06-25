from utils.LModel import *

Prevmsg = []  # 对话历史


async def test(parameter):
    model = ERNIEBot(model="ernie-4.0")
    messages = [HumanMessage(parameter)]
    ai_message = await model.chat(messages=messages)
    print(ai_message.content)


if __name__ == '__main__':
    print("Hello World")
