import gradio as gr
import pyopenjtalk
from ondevchatjp import *


transcriber = None


def text2speech(history):
    text = history[-1][1]
    audio, sr = pyopenjtalk.tts(text)
    return sr, audio

def speech2text(audio, history):
    sr, y = audio
    text = transcriber.transcribe(y, sr)
    history += [[text, None]]
    return history

def user(user_message, history):
    return "", history + [[user_message, None]]

def bot(history):
    # プロンプトを作成
    prompt = construct_prompt(history)
    print(prompt)

    # 推論
    streamer = llm.create_completion(prompt, max_tokens=MAX_TOKENS, stream=True)

    # 推論結果をストリーム表示
    history[-1][1] = ""
    for msg in streamer:
        message = msg["choices"][0]
        if 'text' in message:
            new_token = message["text"]
            if new_token != "<":
                history[-1][1] += new_token
                yield history

with gr.Blocks() as demo:
    transcriber = Transcriber()

    chatbot = gr.Chatbot(label="チャット")
    msg = gr.Textbox("", label="あなたからのメッセージ")
    clear = gr.Button("チャット履歴の消去")
    audio_in = gr.Audio(sources=["microphone"], label="あなたからのメッセージ")
    audio_out = gr.Audio(type="numpy", label="AIからのメッセージ", autoplay=True)

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
    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue().launch()