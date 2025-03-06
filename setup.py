from setuptools import setup, find_packages

setup(
    name='malaya-speech-cli',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A CLI application for generating audio files from text using Malaya Speech TTS VITS multispeaker model.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'malaya-speech',
        'numpy',
        'matplotlib',
        'IPython'
    ],
    entry_points={
        'console_scripts': [
            'malaya-speech-cli=main:main',
        ],
    },
)