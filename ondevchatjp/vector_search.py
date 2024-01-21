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


import gradio as gr
import pandas as pd
import json
from ondevchatjp.vector_store import *


vector_db = VectorStore()


# 指定したURLからベクトルデータを作成する
def add_document(url):
    global vector_db

    sources = vector_db.get_metadata_values("source")
    if url in sources:
        gr.Info("ベクトル情報が既に存在します")
        return (gr.update(interactive=True, value=""), gr.update(interactive=True))

    gr.Info("ベクトル情報を作成しています")
    vector_db.add_web_document(url)
    gr.Info(f"ベクトル情報の作成を完了しました。{str(vector_db.get_num_docs())}")
    return (gr.update(interactive=True, value=""), gr.update(interactive=True))


# queryで指定した文章と高い類似度を持つ上位k個の結果を返す
def vector_search(query, k):
    docs = vector_db.store.similarity_search_with_relevance_scores(query, k=k)
    headers = ["文章", "スコア", "メタデータ"]
    l2d = [
        [doc[0].page_content] 
        + [doc[1]]
        + [json.dumps(doc[0].metadata, ensure_ascii=False)] 
        for doc in docs
    ]
    df = pd.DataFrame(l2d, columns=headers)
    return df


# Chromaデータベースからコレクションを削除する
def reset_db():
    vector_db.delete_all()
    return (gr.update(interactive=False, value=""), gr.update(interactive=False))


with gr.Blocks() as demo:
    ndocs = vector_db.get_num_docs()

    with gr.Row():
        url = gr.Textbox(value="", label="情報ソースURL", scale=5)
        vect_btn = gr.Button(value="ベクトル化")
    with gr.Row():
        flg = True if ndocs > 0 else False
        query = gr.Textbox(value="", label="質問", interactive=flg, scale=5)
        query_btn = gr.Button(value="検索", interactive=flg)
    with gr.Row():
        rst_btn = gr.Button(value="ベクトル情報をリセット")
        k_val = gr.Number(value=4, label="抽出数", minimum=1, maximum=100)
    results = gr.Dataframe(
        row_count = (1, "dynamic"),
        col_count=(3, "fixed"),
        label="検索結果",
        headers=["文章", "スコア", "メタデータ"],
        wrap=True
    )

    # 「情報ソースURL」テキストフィールドでリターンキーを押した時および
    # 「ベクトル化」ボタンをクリックした時のイベントハンドリング
    gr.on(
        triggers=[url.submit, vect_btn.click],
        fn=add_document,
        inputs=url,
        outputs=[query, query_btn]
    )

    # 「質問」テキストフィールドでリターンキーを押した時および
    # 「検索」ボタンをクリックした時のイベントハンドリング
    gr.on(
        triggers=[query.submit, query_btn.click],
        fn=vector_search,
        inputs=[query, k_val],
        outputs=results
    )

    # 「ベクトル情報をリセット」ボタンをクリックした時にイベントハンドリング
    rst_btn.click(fn=reset_db, inputs=None, outputs=[query, query_btn])


demo.queue().launch(inbrowser=True)