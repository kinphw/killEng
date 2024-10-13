#GITHUB에 보관할 수 없는 API KEY를 로컬에서 읽어서 반환하는 클래스
class KeyReader:
    _instance = None  # 싱글턴 인스턴스 저장
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(KeyReader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        with open('key', 'r', encoding='utf-8') as key_file:
            self.auth_key = key_file.read().strip()

    def getKey(self):
        return self.auth_key

if __name__ == "__main__":
    tmp = KeyReader().getKey()
    print(tmp)