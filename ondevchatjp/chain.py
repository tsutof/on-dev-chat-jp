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


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


RAG_TEMPLATE = """<s>[INST] <<SYS>>
あなたは誠実で優秀な日本人のアシスタントです。前提条件の情報だけで回答してください。
<</SYS>>

前提条件：{context}

質問：{question} [/INST]"""

FREE_TALK_TEMPLATE = """<s>[INST] <<SYS>>
あなたは誠実で優秀な日本人のアシスタントです。前提条件の情報だけで回答してください。
<</SYS>>

{quote} {question} [/INST]"""


def make_rag_chain(retriever, llm):
    prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
    output_parser = StrOutputParser()
    setup_and_retrieval = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    )
    chain = setup_and_retrieval | prompt | llm | output_parser
    return chain


def make_free_talk_chain(llm):
    prompt = ChatPromptTemplate.from_template(FREE_TALK_TEMPLATE)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain