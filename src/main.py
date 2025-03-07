import os
import sys
from malaya_speech import tts
from malaya_speech.utils.astype import float_to_int
import scipy.io.wavfile as wavfile

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

    # Sample rate for the audio is 22050 Hz
    sample_rate = 22050

    for idx, line in enumerate(lines):
        line = line.strip()
        if line:
            audio_output = model.predict(line)
            # file name is the first 5 words of the line
            file_name = ' '.join(line.split()[:5])
            audio_file_path = os.path.join(output_dir, f"{file_name}.wav")
            
            # Convert float audio to int16
            audio_int = float_to_int(audio_output['y'])
            
            # Save with proper sample rate using scipy
            wavfile.write(audio_file_path, sample_rate, audio_int)
            
            print(f"Generated audio for line {idx + 1}: {audio_file_path}")

if __name__ == "__main__":
    main()