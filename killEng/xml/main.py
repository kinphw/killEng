from lxml import etree
from killEng.common.baseIO import BaseIO

class SECXmlParser(BaseIO):

    def __init__(self):
        self._initSet("Parsing할 SEC XML파일 선택", "_parsed", "txt")

    def run(self):
        # XML 문자열을 파일로부터 읽어옴
        root = etree.parse(self.strInput)   

        # 결과 리스트 반환
        texts_list = self.extract_text_tags(root)

        # texts_list를 각 요소를 개행문자로 구분한 후 텍스트 파일로 저장
        with open(self.strOutput, 'w', encoding='utf-8') as f:
            f.write('\n'.join(texts_list))

        print(f"파싱된 텍스트를 {self.strOutput}에 저장하였습니다.")

    # 원하는 태그의 텍스트를 추출하여 리스트로 반환
    def extract_text_tags(self, root):
        extracted_texts = []
        # <HD>, <P>, <FP> 태그를 모두 순회
        for elem in root.iter():
            # <FTNT> 내부의 <P> 태그는 무시
            if elem.tag == 'P' and elem.getparent().tag == 'FTNT':
                continue
            # <FTNT> 외부의 <HD>, <P>, <FP> 태그의 텍스트만 추가
            if elem.tag in {'HD', 'P', 'FP', 'SECTNO', 'SUBJECT', 'AMDPAR'}:
                # <SU> 태그의 텍스트를 제외하고 수집
                # text_content = ''.join(
                #     text for text in elem.itertext() if elem.find('.//SU') is None or text not in [su.text for su in elem.findall('.//SU')]
                # ).strip()

                # 1. <SU> 태그의 존재 여부 확인
                has_su_tag = elem.find('.//SU') is not None

                # 2. <SU> 태그 내의 텍스트들을 리스트로 생성
                su_texts = [su.text for su in elem.findall('.//SU')] #. : 현재 요소 // : 하위 요소 재귀적탐색

                # 3. <SU> 태그가 없거나, <SU> 태그 텍스트가 아닌 경우에만 텍스트 포함
                filtered_texts = [
                    text for text in elem.itertext()
                    if not has_su_tag or text not in su_texts
                ]

                # 4. 텍스트들을 결합하고, 양쪽 공백 제거
                text_content = ''.join(filtered_texts).strip()

                # 중복 공백을 제거
                clean_text = ' '.join(text_content.split())

                if clean_text:
                    extracted_texts.append(clean_text)
        return extracted_texts            
    
if __name__ == "__main__":
    SECXmlParser().run()