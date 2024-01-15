from huggingface_hub import hf_hub_download
from langchain_community.llms import LlamaCpp
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, ConfigurableField

CONTEXT_SIZE = 2048
LLM_REPO_ID = "mmnga/ELYZA-japanese-Llama-2-7b-instruct-gguf"
LLM_FILE = "ELYZA-japanese-Llama-2-7b-instruct-q8_0.gguf"
CHUNK_SIZE = 256
CHUNK_OVERLAP = 64
EMB_MODEL = "sentence-transformers/distiluse-base-multilingual-cased-v2"
COLLECTION_NAME = "langchain"
SRC_INFO_URL = "https://www.aozora.gr.jp/cards/000081/files/43754_17659.html"

# LLMを生成
model_path = hf_hub_download(repo_id=LLM_REPO_ID, filename=LLM_FILE)
llm = LlamaCpp(
    model_path=model_path, 
    n_gpu_layers=128, 
    n_ctx=CONTEXT_SIZE,
    f16_kv=True,
    verbose=True,
    seed=0
)

# 埋め込み表現生成用モデルを準備
embeddings = HuggingFaceEmbeddings(model_name=EMB_MODEL)

# 指定したURLから情報ソースをロード
loader = WebBaseLoader(SRC_INFO_URL)
data = loader.load()

# ロードしたテキストをチャンクに分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
)
all_splits = text_splitter.split_documents(data)

# ベクトル化してベクトルDBへ格納
vector_store = Chroma.from_documents(
    documents=all_splits, embedding=embeddings
)

# ベクトルDBをLangChainのRetrieverに設定
retriever = vector_store.as_retriever()

# Llama2プロンプトテンプレート
template = """<s>[INST] <<SYS>>
あなたは誠実で優秀な日本人のアシスタントです。前提条件の情報だけで回答してください。
<</SYS>>

前提条件：{context}

質問：{question} [/INST]"""

# LangChain LCELでチェインを構築
prompt = ChatPromptTemplate.from_template(template)
output_parser = StrOutputParser()
setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)
chain = setup_and_retrieval | prompt | llm | output_parser

# チェインを起動して、回答をストリーミング出力
for s in chain.stream("2人の紳士が連れていた動物は何ですか？"):
    print(s, end="", flush=True)