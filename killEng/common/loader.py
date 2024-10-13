# Text 또는 Excel을 읽어서 list나 DataFrame으로 반환하는 클래스

import pandas as pd

class LoaderFromText:

    def __init__(self, path:str, bText:bool = True):
        self.path = path

    def readTextRaw(self, encoding:str = 'utf-8') -> str:
        with open(self.path, 'rt', encoding=encoding) as f:
            return f.read()
        
    def readText(self, encoding: str = 'utf-8') -> list[str]:
        with open(self.path, 'rt', encoding=encoding) as f:
            return [line.rstrip('\n') for line in f.readlines()] # 개행문자 제거
        
if __name__ == "__main__":
    tmp = LoaderFromText("test/test.txt").readTextRaw()

    tmp = LoaderFromText("test/test.txt").readText()

    print("END")

