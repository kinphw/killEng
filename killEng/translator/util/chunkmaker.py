import random
import string

class ChunkedListMaker:

    string_list: list[str]
    max_size_bytes: int

    def __init__(self, string_list: list[str], max_size_kib: int = 128):
        self.string_list = string_list
        self.max_size_bytes = max_size_kib * 1024  # 128 KiB를 바이트로 변환

    def get_chunks(self) -> list[list[str]]:
        chunks = []
        current_chunk = []
        current_size = 0

        for text in self.string_list:
            text_size = len(text.encode('utf-8'))  # 문자열을 UTF-8로 인코딩하여 바이트 크기 계산

            # 각 텍스트가 max_size_bytes를 초과하는지 확인
            if text_size > self.max_size_bytes:
                raise ValueError(f"Single text element exceeds maximum chunk size: {text_size} bytes")

            # 추가하려는 텍스트가 제한을 초과할 경우
            if current_size + text_size > self.max_size_bytes:
                chunks.append(current_chunk)
                current_chunk = []
                current_size = 0

            # 현재 청크에 텍스트 추가
            current_chunk.append(text)
            current_size += text_size

        # 마지막 청크가 남아있다면 추가
        if current_chunk:
            chunks.append(current_chunk)

        return chunks
