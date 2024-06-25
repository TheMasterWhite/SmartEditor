# 项目文件目录树

SmartEditor
├── Main.py		#主程序运行文件夹
├── Prompt		#Prompt存放文件夹
│   ├── AgentPrompt.txt		#聊天助理Prompt，没写
│   ├── CorrectPrompt.txt		#句子纠错Prompt
│   ├── PolishPrompt.txt		#句子润色Prompt
│   ├── SummaryPrompt.txt		#句子总结Prompt
│   └── TranslatePrompt.txt		#翻译Prompt
├── Readme.md
├── Saves		#小模型调用结果储存文件夹
│   ├── OcrResult_2024_06_06_20_25_35.json
│   └── OcrResult_2024_06_06_21_24_43.json
├── Test.py		#测试文件
├── __pycache__
│   └── Main.cpython-311.pyc
├── requirements.txt
├── resources		#前端传入文件
│   ├── Poem.mp3
│   ├── Poster.jpg
│   ├── zh.wav
│   ├── 作文.docx
│   └── 作文.pdf
└── utils		#静态方法存放文件夹
    ├── Config.cfg		#项目配置文件，存放环境变量
    ├── FileProcess.py		#文件处理类
    ├── HeadFiles.py		#项目头文件，用于一键导包和配置环境变量
    ├── LModel.py		#大模型调用类
    ├── SModel.py		#小模型调用类
    ├── UT.py		#测试文件
    ├── __init__.py
    └── __pycache__
        ├── FileProcess.cpython-311.pyc
        ├── HeadFiles.cpython-311.pyc
        ├── LModel.cpython-311.pyc
        ├── SModel.cpython-311.pyc
        └── __init__.cpython-311.pyc

## FileProcess类：

```python
def Read(cls,FilePath):  #打开txt文件并返回内容，传参为文件地址
```

```python
def Base64(cls,InputFilePath):    #对文件进行Base64编码，返回编码内容文件
```

```python
def AbsPath(cls,FilePath):   #传入相对路径返回绝对路径
```

```python
def SaveWithTime(cls,FileName,FileFolder,FileExtension):#传入文件名、扩展名和保存地址，文件名添加时间并保存到指定目录
```

## 

## OSS云服务处理类：

```python
def UploadFile(FilePath,FileExtension,BucketName="masterwhite"):    #上传文件到阿里云，传入相对路径和文件扩展名,返回OSS文件路径
```



## LModel类：

```python
def GetResponse_String(Prompt):  #获取推理结果，传入字符串，返回String
```

```python
def GetResponseStream_String(Prompt):  #流式获取推理结果，传入字符串，返回迭代器
```

```python
def GetResponse_List(ListPrompt):  #获取推理结果，传入List，返回String
```

```python
def GetResponseStream_List(ListPrompt):  #流式获取推理结果，传入List，返回迭代器
```

```python
def Translate(Tartext, LanCode=2):  #Tartext传入翻译目标字符串，TarLanguage传入int型目标语言代号,返回String
```

```python
def Summary(Tartext):  # 精炼语言，传入目标句子，返回String
```

```python
def Correct(Tartext):  # 句子纠错，Tartext传入目标字符串，OpeartionCode传入操作代码(int),返回String
```

```python
def Polish(Tartext):#文章润色
```

```python
def AgentInit():#初始化聊天助手，没写完
```



## SModel类：

```python
def GetAccessToken():#百度智能云获取access_token，初始化
```

```python
def GetOcrResult(FilePath,FileType=0,SavePath="Saves"):
    #获取OCR识别内容，传入相对文件地址、文件类型和JSON文件保存地址，0为PDF，1为图片,返回解析文本
```

```python
def GetSTTResult(FilePath,FileExtension,Language="Chinese",SavePath="Saves"):#Chinese或English
    #获取语音转文字结果，传入相对路径、扩展名和语言，返回转写结果
```