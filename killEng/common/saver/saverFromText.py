import os

class SaverFromText():

    text:str

    def __init__(self, text:str) -> None:
        self.text = text

    def saveAsText(self, strOutput:str, encoding:str = 'utf-8'):
        with open(strOutput, 'wt', encoding=encoding) as file:
            file.write(self.text)
        file_size = os.path.getsize(strOutput)
        print(f"File saved: {strOutput}, Size: {file_size} bytes")