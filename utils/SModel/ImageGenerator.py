import logging
import os.path
from ..LModel.Interface import LLMInterface
import erniebot, copy
from utils.Config.FileProcess import FileProcess, OSSProcess, JsonOperator
from Config import *
from utils import Tools
import cv2


class ImageGenerator():

    # 图片生成，返回图片url
    @staticmethod
    def generate_image(Prompt, Size):
        try:
            erniebot.api_type = "yinian"
            erniebot.access_token = GetAccessToken_Image()
            response = erniebot.Image.create(model = "ernie-vilg-v2",
                                             prompt = Prompt,
                                             width = Size[0],
                                             height = Size[1],
                                             version = "v2",
                                             image_num = 1)
            url = response.get_result()[0]
            return url

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[GenImage]" + str(e))
            raise e


    # 调整图像大小
    @staticmethod
    def resize_image(ImagePath, Size):
        try:
            imageObj = cv2.imread(ImagePath)
            resizedImage = cv2.resize(imageObj, Size)
            cv2.imwrite(ImagePath, resizedImage)

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[ResizeImage]" + str(e))
            raise e


    @staticmethod
    def download_image(ImageUrl):
        try:
            with requests.get(Url, stream = True) as r:
                r.raise_for_status()  # 确保请求成功
                savePath = os.path.join(GLOBAL_ResourcesSavePath, "PPTImage.jpg")
                with open(savePath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size = 8192):
                        # 如果是有效的chunk，写入到文件中
                        if chunk:
                            f.write(chunk)
            return savePath

        except Exception as e:
            curTime = Tools.GetTime()
            logging.error(f"[{curTime}]Module:[DownloadImage]" + str(e))
            raise e
