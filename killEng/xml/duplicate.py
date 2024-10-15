import xml.etree.ElementTree as ET

def get_unique_tag_paths(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    unique_paths = set()

    def parse_element(element, path):
        # 현재 경로 업데이트 (부모 경로 + 현재 태그)
        current_path = f"{path}/{element.tag}"
        # 경로를 집합에 추가
        unique_paths.add(current_path)
        # 자식 요소들에 대해 재귀적으로 경로를 탐색
        for child in element:
            parse_element(child, current_path)

    parse_element(root, "")
    return unique_paths

# 사용 예시: 'sample.xml' 파일의 태그 경로를 파악하여 출력
xml_file_path = 'test/2024-05137.xml'  # 분석할 XML 파일 경로
paths = get_unique_tag_paths(xml_file_path)

# 결과를 txt 파일로 저장
output_file_path = 'unique_tag_paths.txt'
with open(output_file_path, 'w') as file:
    file.write("Unique tag paths in XML structure:\n")
    for path in sorted(paths):
        file.write(path + '\n')

print(f"Unique tag paths saved to {output_file_path}")


