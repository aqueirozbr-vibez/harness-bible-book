# Lab 03 — The transformer block

Runs the chapter's NumPy decoder block (`block.py`, extracted verbatim from Chapter 03) forward at Llama 3 8B dimensions on a 16-token sequence — shape, residual retention, and causal-mask checks — then reconciles `count_params` against the published Llama 3 totals (8.03B, 70.6B, 405.9B) from the paper's configurations. Reproduces every figure in 03.3 within 0.1%. CPU, under a minute. `python run.py`; exit 0 = reproduced.
