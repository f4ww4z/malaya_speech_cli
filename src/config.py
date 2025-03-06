import os

# Configuration settings for the project
MODEL_NAME = 'mesolitica/VITS-osman'
INPUT_FILE_PATH = os.path.join('data', 'input', 'sample.txt')
OUTPUT_DIR = os.path.join('data', 'output')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)