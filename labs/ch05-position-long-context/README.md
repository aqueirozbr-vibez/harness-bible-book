# Lab 05 — Positional encoding and long context

Runs the chapter's RoPE code (`rope.py`, extracted verbatim from Chapter 05). Reproduces the relative-position identity to floating-point precision, the wavelength tables at bases 10,000 and 500,000, the position-interpolation and NTK-aware extension parameters, the fill-versus-retrieve arithmetic, and norm preservation under rotation. CPU, seconds. `python run.py`; exit 0 = reproduced. The effective-length measurement (Lab 05b, described in 05.8) needs a model and the plant's golden set.
