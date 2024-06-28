from paddlespeech.server.bin.paddlespeech_client import ASRClientExecutor
from paddle import *
import torch


def main():
    audio = "resources/zh.wav"
    asr = ASRExecutor()
    result = asr(audio_file=audio, model='conformer_online_wenetspeech')
    print(result)

def test():
    tts = TTSExecutor()
    tts(text="今天天气十分不错。", output="output.wav")


if __name__ == '__main__':
    pass