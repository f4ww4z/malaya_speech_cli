# Malaya Speech TTS - Malaysian Text-to-Speech Web Application

A beautiful, dockerized FastAPI web application for Malaysian language Text-to-Speech (TTS) using Malaya Speech.

## Features

- Interactive web interface with beautiful animations
- Multiple Malaysian voice models support
- Batch processing of text lines
- Downloadable audio output files
- Responsive design for all devices
- Easy setup with Docker

## Available Voice Models

- Osman
- Yasmin
- Female Singlish
- Haqkiem

## Quick Start with Docker

1. Make sure you have Docker and Docker Compose installed.

2. Clone this repository:
   ```
   git clone <repository-url>
   cd malaya_speech_cli
   ```

3. Create `.env` file and specify `PORT=xxxx`

4. Build and start the Docker container:
   ```
   docker-compose up -d
   ```

5. Access the web application in your browser:
   ```
   http://localhost:<PORT>
   ```

## Usage

1. Open the web application in your browser.
2. Select a voice model from the dropdown.
3. Enter your text (one line per audio file) in the text area.
4. Click "Convert to Speech" to generate the audio.
5. Use the player to preview the generated audio.
6. Download individual audio files or all files at once.

## Development

### Prerequisites

- Python 3.8+
- Required packages listed in `requirements.txt`
- Additional packages: `fastapi`, `uvicorn`, `jinja2`

### Local Setup (without Docker)

1. Install dependencies:
   ```
   pip install -r requirements.txt
   pip install fastapi uvicorn jinja2
   ```

2. Run the application:
   ```
   cd malaya_speech_cli
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

- `GET /api/models` - Get all available TTS models
- `POST /api/synthesize` - Synthesize speech from a single text
- `POST /api/synthesize-batch` - Synthesize speech from multiple lines of text
- `GET /api/download/{filename}` - Download an audio file

## License

This project is open-source under the terms of the original licensing terms of Malaya Speech.

## Credits

- Malaya Speech for the TTS models
- [LottieFiles](https://lottiefiles.com/) for the animations