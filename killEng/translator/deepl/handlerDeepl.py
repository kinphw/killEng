# input : list[str] : 번역대상
# do : input에 따라 하나씩 또는 여러개씩 번역기 클래스에 던지고 결과를 받아서 데이터프레임에 쌓음
# output : list[str] : 번역결과 => 데이터프레임으로 변경하는 것은 외부에서 처리

# 언어별 핸들러 분리

import pandas as pd
import tqdm

# from killEng.translator.util.baseTrans import BaseTranslator
from killEng.translator.deepl.deepl import DeepLTranslator
from killEng.translator.util.chunkmaker import ChunkedListMaker
from killEng.translator.util.toolinfo import ToolInfo
from killEng.translator.util.baseHandler import BaseTranslationHandler

class TranslationHandlerDeepl(BaseTranslationHandler):

    liStrBefore:list[str]
    objTool:DeepLTranslator
    
    intBatch:int
    intChunksize:int

    source_lang:str #DEEPL
    target_lang:str #DEEPL

    bDebug:bool

    def __init__(self, liStrBefore:list[str]) -> None:        
        self.liStrBefore = liStrBefore
        self.objTool = DeepLTranslator()

         # 번역방향 설정부
        super().__init__()
        self._setVariable() # 번역방향에 따라 소스, 타겟 언어 변수를 클래스 변수로 선언

    def run(self, bDebug:bool = False) -> list[str]:        

        self._setBatch()
        self.bDebug = bDebug

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

    def _setBatch(self) -> None:

        #호출방법
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

        # 고정배치인 경우 chunk size 설정
        if self.intBatch == ToolInfo.BATCH_FIXED:            
            print("Chunk size를 선택하세요. 기본값 10")
            size:str = input(">>") or '10'
            self.intChunksize = int(size)

    def _setVariable(self) -> None:

        #방향에 따라 분기
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
            strResult = self.objTool.translateEach(strBefore, source_lang=self.source_lang, target_lang=self.target_lang)
            liStrAfter.append(strResult)
        return liStrAfter

    #########################################################################
    # 고정 갯수씩 traslateBatch에 던짐 (그렇게 효율적이지는 않은 것 같음)
    def _translateBatch(self, chunk_size:int) -> list[str]:
        
        liStrAfter:list[str] = []
        for chunk in tqdm.tqdm(
            self._chunk_list(self.liStrBefore, chunk_size)
            , desc = "Translating"
            , total = self._get_total_chunks(self.liStrBefore, chunk_size)
            ):
            
            liStrAfter.extend(self.objTool.translateBatch(chunk, source_lang=self.source_lang, target_lang=self.target_lang))

        return liStrAfter

    # 리스트를 청크로 나누는 제너레이터 함수
    def _chunk_list(self, data, chunk_size):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]    

    def _get_total_chunks(self, data, chunk_size):
        return (len(data) + chunk_size - 1) // chunk_size        

    #########################################################################

    def _translateBatchVariable(self) -> list[str]:
        
        liStrAfter:list[str] = []

        max_size_kib = 100 # 128 KiB를 바이트로 변환 : Deepl
        liChunked:list[list[str]] = ChunkedListMaker(self.liStrBefore, max_size_kib).get_chunks()

        for chunk in tqdm.tqdm(liChunked, desc = "Translating"):
            if self.bDebug:            
                total_length = sum(len(item) for item in chunk)
                print(f"Chunk length: {total_length}")
            else:
                liStrAfter.extend(self.objTool.translateBatch(chunk, source_lang=self.source_lang, target_lang=self.target_lang))            

        if self.bDebug: exit(1)       

        return liStrAfter
    
    #########################################################################

if __name__ == "__main__":
    liStrBefore = ["Hello", "World", "Python", "Java", "What the hell", "Come on bro..!", "Who Are You?", "I'm a Programmer", "I'm a Student", "I'm a Teacher"]
    #liStrBefore = ["Hello", "I'm a Student", "I'm a Teacher"]
    liStrAfter = TranslationHandlerDeepl(liStrBefore).run()
    print(liStrAfter)