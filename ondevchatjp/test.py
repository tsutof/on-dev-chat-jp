from chain import *
from model import *
from transcriber import *
from vector_store import *


URL = "https://www.aozora.gr.jp/cards/000081/files/43754_17659.html"
QUESTION = "2人の紳士が連れていた動物は何ですか？"


def main():
    db = VectorStore()
    db.add_web_document(URL)
    retriever = db.as_retriever(search_k=3)
    llm = get_model(seed=0)
    chain = make_chain(retriever, llm)
    for s in chain.stream(QUESTION):
        print(s, end="", flush=True)


if __name__ == "__main__":
    main()