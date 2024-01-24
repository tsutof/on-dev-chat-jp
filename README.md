# on-dev-chat-jp
Llama.cppベースのオンデバイス・チャットボット

詳細は以下の技術記事で紹介しています。

https://zenn.dev/tsutof/articles/177b3bd82b05e8

## インストール

### MacOS

1. FFmpegとPortAudioをbrewでインストール
    ```
    brew install ffmpeg portaudio
    ```

1. Python仮想環境をセットアップ（既存Python環境とのコンフリクトを避けるため、Miniforge3など仮想環境に本パッケージをインストールするよう推奨）
    ```
    conda create --name ondevchatjp python=3.10 --yes \
    && conda activate ondevchatjp
    ```

1. [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)パッケージをインストール。MacOSの場合、Metalによる高速化が有効になるよう設定する。
    ```
    CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
    ```

1. 本リポジトリをクローンして、インストール
    ```
    git clone https://github.com/tsutof/on-dev-chat-jp \
    && cd on-dev-chat-jp \
    && pip install -e .
    ```

### Linux (Ubuntu) OpenBLAS

1. OpenBLAS、FFmpeg、PortAudioをaptでインストール
    ```
    sudo apt update \
    && sudo apt install libopenblas-dev ffmpeg portaudio19-dev
    ```

1. Python仮想環境をセットアップ（既存Python環境とのコンフリクトを避けるため、Miniforge3など仮想環境に本パッケージをインストールするよう推奨）
    ```
    conda create --name ondevchatjp python=3.10 --yes \
    && conda activate ondevchatjp
    ```

1. [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)パッケージをインストール。OpenBLASによる高速化が有効になるよう設定する
    ```
    CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
    ```

1. 本リポジトリをクローンして、インストール
    ```
    git clone https://github.com/tsutof/on-dev-chat-jp \
    && cd on-dev-chat-jp \
    && pip install -e .
    ```

### Linux (Ubuntu) cuBLAS

1. FFmpeg、PortAudioをaptでインストール
    ```
    sudo apt update \
    && sudo apt install ffmpeg portaudio19-dev
    ```

1. Python仮想環境をセットアップ（既存Python環境とのコンフリクトを避けるため、Miniforge3など仮想環境に本パッケージをインストールするよう推奨）
    ```
    conda create --name ondevchatjp python=3.10 --yes \
    && conda activate ondevchatjp
    ```

1. [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)パッケージをインストール。cuBLASによる高速化が有効になるよう設定する
    ```
    CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
    ```

1. 本リポジトリをクローンして、インストール
    ```
    git clone https://github.com/tsutof/on-dev-chat-jp \
    && cd on-dev-chat-jp \
    && pip install -e .
    ```

## 実行方法

Python仮想環境を有効にする（Miniforgeを利用している場合）
```
conda activate ondevchatjp
```

### フリートーク形式のチャットボット
```
python -m ondevchatjp.free_chat
```

### 簡単なRAGを使ったチャットボット
```
python -m ondevchatjp.rag_chat
```

### ベクトル検索
```
python -m ondevchatjp.vector_search
```



