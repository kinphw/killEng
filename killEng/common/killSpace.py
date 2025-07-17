from killEng.common.myFileDialog import MyFileDialog
import os

class EmptyLineRemover:
    def __init__(self):
        self.input_file = None
        self.output_file = None

    def select_files(self):
        print("Select the input file:")
        self.input_file = MyFileDialog.askopenfilename(title="Select Input File")
        print(f"Input file selected: {self.input_file}")

        # Automatically generate the output file name
        if self.input_file:
            base, ext = os.path.splitext(self.input_file)
            self.output_file = f"{base}_cleaned.txt"
            print(f"Output file will be: {self.output_file}")

    def remove_empty_lines(self):
        if not self.input_file or not self.output_file:
            print("Input file not selected or output file not generated.")
            return

        with open(self.input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        with open(self.output_file, 'w', encoding='utf-8') as outfile:
            for line in lines:
                if line.strip():  # Check if the line is not empty after stripping whitespace
                    outfile.write(line)

# Example usage
if __name__ == "__main__":
    remover = EmptyLineRemover()
    remover.select_files()
    remover.remove_empty_lines()