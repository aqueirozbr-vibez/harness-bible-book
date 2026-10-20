# Lab 27 — Graders and agent evaluation

Runs the chapter's grading, calibration, and CI-gate code (`graders.py`, extracted verbatim from Chapter 27) with a simulated grader carrying injected position and verbosity biases (stub, labelled; seed 27). Reproduces κ per criterion with retirement below 0.6, the chapter's κ example, verbosity bias made visible, the both-orders control turning a position-biased grader's spurious winners into ties, and the CI gate blocking a six-point regression while merging a no-change candidate on 300 items. CPU, seconds. `python run.py`; exit 0 = reproduced.
