from killEng.pdfToText.main import PdfToText
from killEng.textPrep.main import TextPrep
from killEng.translator.main import Translator
from killEng.common.lengthCounter import LengthCounter

class KillEng:

    def __init__(self):
        pass

    def run(self):
        while True:
            print("Kill English")
            print("1. PDF to TEXT")
            print("2. TEXT Prep")
            print("3. Text Translate")
            print("9. 글자수 확인")
            print("0. Exit")
            menu = input("Select menu: ")

            if menu == "1": # 1. PDF를 TEXT로 추출    
                PdfToText().run()
            elif menu == "2": # 2. 추출한 TEXT 전처리 
                TextPrep().run()
            elif menu == "3": # 3. API 활용하여 TEXT를 영한번역 (문장단위 api 클래스에 던짐)
                Translator().run()                                
            elif menu == "9":
                LengthCounter().count_characters()
            elif menu == "0":
                print("Exit")
                break
            else:
                print("Invalid menu")

if __name__ == "__main__":
    KillEng().run()