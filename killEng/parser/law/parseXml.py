# v0.1.1
# date : 2025-07-22

from lxml import etree
from killEng.common.myFileDialog import MyFileDialog as myfd
import os

class XMLTextExtractor:
    def __init__(self):
        self.indent_unit = "    "  # 4 spaces per level
        self.output_lines = []

    def extract(self, element, level=0):
        tag = element.tag

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
        else:
            # 단, 구조 단위일 때만 fallback_text 출력
            if tag in {"section", "subsection", "clause", "subclause", "paragraph", "subparagraph"}:
                fallback_text = "".join(element.itertext()).strip()
                if fallback_text and not parts:
                    parts.append(fallback_text)

        if parts:
            line = self.indent_unit * level + " ".join(parts)
            self.output_lines.append(line)

        # for child in element:
        #     if child.tag in {"section", "subsection", "clause", "subclause", "paragraph", "subparagraph"}:
        #         self.extract(child, level + 1)
        #     elif child.tag in {"enum", "header", "text"}:
        #         continue
        #     else:
        #         # 하위 quote, term 등은 순회하되 출력은 생략 (중복 방지)
        #         self.extract(child, level)
        for child in element:
            if child.tag in {"section", "subsection", "clause", "subclause", "paragraph", "subparagraph", "article", "subtitle", "toc-item"}:
                self.extract(child, level + 1)
            else:
                self.extract(child, level)        


    def parse_and_write(self, xml_path):
        tree = etree.parse(xml_path)
        root = tree.getroot()

        legis_body = root.find(".//legis-body")
        if legis_body is None:
            print("❌ legis-body를 찾을 수 없습니다.")
            return

        # 전 구조를 통째로 재귀 탐색
        self.extract(legis_body, level=0)

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
