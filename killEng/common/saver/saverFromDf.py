import os

import pandas as pd

from killEng.common.stringHandler import StringHandler as sh

# 데이터프레임을 저장하는 Saver 클래스
class SaverFromDf():
    
    df:pd.DataFrame
    
    def __init__(self, df:pd.DataFrame) -> None:
        self.df = df
    
    def saveAsExcel(self, strOutput:str):
        self.df.to_excel(strOutput, index=False)
        file_size = os.path.getsize(strOutput)
        print(f"File saved: {strOutput}, Size: {file_size} bytes")    

    def saveAsText(self, strOutput:str, encoding:str = 'utf-8'):
        with open(strOutput, 'wt', encoding=encoding) as file:
            for _, row in self.df.iterrows():
                file.write('\n'.join(map(str, row)) + '\n')
        file_size = os.path.getsize(strOutput)
        print(f"File saved: {strOutput}, Size: {file_size} bytes")

    #선택에 따라 분기할 경우
    def saveFacade(self, strOutput:str):
        while True:
            save_option = input("Enter 1 to save as Excel, 2 to save as Text: ")
            
            if save_option == "1":
                strOutput_new = sh.change_extension(strOutput, "xlsx")
                self.saveAsExcel(strOutput_new)
                break
            elif save_option == "2":
                strOutput_new = sh.change_extension(strOutput, "txt")
                self.saveAsText(strOutput_new)
                break
            else:
                print("Invalid option. No file will be saved.")
                continue