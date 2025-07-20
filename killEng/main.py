from killEng.parser.pdfToText.main import PdfToText
from killEng.translatePrep.main import TextPrep
from killEng.translator.main import Translator
from killEng.common.lengthCounter import LengthCounter
from killEng.parser.sec.main import SECXmlParser
from killEng.parsePrep.sec.duplicate import SECXmlTagCounter
from killEng.common.killSpace import EmptyLineRemover
from killEng.parsePrep.law.readXml import XMLAnalyzer
from killEng.translatePrep.numbered import NumberedLineMerger

from killEng.common.ansi import ANSIColor

class KillEng:

    def __init__(self):
        pass

    def run(self):
        while True:
            print(ANSIColor.colorize("Kill English", "bold"))
            print("------------------")
            print(ANSIColor.colorize("I. 텍스트 추출 전 전처리", "yellow"))
            print("------------------")
            print(ANSIColor.colorize("  11. XML 구조 확인(SEC)", "green"))
            print(ANSIColor.colorize("  12. XML 구조 확인(LAW)", "green"))
            print("------------------")
            print(ANSIColor.colorize("II. 파싱 to TEXT", "yellow")) #parser
            print("------------------")
            print(ANSIColor.colorize("  21. PDF to TEXT", "green"))
            print(ANSIColor.colorize("  22. XML 파싱하여 텍스트로 저장(SEC)", "green"))
            print(ANSIColor.colorize("  23. XML 파싱하여 텍스트로 저장(LAW)", "green"))
            print("------------------")
            print(ANSIColor.colorize("III. 번역 전 텍스트 전처리", "yellow")) #translatePrep
            print("------------------")
            print(ANSIColor.colorize("  31. Remove Empty Lines from File", "green"))
            print(ANSIColor.colorize("  32. 텍스트파일 글자수 확인", "green"))
            print(ANSIColor.colorize("  33. TEXT 자연어 전처리(개행구분)", "green"))
            print(ANSIColor.colorize("  34. (FOR MiCAR) 번호가 붙은 문장 병합", "green")) #numbered.py
            print("------------------")
            print(ANSIColor.colorize("IV. 메인 번역(txt)", "yellow")) #translator
            print("------------------")
            print(ANSIColor.colorize("  41. Text Translate", "green")) #v
            print("------------------")
            print(ANSIColor.colorize("0. Exit", "red"))
            menu = input("Select menu: ")

            if menu == "11":
                SECXmlTagCounter().run()
            elif menu == "12":
                analyzer = XMLAnalyzer()
                analyzer.run()

            elif menu == "21": # 1. PDF를 TEXT로 추출    
                PdfToText().run()
            elif menu == "22":
                SECXmlParser().run()

            elif menu == "31":
                remover = EmptyLineRemover()
                remover.select_files()
                remover.remove_empty_lines()
            elif menu == "32":
                LengthCounter().count_characters()                
            elif menu == "33": # 2. 추출한 TEXT 전처리 
                TextPrep().run()                
            elif menu == "34": # 3. 번호가 붙은 문장 병합
                merger = NumberedLineMerger()
                merger.run()                

            elif menu == "41": # 3. API 활용하여 TEXT를 영한번역 (문장단위 api 클래스에 던짐)
                Translator().run()       

            elif menu == "0":
                print("Exit")
                break
            else:
                print("Invalid menu")

if __name__ == "__main__":
    KillEng().run()