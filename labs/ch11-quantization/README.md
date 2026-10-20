# Lab 11 — Quantization, distillation, small models

Runs the chapter's quantizer (`quant.py`, extracted verbatim from Chapter 11) on a 4,096×4,096 Gaussian weight matrix at 8 and 4 bits, per-tensor and per-group, with and without injected outliers, and reproduces the 11.3 error table, effective bits per weight, layer-output error, the memory-by-precision table, and the substitution saving. CPU, under a minute. `python run.py`; exit 0 = reproduced. The golden-set measurement per precision, class, and language (11.4) is on the plant's model.
