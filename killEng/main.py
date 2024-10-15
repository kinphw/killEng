from killEng.pdfToText.main import PdfToText
from killEng.textPrep.main import TextPrep
from killEng.translator.main import Translator
from killEng.common.lengthCounter import LengthCounter
from killEng.xml.main import SECXmlParser
from killEng.xml.duplicate import SECXmlTagCounter

class KillEng:

    def __init__(self):
        pass

    def run(self):
        while True:
            print("Kill English")
            print("11. PDF to TEXT")
            print("12. TEXT Prep")
            print("------------------")            
            print("21. Text Translate")
            print("------------------")            
            print("31. 텍스트파일 글자수 확인")
            print("32. XML 구조 확인")
            print("33. XML 파싱하여 텍스트로 저장(SEC)")
            print("0. Exit")
            menu = input("Select menu: ")

            if menu == "11": # 1. PDF를 TEXT로 추출    
                PdfToText().run()
            elif menu == "12": # 2. 추출한 TEXT 전처리 
                TextPrep().run()
            elif menu == "21": # 3. API 활용하여 TEXT를 영한번역 (문장단위 api 클래스에 던짐)
                Translator().run()                                
            elif menu == "31":
                LengthCounter().count_characters()
            elif menu == "32":
                SECXmlTagCounter().run()
            elif menu == "33":
                SECXmlParser().run()
            elif menu == "0":
                print("Exit")
                break
            else:
                print("Invalid menu")

if __name__ == "__main__":
    KillEng().run()