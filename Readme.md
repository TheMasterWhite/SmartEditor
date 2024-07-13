# 项目文件目录树

SmartEditor
├── Main.py	#项目主入口
├── Readme.md	#Help
├── Saves	#用于保存小模型识别结果
│   ├── OcrResult	#OCR识别结果
│   │   ├── ......
│   ├── SttResult	#语音转文字识别结果
│   │   ├── ......
│   └── TarResult	#目标检测识别结果
│       ├── ......
├── requirements.txt
├── resources	#存放用户输入文件
│   ├── ......
└── utils	#功能接口类
    ├── Config	#基础工具包
    │   ├── Config.cfg	#配置文件
    │   ├── FileProcess.py	#文件处理功能接口类
    │   ├── HeadFiles.py	#头文件类，用于一键导包和初始化项目
    │   ├── PMTProcess.py	#提示词处理与知识库功能接口类
    │   ├── Prompts.json	#存放提示词的表
    │   ├── __init__.py
    │   └── __pycache__
    ├── LModel	#大模型功能类
    │   ├── ChatBot.py	#智能问答机器人类
    │   ├── Interface.py	#大模型基本功能接口类
    │   ├── __init__.py
    │   └── __pycache__
    ├── SModel	#小模型功能类
    │   ├── OCR.py	#OCR
    │   ├── STT.py	#语音转文字
    │   ├── TarDetect.py	#目标检测
    │   └──  __init__.py
    └──UT.py	#单元测试

# PMTProcess.py

GetPrompt类

```python
def Data(self):  # 返回存储Prompt的json字典
    return self.data
#调用方法
a = GetPrompt().Data()["一级目录"]["二级目录"]#返回一个dict
```

KnowledgeLib类

```python
def InitList_String(KnowledgeText):  # 载入用户知识库，传入知识库字符串返回初始化后的列表
def InitList_Path(KnowledgePath):  # 载入用户知识库，传入知识库文件路径返回初始化后的列表
```

# FileProcess.py

FileProcess类

```python
def ReadTxt(FilePath):  # 打开txt文件并返回内容，传参为文件地址
def Base64(FilePath):  # 对文件进行Base64编码，返回编码内容文件，传入文件路径
def AbsPath(FilePath):  # 获取绝对路径
def GetFileTimePath(FileName, TarPath, FileExtension):  # 将文件名赋予时间并返回绝对路径
```

OSSProcess类

```python
def UploadFile(FilePath, FileExtension, BucketName = "smart-editor"):  # 上传文件到阿里云，传入相对路径和文件扩展名,返回OSS文件路径
```

JsonOperator类

```python
def Save(JsonObject, Path, FileName):  # 保存Json文件至指定目录，传入Json对象、保存路径与文件名
def Load(FilePath, FileName):  # 加载Json文件
```

# ChatBot.py

BotBasic类

```python
def AddMessage(self, role, content):
    # 向对象添加交互内容，如果添加的是用户信息则会返回结果，否则返回Lambda表达式
def AddMessageStream(self, role, content):
    # 与上条函数相似，返回迭代器
```

BotInterface类(继承BotBasic)

```python
def GetResponse(self, Content):  # 获取机器人问答结果，传入内容
def GetResponseStream(self, Content):# 流式获取机器人回复内容，传入输入内容返回迭代器
def LoadKnowledgeLib_String(self, KnowledgeText):  # 载入知识库，传入知识库文本
def LoadKnowledgeLib_Path(self, KnowledgePath):  # 载入知识库，传入知识库路径
def ClearHistory(self):  # 清除历史记录
    
用法：需要实例化一个对象
bot = BotInterface()
response = Bot.Getresponse("输入内容")
bot.ClearHistory()
```

# Interface.py

LLMBasic类

```python
def GetResponse_String(Prompt):  # 获取推理结果，传入字符串，返回String
def GetResponseStream_String(Prompt):  # 流式获取推理结果，传入字符串，返回迭代器
def GetResponse_List(ListPrompt):  # 获取推理结果，传入List，返回String
def GetResponseStream_List(ListPrompt):  # 流式获取推理结果，传入List，返回迭代器
```

LLMInterface类(继承LLMBasic)

```python
传参Scene是指ScenePrompt_xxx大类名称
-----------------------------------------------------------------------------------------------------
def Translate(Tartext, Tarlanguage = "英语",Scene = GeneralScene):  
    # 翻译，Tartext传入翻译目标字符串，TarLanguage传入目标语言,返回String
def TranslateStream(...):  # 与上文相同，返回迭代器
-----------------------------------------------------------------------------------------------------
def Summary(Tartext, Scene = GeneralScene):  # 精炼语言，，Tartext传入目标字符串,返回String
def SummaryStream(...):  # 与上文相同，返回迭代器
-----------------------------------------------------------------------------------------------------
def Correct(Tartext, Scene = GeneralScene):  # 句子纠错，Tartext传入目标字符串,返回String
def CorrectStream(...):  # 与上文相同，返回迭代器
----------------------------------------------------------------------------------------------------- 
def Polish(Tartext, Scene = GeneralScene):  # 文章润色，Tartext传入目标字符串,返回String
def PolishStream(...):  # 与上文相同，返回迭代器
-----------------------------------------------------------------------------------------------------
def Check_String(Tartext, KnowledgeContent):  # 检查输入内容与知识库的差异，传入目标文本和用户知识库字符串
def CheckStream_String(Tartext, KnowledgeContent):  
    # 检查输入内容与知识库的差异，传入目标文本和用户知识库文本，返回迭代器
def Check_List(Tartext, KnowledgeList):  # 检查输入内容与知识库的差异，传入目标文本和初始化之后的列表
def CheckStream_List(Tartext, KnowledgeList):  # 检查输入内容与知识库的差异，传入目标文本和初始化之后的列表，返回迭代器
```

# OCR.py

OCRBasic类

```python
def GetDocJson(FilePath, FileCode):  # 获取文档抽取OCR模型识别内容，
    # 传入相对文件地址、文件类型和JSON文件保存地址，文件类型为"IMG"或"PDF",返回解析json
def GetRawJson(FilePath):  # 获取RawOCR识别结果，传入文件地址返回Json对象
```

OCRInterface类(继承OCRBasic)

```python
传参ResultType是提示词列表中OCRPrompt类下的二级类
-----------------------------------------------------------------------------------------------------
def Doc(FilePath, FileType = "IMG", SavePath = "Saves/OcrResult"):
    # 获取DocOCR识别结果，返回String
def Raw(FilePath, SavePath = "Saves/OcrResult"):  # 获取RawOCR结果，返回String
def ProcessDoc(FilePath, FileType = "IMG", SavePath = "Saves/OcrResult", ResultType = "General"):
def ProcessRaw(FilePath, SavePath = "Saves/RawResult", ResultType = "General"):
	# 使用大模型处理OCR识别结果，传入字符串和结果类型对应的Prompt名字，返回字符串
```

# STT.py

STTBasic类

```python
def CreateTask(FilePath, FileExtension, Language = "Chinese"):  # 创建音频转写任务
def QueryTask(TaskID):  # 获取音频转写任务结果
```

STTInterface类(继承STTBasic)

```python
def GetResult(FilePath, FileExtension, Language = "Chinese", SavePath = "Saves/SttResult"):  # 获取语音转文字结果，返回String
```

# TarDetect.py

TarDetectBasic类

```python
def GetJson(FilePath):
	# 获取目标检测结果，传入文件地址返回结果String并返回Json对象
```

TarInterface类(继承TarDetectBasic)

```python
def GetResult(FilePath, SavePath = "Saves/TarResult"):  # 获取目标检测结果
```