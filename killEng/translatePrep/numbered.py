from killEng.common.myFileDialog import MyFileDialog
import os
import re

class NumberedLineMerger:
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
            self.output_file = f"{base}_merged.txt"
            print(f"Output file will be: {self.output_file}")

    def merge_numbered_lines(self):
        if not self.input_file or not self.output_file:
            print("Input file not selected or output file not generated.")
            return

        with open(self.input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        merged_lines = []
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            # Check if the line matches the extended pattern
            if re.match(r"^\(?[a-zA-Z\d]+\)?\.?$", stripped_line):
                # Merge with the next line if it exists
                if i + 1 < len(lines):
                    merged_lines.append(stripped_line + " " + lines[i + 1].strip())
                    lines[i + 1] = ""  # Mark the next line as processed
            else:
                merged_lines.append(line.strip())

        with open(self.output_file, 'w', encoding='utf-8') as outfile:
            for merged_line in merged_lines:
                if merged_line.strip():  # Write non-empty lines
                    outfile.write(merged_line + "\n")

        print(f"✅ Merged lines saved to: {self.output_file}")

    def run(self):
        self.select_files()
        self.merge_numbered_lines()

# Example usage
if __name__ == "__main__":
    merger = NumberedLineMerger()
    merger.run()