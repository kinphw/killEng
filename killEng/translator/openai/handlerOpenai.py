# input : list[str] : 번역대상
# do : input에 따라 하나씩 또는 여러개씩 번역기 클래스에 던지고 결과를 받아서 데이터프레임에 쌓음
# output : list[str] : 번역결과 => 데이터프레임으로 변경하는 것은 외부에서 처리

# 언어별 핸들러 분리

import tqdm

# from killEng.translator.util.baseTrans import BaseTranslator
# from killEng.translator.google.google import GoogleTranslator
from killEng.translator.openai.openai import OpenaiTranslator
from killEng.translator.util.baseHandler import BaseTranslationHandler

class TranslationHandlerOpenai(BaseTranslationHandler):

    liStrBefore:list[str]
    objTool:OpenaiTranslator    

    how:str #OPENAI "한영 or 영한"

    def __init__(self, liStrBefore:list[str]) -> None:
        self.liStrBefore = liStrBefore
        self.objTool = OpenaiTranslator()
        super().__init__()
        self._setVariable()

    def run(self) -> list[str]:
        return self._translateEach()

    def _setVariable(self) -> None:
        if self.intDirection == self.ENKO:
            self.how = "영한"
        elif self.intDirection == self.KOEN:
            self.how = "한영"

    #########################################################################
    # 한개씩 traslateEach에 던짐
    def _translateEach(self) -> list[str]:

        liStrAfter = []
        for strBefore in tqdm.tqdm(self.liStrBefore, "Translating"):
            strAfter: str = self.objTool.translateEach(strBefore, self.how) #추후 필요시 모델 특정
            liStrAfter.append(strAfter)

        return liStrAfter
    #########################################################################

if __name__ == "__main__":
    liStrBefore = ["Hello", "World", "Python", "Java", "What the hell", "Come on bro..!", "Who Are You?", "I'm a Programmer", "I'm a Student", "I'm a Teacher"]
    #liStrBefore = ["Hello", "I'm a Student", "I'm a Teacher"]
    liStrAfter = TranslationHandlerOpenai(liStrBefore).run()
    print(liStrAfter)