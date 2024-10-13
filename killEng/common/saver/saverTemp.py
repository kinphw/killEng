import os
import pickle
from killEng.common.myFileDialog import MyFileDialog as myfd
            
class SaverTemp():

    @staticmethod
    def saveTemp(obj:any, strOutput:str = "temp.pickle"):
        with open(strOutput, 'wb') as file:
            pickle.dump(obj, file)
        file_size = os.path.getsize(strOutput)
        print(f"File saved: {strOutput}, Size: {file_size} bytes")

    @staticmethod
    def loadTemp(strInput:str = ""):
        if strInput == "":
            strInput = myfd.askopenfilename("임시파일을 선택하세요.")

        with open(strInput, 'rb') as file:
            obj = pickle.load(file)
            
        return obj

if __name__ == "__main__":
    list = ["test1", "test2", "test3"]

    SaverTemp.saveTemp(list, "test.pickle")
    list2 = SaverTemp().loadTemp("test.pickle")          
    