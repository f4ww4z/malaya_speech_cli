import os
import sys
from malaya_speech import tts

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_text_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Error: The file {input_file} does not exist.")
        sys.exit(1)

    model = tts.vits(model='mesolitica/VITS-osman')

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_dir = 'data/output'
    os.makedirs(output_dir, exist_ok=True)

    for idx, line in enumerate(lines):
        line = line.strip()
        if line:
            audio_output = model.predict(line)
            audio_file_path = os.path.join(output_dir, f"output_{idx + 1}.wav")
            with open(audio_file_path, 'wb') as audio_file:
                audio_file.write(audio_output['y'])
            print(f"Generated audio for line {idx + 1}: {audio_file_path}")

if __name__ == "__main__":
    main()