from lxml import etree
from collections import defaultdict
from killEng.common.myFileDialog import MyFileDialog as myfd
import os

class XMLAnalyzer:
    def __init__(self):
        self.tag_counter = defaultdict(int)         # 태그별 등장 횟수
        self.text_length_counter = defaultdict(int) # 태그별 포함 텍스트 총 길이
        self.unique_paths = set()                   # 중복 제거된 경로

    def traverse(self, element, level=0, path=()):
        tag = element.tag
        self.tag_counter[tag] += 1

        # 현재 태그 안에 있는 텍스트 길이 포함 (text + tail)
        text_parts = []
        if element.text:
            text_parts.append(element.text)
        if element.tail:
            text_parts.append(element.tail)
        total_text = "".join(text_parts).strip()
        self.text_length_counter[tag] += len(total_text)

        current_path = path + (tag,)
        self.unique_paths.add(current_path)

        for child in element:
            self.traverse(child, level + 1, current_path)

    def write_output(self, file_path, output_txt_path):
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write("🔍 중복 제거된 태그 트리 구조 및 통계 (출현 수, 글자 수):\n")
            sorted_paths = sorted(self.unique_paths)

            for path in sorted_paths:
                indent = "  " * (len(path) - 1)
                tag = path[-1]
                count = self.tag_counter[tag]
                length = self.text_length_counter[tag]
                f.write(f"{indent}<{tag}> ({count}회, {length}자)\n")

        print(f"\n✅ 분석 결과가 저장되었습니다: {output_txt_path}")

    def analyze_xml_structure(self, file_path):
        tree = etree.parse(file_path)
        root = tree.getroot()

        self.traverse(root)

        output_name = os.path.splitext(os.path.basename(file_path))[0] + "_structure.txt"
        output_txt_path = os.path.join(os.path.dirname(file_path), output_name)
        self.write_output(file_path, output_txt_path)

    def analyze_xml_structure_with_duplicates(self, file_path):
        tree = etree.parse(file_path)
        root = tree.getroot()

        with open(os.path.join(os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0] + "_structure_with_duplicates.txt"), "w", encoding="utf-8") as f:
            f.write("🔍 중복 포함 태그 트리 구조 및 통계 (출현 수, 글자 수):\n")
            self.traverse_with_duplicates(root, f)

        print(f"\n✅ 분석 결과가 저장되었습니다: {os.path.join(os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0] + '_structure_with_duplicates.txt')}")

    def traverse_with_duplicates(self, element, file, level=0, path=()):
        tag = element.tag
        self.tag_counter[tag] += 1

        # 현재 태그 안에 있는 텍스트 길이 포함 (text + tail)
        text_parts = []
        if element.text:
            text_parts.append(element.text)
        if element.tail:
            text_parts.append(element.tail)
        total_text = "".join(text_parts).strip()
        self.text_length_counter[tag] += len(total_text)

        current_path = path + (tag,)
        indent = "  " * level
        count = self.tag_counter[tag]
        length = self.text_length_counter[tag]
        file.write(f"{indent}<{tag}> ({count}회, {length}자)\n")

        for child in element:
            self.traverse_with_duplicates(child, file, level + 1, current_path)


    def run(self):
        mode = input("모드를 선택하세요 (1: 중복 제거, 2: 중복 포함): ")
        file_path = myfd.askopenfilename("분석할 XML 파일을 선택하세요")
        if file_path:
            if mode == "1":
                self.analyze_xml_structure(file_path)
            elif mode == "2":
                self.analyze_xml_structure_with_duplicates(file_path)
            else:
                print("잘못된 모드 선택입니다. 프로그램을 종료합니다.")
        else:
            print("파일 경로를 선택하지 않았습니다.")


if __name__ == "__main__":
    analyzer = XMLAnalyzer()
    analyzer.run()
