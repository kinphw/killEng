# deepl.py
import requests
from dotenv import load_dotenv
import os
import urllib3

from killEng.translator.util.baseTrans import BaseTranslator

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DeepLTranslator(BaseTranslator):
    
    _instance = None  # 싱글턴 인스턴스 저장
    auth_key:str
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DeepLTranslator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        load_dotenv("key.env")        
        # self.auth_key = KeyReader().getKey()
        self.auth_key = os.getenv("DEEPL_API_KEY")
        if self.auth_key is None:
            raise EnvironmentError(f"Environment variable 'key' not found")

        # self.url = 'https://api-free.deepl.com/v2/translate'  # 무료 API 엔드포인트
        self.url = 'https://api.deepl.com/v2/translate'

    def translateEach(self, text:str, source_lang='EN', target_lang='KO') -> str:

        params = {
            'auth_key': self.auth_key,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'text': text
        }

        # API에 배치 요청
        response = requests.post(self.url, data=params, verify=False) #추후 제거

        if response.status_code == 200:
            result = response.json()
            translation_text:str

            if result['translations'][0]['text'] is not None:
                translation_text = result['translations'][0]['text']
            else:
                translation_text = ""
            
            return translation_text
                        
        else:
            print(f"오류 발생: {response.status_code} - {response.text}")            
            return ""

    def translateBatch(self, liText:list[str], source_lang='EN', target_lang='KO') -> list[str]:        

        params = {
            'auth_key': self.auth_key,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'text': liText  # 현재 배치 전송
        }

        # API에 배치 요청
        response = requests.post(self.url, data=params, verify=False) #추후 제거

        if response.status_code == 200:
            result = response.json()

            list_translated_texts = []
            for item in result['translations']:
                if item['text'] is not None:
                    list_translated_texts.append(item['text'])
                else:
                    list_translated_texts.append("")
            
            return list_translated_texts
            
        else:
            print(f"오류 발생: {response.status_code} - {response.text}")
            return [""] * len(liText) # liText의 길이만큼 빈 문자열을 반환

if __name__ == "__main__":
    #tmp = DeepLTranslator().translateEach("Hello, World!")
    tmp = DeepLTranslator().translateBatch(["Hello, World!", "Goodbye, World!"])
    print(tmp)