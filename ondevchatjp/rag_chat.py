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


model_kwargs = vars(
    argparse.ArgumentParser(parents=[get_model_arg_paser()]).parse_args()
)
print(json.dumps(model_kwargs, ensure_ascii=False))


with gr.Blocks() as demo:
    db = VectorStore()
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
        return gr.update(interactive=True, value="")

    def reset_db():
        global db
        db.delete_all()
        gr.Info("すべてのベクトル情報を削除しました")
        gr.update(interactive=False, value="")

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

    with gr.Row():
        url = gr.Textbox(value="", label="情報ソースURL", scale=5)
        rst_btn = gr.Button(value="ベクトル情報をリセット")
    chatbot = gr.Chatbot(label="チャット")
    # clear = gr.Button("チャット履歴の消去")
    flg = True if db.get_num_docs() > 0 else False
    msg = gr.Textbox("", label="あなたからのテキストメッセージ", interactive=flg)
    audio_in = gr.Audio(sources=["microphone"], label="あなたからの音声メッセージ")
    audio_out = gr.Audio(type="numpy", label="AIからの音声メッセージ", autoplay=True)

    # テキスト入力時のイベントハンドリング
    msg.submit(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        bot, chatbot, chatbot
    ).then(
        text2speech, chatbot, audio_out
    )

    # 音声入力時のイベントハンドリング
    audio_in.stop_recording(
        speech2text, [audio_in, chatbot], chatbot, queue=False
    ).then(
        bot, chatbot, chatbot
    ).then(
        text2speech, chatbot, audio_out
    )

    # チャット履歴の消去
    # clear.click(lambda: None, None, chatbot, queue=False)

    # ベクトル情報をリセット
    rst_btn.click(fn=reset_db, inputs=None, outputs=msg)

    # 情報ソースURLの入力
    url.submit(add_documnet, url, msg, queue=False)

demo.queue().launch(inbrowser=True)