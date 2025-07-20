import os

import pdfplumber
from tqdm import tqdm

from killEng.common.stringHandler import StringHandler as sh
from killEng.common.baseIO import BaseIO
from killEng.common import saver

class PdfToText(BaseIO):    

    def __init__(self) -> None:
        self._initSet("PDF 파일을 선택하세요.", "_text", "txt")

    def run(self):
        all_text = self._readPdf()
        saver.SaverFromText(all_text).saveAsText(self.strOutput)

    def _readPdf(self) -> str:
        ##################################################
        # PDF TO TEXT

        # pdfplumber를 사용하여 PDF 파일 열기
        with pdfplumber.open(self.strInput) as pdf:
            all_text = ""
            # 각 페이지에서 텍스트 추출
            for page in tqdm(pdf.pages, desc="Extracting text from pages"):
                text = page.extract_text()
                all_text += text if text else ""

        # 추출한 텍스트 출력
        print(len(all_text), "글자 읽음")
        return all_text

if __name__ == "__main__":
    PdfToText().run()