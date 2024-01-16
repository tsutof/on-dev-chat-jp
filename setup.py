from setuptools import setup, find_packages

setup(
    name='ondevchatjp',
    version='0.0.1',
    packages=find_packages(),
    cmake_args=['-DLLAMA_METAL=on'],
    install_requires=[
        'torch',
        'torchvision',
        'torchaudio',
        'pyopenjtalk',
        'openai-whisper',
        'pyaudio',
        'gradio',
        'langsmith',
        'langchain',
        'langchain-community',
        'chromadb',
        'bs4',
        'sentence_transformers',
        'llama-cpp-python',
    ]
)