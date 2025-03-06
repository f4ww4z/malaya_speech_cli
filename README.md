# Malaya Speech CLI

This project utilizes the Malaya Speech TTS VITS multispeaker model to generate audio files from text input. Each line of a text file corresponds to a separate audio file, allowing for easy conversion of paragraphs into speech.

## Project Structure

```
malaya-speech-cli
├── src
│   ├── __init__.py
│   ├── main.py          # Entry point for the CLI application
│   ├── tts.py           # Contains the TTS class for audio generation
│   ├── config.py        # Configuration settings for the project
│   └── utils
│       ├── __init__.py
│       ├── audio.py     # Utility functions for audio operations
│       └── text.py      # Utility functions for text processing
├── tests
│   ├── __init__.py
│   ├── test_tts.py      # Unit tests for TTS functionality
│   └── test_utils.py     # Unit tests for utility functions
├── data
│   ├── input
│   │   └── sample.txt   # Sample input text for audio generation
│   └── output           # Directory for generated audio files
├── requirements.txt      # Project dependencies
├── setup.py              # Setup script for the project
├── .gitignore            # Files and directories to ignore by Git
└── README.md             # Project documentation
```

## Installation

To install the required dependencies, run:

```bash
uv sync
```

## Usage

To generate audio files from the text in `data/input/sample.txt`, run the following command:

```bash
python src/main.py data/input/sample.txt
```

This will create audio files in the `data/output` directory, with each line of the input text resulting in a separate audio file.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.