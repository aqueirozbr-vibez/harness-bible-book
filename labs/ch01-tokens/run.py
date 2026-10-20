#!/usr/bin/env python3
"""Lab 01 — Tokens and tokenizers. Trains the chapter's byte-level BPE (bpe.py, extracted verbatim) on a small synthetic
industrial corpus (English and Portuguese maintenance text with equipment tags; labelled synthetic) at three vocabulary
sizes. Reproduces: (1) round-trip fidelity; (2) tags fragment into more tokens than words of the same length at every
vocabulary size; (3) tokens per 1,000 words fall as vocabulary grows; (4) the embedding-matrix arithmetic of 01.3;
(5) the pre-tokenizer never merges across a letter–digit or punctuation boundary. Note: the corpus is too small to
measure a per-language ratio — that measurement is the reader's, with the production tokenizer on real text."""
import json, sys, subprocess, datetime, random
from bpe import BPE, PRE_TOKENIZE
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
random.seed(1)
EN = ["Replace the mechanical seal on pump P-101 following procedure MP-0417 revision 7.",
      "Isolation is covered by the permit process; the work order must cite the hazard class.",
      "Inspect bearing temperature on pump P-204 and record the reading in the equipment history.",
      "Order parts SEAL-88 and GASKET-12 from the approved list before scheduling the maintenance.",
      "The hot work permit applies when the pump handled hydrocarbons; see standard API 610 and ISO 14224."]
PT = ["Substituir o selo mecânico da bomba P-101 conforme o procedimento MP-0417 revisão 7.",
      "O isolamento é coberto pelo processo de permissão; a ordem de serviço deve citar a classe de risco.",
      "Inspecionar a temperatura do mancal da bomba P-204 e registrar a leitura no histórico do equipamento.",
      "Solicitar as peças SEAL-88 e GASKET-12 da lista aprovada antes de programar a manutenção.",
      "A permissão de trabalho a quente se aplica quando a bomba operou com hidrocarbonetos; ver API 610 e ISO 14224."]
corpus = " ".join(random.choice(EN + PT) for _ in range(400))
ok = True; results = {}
for V in (300, 600, 1200):
    t = BPE().train(corpus, V)
    sample = " ".join(EN)
    ids = t.encode(sample)
    words = len(sample.split()); tpw = len(ids) / words * 1000
    tags = ["P-101", "MP-0417", "SEAL-88", "ISO 14224"]; tag_tokens = {g: len(t.tokens(g)) for g in tags}
    word_tokens = {w: len(t.tokens(w)) for w in ["pump", "seal", "permit", "bomba", "procedimento"]}
    # round trip: decode ids back through the vocab
    inv = {v: k for k, v in t.vocab.items()}; rt = b"".join(inv[i] for i in ids).decode("utf-8") == sample
    results[V] = dict(tokens_per_1000_words=round(tpw), tag_tokens=tag_tokens, word_tokens=word_tokens, round_trip=rt)
    print(f"V={V:5d}: tokens/1000 words {tpw:6.0f}; round trip {rt}; tags {tag_tokens}; words {word_tokens}")
    ok &= rt
    ok &= sum(tag_tokens.values())/len(tag_tokens) > sum(word_tokens.values())/len(word_tokens)   # tags fragment more
# tokens per word must not increase with vocabulary
tp = [results[V]["tokens_per_1000_words"] for V in (300, 600, 1200)]; ok &= tp[0] >= tp[1] >= tp[2]
print("tokens per 1,000 words non-increasing with vocabulary:", tp[0] >= tp[1] >= tp[2])
# pre-tokenizer boundary property
pieces = PRE_TOKENIZE.findall("P-101 MP-0417"); boundary_ok = pieces == ["P", "-", "101", " ", "MP", "-", "0417"]
print("pre-tokenizer splits letter/digit/punctuation:", boundary_ok, pieces); ok &= boundary_ok
# embedding arithmetic
checks = [("Llama 3 8B embed params", d["embed_params_Llama 3 8B"], 128256*4096), ("Llama 3 8B embed share %", d["llama3_8B_embed_share_of_8B_pct"], 13.1),
          ("PT tokens/1000 words", d["tokens_per_1000_words_Portuguese"], 2000), ("PT words per 512-token chunk", d["words_in_512_token_chunk_Portuguese"], 256)]
for n, got, exp in checks:
    m = abs(got - exp) <= max(1, 0.01*exp); ok &= m; print(f"{n:28s} chapter {exp}  derived {got}  {'OK' if m else 'MISMATCH'}")
json.dump({"results": {str(k): v for k, v in results.items()}, "boundary_ok": boundary_ok, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 01:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
