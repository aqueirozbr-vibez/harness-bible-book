# Lab 19 — Context engineering

Runs the chapter's assembler (`context.py`, extracted verbatim from Chapter 19) through a simulated 16-iteration task (seed 19). Reproduces the constant compacted window against ~4.8× uncompacted growth, tool-result trimming from thousands of tokens to a few hundred with the reference id kept, the chunk-start fraction (near 0.67 compacted, drifting toward 0.93 uncompacted with history first), the instruction last, and compaction within budget. CPU, seconds. `python run.py`; exit 0 = reproduced. Token counts use a 4-chars/token stand-in.
