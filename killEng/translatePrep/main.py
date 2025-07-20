from killEng.common.baseIO import BaseIO
from killEng.common.loader import LoaderFromText
from killEng.common import saver
from killEng.translatePrep.tokenizer import TextTokenizer
from killEng.translatePrep.deleteEmptyLines import DeleteEmptyLines

#from killEng.common.saver.saverTemp import SaverFromListText

# PDF를 변환한 Text파일을 읽어서 자연스럽게 전처리 (NLTK 사용)

# NLTK에서 사용할 데이터 다운로드 (최초 실행 시)
# nltk.download('punkt')

class TextPrep(BaseIO):

    def __init__(self):
        self._initSet("자연어 전처리할 Text 파일을 선택하세요.", "_cleaned", "txt")

    def run(self):

        print("1. 문장 단위로 분할")
        print("2. 공백 행 삭제")
        match input(">>"):
            case "1": self._run_tokenize()
            case "2": self._run_delete_empty_lines()
            case _:
                print("잘못된 입력입니다.")
                exit(1)

    def _run_tokenize(self) -> None:
        text:str = LoaderFromText(self.strInput).readTextRaw() # Raw로 읽어야 함
        sentences = TextTokenizer(text).run()
        saver.SaverFromListText(sentences).saveAsText(self.strOutput)

    def _run_delete_empty_lines(self) -> None:
        liText:str = LoaderFromText(self.strInput).readText()
        liTextProcessed:list[str] =  DeleteEmptyLines(liText).run()
        saver.SaverFromListText(liTextProcessed).saveAsText(self.strOutput)        

if __name__ == "__main__":
    TextPrep().run()