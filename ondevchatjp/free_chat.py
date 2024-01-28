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


B_INST, E_INST = "[INST]", "[/INST]"
B_OS, E_OS = "<s>", "</s>"


with gr.Blocks() as demo:
    args, model_kwargs = parse_args()
    transcriber = Transcriber()
    llm = get_model(**model_kwargs)
    chain = make_free_talk_chain(llm)

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
    
    def get_quote(history, mem_len=2):
        quote = ""
        for item in history[-(mem_len + 1):-1]:
            quote += "{user} {e_inst} {assistant} {eos_token}{bos_token}{b_inst} ".format(
                user=item[0],
                e_inst=E_INST,
                assistant=item[1],
                eos_token=E_OS,
                bos_token=B_OS,
                b_inst=B_INST
            )
        return quote

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        global chain
        quote = get_quote(history)
        history[-1][1] = ""
        for s in chain.stream({"quote": quote, "question": history[-1][0]}):
            print(s, end="", flush=True)
            history[-1][1] += s
            yield history

    def switch_autoplay(flag):
        return gr.update(autoplay=flag)

    chatbot = gr.Chatbot(label="チャット")
    clear = gr.Button("チャット履歴の消去")
    msg = gr.Textbox(
        "", label="あなたからのテキストメッセージ",
        placeholder="メッセージを入力後、リターンキーを押す"
    )
    audio_in = gr.Audio(sources=["microphone"], label="あなたからの音声メッセージ")
    audio_out = gr.Audio(type="numpy", label="AIからの音声メッセージ", autoplay=True)
    gr.Textbox(json.dumps(model_kwargs, ensure_ascii=False), label="モデル パラメータ")

    # テキスト入力時のイベントハンドリング
    msg.submit(
        user, [msg, chatbot], [msg, chatbot], queue=True
    ).then(
        bot, chatbot, chatbot
    ).then(
        text2speech, chatbot, audio_out
    )

    # 音声入力時のイベントハンドリング
    audio_in.stop_recording(
        speech2text, [audio_in, chatbot], chatbot, queue=True
    ).then(
        bot, chatbot, chatbot
    ).then(
        text2speech, chatbot, audio_out
    )

    # チャット履歴の消去
    clear.click(lambda: None, None, chatbot, queue=False)


demo.queue().launch(inbrowser=args.inbrowser, share=args.share)