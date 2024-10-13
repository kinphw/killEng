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

            # 추가하려는 텍스트가 제한을 초과하는 경우, 현재 청크를 추가하고 새 청크를 시작
            if current_size + text_size > self.max_size_bytes:
                chunks.append(current_chunk)
                current_chunk = [text]
                current_size = text_size
            else:
                # 제한 이내라면 텍스트를 현재 청크에 추가
                current_chunk.append(text)
                current_size += text_size

        # 마지막 청크가 남아있다면 추가
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

# # 예제 사용
# string_list = ["문장1", "문장2", "길이가 매우 긴 문장..." * 500, "짧은 문장", "또 다른 문장들..."]  # 가변적 길이의 문자열 리스트
# translator = ChunkedTranslator(string_list)
# chunks = translator.get_chunks()

# for i, chunk in enumerate(chunks, 1):
#     print(f"Chunk {i} (총 크기: {sum(len(s.encode('utf-8')) for s in chunk)} bytes): {chunk}")


class Test:
    # 문자열 생성 함수 (임의의 길이로 생성)
    def generate_random_string(self, length):
        return ''.join(random.choices(string.ascii_letters + string.digits + " ", k=length))
    
    def run(self):
    # 테스트를 위한 다양한 길이의 문자열 리스트
        string_list = [
            self.generate_random_string(10),      # 짧은 문자열
            self.generate_random_string(50),      # 중간 길이 문자열
            self.generate_random_string(1500),    # 긴 문자열
            self.generate_random_string(3000),    # 매우 긴 문자열
            self.generate_random_string(5000),    # 더 긴 문자열
            self.generate_random_string(800),     # 중간 길이 문자열
            self.generate_random_string(200),     # 짧은 문자열
            self.generate_random_string(4000),    # 매우 긴 문자열
            self.generate_random_string(100),     # 짧은 문자열
            self.generate_random_string(2500),    # 긴 문자열
        ]

    # 추가적인 랜덤 길이의 문자열을 포함하여 리스트 확장
        for _ in range(10):
            random_length = random.randint(10, 6000)  # 10 ~ 6000 길이의 랜덤 문자열
            string_list.append(self.generate_random_string(random_length))
        
        return string_list

if __name__ == "__main__":
    string_list = Test().run()

    # 예제 리스트 출력
    for i, s in enumerate(string_list, 1):
        print(f"String {i} (길이: {len(s.encode('utf-8'))} bytes): {s[:50]}...")  # 각 문자열의 길이와 일부 내용 출력

    # 총 바이트 수 계산 및 출력
    total_bytes = sum(len(s.encode('utf-8')) for s in string_list)
    print(f"\nTotal bytes: {total_bytes} bytes")

    # 청크 생성
    cl = ChunkedListMaker(string_list, 10).get_chunks()
    
    for i, chunk in enumerate(cl, 1):
        chunk_size = sum(len(s.encode('utf-8')) for s in chunk)
        print(f"Chunk {i}: {len(chunk)} strings, {chunk_size} bytes")
    
