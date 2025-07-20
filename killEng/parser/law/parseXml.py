from lxml import etree
from killEng.common.myFileDialog import MyFileDialog as myfd
import os

class XMLTextExtractor:
    def __init__(self):
        self.indent_unit = "    "  # 4 spaces per level
        self.output_lines = []

    def extract(self, element, level=0):
        tag = element.tag

        # 텍스트 구성
        enum = element.findtext("enum")
        header = element.findtext("header")
        text = element.find("text")

        parts = []
        if enum:
            parts.append(enum.strip())
        if header:
            parts.append(header.strip() + "—")

        if text is not None:
            inner_text = "".join(text.itertext()).strip()
            if inner_text:
                parts.append(inner_text)

        if parts:
            line = self.indent_unit * level + " ".join(parts)
            self.output_lines.append(line)

        # 하위 처리 (들여쓰기 깊이 고려)
        for child in element:
            # 구조 태그일 경우 level 증가
            if child.tag in {"paragraph", "subparagraph", "clause", "subclause", "subsection", "section"}:
                self.extract(child, level + 1)
            elif child.tag in {"enum", "header", "text"}:
                continue  # 이미 상단에서 처리함
            else:
                self.extract(child, level)

    def parse_and_write(self, xml_path):
        tree = etree.parse(xml_path)
        root = tree.getroot()

        # <legis-body> 안의 내용만 추출
        legis_body = root.find(".//legis-body")
        if legis_body is None:
            print("❌ legis-body를 찾을 수 없습니다.")
            return

        for section in legis_body.findall("section"):
            self.extract(section, level=0)

        # 출력 파일 저장
        output_path = os.path.splitext(xml_path)[0] + "_text.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            for line in self.output_lines:
                f.write(line + "\n")

        print(f"✅ 파싱 결과가 저장되었습니다: {output_path}")

    def run(self):
        file_path = myfd.askopenfilename("텍스트를 추출할 XML 파일을 선택하세요")
        if file_path:
            self.parse_and_write(file_path)
        else:
            print("❌ 파일을 선택하지 않았습니다.")


if __name__ == "__main__":
    extractor = XMLTextExtractor()
    extractor.run()
