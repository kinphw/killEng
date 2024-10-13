from killEng.common.myFileDialog import MyFileDialog as myfd
from killEng.common.stringHandler import StringHandler as sh

class BaseIO:

    strInput:str
    strOutput:str

    # def __init__(self, msgInput:str = "", outputSuffix:str = "", outputExt:str = "") -> None:
    #     # self.strInput = myfd.askopenfilename(msgInput)
    #     # self.strOutput = sh.add_output_suffix(self.strInput, outputSuffix, outputExt)

    def _initSet(self, msgInput:str = "", outputSuffix:str = "", outputExt:str = ""):
        self.strInput = myfd.askopenfilename(msgInput)
        self.strOutput = sh.add_output_suffix(self.strInput, outputSuffix, outputExt)