import requests
import urllib3
from urllib.parse import quote
from html import unescape
import os
from dotenv import load_dotenv

from killEng.translator.util.baseTrans import BaseTranslator

class OpenaiTranslator(BaseTranslator):
    _instance = None
    api_key:str

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OpenaiTranslator, cls).__new__(cls)
        return cls._instance

    def __init__(self): #영한 or 한영
        if not hasattr(self, 'initialized'):  # Ensure __init__ is only called once
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            # .env 파일에서 OpenAI API 키 불러오기
            load_dotenv("key.env")
            self.api_key = os.getenv("OPENAI_API_KEY")            
            if self.api_key is None:
                raise EnvironmentError(f"Environment variable 'key' not found")

            self.initialized = True

    def translateEach(self, text:str, how:str="영한", model:str="gpt-3.5-turbo") -> str:
        # OpenAI API 엔드포인트 및 헤더 설정
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"}

        system_content:str
        if how == "영한":
            system_content = "Translate the following English text to Korean."
        elif how == "한영":
            system_content = "Translate the following Korean text to English."
        
        # 요청 데이터 설정
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": text}
            ],
            "temperature": 0.3}
        
        # 요청 보내기
        response = requests.post(url, headers=headers, json=data)

        # 응답 확인 및 번역 출력
        if response.status_code == 200:
            translated_text = response.json()['choices'][0]['message']['content']
            return translated_text
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.json())
            exit(1)

    def translateBatch(self, liText:list[str], how:str="영한", model:str="gpt-3.5-turbo") -> list[str]:
        """
        Translate a batch of texts using OpenAI API.

        :param liText: List of texts to translate.
        :param how: Translation direction ("영한" or "한영").
        :param model: OpenAI model to use for translation.
        :return: List of translated texts.
        """
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        system_content = "Translate the following English text to Korean." if how == "영한" else "Translate the following Korean text to English."

        # Prepare messages for batch translation
        messages = [{"role": "system", "content": system_content}]
        for text in liText:
            messages.append({"role": "user", "content": text})

        data = {
            "model": model,
            "messages": messages,
            "temperature": 0.3
        }

        # Send request
        response = requests.post(url, headers=headers, json=data)

        # Process response
        if response.status_code == 200:
            choices = response.json()['choices']
            return [choice['message']['content'] for choice in choices]
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.json())
            exit(1)
# 예제 사용
if __name__ == "__main__":
    translator = OpenaiTranslator()
    translated_text = translator.translateEach("키즈카페는 정말 행복한 곳입니다.", how="한영")
    print(translated_text)

