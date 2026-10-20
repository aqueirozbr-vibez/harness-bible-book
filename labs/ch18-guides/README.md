# Lab 18 — Guides

Runs the chapter's assembler (`guides.py`, extracted verbatim from Chapter 18) on a synthetic work-order guide sized to the scenario's composition. Reproduces byte-identical assembly (one hash over 100 builds), refusal of volatile content (date, task id, time) at build time, the cache-minimum check, the element budget, the pairing audit (9 of 12 enforced, unenforced named), and window composition with the instruction last. CPU, seconds. `python run.py`; exit 0 = reproduced. Token counts use a 4-chars/token stand-in; production uses the model's tokenizer (ch01).
