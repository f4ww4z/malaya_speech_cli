import os
import numpy as np
import malaya_speech
from malaya_speech import Pipeline

def save_audio(waveform, filename, sample_rate=22050):
    """Save the generated audio waveform to a file."""
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    malaya_speech.utils.save_wav(filename, waveform, sample_rate)

def generate_audio_from_text(text, model, speaker_id, output_dir):
    """Generate audio from a given text using the specified TTS model and save it to the output directory."""
    result = model.predict(text, sid=speaker_id)
    audio_filename = os.path.join(output_dir, f"{text[:10]}.wav")  # Use first 10 characters of text as filename
    save_audio(result['y'], audio_filename)