import os

import pandas as pd

class SaverFromListText():

    li:list[str]

    def __init__(self, li:list[str]) -> None:
        self.li = li

    def saveAsText(self, strOutput:str, encoding:str = 'utf-8'):
        with open(strOutput, 'wt', encoding=encoding) as file:
            for item in self.li:
                file.write(item + '\n')
        file_size = os.path.getsize(strOutput)
        print(f"File saved: {strOutput}, Size: {file_size} bytes")

    def saveAsExcel(self, strOutput:str):
        df = pd.DataFrame(self.li, columns=["Text"])
        df.to_excel(strOutput, index=False)
        file_size = os.path.getsize(strOutput)
        print(f"File saved: {strOutput}, Size: {file_size} bytes")