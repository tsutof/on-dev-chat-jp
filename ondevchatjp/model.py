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


from huggingface_hub import hf_hub_download
from langchain_community.llms import LlamaCpp


DEFAULT_CONTEXT_SIZE = 2048
DEFAULT_LLM_REPO_ID = "mmnga/ELYZA-japanese-Llama-2-7b-instruct-gguf"
DEFAULT_LLM_FILE = "ELYZA-japanese-Llama-2-7b-instruct-q8_0.gguf"


def get_model(
        repo_id: str=DEFAULT_LLM_REPO_ID, 
        file: str=DEFAULT_LLM_FILE,
        cntx_size: int=DEFAULT_CONTEXT_SIZE,
        seed: int=-1):
    model_path = hf_hub_download(repo_id=repo_id, filename=file)
    llm = LlamaCpp(
        model_path=model_path, 
        n_gpu_layers=128, 
        n_ctx=cntx_size,
        f16_kv=True,
        verbose=True,
        seed=seed
    )
    return llm
