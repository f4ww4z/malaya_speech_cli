def read_lines_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line.strip()]  # Return non-empty lines

def write_audio_file(file_path, audio_data):
    with open(file_path, 'wb') as audio_file:
        audio_file.write(audio_data)  # Write the audio data to the file