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


import argparse
import json
import gradio as gr
import pyopenjtalk
from ondevchatjp import *


PERSIST_DIRECTORY = ".chroma_db"


with gr.Blocks() as demo:
    args, model_kwargs = parse_args()
    db = VectorStore(persist_path=PERSIST_DIRECTORY)
    retriever = db.as_retriever(search_k=2)
    transcriber = Transcriber()
    llm = get_model(**model_kwargs)
    chain = make_rag_chain(retriever, llm)

    def add_documnet(url):
        global db
        gr.Info("ベクトル情報を作成しています")
        n = db.add_web_document(url)
        if n <= 0:
            gr.Info("ベクトル情報が既に存在します")
        else:
            gr.Info(f"ベクトル情報の作成を完了しました{str(n)}")
        return (
            gr.update(visible=True, value=""),
            gr.update(visible=True)
        )

    def reset_db():
        global db
        db.delete_all()
        gr.Info("すべてのベクトル情報を削除しました")
        return (
            gr.update(visible=False, value=""),
            gr.update(visible=False),
            ""
        )

    def text2speech(history):
        text = history[-1][1]
        audio, sr = pyopenjtalk.tts(text)
        audio = audio.astype(np.int16)
        return sr, audio

    def speech2text(audio, history):
        sr, y = audio
        text = transcriber.transcribe(y, sr)
        history += [[text, None]]
        return history

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        global chain
        history[-1][1] = ""
        for s in chain.stream(history[-1][0]):
            print(s, end="", flush=True)
            history[-1][1] += s
            yield history

    
    url = gr.Textbox(
        value="", label="情報ソースURL",
        placeholder="情報ソースとなるウェブページのURLを入力後、リターンキーを押す"
    )
    rst_btn = gr.Button(value="ベクトル情報をリセット（削除）")
    chatbot = gr.Chatbot(label="チャット")
    flg = True if db.get_num_docs() > 0 else False
    msg = gr.Textbox(
        "", label="あなたからのテキストメッセージ", visible=flg,
        placeholder="質問を入力後、リターンキーを押す"
    )
    audio_in = gr.Audio(
        sources=["microphone"], label="あなたからの音声メッセージ", visible=flg
    )
    audio_out = gr.Audio(
        type="numpy", label="AIからの音声メッセージ", autoplay=True
    )
    gr.Textbox(json.dumps(model_kwargs, ensure_ascii=False), label="モデル パラメータ")

    # テキスト入力時のイベントハンドリング
    msg.submit(
        user, [msg, chatbot], [msg, chatbot], queue=True
    ).then(
        bot, chatbot, chatbot,
    ).then(
        text2speech, chatbot, audio_out,
    )

    # 音声入力時のイベントハンドリング
    audio_in.stop_recording(
        speech2text, [audio_in, chatbot], chatbot, queue=True
    ).then(
        bot, chatbot, chatbot
    ).then(
        text2speech, chatbot, audio_out
    )

    # ベクトル情報をリセット
    rst_btn.click(reset_db, None, [msg, audio_in, url], queue=True)

    # 情報ソースURLの入力
    url.submit(add_documnet, url, [msg, audio_in], queue=True)

demo.queue().launch(inbrowser=args.inbrowser, share=args.share)