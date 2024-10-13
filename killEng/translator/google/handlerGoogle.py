# input : list[str] : 번역대상
# do : input에 따라 하나씩 또는 여러개씩 번역기 클래스에 던지고 결과를 받아서 데이터프레임에 쌓음
# output : list[str] : 번역결과 => 데이터프레임으로 변경하는 것은 외부에서 처리

# 언어별 핸들러 분리

# import pandas as pd
import tqdm

# from killEng.translator.util.baseTrans import BaseTranslator
from killEng.translator.google.google import GoogleTranslator
# from killEng.translator.util.chunkmaker import ChunkedListMaker
# from killEng.translator.util.toolinfo import ToolInfo
from killEng.translator.util.baseHandler import BaseTranslationHandler

class TranslationHandlerGoogle(BaseTranslationHandler):

    liStrBefore:list[str]
    objTool:GoogleTranslator

    source_lang:str #GOOGLE
    target_lang:str #GOOGLE

    def __init__(self, liStrBefore:list[str]) -> None:
        self.liStrBefore = liStrBefore
        self.objTool = GoogleTranslator()

         # 번역방향 설정부
        super().__init__()
        self._setVariable()

    def run(self) -> list[str]:
        return self._translateEach()

    def _setVariable(self) -> None:
        if self.intDirection == self.ENKO:
            self.source_lang = "en"
            self.target_lang = "ko"
        elif self.intDirection == self.KOEN:
            self.source_lang = "ko"
            self.target_lang = "en"

    #########################################################################
    # 한개씩 traslateEach에 던짐
    def _translateEach(self) -> list[str]:

        liStrAfter = []
        for strBefore in tqdm.tqdm(self.liStrBefore, "Translating"):
            strAfter = self.objTool.translateEach(strBefore, self.source_lang, self.target_lang)
            liStrAfter.append(strAfter)

        return liStrAfter
    #########################################################################

if __name__ == "__main__":
    liStrBefore = ["Hello", "World", "Python", "Java", "What the hell", "Come on bro..!", "Who Are You?", "I'm a Programmer", "I'm a Student", "I'm a Teacher"]
    #liStrBefore = ["Hello", "I'm a Student", "I'm a Teacher"]
    liStrAfter = TranslationHandlerGoogle(liStrBefore).run()
    print(liStrAfter)