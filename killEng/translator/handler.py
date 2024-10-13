# input : list[str] : 번역대상
# do : input에 따라 하나씩 또는 여러개씩 번역기 클래스에 던지고 결과를 받아서 데이터프레임에 쌓음
# output : list[str] : 번역결과 => 데이터프레임으로 변경하는 것은 외부에서 처리

# 언어별 핸들러 분리

from killEng.translator.deepl.handlerDeepl import TranslationHandlerDeepl
from killEng.translator.google.handlerGoogle import TranslationHandlerGoogle
from killEng.translator.openai.handlerOpenai import TranslationHandlerOpenai
from killEng.translator.util.toolinfo import ToolInfo

class TranslationHandler:

    liStrBefore:list[str]
    intTool:int    

    def __init__(self, liStrBefore:list[str]) -> None:
        self.liStrBefore = liStrBefore

    def run(self) -> list[str]:
        
        self._setTool()        

        match self.intTool:
            case ToolInfo.GOOGLE:
                return TranslationHandlerGoogle(self.liStrBefore).run()
            case ToolInfo.DEEPL:
                return TranslationHandlerDeepl(self.liStrBefore).run()
            case ToolInfo.OPENAI:
                return TranslationHandlerOpenai(self.liStrBefore).run()
            case _:
                print("ERROR")
                exit(1)

    #########################################################################

    def _setTool(self) -> None:    
        print("1> Google(무료)")
        print("2> Deepl(유료)")
        print("3> OpenAI(유료)")
        match(input(">>")):
            case "1": self.intTool = ToolInfo.GOOGLE
            case "2": self.intTool = ToolInfo.DEEPL
            case "3": self.intTool = ToolInfo.OPENAI
            case _: 
                print("잘못된 입력입니다.")
                exit(1)

        # self._setToolObject()                

if __name__ == "__main__":
    liStrBefore = ["Hello", "World", "Python", "Java", "What the hell", "Come on bro..!", "Who Are You?", "I'm a Programmer", "I'm a Student", "I'm a Teacher"]
    #liStrBefore = ["Hello", "I'm a Student", "I'm a Teacher"]
    liStrAfter = TranslationHandler(liStrBefore).run()
    print(liStrAfter)