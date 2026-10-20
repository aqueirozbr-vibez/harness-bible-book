import numpy as np

def expected_score(p_correct: float, wrong_penalty: float) -> float:
    """Expected score of answering at confidence p under +1 correct / -wrong_penalty wrong / 0 abstain."""
    return p_correct - (1 - p_correct) * wrong_penalty

def answer_threshold(cost_wrong: float, cost_abstain: float) -> float:
    """Answer only when P(correct) exceeds this; below it, abstaining is cheaper in expectation."""
    return 1 - cost_abstain / cost_wrong

def ece(confidence: np.ndarray, correct: np.ndarray, bins: int = 10) -> float:
    total = 0.0
    for i in range(bins):
        m = (confidence >= i / bins) & (confidence < (i + 1) / bins)
        if m.any():
            total += m.mean() * abs(correct[m].mean() - confidence[m].mean())
    return float(total)

def selective(confidence: np.ndarray, correct: np.ndarray, threshold: float):
    """Coverage and accuracy when answering only above the threshold."""
    m = confidence > threshold
    return float(m.mean()), float(correct[m].mean()) if m.any() else float("nan")

def harness_confidence(retrieval_support: bool, sensors_pass: bool, grader_agrees: bool) -> str:
    """The harness's stand-in for model confidence: answer, repair, or abstain."""
    if not retrieval_support:
        return "abstain"          # not in the governed documents → human
    if not sensors_pass:
        return "repair"           # deterministic check failed → loop
    return "answer" if grader_agrees else "review"
