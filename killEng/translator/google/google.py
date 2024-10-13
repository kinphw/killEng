import requests
import urllib3
from urllib.parse import quote
from html import unescape

from killEng.translator.util.baseTrans import BaseTranslator

class GoogleTranslator(BaseTranslator):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GoogleTranslator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Ensure __init__ is only called once
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.initialized = True

    def translateEach(self, text:str, source_lang='en', target_lang='ko'):

        # 언어 설정 
        # self.source_lang = source_lang
        # self.target_lang = target_lang
        self.base_url = "https://translate.google.com/m?hl={}&sl={}&tl={}&ie=UTF-8&prev=_m&q=".format(
            source_lang, source_lang, target_lang
        )

        # URL 인코딩하여 요청 URL 생성
        url = self.base_url + quote(text)
        
        # 요청 보내기
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, verify=False) #추후 제거
        
        if response.status_code == 200:
            # 응답에서 번역 결과 추출
            start_idx = response.text.find('class="result-container">') + len('class="result-container">')
            end_idx = response.text.find('</div>', start_idx)
            translated_text = response.text[start_idx:end_idx]
            
            return unescape(translated_text.strip())
        else:
            raise Exception("Translation failed with status code: {}".format(response.status_code))

    def translateBatch(self, liText):
        print("구글 번역기는 배치 번역을 지원하지 않습니다.")
        exit(1)

# 예제 사용
if __name__ == "__main__":
    translator = GoogleTranslator(source_lang='ko', target_lang='en')
    translated_text = translator.translate("너 이름이 뭐니?")
    print(translated_text)
