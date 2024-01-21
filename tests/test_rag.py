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


import unittest
from ondevchatjp import *


URL = "https://www.aozora.gr.jp/cards/000081/files/43754_17659.html"
QUESTION = "2人の紳士が連れていた動物は何ですか？"
LLM_REPO_ID = "mmnga/ELYZA-japanese-Llama-2-7b-instruct-gguf"
LLM_FILE = "ELYZA-japanese-Llama-2-7b-instruct-q4_K_S.gguf"


class OnDevChatJpRagTest(unittest.TestCase):

    def test_rag(self):
        db = VectorStore()
        db.add_web_document(URL)
        retriever = db.as_retriever(search_k=3)
        llm = get_model(repo_id=LLM_REPO_ID, file=LLM_FILE, seed=0)
        chain = make_rag_chain(retriever, llm)
        answer = ""
        for s in chain.stream(QUESTION):
            answer += s
            print(s, end="", flush=True)
        expected_answer = "  2人の紳士が連れていた動物は、「白熊のような犬」であると前提条件に記載されています。"
        self.assertEqual(expected_answer, answer)
    

if __name__ == "__main__":
    unittest.main()