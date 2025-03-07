import malaya_speech
import os

class TTS:
    def __init__(self, model_name='mesolitica/VITS-osman'):
        self.model = malaya_speech.tts.vits(model=model_name)

    def generate_audio(self, text, output_file):
        result = self.model.predict(text, temperature=0.6666, length_ratio=1)
        audio_data = result['y']
        
        # Save the audio data to a file
        with open(output_file, 'wb') as f:
            f.write(audio_data)

    def process_text_file(self, input_file, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(input_file, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            line = line.strip()
            if line:  # Only process non-empty lines
                output_file = os.path.join(output_dir, f'audio_{i}.wav')
                self.generate_audio(line, output_file)