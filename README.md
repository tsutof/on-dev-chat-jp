# on-dev-chat-jp
Llama.cppベースのオンデバイス・チャットボット

## インストール

### MacOS

```
brew install ffmpeg portaudio
```

```
conda create --name ondevchatjp python=3.10 --yes
conda activate ondevchatjp
```

```
git clone https://github.com/tsutof/on-dev-chat-jp
cd on-dev-chat-jp
pip install -e .
```

## 実行方法

（Miniforgeを利用している場合）Python仮想環境を有効にする
```
conda activate ondevchatjp
```

### フリートーク形式のチャットボット
```
python -m ondevchatjp.free_chat
```

### RAGを使ったチャットボット
```
python -m ondevchatjp.rag_chat
```

### ベクトル検索
```
python -m ondevchatjp.vector_search
```



