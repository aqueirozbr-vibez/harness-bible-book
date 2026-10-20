# Lab 07 — Pre-training data and pipelines

Runs the chapter's MinHash/LSH near-duplicate detector and 13-gram contamination check (`pipeline.py`, extracted verbatim from Chapter 07) on a synthetic corpus (seed 7). Reproduces the LSH flagging probabilities at 14 bands × 8 rows by simulation, recall of one-word revisions above 0.97 with no templated documents flagged at the 0.8 threshold, and detection of all five seeded golden-set leaks with no false hits. CPU, under a minute. `python run.py`; exit 0 = reproduced.
