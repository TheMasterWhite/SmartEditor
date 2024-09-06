from flask import Flask, Blueprint
from utils import Tools
from utils.SModel.OCR import *
from utils.SModel.TarDetect import *
from utils.SModel.STT import *

OCRBlueprint = Blueprint("OCRBlueprint", __name__, url_prefix = "/OCRInterface")


@OCRBlueprint.route("/Doc", methods = ["POST"])
def GetRawOCR():
    requestData = request.json
    filePath = requestData["filePath"]
    fileType = requestData["fileType"]
    file
    OCR_ResultString = OCRInterface.Doc(FilePath = filePath,
                                        FileType = fileType)
    pass
