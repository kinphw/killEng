import nltk
import re
import spacy

# nltk.download('punkt')

class TextTokenizer():

    text:str

    def __init__(self, text:str):
        self.text = text

    def run(self) -> list[str]:

        # 정규 표현식으로 불필요한 개행 문자 제거
        text = re.sub(r'\n+', ' ', self.text)  # 모든 개행을 공백으로 변환
        text = re.sub(r'\s+', ' ', self.text).strip()  # 연속된 공백을 하나로 줄임

        print("1. NLTK")
        print("2. SpaCy")
        match(input(">>")):
            case "1": return self._clean_text_nltk(text)
            case "2": return self._clean_text_spacy(text)
            case _: 
                print("잘못된 입력입니다.")
                exit(1)

    def _clean_text_nltk(self, text) -> list[str]:

        # 문장 단위로 텍스트를 분할
        sentences = nltk.sent_tokenize(text)

        # # 문장들을 연결하여 자연스러운 문장 흐름으로 변환
        # cleaned_text = ' '.join(sentences)
        return sentences

    def _clean_text_spacy(self, text) -> list[str]:

        nlp = spacy.load('en_core_web_sm')
        nlp.max_length = 2000000
        doc = nlp(text)

        sentences:list[str] = [sent.text for sent in doc.sents]
        return sentences


if __name__ == "__main__":
    text = "안녕하세요. 박형원입니다. 넌 누구냐?"
    li = TextTokenizer(text).run()
    print(li)