# 실제 번역 util이 아니라 각 Tool별 번역 로직 핸들러 Class에 상속시키는 클래스 (not abs)

class BaseTranslationHandler:

    #번역방향 상수
    ENKO = 1
    KOEN = 2

    #번역방향 클래스변수
    intDirection:int # 번역 방향

    def __init__(self) -> None:
        self.askDirection()

    #임의로 설정
    def setDirection(self, intDirection:int) -> None:
        self.intDirection = intDirection

    #질의로 설정
    def askDirection(self) -> None:
        print("1> 영한")
        print("2> 한영")
        match input(">>"):
            case "1": self.intDirection = self.ENKO
            case "2": self.intDirection = self.KOEN
            case _: 
                print("잘못된 입력입니다.")
                exit(1)