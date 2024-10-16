# <center>基于PaddlePaddle<br>和ERNIE SDK的智能写作助手</center>

## <center>项目概述</center>

随着大模型的广泛应用，各类AI智能写作辅助工具如雨后春笋般涌现，然而市面上多数产品仍以chat的形式为用户提供简单的写作辅助服务，在基于特定素材的进行创作的场景中表现出一定的局限性，且这类辅助工具未集成文本编辑器，导致用户在写作时需要频繁切换窗口，对工作效率产生了一定的影响。

为了提高文本写作的工作效率、改善写作辅助工具的用户体验，本项目基于PaddlePaddle、ERNIE SDK、WangEditor框架等技术，构建了一款智能写作助手。该助手旨在实现如下目标：

- 在不切换窗口的情况下**同步写作与使用AI辅助功能**
- 调用多模态模型**自动化处理用户上传的素材文件**

- 基于用户提供的知识库进行**格式化文本生成**

## <center>项目技术方案</center>

系统功能架构主要包括文本智能润色、格式化文本生成、多媒体信息处理以及用户知识库管理等模块，总体功能架构如图1所示。

<p align="center">
  <img src="https://smart-editor.oss-cn-shenzhen.aliyuncs.com/%E7%B3%BB%E7%BB%9F%E6%80%BB%E4%BD%93%E6%9E%B6%E6%9E%84%E5%9B%BE.png" alt="图注内容" style="display:block;margin:auto;">
  <p style="text-align:center;">图 1 系统总体功能架构图</p>
</p>
文本智能润色模块提供翻译、总结、纠错、润色、文档助手五大功能，与文本编辑器相结合，实现无需切换窗口即可在AI助力下完成文档撰写工作。格式化文本生成模块依托文心大模型强大的文本生成能力，提供了丰富的文本生成工具，用户只需提供必要的信息即可快速生成一篇格式化文本。多媒体信息处理模块支持多种文件格式，系统将自动判断上传的文件类型并调用相应的的小模型对多媒体文件进行处理。用户知识库管理模块储存用户上传的多媒体文件，提供增删查改四大基础功能，此外也可使用大模型的联网搜索增强功能对知识库内容进行检查，以验证其时效性。相较于其他智能写作辅助工具，本项目主要创新点如下：

- **多媒体数据处理+格式化文本生成工具链**
- **智能润色+知识库检查工具链**
- **知识库联网检查**
- **在线文档与知识库管理模块**

#### **智能润色模块**

该模块集成AI基础润色功能、写作情境选择功能、文档编辑助手以及在线文本编辑器，模块功能集中便于用户使用，其搭载的智能润色+知识库检查工具链架构如图2所示，页面如图3所示。用户通过选定目标文本并指定所需的润色功能，后端服务接收到请求后，根据用户选择的写作情景载入相应的提示词，并将提示词与原始文本拼接，通过ERNIE SDK向大模型发送文本生成请求，接收到生成结果后将内容返回给用户。

<p align="center">
  <img src="https://smart-editor.oss-cn-shenzhen.aliyuncs.com/%E6%96%87%E6%9C%AC%E6%B6%A6%E8%89%B2%E6%B5%81%E7%A8%8B.png" alt="图注内容" style="display:block;margin:auto;">
  <p style="text-align:center;">图 2 智能润色+知识库检查工具链架构图</p>
</p>
<p align="center">
  <img src="https://smart-editor.oss-cn-shenzhen.aliyuncs.com/%E7%BC%96%E8%BE%91%E5%99%A8%E9%A1%B5%E9%9D%A2.png" alt="图注内容" style="display:block;margin:auto;">
  <p style="text-align:center;">图 3 编辑器页面展示图</p>
</p>

#### **格式化文本生成模块**

该模块基于多媒体数据处理+格式化文本生成工具链搭建，其功能架构如图4所示，页面效果如图5、图6所示。，载入文本生成提示词与用户需求，通过ERNIE SDK向文心大模型发起调用，如果对大模型生成结果不满意，可选择重新生成。
<p align="center">
  <img src="https://smart-editor.oss-cn-shenzhen.aliyuncs.com/%E6%A0%BC%E5%BC%8F%E5%8C%96%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E5%B7%A5%E5%85%B7%E9%93%BE.png" alt="图注内容" style="display:block;margin:auto;">
  <p style="text-align:center;">图 4 多媒体数据处理+格式化文本生成工具链架构图</p>
</p>
<p align="center">
  <img src="https://smart-editor.oss-cn-shenzhen.aliyuncs.com/%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E5%B7%A5%E5%85%B7%E7%AE%B1%E4%B8%BB%E9%A1%B5%E9%9D%A2.png" alt="图注内容" style="display:block;margin:auto;">
  <p style="text-align:center;">图 5 文本生成工具箱界面</p>
</p>
<p align="center">
  <img src="https://smart-editor.oss-cn-shenzhen.aliyuncs.com/%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E5%B7%A5%E5%85%B7%E7%AE%B1%E8%AF%A6%E7%BB%86%E9%A1%B5%E9%9D%A2.png" alt="图注内容" style="display:block;margin:auto;">
  <p style="text-align:center;">图 6 文本生成工具箱详细界面</p>
</p>
#### **多媒体信息处理模块**

该模块同样基于多媒体数据处理+格式化文本生成工具链搭建，系统接收用户上传的多媒体文件，随后，识别文件格式并对其进行预处理，处理完毕后向部署在AI Studio上的模型服务发起调用请求，接收到模型处理结果后将其保存至用户知识库中。其多媒体文件上传页面效果如图7所示

<p align="center">
  <img src="https://smart-editor.oss-cn-shenzhen.aliyuncs.com/%E5%A4%9A%E5%AA%92%E4%BD%93%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E7%95%8C%E9%9D%A2.png" alt="图注内容" style="display:block;margin:auto;">
  <p style="text-align:center;">图 7 多媒体文件上传页面</p>
</p>

#### **用户知识库管理模块**

该模块实现了个人与团队知识资产的集中管理与高效利用，用户可以在该模块中维护专有知识库，同时还可以利用大模型的联网搜索增强功能对知识库文件进行联网检查，知识库联网检查流程如图7所示，知识库文件管理页面效果如图8所示。
<p align="center">
  <img src="https://smart-editor.oss-cn-shenzhen.aliyuncs.com/%E7%9F%A5%E8%AF%86%E5%BA%93%E6%A3%80%E6%9F%A5%E6%B5%81%E7%A8%8B.png" alt="图注内容" style="display:block;margin:auto;">
  <p style="text-align:center;">图 7 知识库检查流程示意图</p>
</p>
<p align="center">
  <img src="https://smart-editor.oss-cn-shenzhen.aliyuncs.com/%E5%9C%A8%E7%BA%BF%E6%96%87%E6%A1%A3%E7%95%8C%E9%9D%A2.png" alt="图注内容" style="display:block;margin:auto;">
  <p style="text-align:center;">图 8 知识库文件管理页面</p>
</p>