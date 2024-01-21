from setuptools import setup, find_packages
import platform

cmake_args = []
if platform.system() == "Darwin" and platform.processor() == "arm":
    cmake_args += ['-DLLAMA_METAL=on']

setup(
    name='ondevchatjp',
    version='0.0.1',
    packages=find_packages(),
    cmake_args=cmake_args,
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