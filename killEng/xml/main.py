from lxml import etree
from killEng.common.baseIO import BaseIO

class SECXmlParser(BaseIO):

    # 아예 조상에 포함되어 있으면 생략할 태그 리스트
    set0:set = {'FTNT'}
    # 하위요소 iter()해서 추출할 태그
    set1:set = {'P',
                'GPOTABLE'} #'ENT',
    # P는 내부에 E 태그 등을 포함하고 tail도 있는 경우가 많아서 반드시 포함해야 함

    # text만 추출할 태그
    set2:set = {
                'AGY', 'ACT', 'SUM', 'EFFDATE', 'SECTION', # 수준을 내림
                'HD', 'FP'
                , 'SECTNO', 'SUBJECT', 'AMDPAR'
                , 'TTITLE', 'CHED', 'ROW'}

    def __init__(self, bDebug:bool=False):
        self._initSet("Parsing할 SEC XML파일 선택", "_parsed", "txt")

        #bDebug면 묶음들을 개별로 내림 (즉 분해함)
        # if bDebug:
        #     li = ['AGY', 'ACT', 'SUM', 'EFFDATE', 'SECTION']
        #     for ele in li:
        #         self.set1.remove(ele)
        #         self.set2.add(ele)

    def run(self):
        root = etree.parse(self.strInput)
        texts_list = self.extract_text_tags(root)
        with open(self.strOutput, 'w', encoding='utf-8') as f:
            f.write('\n'.join(texts_list))
        print(f"파싱된 텍스트를 {self.strOutput}에 저장하였습니다.")

    def check_parent(self, elem,  set:set) -> bool:        
        parent = elem.getparent()
        while parent is not None:
            if parent.tag in set:
                # continue  # 조상 중 <P> 태그가 있는 경우, 현재 elem을 건너뜀
                return True
            parent = parent.getparent()
        return False

    def extract_text_tags(self, root):
        
        extracted_texts = []
        
        for elem in root.iter():

            text_content:str = ''
            # 조건1 : <FTNT> 내부의 <P> 태그는 아예 무시
            # if elem.tag == 'P' and elem.getparent().tag == 'FTNT':
            #     continue
            if self.check_parent(elem, self.set0):
                continue

            # 조건2 : 조상 중에 set1이 있으면 무시 : 왜냐면 스스로 set1일 경우에 아래에 걸리니까
            elif self.check_parent(elem, self.set1):
                continue            
            # 조건1-2
            # ste1, set2에 있는 것(P) 은 set1에만 걸려야함
            # # 그래서 현재 태그가 set2이고 부모가 set1이면 continue

            # 조건2 : P와 ENT 태그의 경우에만 itertext()로 모든 하위 텍스트를 포함하되 SU 제외
            ###########################################################################
            ## ENT보다 상위로 올라가서 표 전체에 itertext() 적용 고려!!! #############################
            # <P> 또는 <ENT> 태그의 경우에만 itertext()로 모든 하위 텍스트를 포함하되 <SU> 제외
            elif elem.tag in self.set1:
                su_texts = [su.text for su in elem.findall('.//SU')]
                filtered_texts = [
                    text for text in elem.itertext()
                    if text and text not in su_texts
                ]

                # 이 단계에서 filtered_text는 List

                # List => str 가공1단계 filtered_texts에서 SU를 제외한 텍스트를 결합
                text_content_before = ' '.join(filtered_texts).strip()

                # str => str
                # 가공2단계 텍스트들을 결합하고, 양쪽 공백 제거                
                text_content = ' '.join(''.join(text_content_before).split())

                if elem.tag == 'GPOTABLE': #표인 경우에는 표 표시 추가
                    text_content = f"<표> {text_content}"

            # 조건 3 : 개별 태그 인식
            # <HD>, <P>, <FP> : 기본 내용들
            # <SECTNO>, <SUBJECT>, <AMDPAR> : 추가 내용들
            # <TTITLE>, <CHED>, <ROW>, <ENT>, <LI> 표 관련 내용들
            elif elem.tag in self.set2: #'LI'}:
                
                if self.check_parent(elem, self.set1):
                    continue 

                # # 분리조건 추가: 조상 태그 중에 <P> 또는 <ENT> 태그가 있는 경우 무시
                # parent = elem.getparent()
                # while parent is not None:
                #     if parent.tag in self.set1:
                #         continue  # 조상 중 <P> 태그가 있는 경우, 현재 elem을 건너뜀
                #     parent = parent.getparent()

                if self.check_parent(elem, self.set1):
                    continue

                # 기본적으로는 elem.text만 포함
                text_content_before = elem.text if elem.text else ''
                
                # str => str
                text_content = ' '.join(''.join(text_content_before).split())                

                # if clean_text:
                #     # 태그별로 구분하여 라벨 추가
                #     if elem.tag == 'TTITLE':
                #         clean_text = f"<표> {clean_text}"
                #     elif elem.tag == 'CHED':
                #         clean_text = f"<표 헤더> {clean_text}"
                #     elif elem.tag == 'ENT' and elem.getparent().tag == 'ROW':
                        # clean_text = f"<표 내용> {clean_text}"
                    
            if text_content:
                extracted_texts.append(text_content)
                text_content = '' #초기화

        return extracted_texts

if __name__ == "__main__":
    SECXmlParser().run()
