# MIT License
#
# Copyright (c) 2024 Tsutomu Furuse
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from typing import Optional
import argparse
from huggingface_hub import hf_hub_download
from langchain_community.llms import LlamaCpp


DEFAULT_CONTEXT_SIZE = 2048
DEFAULT_TEMPERATURE = 0.8
DEFAULT_LLM_REPO_ID = "mmnga/ELYZA-japanese-Llama-2-7b-instruct-gguf"
DEFAULT_LLM_FILE = "ELYZA-japanese-Llama-2-7b-instruct-q4_K_S.gguf"


def get_model(
        repo_id: str=DEFAULT_LLM_REPO_ID, 
        gguf_file: str=DEFAULT_LLM_FILE,
        model_path: Optional[str]=None,
        cntx_size: int=DEFAULT_CONTEXT_SIZE,
        temperature: float=DEFAULT_TEMPERATURE,
        seed: int=-1):
    if model_path is None or model_path == "":
        model_path = hf_hub_download(repo_id=repo_id, filename=gguf_file)
    llm = LlamaCpp(
        model_path=model_path, 
        n_gpu_layers=128, 
        n_ctx=cntx_size,
        f16_kv=True,
        verbose=True,
        seed=seed,
        temperature=temperature
    )
    return llm


def get_model_arg_paser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--repo_id", "-r",
        type=str, default=DEFAULT_LLM_REPO_ID, metavar="LLM_REPO",
        help=f"Hugging Face Hub repository ID (default: {DEFAULT_LLM_REPO_ID})"
    )
    parser.add_argument("--gguf_file", "-f",
        type=str, default=DEFAULT_LLM_FILE, metavar="LLM_FILE",
        help=f"GGUF file name (default: {DEFAULT_LLM_FILE})"
    )
    parser.add_argument("--model_path", "-p",
        type=str, default="", metavar="PATH",
        help="GGUF file path if you have the model in loacl computer"
    )
    parser.add_argument("--cntx_size", "-c",
        type=int, default=DEFAULT_CONTEXT_SIZE, metavar="CNTX_SIZE",
        help=f"Context size (default: {DEFAULT_CONTEXT_SIZE})"
    )
    parser.add_argument("--seed", "-s",
        type=int, default=-1, metavar="SEED",
        help="Seed value (default=-1: Random Seed)"
    )
    parser.add_argument("--temperature", "-t",
        type=float, default=DEFAULT_TEMPERATURE, metavar="TEMPERATURE",
        help=f"Temperatue to use for sampling (default: {DEFAULT_TEMPERATURE})"
    )
    return parser
