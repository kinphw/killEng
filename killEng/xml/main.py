import pandas as pd
from lxml import etree

# XML 문자열을 파일로부터 읽어옴
root = etree.parse('test/2024-05137.xml')

# 원하는 태그의 텍스트를 추출하여 리스트로 반환
def extract_text_tags(root):
    extracted_texts = []
    # <HD>, <P>, <FP> 태그를 모두 순회
    for elem in root.iter():
        # <FTNT> 내부의 <P> 태그는 무시
        if elem.tag == 'P' and elem.getparent().tag == 'FTNT':
            continue
        # <FTNT> 외부의 <HD>, <P>, <FP> 태그의 텍스트만 추가
        if elem.tag in {'HD', 'P', 'FP'}:
            # <SU> 태그의 텍스트를 제외하고 수집
            text_content = ''.join(
                text for text in elem.itertext() if elem.find('.//SU') is None or text not in [su.text for su in elem.findall('.//SU')]
            ).strip()
            # 중복 공백을 제거
            clean_text = ' '.join(text_content.split())
            if clean_text:
                extracted_texts.append(clean_text)
    return extracted_texts

# 결과 리스트 반환
texts_list = extract_text_tags(root)

# texts_list를 각 요소를 개행문자로 구분한 후 텍스트 파일로 저장
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(texts_list))