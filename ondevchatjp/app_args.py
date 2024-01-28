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


from typing import Any
import copy
import argparse
import ondevchatjp


def parse_args() -> tuple[argparse.Namespace, dict[str, Any]]:
    model_parser = ondevchatjp.get_model_arg_paser()
    parser = argparse.ArgumentParser(parents=[model_parser])
    parser.add_argument("--inbrowser", action="store_true", default=False,
        help="Launch the interface in a new tab on the default browser"
    )
    parser.add_argument("--share", action="store_true", default=False,
        help="Create a publicly shareable link for the interface"
    )
    args = parser.parse_args()
    model_kwargs = vars(copy.copy(args))
    del model_kwargs["inbrowser"]
    del model_kwargs["share"]
    if (model_kwargs["model_path"] is not None) and (model_kwargs["model_path"] != ""):
        model_kwargs["repo_id"] = ""
        model_kwargs["gguf_file"] = ""

    return args, model_kwargs
