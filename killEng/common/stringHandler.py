from nltk.tokenize import sent_tokenize

class StringHandler:
    @staticmethod
    def add_output_suffix(file_name, suffix="_output", extension=''):
        file_name_parts = file_name.split('.')
        if len(file_name_parts) > 1:
            file_extension = file_name_parts[-1]
            file_name_without_extension = '.'.join(file_name_parts[:-1])
            if extension != '':
                file_extension = extension
            return f"{file_name_without_extension}{suffix}.{file_extension}"
        else:
            return f"{file_name}{suffix}"
        
    @staticmethod
    def split(text: str) -> list[str]:
        ##################################################        
        # 전체 텍스트를 문장 단위로 분할
        sentences = sent_tokenize(text)
        return sentences
    
    @staticmethod
    def change_extension(file_name:str, new_extension:str):
        file_name_parts = file_name.split('.')
        if len(file_name_parts) > 1:
            file_name_parts[-1] = new_extension
            return '.'.join(file_name_parts)
        else:
            return file_name

