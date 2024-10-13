class DeleteEmptyLines:

    liText:list[str]

    def __init__(self, liText:list[str]):
        self.liText = liText

    def run(self) -> list[str]:
        liText = self.liText
        liText = [line for line in liText if line.strip()]
        return liText
