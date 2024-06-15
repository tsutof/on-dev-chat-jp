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
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


DEFAULT_EMBEDDING = "sentence-transformers/distiluse-base-multilingual-cased-v2"
DEFAULT_COLLECTION = "langchain"


class VectorStore:

    def __init__(self, 
            chunk_size: int=256, 
            chunk_overlap: int=64,
            persist_path: Optional[str] = None,
            collection: str=DEFAULT_COLLECTION,
            embedding_model: str=DEFAULT_EMBEDDING) -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.collection = collection
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.store = Chroma(
            self.collection,
            persist_directory=persist_path,
            embedding_function=self.embeddings,
            collection_metadata={"hnsw:space": "cosine"}
        )

    def add_web_document(self, url: str) -> int:
        sources = self.get_metadata_values("source")
        if url in sources:
            return 0
        loader = WebBaseLoader(url)
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, 
            chunk_overlap=self.chunk_overlap
        )
        all_splits = text_splitter.split_documents(data)
        self.store.add_documents(all_splits)
        self.store.persist()
        return len(all_splits)
    
    def delete_all(self) -> None:
        for collection in self.store._client.list_collections():
            if collection.name == self.collection:
                ids = collection.get()['ids']
                print('Removing %s document(s) from %s collection' % (str(len(ids)), collection.name))
                if len(ids):
                    collection.delete(ids)

    def get_num_docs(self) -> int:
        info_dict = {}
        for collection in self.store._client.list_collections():
            ids = collection.get()["ids"]
            info_dict[collection.name] = len(ids)
        return info_dict[self.collection]
    
    def get_metadata_values(self, attr: str):
        info_dict = {}
        for collection in self.store._client.list_collections():
            data = [meta[attr] for meta in collection.get()["metadatas"] if attr in meta.keys()]
            info_dict[collection.name] = data
        return info_dict[self.collection]
    
    def as_retriever(self, search_k: int=4):
        return self.store.as_retriever(search_kwargs={"k": search_k})