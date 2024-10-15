from lxml import etree
from killEng.common.baseIO import BaseIO

class SECXmlParser(BaseIO):

    def __init__(self):
        self._initSet("Parsing할 SEC XML파일 선택", "_parsed", "txt")

    def run(self):
        root = etree.parse(self.strInput)
        texts_list = self.extract_text_tags(root)
        with open(self.strOutput, 'w', encoding='utf-8') as f:
            f.write('\n'.join(texts_list))
        print(f"파싱된 텍스트를 {self.strOutput}에 저장하였습니다.")

    def extract_text_tags(self, root):
        extracted_texts = []
        for elem in root.iter():
            # 조건1 : <FTNT> 내부의 <P> 태그는 아예 무시
            if elem.tag == 'P' and elem.getparent().tag == 'FTNT':
                continue

            # 조건 2 : 특정 태그만 ㅇ니식
            # <HD>, <P>, <FP> : 기본 내용들
            # <SECTNO>, <SUBJECT>, <AMDPAR> : 추가 내용들
            # <TTITLE>, <CHED>, <ROW>, <ENT>, <LI> 표 관련 내용들
            if elem.tag in {
                'HD', 'P', 'FP'
                , 'SECTNO', 'SUBJECT', 'AMDPAR'
                , 'TTITLE', 'CHED', 'ROW', 'ENT'}: #'LI'}:
                
                # 기본적으로는 elem.text만 포함
                text_content = elem.text if elem.text else ''

                ###########################################################################
                ## ENT보다 상위로 올라가서 표 전체에 itertext() 적용 고려!!! #############################
                # <P> 또는 <ENT> 태그의 경우에만 itertext()로 모든 하위 텍스트를 포함하되 <SU> 제외
                if elem.tag in {'P', 'ENT'}:
                    su_texts = [su.text for su in elem.findall('.//SU')]
                    filtered_texts = [
                        text for text in elem.itertext()
                        if text and text not in su_texts
                    ]
                    # filtered_texts에서 SU를 제외한 텍스트를 결합
                    text_content = ' '.join(filtered_texts).strip()

                # 텍스트들을 결합하고, 양쪽 공백 제거                
                clean_text = ' '.join(''.join(text_content).split())

                if clean_text:
                    # 태그별로 구분하여 라벨 추가
                    if elem.tag == 'TTITLE':
                        clean_text = f"<표> {clean_text}"
                    elif elem.tag == 'CHED':
                        clean_text = f"<표 헤더> {clean_text}"
                    elif elem.tag == 'ENT' and elem.getparent().tag == 'ROW':
                        clean_text = f"<표 내용> {clean_text}"
                    
                    extracted_texts.append(clean_text)

        return extracted_texts

if __name__ == "__main__":
    SECXmlParser().run()
