# Lab 32 — Self-improving harnesses

Runs the chapter's miner, branch runner, merge rule, and version bumper (`improve.py`, extracted verbatim from Chapter 32). Mines a synthetic month of failures into the chapter's ranked clusters; runs three branches on a 500-item golden set with a 20% holdout — a real fix (merged), an overfit fix (rejected on the holdout), a neutral edit (rejected for no gain); routes a safety-class branch to safety review; bumps versions by rule. CPU, seconds (seed 32). `python run.py`; exit 0 = reproduced.
