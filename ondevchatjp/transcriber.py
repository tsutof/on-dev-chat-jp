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


import torch
import numpy as np
import whisper


class Transcriber:

    def __init__(self, model: str = "small") -> None:
        self.transcriber = whisper.load_model(model)

    def transcribe(self, y, sr: int) -> str:
        # Convert data type to floating point
        y = y.astype(np.float32)
        y /= np.max(np.abs(y))

        # Convert rate to 16kHz which is expected by Whisper
        y_tensor = torch.from_numpy(y).clone()
        resample_rate = whisper.audio.SAMPLE_RATE
        resampler = T.Resample(sr, resample_rate, dtype=y_tensor.dtype)
        y2_tensor = resampler(y_tensor)
        y2_float = y2_tensor.to("cpu").detach().numpy().copy()

        # Recognize voice
        result = self.transcriber.transcribe(
            y2_float, 
            verbose=True, 
            fp16=False, 
            language="ja"
        )
        text = result["text"]

        return text
