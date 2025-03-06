import os
import pytest
from malaya_speech import tts

def test_tts_generation():
    model = tts.vits(model='mesolitica/VITS-osman')
    input_text = "This is a test sentence for TTS generation."
    
    # Generate audio
    result = model.predict(input_text, sid=0)
    
    # Check if the result contains the expected keys
    assert 'y' in result
    assert 'ids' in result
    assert 'alignment' in result
    assert 'string' in result
    
    # Check if the audio output is not empty
    assert len(result['y']) > 0

def test_multiple_lines_generation():
    model = tts.vits(model='mesolitica/VITS-osman')
    lines = [
        "First line of text.",
        "Second line of text.",
        "Third line of text."
    ]
    
    for i, line in enumerate(lines):
        result = model.predict(line, sid=0)
        assert 'y' in result
        assert len(result['y']) > 0
        assert result['string'] == line

def test_invalid_input():
    model = tts.vits(model='mesolitica/VITS-osman')
    invalid_text = ""
    
    # Generate audio for invalid input
    result = model.predict(invalid_text, sid=0)
    
    # Check if the result is empty or raises an error
    assert 'y' in result
    assert len(result['y']) == 0