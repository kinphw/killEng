from killEng.parser.pdfToText.main import PdfToText
from killEng.translatePrep.main import TextPrep
from killEng.translator.main import Translator
from killEng.common.lengthCounter import LengthCounter
from killEng.parser.sec.main import SECXmlParser
from killEng.parsePrep.sec.duplicate import SECXmlTagCounter
from killEng.common.killSpace import EmptyLineRemover
from killEng.parsePrep.law.readXml import XMLAnalyzer

class KillEng:

    def __init__(self):
        pass

    def run(self):
        while True:
            print("Kill English")
            print("------------------")                        
            print("I. 텍스트 추출 전 전처리") #parsePrep                    
            print("------------------")                                       
            print("  11. XML 구조 확인(SEC)")
            print("  12. XML 구조 확인(LAW)")            
            print("------------------")                                       
            print("II. 파싱 to TEXT") #parser              
            print("------------------")            
            print("  21. PDF to TEXT")            
            print("  22. XML 파싱하여 텍스트로 저장(SEC)")
            print("  23. XML 파싱하여 텍스트로 저장(LAW)")            
            print("------------------")                        
            print("III. 번역 전 텍스트 전처리") #translatePrep
            print("------------------")                                        
            print("  31. Remove Empty Lines from File")            
            print("  32. 텍스트파일 글자수 확인")       
            print("  33. TEXT 자연어 전처리(개행구분)")                 
            print("------------------")                            
            print("IV. 메인 번역(txt)") #translator
            print("------------------")                                                    
            print("  41. Text Translate") #v
            print("------------------")            
            print("0. Exit")
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

            elif menu == "41": # 3. API 활용하여 TEXT를 영한번역 (문장단위 api 클래스에 던짐)
                Translator().run()       

            elif menu == "0":
                print("Exit")
                break
            else:
                print("Invalid menu")

if __name__ == "__main__":
    KillEng().run()