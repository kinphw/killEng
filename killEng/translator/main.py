import pandas as pd

from killEng.common.baseIO import BaseIO
from killEng.common import saver
from killEng.common.loader import LoaderFromText
from killEng.translator.handler import TranslationHandler

class Translator(BaseIO):

    def __init__(self):
        self._initSet("번역할 텍스트파일을 선택하세요", "_translated", "xlsx")

    def run(self, bDebug:bool=False):
        # liStrBefore = LoaderFromText(self.strInput).readText()
        liStrBefore = self._read()
        self._getLength(liStrBefore)

        if not bDebug:
            liStrAfter = TranslationHandler(liStrBefore).run()
            saver.SaverTemp.saveTemp(liStrAfter) # 임시 저장
        elif bDebug:
            liStrAfter = saver.SaverTemp.loadTemp() #만약 번역 이후 뻑났을 경우에는 임시파일을 로드 (돈이 드니까)

        self._save(liStrBefore, liStrAfter)

    ##########################################################################################

    def _read(self) -> list[str]:
        print("1. Line별로 번역(기본값)")
        print("2. 전체를 번역 (양이 적은 경우, 개별 추적이 불필요한 경우 등)")
        match (input(">>") or '1'):
            case "1": 
                return LoaderFromText(self.strInput).readText()
            case "2":
                return [LoaderFromText(self.strInput).readTextRaw()]

    def _getLength(self, liStrBefore:list[str]) -> None:
        total_length = sum(len(s) for s in liStrBefore)
        print(f"전체 글자수: {total_length}")

    def _save(self, liStrBefore:list[str], liStrAfter:list[str]) -> None:
        
        bSaveBefore = self._askHow()

        if bSaveBefore: # 번역 전 원문 저장
            dfTranslated = pd.DataFrame(zip(liStrBefore, liStrAfter), columns=["원문", "번역결과"])
        else: # 결과만 저장
            dfTranslated = pd.DataFrame(liStrAfter, columns=["번역결과"])

        saver.SaverFromDf(dfTranslated).saveFacade(self.strOutput)

    def _askHow(self) -> bool:
        bSaveBefore:bool # 번역 전 원문 저장 여부
        print("1> 원문과 결과를 같이 저장")
        print("2> 결과만 저장")
        
        match(input(">>")):
            case "1": bSaveBefore = True
            case "2": bSaveBefore = False

        return bSaveBefore

if __name__=='__main__':
    Translator().run(bDebug=False)