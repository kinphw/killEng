import abc

# Handler가 아니라 실제로 번역하는 Class에 상속시키는 추상 클래스
class BaseTranslator(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def translateEach(self, text:str) -> str:
        pass

    @abc.abstractmethod
    def translateBatch(self, liText:list[str]) -> list[str]:
        pass