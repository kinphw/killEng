
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
    
