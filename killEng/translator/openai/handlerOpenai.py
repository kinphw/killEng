# input : list[str] : 번역대상
# do : input에 따라 하나씩 또는 여러개씩 번역기 클래스에 던지고 결과를 받아서 데이터프레임에 쌓음
# output : list[str] : 번역결과 => 데이터프레임으로 변경하는 것은 외부에서 처리

# 언어별 핸들러 분리

import tqdm

# from killEng.translator.util.baseTrans import BaseTranslator
# from killEng.translator.google.google import GoogleTranslator
from killEng.translator.openai.openai import OpenaiTranslator
from killEng.translator.util.baseHandler import BaseTranslationHandler
from killEng.translator.util.toolinfo import ToolInfo
from killEng.translator.util.chunkmaker import ChunkedListMaker

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
        self._setBatch()

        match self.intBatch:
            case ToolInfo.SINGLE:
                return self._translateEach()
            case ToolInfo.BATCH_FIXED:
                return self._translateBatch(self.intChunksize)
            case ToolInfo.BATCH_VARIABLE:
                return self._translateBatchVariable()
            case _:
                print("ERROR")
                exit(1)

    def _setVariable(self) -> None:
        if self.intDirection == self.ENKO:
            self.how = "영한"
        elif self.intDirection == self.KOEN:
            self.how = "한영"

    def _setBatch(self) -> None:
        print("1> Single")
        print("2> Batch : 고정갯수")
        print("3> Batch : Tool별 변동갯수 >> 효율적")
        match(input(">>")):
            case "1": 
                self.intBatch = ToolInfo.SINGLE
            case "2": 
                self.intBatch = ToolInfo.BATCH_FIXED
            case "3":
                self.intBatch = ToolInfo.BATCH_VARIABLE
            case _:
                print("잘못된 입력입니다.")
                exit(1)

        if self.intBatch == ToolInfo.BATCH_FIXED:
            print("Chunk size를 선택하세요. 기본값 10")
            size:str = input(">>") or '10'
            self.intChunksize = int(size)

    #########################################################################
    # 한개씩 traslateEach에 던짐
    def _translateEach(self) -> list[str]:

        liStrAfter = []
        for strBefore in tqdm.tqdm(self.liStrBefore, "Translating"):
            strAfter: str = self.objTool.translateEach(strBefore, self.how) #추후 필요시 모델 특정
            liStrAfter.append(strAfter)

        return liStrAfter
    #########################################################################

    def _translateBatch(self, chunk_size:int) -> list[str]:
        liStrAfter:list[str] = []
        for chunk in tqdm.tqdm(
            self._chunk_list(self.liStrBefore, chunk_size),
            desc="Translating",
            total=self._get_total_chunks(self.liStrBefore, chunk_size)
        ):
            liStrAfter.extend(self.objTool.translateBatch(chunk, how=self.how))
        return liStrAfter

    def _chunk_list(self, data, chunk_size):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

    def _get_total_chunks(self, data, chunk_size):
        return (len(data) + chunk_size - 1) // chunk_size

    def _translateBatchVariable(self) -> list[str]:
        liStrAfter:list[str] = []

        max_size_kib = 100  # 128 KiB를 바이트로 변환
        liChunked:list[list[str]] = ChunkedListMaker(self.liStrBefore, max_size_kib).get_chunks()

        for chunk in tqdm.tqdm(liChunked, desc="Translating"):
            liStrAfter.extend(self.objTool.translateBatch(chunk, how=self.how))

        return liStrAfter

if __name__ == "__main__":
    liStrBefore = ["Hello", "World", "Python", "Java", "What the hell", "Come on bro..!", "Who Are You?", "I'm a Programmer", "I'm a Student", "I'm a Teacher"]
    #liStrBefore = ["Hello", "I'm a Student", "I'm a Teacher"]
    liStrAfter = TranslationHandlerOpenai(liStrBefore).run()
    print(liStrAfter)