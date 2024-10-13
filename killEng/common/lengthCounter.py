from killEng.common.myFileDialog import MyFileDialog as myfd

class LengthCounter:

    filename:str

    def __init__(self, filename:str=None):
        if filename:
            self.filename = filename
        else:
            self.filename = myfd.askopenfilename("파일을 선택하세요.")

    def count_characters(self):
        with open(self.filename, 'rt', encoding='utf8') as file:
            text = file.read()
        print(self.filename, ":", len(text), "글자")

