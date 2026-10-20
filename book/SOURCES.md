# Book source registry (merged 23 Sep 2026, with links)

436 rows. Links: 322 URLs (arXiv/DOI/official/fetched), 32 repository paths, 74 none (illustrative, open, cross-reference), 8 needing fetch (Darú's book, RouterArena, JudgeBiasBench/RAND).

| Ch | # | Claim or figure | Source | Tier | Verified | Link |
|---|---|---|---|---|---|---|
| 01 | 1 | BPE for subword units | Sennrich, Haddow, Birch, ACL 2016, arXiv 1508.07909 | primary | Sep 2026 | https://arxiv.org/abs/1508.07909 |
| 01 | 2 | Byte-level BPE; 50,257 vocabulary | Radford et al., "Language Models are Unsupervised Multitask Learners," 2019 | primary | Sep 2026 | https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf |
| 01 | 3 | Unigram tokenization; subword regularization | Kudo, ACL 2018, arXiv 1804.10959 | primary | Sep 2026 | https://arxiv.org/abs/1804.10959 |
| 01 | 4 | SentencePiece | Kudo & Richardson, EMNLP 2018, arXiv 1808.06226 | primary | Sep 2026 | https://arxiv.org/abs/1808.06226 |
| 01 | 5 | WordPiece | Wu et al., Google NMT, 2016, arXiv 1609.08144 | primary | Sep 2026 | https://arxiv.org/abs/1609.08144 |
| 01 | 6 | Multilingual tax: Italian ~1.6×, Bulgarian ~2.6×, Portuguese/German ~1.5×, spread ~15× | Petrov, La Malfa, Torr, Bibi, NeurIPS 2023, arXiv 2305.15425 | primary | Sep 2026 | https://arxiv.org/abs/2305.15425 |
| 01 | 7 | Llama 3: 128,256 vocabulary, tiktoken-based, 100K + 28K; hidden sizes | Dubey et al., "The Llama 3 Herd of Models," 2024, arXiv 2407.21783 | primary | Sep 2026 | https://arxiv.org/abs/2407.21783 |
| 01 | 8 | Vocabulary sizes for GPT-4, GPT-4o/5, Llama 2, Llama 4, Gemma | Model cards and tokenizer releases | vendor | Sep 2026 | https://huggingface.co/models |
| 01 | 9 | Digit grouping in tiktoken/Llama 3; single digits in Llama 2 | Tokenizer documentation and source | vendor | Sep 2026 | https://huggingface.co/docs/tokenizers |
| 01 | 10 | Cache minimum prefix 1,024 tokens (larger for some small models) | Anthropic prompt-caching documentation | vendor | Sep 2026 | https://www.anthropic.com/engineering |
| 01 | 11 | Glitch tokens | Rumbelow & Watkins, "SolidGoldMagikarp," LessWrong, Feb 2023 | practitioner | Sep 2026 | https://www.lesswrong.com/posts/aPeJE8bSo6rAFoLqg/solidgoldmagikarp-plus-prompt-generation |
| 01 | 12 | Embedding parameters and sizes; tokens per 1,000 words; words per chunk; cache minimum in words; scenario input cost | `labs/ch01-tokens/derive.py` | derived | Sep 2026 | labs/ch01-tokens/derive.py |
| 01 | 13 | 0.75 words per token in English; 1.8 tokens per word for a legend; 20–40% formatting overhead | Rules of thumb and estimates | illustrative | Sep 2026 | — |
| 01 | 14 | Per-class token counts for industrial Portuguese text | None published | open | Sep 2026 | — |
| 02 | 1 | Distributed word representations | Mikolov et al., 2013, arXiv 1301.3781 | primary | Sep 2026 | https://arxiv.org/abs/1301.3781 |
| 02 | 2 | Sentence embeddings by contrastive training | Reimers & Gurevych, Sentence-BERT, EMNLP 2019, arXiv 1908.10084 | primary | Sep 2026 | https://arxiv.org/abs/1908.10084 |
| 02 | 3 | Dense passage retrieval | Karpukhin et al., EMNLP 2020, arXiv 2004.04906 | primary | Sep 2026 | https://arxiv.org/abs/2004.04906 |
| 02 | 4 | HNSW approximate search | Malkov & Yashunin, 2018, arXiv 1603.09320 | primary | Sep 2026 | https://arxiv.org/abs/1603.09320 |
| 02 | 5 | FAISS; IVF and product quantization | Johnson, Douze, Jégou, 2017, arXiv 1702.08734 | primary | Sep 2026 | https://arxiv.org/abs/1702.08734 |
| 02 | 6 | BM25 | Robertson & Zaragoza, "The Probabilistic Relevance Framework," 2009 | primary | Sep 2026 | https://doi.org/10.1561/1500000019 |
| 02 | 7 | Cross-encoder re-ranking | Nogueira & Cho, "Passage Re-ranking with BERT," 2019, arXiv 1901.04085 | primary | Sep 2026 | https://arxiv.org/abs/1901.04085 |
| 02 | 8 | Matryoshka representation learning; truncatable dimensions | Kusupati et al., NeurIPS 2022, arXiv 2205.13147; provider docs | primary / vendor | Sep 2026 | https://arxiv.org/abs/2205.13147 |
| 02 | 9 | MTEB benchmark | Muennighoff et al., 2022, arXiv 2210.07316 | primary (benchmark) | Sep 2026 | https://arxiv.org/abs/2210.07316 |
| 02 | 10 | Hybrid + contextual chunks: −49% top-20 retrieval failures; −67% with re-ranking | Anthropic, "Introducing Contextual Retrieval," Sep 2024 | vendor | Sep 2026 | https://www.anthropic.com/news/contextual-retrieval |
| 02 | 11 | Index sizes; noise-floor curve; brute-force cost; embedding-line costs | `labs/ch02-embeddings/derive.py` | derived | Sep 2026 | labs/ch02-embeddings/derive.py |
| 02 | 12 | 20,000 documents × 12 chunks; $0.13/M embedding rate; 10 GFLOP/s; three retrievals per query | Scenario and illustrative rates | illustrative / scenario | Sep 2026 | — |
| 02 | 13 | Per-language retrieval quality on industrial technical text | None published | open | Sep 2026 | — |
| 03 | 1 | The transformer block; original FFN at $4d$ with ReLU | Vaswani et al., NeurIPS 2017 | primary | Sep 2026 | https://arxiv.org/abs/1706.03762 |
| 03 | 2 | Residual connections | He et al., CVPR 2016 | primary | Sep 2026 | https://arxiv.org/abs/1512.03385 |
| 03 | 3 | Residual stream as a communication channel | Elhage et al., "A Mathematical Framework for Transformer Circuits," Anthropic, 2021 | primary | Sep 2026 | https://www.anthropic.com/engineering |
| 03 | 4 | Pre-norm stabilizes deep transformers | Xiong et al., ICML 2020, arXiv 2002.04745 | primary | Sep 2026 | https://arxiv.org/abs/2002.04745 |
| 03 | 5 | LayerNorm; RMSNorm | Ba, Kiros, Hinton 2016, arXiv 1607.06450; Zhang & Sennrich, NeurIPS 2019, arXiv 1910.07467 | primary | Sep 2026 | https://arxiv.org/abs/1607.06450 |
| 03 | 6 | SwiGLU | Shazeer, "GLU Variants Improve Transformer," 2020, arXiv 2002.05202 | primary | Sep 2026 | https://arxiv.org/abs/2002.05202 |
| 03 | 7 | FFN layers as key–value memories | Geva et al., EMNLP 2021, arXiv 2012.14913 | primary | Sep 2026 | https://arxiv.org/abs/2012.14913 |
| 03 | 8 | Induction heads | Olsson et al., Anthropic, 2022 | primary | Sep 2026 | https://www.anthropic.com/engineering |
| 03 | 9 | Superposition; interpretable features at scale | Templeton et al., "Scaling Monosemanticity," Anthropic, 2024 | primary | Sep 2026 | https://www.anthropic.com/engineering |
| 03 | 10 | Llama 3 configurations; untied output projection; published sizes | Dubey et al., 2024, arXiv 2407.21783, Table 3 and model cards | primary / vendor | Sep 2026 | https://arxiv.org/abs/2407.21783 |
| 03 | 11 | FLOPs per token ≈ $2N$ | Kaplan et al., "Scaling Laws for Neural Language Models," 2020, arXiv 2001.08361 | primary | Sep 2026 | https://arxiv.org/abs/2001.08361 |
| 03 | 12 | Per-layer and total parameter counts; shares; FLOPs per token; weight sizes by precision | `labs/ch03-transformer-block/derive.py` | derived | Sep 2026 | labs/ch03-transformer-block/derive.py |
| 03 | 13 | 400 TFLOP/s sustained; 20 GB cache headroom | Illustrative (ch04) | illustrative | Sep 2026 | — |
| 03 | 14 | Configurations of closed frontier models | Not disclosed | open | Sep 2026 | — |
| 04 | 1 | Scaled dot-product attention; 1/√d_k variance argument; h=8, d_model=512, d_k=64 | Vaswani et al., "Attention Is All You Need," NeurIPS 2017, §3.2 | primary | Sep 2026 | https://arxiv.org/abs/1706.03762 |
| 04 | 2 | Multi-query attention; decode bandwidth argument | Shazeer, "Fast Transformer Decoding," 2019, arXiv 1911.02150 | primary | Sep 2026 | https://arxiv.org/abs/1911.02150 |
| 04 | 3 | GQA; uptraining with ~5% compute; GQA-8 on T5-XXL near MHA quality at near-MQA speed | Ainslie et al., "GQA," EMNLP 2023, arXiv 2305.13245 | primary | Sep 2026 | https://arxiv.org/abs/2305.13245 |
| 04 | 4 | Llama 2 70B: 64 query heads, 8 KV heads | Touvron et al., "Llama 2," 2023, arXiv 2307.09288 | primary | Sep 2026 | https://arxiv.org/abs/2307.09288 |
| 04 | 5 | Llama 3 8B/70B/405B layers, heads, KV heads, model dimension, head dim 128 | Dubey et al., "The Llama 3 Herd of Models," 2024, arXiv 2407.21783, Table 3 | primary | Sep 2026 | https://arxiv.org/abs/2407.21783 |
| 04 | 6 | FlashAttention: 15% BERT-large MLPerf 1.1; 3× GPT-2 at 1K; 2.4× LRA; linear memory | Dao et al., NeurIPS 2022, arXiv 2205.14135, abstract | primary | Sep 2026 | https://arxiv.org/abs/2205.14135 |
| 04 | 7 | FlashAttention-2: ~2× over v1; 50–73% of A100 peak; 230 TFLOPs/s kernel; 225 TFLOPs/s (72% MFU) end-to-end; up to 9× vs PyTorch; 335 TFLOPs/s on H100 | Dao, 2023, arXiv 2307.08691; Stanford CRFM blog 17 Jul 2023 | primary / vendor | Sep 2026 | https://arxiv.org/abs/2307.08691 |
| 04 | 8 | FlashAttention-3: 1.5–2.0× over FA2; 740 TFLOPs/s = 75% H100; FP8 ~1.2 PFLOPs/s with 2.6× lower error; FA2 at 35% on H100 | Shah et al., 2024, arXiv 2407.08608; Together AI blog 11 Jul 2024 | primary / vendor | Sep 2026 | https://arxiv.org/abs/2407.08608 |
| 04 | 9 | Sparse transformers O(n√n) | Child et al., 2019, arXiv 1904.10509 | primary | Sep 2026 | https://arxiv.org/abs/1904.10509 |
| 04 | 10 | Sliding-window attention; receptive field grows by w per layer | Beltagy et al., "Longformer," 2020, arXiv 2004.05150 | primary | Sep 2026 | https://arxiv.org/abs/2004.05150 |
| 04 | 11 | Mistral 7B: window 4,096; 32 layers; 32 heads; 8 KV heads; rolling buffer | Jiang et al., "Mistral 7B," 2023, arXiv 2310.06825 | primary | Sep 2026 | https://arxiv.org/abs/2310.06825 |
| 04 | 12 | MLA: d_c=512, d_h^R=64, 128 heads × 128; 93.3% KV reduction and 5.76× throughput vs DeepSeek 67B | DeepSeek-AI, "DeepSeek-V2," 2024, arXiv 2405.04434, §2.1 and abstract | primary | Sep 2026 | https://arxiv.org/abs/2405.04434 |
| 04 | 12a | Induction heads implement in-context copying | Olsson et al., "In-context Learning and Induction Heads," Anthropic 2022 | primary | Sep 2026 | https://www.anthropic.com/engineering |
| 04 | 12b | Linear attention; selective state-space models | Katharopoulos et al. 2020, arXiv 2006.16236; Gu & Dao, "Mamba," 2023, arXiv 2312.00752 | primary | Sep 2026 | https://arxiv.org/abs/2006.16236 |
| 04 | 13 | Prior serving systems use 20.4–38.2% of KV memory; paged cache | Kwon et al., "PagedAttention," SOSP 2023 | primary | Sep 2026 | https://arxiv.org/abs/2309.06180 |
| 04 | 13a | Attention sinks; StreamingLLM keeps initial tokens plus a window | Xiao et al., "Efficient Streaming Language Models with Attention Sinks," 2023, arXiv 2309.17453 | primary | Sep 2026 | https://arxiv.org/abs/2309.17453 |
| 04 | 14 | H100 SXM HBM bandwidth ~3.35 TB/s | NVIDIA H100 datasheet | vendor | Sep 2026 | https://www.nvidia.com/en-us/data-center/h100/ |
| 04 | 15 | SDPA backend selection; HF `attn_implementation` | PyTorch 2.x docs; Hugging Face Transformers docs | vendor | Sep 2026 | https://huggingface.co/docs/tokenizers |
| 04 | 16 | KV bytes/token for Llama 3 sizes; no-GQA counterfactual; cache-per-sequence table; attention vs MLP arithmetic at 8K/32K/128K; decode read times | Derived in this chapter from sources 5 and 14 | primary arithmetic; MLP multiplier illustrative | Sep 2026 | — |
| 04 | 17 | Crossover context ~2d–4d; fallback headroom of ~10 sequences | Derived; illustrative | illustrative | Sep 2026 | — |
| 04 | 18 | Attention share of end-to-end decode latency at 32K–128K on production stacks; GQA/MLA quality on agentic tasks | No independent published measurement found | open | Sep 2026 | — |
| 05 | 1 | Sinusoidal absolute encoding | Vaswani et al., NeurIPS 2017 | primary | Sep 2026 | https://arxiv.org/abs/1706.03762 |
| 05 | 2 | Learned absolute positions | Radford et al. 2019; Devlin et al. 2019 | primary | Sep 2026 | https://arxiv.org/abs/2306.00978 |
| 05 | 3 | RoPE; relative-position property | Su et al., "RoFormer," 2021, arXiv 2104.09864 | primary | Sep 2026 | https://arxiv.org/abs/2104.09864 |
| 05 | 4 | ALiBi | Press, Smith, Lewis, ICLR 2022, arXiv 2108.12409 | primary | Sep 2026 | https://arxiv.org/abs/2108.12409 |
| 05 | 5 | Position interpolation | Chen et al., 2023, arXiv 2306.15595 | primary | Sep 2026 | https://arxiv.org/abs/2306.15595 |
| 05 | 6 | NTK-aware base scaling; YaRN | bloc97, 2023 (community post); Peng et al., 2023, arXiv 2309.00071 | practitioner / primary | Sep 2026 | https://arxiv.org/abs/2309.00071 |
| 05 | 7 | Llama 3.1: base 500,000; staged extension to 128K | Dubey et al., 2024, arXiv 2407.21783 | primary | Sep 2026 | https://arxiv.org/abs/2407.21783 |
| 05 | 8 | RULER: effective vs advertised length | Hsieh et al., 2024, arXiv 2404.06654 | primary | Sep 2026 | https://arxiv.org/abs/2404.06654 |
| 05 | 9 | NoLiMa: 11/13 below 50% at 32K; GPT-4o 99.3 → 69.7 → 56; effective 8K / 2K at 85% | Modarressi et al., ICML 2025, arXiv 2502.05167 | primary | Sep 2026 | https://arxiv.org/abs/2502.05167 |
| 05 | 10 | Lost in the middle | Liu et al., 2023, arXiv 2307.03172 | primary | Sep 2026 | https://arxiv.org/abs/2307.03172 |
| 05 | 11 | Agent distraction beyond ~100K | Gemini 2.5 Technical Report, 2025, arXiv 2507.06261 | primary | Sep 2026 | https://arxiv.org/abs/2507.06261 |
| 05 | 12 | Needle-in-a-haystack | Kamradt, 2023 | practitioner | Sep 2026 | https://github.com/gkamradt/LLMTest_NeedleInAHaystack |
| 05 | 13 | Wavelengths; extension parameters; attention, cache, and bill at 6K vs 128K; NoLiMa ratios | `labs/ch05-position-long-context/derive.py` | derived | Sep 2026 | labs/ch05-position-long-context/derive.py |
| 05 | 14 | 150,000-token manual; a few hundred dollars for the measurement | Illustrative | illustrative | Sep 2026 | — |
| 05 | 15 | Effective length on Portuguese industrial text | None published | open | Sep 2026 | — |
| 06 | 1 | $6ND$ training compute; power-law scaling; favor parameters | Kaplan et al., 2020, arXiv 2001.08361 | primary | Sep 2026 | https://arxiv.org/abs/2001.08361 |
| 06 | 2 | Chinchilla: ~20 tokens per parameter; 70B/1.4T beats 280B/300B; parametric fit constants | Hoffmann et al., 2022, arXiv 2203.15556 | primary | Sep 2026 | https://arxiv.org/abs/2203.15556 |
| 06 | 3 | Replication: published fit inconsistent; refit ~20–25 | Besiroglu et al., Epoch AI, 2024, arXiv 2404.10102 | analyst | Sep 2026 | https://arxiv.org/abs/2404.10102 |
| 06 | 4 | Inference-aware optimum: smaller N, larger D | Sardana & Frankle, 2023, arXiv 2401.00448 | primary | Sep 2026 | https://arxiv.org/abs/2401.00448 |
| 06 | 5 | Mixture of experts; load-balancing loss | Shazeer et al., 2017, arXiv 1701.06538; Fedus, Zoph, Shazeer, 2022, arXiv 2101.03961 | primary | Sep 2026 | https://arxiv.org/abs/1701.06538 |
| 06 | 6 | DeepSeek-V3: 671B / 37B active; 256 + 1 shared experts; auxiliary-loss-free balancing; 14.8T tokens; 2.79M GPU-hours | DeepSeek-AI, 2024, arXiv 2412.19437 | primary | Sep 2026 | https://arxiv.org/abs/2412.19437 |
| 06 | 7 | Llama 3 tokens (~15T; 15.6T for 405B); 3.8 × 10²⁵ FLOPs | Dubey et al., 2024, arXiv 2407.21783 | primary | Sep 2026 | https://arxiv.org/abs/2407.21783 |
| 06 | 8 | GPT-3 175B on 300B tokens | Brown et al., 2020, arXiv 2005.14165 | primary | Sep 2026 | https://arxiv.org/abs/2005.14165 |
| 06 | 9 | Mixtral, Llama 4, Qwen3 parameter and expert counts | Model cards and reports | vendor | Sep 2026 | https://huggingface.co/models |
| 06 | 10 | Optimal ratios under the published fit; over-training comparison; MoE memory and compute; balanced expert share | `labs/ch06-scale/derive.py` | derived | Sep 2026 | labs/ch06-scale/derive.py |
| 06 | 10a | Data stock estimates | Villalobos et al., Epoch AI, 2022–2024 | analyst | Sep 2026 | https://epoch.ai/ |
| 06 | 10b | Repeated-epoch returns | Muennighoff et al., 2023, arXiv 2305.16264 | primary | Sep 2026 | https://arxiv.org/abs/2305.16264 |
| 06 | 10c | Emergent abilities; mirage under continuous metrics | Wei et al., 2022, arXiv 2206.07682; Schaeffer, Miranda, Koyejo, 2023, arXiv 2304.15004 | primary | Sep 2026 | https://arxiv.org/abs/2206.07682 |
| 06 | 11 | Corrected fit constants from the replication | Not reproduced here | open | Sep 2026 | — |
| 07 | 1 | Llama 3: ~15T tokens; mixture ~50/25/17/8; annealing | Dubey et al., 2024, arXiv 2407.21783 | primary | Sep 2026 | https://arxiv.org/abs/2407.21783 |
| 07 | 2 | FineWeb: 96 snapshots, 15T tokens; extractor and filter ablations; FineWeb-Edu | Penedo et al., 2024, arXiv 2406.17557 | primary | Sep 2026 | https://arxiv.org/abs/2406.17557 |
| 07 | 3 | RefinedWeb pipeline | Penedo et al., 2023, arXiv 2306.01116 | primary | Sep 2026 | https://arxiv.org/abs/2306.01116 |
| 07 | 4 | Dolma; The Pile | Soldaini et al., 2024, arXiv 2402.00159; Gao et al., 2020, arXiv 2101.00027 | primary | Sep 2026 | https://arxiv.org/abs/2402.00159 |
| 07 | 5 | Gopher and C4 filtering rules | Rae et al., 2021, arXiv 2112.11446; Raffel et al., 2020, arXiv 1910.10683 | primary | Sep 2026 | https://arxiv.org/abs/2112.11446 |
| 07 | 6 | Deduplication improves models; ~10× less memorized emission | Lee et al., 2022, arXiv 2107.06499 | primary | Sep 2026 | https://arxiv.org/abs/2107.06499 |
| 07 | 7 | MinHash | Broder, "On the resemblance and containment of documents," 1997 | primary | Sep 2026 | https://doi.org/10.1109/SEQUEN.1997.666900 |
| 07 | 8 | 13-gram decontamination | Brown et al., 2020, arXiv 2005.14165 | primary | Sep 2026 | https://arxiv.org/abs/2005.14165 |
| 07 | 9 | Repeated epochs: returns diminish after ~4 | Muennighoff et al., 2023, arXiv 2305.16264 | primary | Sep 2026 | https://arxiv.org/abs/2305.16264 |
| 07 | 10 | Datasheets for datasets | Gebru et al., CACM 2021 | primary | Sep 2026 | https://doi.org/10.1145/3458723 |
| 07 | 11 | Training-data extraction | Carlini et al., 2021, arXiv 2012.07805 | primary | Sep 2026 | https://arxiv.org/abs/2012.07805 |
| 07 | 12 | Recursion on model-generated data | Shumailov et al., 2023, arXiv 2305.17493 | primary | Sep 2026 | https://arxiv.org/abs/2305.17493 |
| 07 | 13 | LSH probabilities and thresholds; corpus proportions; contamination probabilities | `labs/ch07-data/derive.py` | derived | Sep 2026 | labs/ch07-data/derive.py |
| 07 | 14 | Scenario corpus counts; ingestion-run figures; leak rates | Illustrative | illustrative | Sep 2026 | — |
| 07 | 15 | Near-duplicate structure of industrial corpora | None published | open | Sep 2026 | — |
| 08 | 1 | RLHF from preferences | Christiano et al., 2017, arXiv 1706.03741; Stiennon et al., 2020, arXiv 2009.01325 | primary | Sep 2026 | https://arxiv.org/abs/1706.03741 |
| 08 | 2 | InstructGPT: 1.3B preferred over 175B; ~13k / 33k / 31k prompts | Ouyang et al., 2022, arXiv 2203.02155 | primary | Sep 2026 | https://arxiv.org/abs/2203.02155 |
| 08 | 3 | DPO objective; matches or exceeds PPO-RLHF on measured tasks | Rafailov et al., NeurIPS 2023, arXiv 2305.18290 | primary | Sep 2026 | https://arxiv.org/abs/2305.18290 |
| 08 | 4 | Constitutional AI | Bai et al., 2022, arXiv 2212.08073 | primary | Sep 2026 | https://arxiv.org/abs/2212.08073 |
| 08 | 5 | GRPO | Shao et al., "DeepSeekMath," 2024, arXiv 2402.03300 | primary | Sep 2026 | https://arxiv.org/abs/2402.03300 |
| 08 | 6 | RLVR; emergent reasoning; verifier limit | DeepSeek-AI, "DeepSeek-R1," Nature 2025 | primary | Sep 2026 | https://api-docs.deepseek.com/quick_start/pricing |
| 08 | 7 | LoRA: 10,000× fewer trainable params, 3× memory | Hu et al., 2021, arXiv 2106.09685 | primary | Sep 2026 | https://arxiv.org/abs/2106.09685 |
| 08 | 8 | QLoRA | Dettmers et al., 2023, arXiv 2305.14314 | primary | Sep 2026 | https://arxiv.org/abs/2305.14314 |
| 08 | 9 | Reward-model over-optimization | Gao, Schulman, Hilton, 2023, arXiv 2210.10760 | primary | Sep 2026 | https://arxiv.org/abs/2210.10760 |
| 08 | 10 | Sycophancy from preference data | Sharma et al., Anthropic, 2023, arXiv 2310.13548 | primary | Sep 2026 | https://arxiv.org/abs/2310.13548 |
| 08 | 11 | Fine-tuning compromises safety | Qi et al., 2023, arXiv 2310.03693 | primary | Sep 2026 | https://arxiv.org/abs/2310.03693 |
| 08 | 12 | LIMA: 1,000 examples | Zhou et al., 2023, arXiv 2305.11206 | primary | Sep 2026 | https://arxiv.org/abs/2305.11206 |
| 08 | 12a | Instruction hierarchy | Wallace et al., OpenAI, 2024, arXiv 2404.13208 | primary | Sep 2026 | https://arxiv.org/abs/2404.13208 |
| 08 | 12b | Knowledge distillation; distilled reasoning models | Hinton, Vinyals, Dean, 2015, arXiv 1503.02531; DeepSeek-AI 2025 | primary | Sep 2026 | https://arxiv.org/abs/1503.02531 |
| 08 | 13 | Adapter sizes; DPO loss values; GRPO advantages; fine-tune compute and hours; interval widths | `labs/ch08-post-training/derive.py` | derived | Sep 2026 | labs/ch08-post-training/derive.py |
| 08 | 14 | 300 TFLOP/s sustained; scenario pass rates; 2,000 pairs | Illustrative | illustrative | Sep 2026 | — |
| 08 | 15 | Site-style adapter effect on an industrial golden set | None published | open | Sep 2026 | — |
| 09 | 1 | Chain-of-thought prompting | Wei et al., 2022, arXiv 2201.11903 | primary | Sep 2026 | https://arxiv.org/abs/2201.11903 |
| 09 | 2 | Zero-shot chain of thought | Kojima et al., 2022, arXiv 2205.11916 | primary | Sep 2026 | https://arxiv.org/abs/2205.11916 |
| 09 | 3 | Self-consistency; ~+18 points on GSM8K (PaLM 540B) | Wang et al., 2022, arXiv 2203.11171 | primary | Sep 2026 | https://arxiv.org/abs/2203.11171 |
| 09 | 4 | Coverage scaling with samples | Brown et al., "Large Language Monkeys," 2024, arXiv 2407.21787 | primary | Sep 2026 | https://arxiv.org/abs/2407.21787 |
| 09 | 5 | Process supervision beats outcome supervision | Lightman et al., 2023, arXiv 2305.20050 | primary | Sep 2026 | https://arxiv.org/abs/2305.20050 |
| 09 | 6 | Tree of Thoughts | Yao et al., 2023, arXiv 2305.10601 | primary | Sep 2026 | https://arxiv.org/abs/2305.10601 |
| 09 | 7 | Compute-optimal test-time scaling; can match a 14× larger model | Snell et al., 2024, arXiv 2408.03314 | primary | Sep 2026 | https://arxiv.org/abs/2408.03314 |
| 09 | 8 | RL-trained reasoning; distilled variants | DeepSeek-AI, "DeepSeek-R1," Nature 2025 | primary | Sep 2026 | https://api-docs.deepseek.com/quick_start/pricing |
| 09 | 9 | Complexity collapse; token use falls past threshold | Shojaee et al., Apple, 2025 | primary | Sep 2026 | https://machinelearning.apple.com/research/illusion-of-thinking |
| 09 | 10 | Unfaithful chain of thought | Turpin et al., 2023, arXiv 2305.04388 | primary | Sep 2026 | https://arxiv.org/abs/2305.04388 |
| 09 | 10a | Chain of thought extends expressive power with sequence length | Merrill & Sabharwal, ICLR 2024, arXiv 2310.07923 | primary | Sep 2026 | https://arxiv.org/abs/2310.07923 |
| 09 | 11 | Reasoning tokens billed as output; effort controls | OpenAI, Anthropic, Google documentation | vendor | Sep 2026 | https://openai.com/index/ |
| 09 | 12 | Costs, latencies, majority and coverage tables, imperfect-verifier results, sandwich saving | `labs/ch09-reasoning/derive.py` | derived | Sep 2026 | labs/ch09-reasoning/derive.py |
| 09 | 13 | 50 tokens/s; 2,000-token budgets; per-sample accuracies | Illustrative | illustrative | Sep 2026 | — |
| 09 | 14 | Accuracy–effort curve per step class on industrial tasks | None published | open | Sep 2026 | — |
| 09 | C | Cost-optimization checklist measured on a claims agent: 10-claim eval, 2 trials per configuration | Anthropic, "Cost Optimization on the Claude API," Claude Cookbook, Aug 2026 (Lehrburger) | vendor | Sep 2026 | https://platform.claude.com/cookbook/cost-optimization-cost-optimization |
| 10 | 1 | Roofline model | Williams, Waterman, Patterson, CACM 2009 | primary | Sep 2026 | https://doi.org/10.1145/1498765.1498785 |
| 10 | 2 | Transformer inference roofline; batching; parallelism | Pope et al., 2022, arXiv 2211.05102 | primary | Sep 2026 | https://arxiv.org/abs/2211.05102 |
| 10 | 3 | PagedAttention; 20.4–38.2% prior utilization; 2–4× throughput; 16-token blocks | Kwon et al., SOSP 2023 | primary | Sep 2026 | https://arxiv.org/abs/2309.06180 |
| 10 | 4 | Continuous batching | Yu et al., "Orca," OSDI 2022 | primary | Sep 2026 | https://www.usenix.org/conference/osdi22/presentation/yu |
| 10 | 5 | Speculative decoding; distribution preserved | Leviathan, Kalman, Matias, ICML 2023, arXiv 2211.17192; Chen et al., 2023, arXiv 2302.01318 | primary | Sep 2026 | https://arxiv.org/abs/2211.17192 |
| 10 | 6 | Prefix caching / RadixAttention | Zheng et al., "SGLang," 2023, arXiv 2312.07104; vLLM docs | primary / vendor | Sep 2026 | https://arxiv.org/abs/2312.07104 |
| 10 | 7 | Tensor parallelism | Shoeybi et al., "Megatron-LM," 2019, arXiv 1909.08053 | primary | Sep 2026 | https://arxiv.org/abs/1909.08053 |
| 10 | 8 | H100 SXM: ~989 TFLOP/s dense fp16; 3.35 TB/s HBM3 | NVIDIA H100 datasheet | vendor | Sep 2026 | https://www.nvidia.com/en-us/data-center/h100/ |
| 10 | 9 | Serving stacks and their features | vLLM, SGLang, TensorRT-LLM, TGI documentation | vendor | Sep 2026 | https://docs.vllm.ai/ |
| 10 | 10 | $2.99 per H100-hour | RunPod on-demand (ch37) | vendor | Sep 2026 | — |
| 10 | 11 | Floors, ridge, crossover, capacity, throughput, cost per token, speculative gains, prefill times | `labs/ch10-inference/derive.py` | derived | Sep 2026 | labs/ch10-inference/derive.py |
| 10 | 12 | 40% and 70% utilization; 6,000-token context | Illustrative / scenario | illustrative | Sep 2026 | — |
| 10 | 13 | Measured stack efficiency on current versions | None published in comparable form | open | Sep 2026 | — |
| 11 | 1 | Outlier features; LLM.int8 mixed precision | Dettmers et al., 2022, arXiv 2208.07339 | primary | Sep 2026 | https://arxiv.org/abs/2208.07339 |
| 11 | 2 | GPTQ | Frantar et al., 2022, arXiv 2210.17323 | primary | Sep 2026 | https://arxiv.org/abs/2210.17323 |
| 11 | 3 | AWQ | Lin et al., 2023, arXiv 2306.00978 | primary | Sep 2026 | https://arxiv.org/abs/2306.00978 |
| 11 | 4 | SmoothQuant | Xiao et al., 2022, arXiv 2211.10438 | primary | Sep 2026 | https://arxiv.org/abs/2211.10438 |
| 11 | 5 | QLoRA; NF4 | Dettmers et al., 2023, arXiv 2305.14314 | primary | Sep 2026 | https://arxiv.org/abs/2305.14314 |
| 11 | 6 | FP8 formats | Micikevicius et al., 2022, arXiv 2209.05433 | primary | Sep 2026 | https://arxiv.org/abs/2209.05433 |
| 11 | 7 | Knowledge distillation | Hinton, Vinyals, Dean, 2015, arXiv 1503.02531 | primary | Sep 2026 | https://arxiv.org/abs/1503.02531 |
| 11 | 8 | Distilled reasoning models | DeepSeek-AI, "DeepSeek-R1," Nature 2025 | primary | Sep 2026 | https://api-docs.deepseek.com/quick_start/pricing |
| 11 | 9 | Small models for agent subtasks; 10–30× cheaper; limits on multi-hop and tool syntax | Belcak et al., NVIDIA Research, 2025, arXiv 2506.02153 | primary | Sep 2026 | https://arxiv.org/abs/2506.02153 |
| 11 | 9a | One-shot pruning | Frantar & Alistarh, "SparseGPT," 2023, arXiv 2301.00774 | primary | Sep 2026 | https://arxiv.org/abs/2301.00774 |
| 11 | 10 | GGUF / llama.cpp quantization types | llama.cpp documentation | practitioner | Sep 2026 | https://github.com/ggml-org/llama.cpp |
| 11 | 11 | FP8/INT8 KV cache support | vLLM, TensorRT-LLM documentation | vendor | Sep 2026 | https://docs.vllm.ai/ |
| 11 | 12 | Memory by precision; error tables; overhead bits; floors; distillation cost; substitution saving | `labs/ch11-quantization/derive.py` | derived | Sep 2026 | labs/ch11-quantization/derive.py |
| 11 | 13 | 0.01% outliers at 50×; 50,000 examples × 800 tokens; review rates | Illustrative | illustrative | Sep 2026 | — |
| 11 | 14 | 4-bit effects on Portuguese technical text | None published | open | Sep 2026 | — |
| 12 | 1 | Wilson score interval | Wilson, JASA 1927 | primary | Sep 2026 | https://doi.org/10.1080/01621459.1927.10502953 |
| 12 | 2 | Bootstrap | Efron, Annals of Statistics 1979 | primary | Sep 2026 | https://doi.org/10.1214/aos/1176344552 |
| 12 | 3 | Significance testing practice in NLP | Dror et al., ACL 2018 | primary | Sep 2026 | https://aclanthology.org/P18-1128/ |
| 12 | 4 | Cohen's κ; Krippendorff's α | Cohen 1960; Krippendorff, Content Analysis, 2004 | primary | Sep 2026 | https://doi.org/10.1177/001316446002000104 |
| 12 | 5 | Grader agreement 85% vs 81%; position, verbosity, self-enhancement biases | Zheng et al., NeurIPS 2023, arXiv 2306.05685 | primary | Sep 2026 | https://arxiv.org/abs/2306.05685 |
| 12 | 6 | MMLU; HELM; SWE-bench; SWE-bench Verified; τ-bench | Hendrycks 2021 (2009.03300); Liang 2022 (2211.09110); Jimenez 2023 (2310.06770); Chowdhury 2024; Yao 2024 (2406.12045) | primary | Sep 2026 | https://arxiv.org/abs/2310.06770 |
| 12 | 7 | Benchmark contamination | Sainz et al., EMNLP Findings 2023, arXiv 2310.18018 | primary | Sep 2026 | https://arxiv.org/abs/2310.18018 |
| 12 | 8 | MMLU label errors | Gema et al., 2024, arXiv 2406.04127 | primary | Sep 2026 | https://arxiv.org/abs/2406.04127 |
| 12 | 9 | Reproducible evaluation framework | UK AI Security Institute, Inspect AI documentation | primary | Sep 2026 | https://inspect.aisi.org.uk/ |
| 12 | 10 | Interval table; power table; κ example; golden-set sizes; run cost; contamination probability | `labs/ch12-evaluation/derive.py` | derived | Sep 2026 | labs/ch12-evaluation/derive.py |
| 12 | 11 | $0.009 per query (configuration C) | ch37 | derived | Sep 2026 | — |
| 12 | 12 | Eleven classes; six weeks of labelling; κ = 0.71; the Portuguese permit-judgment finding | Illustrative | illustrative | Sep 2026 | — |
| 12 | 13 | A public golden set for industrial maintenance work | None exists | open | Sep 2026 | — |
| 13 | 1 | Hallucination as classification error; binary grading rewards guessing; singleton floor | Kalai, Nachum, Vempala, Zhang, OpenAI, 2025, arXiv 2509.04664 | primary | Sep 2026 | https://arxiv.org/abs/2509.04664 |
| 13 | 2 | Expected calibration error | Guo et al., ICML 2017, arXiv 1706.04599 | primary | Sep 2026 | https://arxiv.org/abs/1706.04599 |
| 13 | 3 | Base-model calibration and its limits | Kadavath et al., Anthropic, 2022, arXiv 2207.05221 | primary | Sep 2026 | https://arxiv.org/abs/2207.05221 |
| 13 | 4 | Sycophancy from preference data | Sharma et al., Anthropic, 2023, arXiv 2310.13548 | primary | Sep 2026 | https://arxiv.org/abs/2310.13548 |
| 13 | 5 | Indirect prompt injection; adaptive attacks break twelve defences (>90%) | Greshake et al., 2023, arXiv 2302.12173; Nasr et al., 2025 | primary | Sep 2026 | https://arxiv.org/abs/2302.12173 |
| 13 | 6 | Over-refusal on safe prompts | Röttger et al., "XSTest," 2023, arXiv 2308.01263 | primary | Sep 2026 | https://arxiv.org/abs/2308.01263 |
| 13 | 7 | Training-data extraction | Carlini et al., 2021, arXiv 2012.07805 | primary | Sep 2026 | https://arxiv.org/abs/2012.07805 |
| 13 | 8 | Bias and fairness survey | Gallegos et al., 2024, arXiv 2309.00770 | primary | Sep 2026 | https://arxiv.org/abs/2309.00770 |
| 13 | 9 | Scoring-rule table; selective-prediction tables; ECE values; abstention threshold | `labs/ch13-failure/derive.py` | derived | Sep 2026 | labs/ch13-failure/derive.py |
| 13 | 10 | $150 wrong / $6 abstain; "nine times in ten"; simulated confidence distribution | Illustrative (costs from ch26) | illustrative | Sep 2026 | — |
| 13 | 11 | Bare-model failure rates on industrial Portuguese probes | None published | open | Sep 2026 | — |
| 14 | 1 | Vision transformer; patches as tokens | Dosovitskiy et al., ICLR 2021, arXiv 2010.11929 | primary | Sep 2026 | https://arxiv.org/abs/2010.11929 |
| 14 | 2 | Contrastive image–text alignment | Radford et al., CLIP, 2021, arXiv 2103.00020 | primary | Sep 2026 | https://arxiv.org/abs/2103.00020 |
| 14 | 3 | Connecting vision encoders to language models | Alayrac et al., Flamingo, 2022, arXiv 2204.14198; Liu et al., LLaVA, 2023, arXiv 2304.08485 | primary | Sep 2026 | https://arxiv.org/abs/2204.14198 |
| 14 | 4 | Document question answering | Mathew, Karatzas, Jawahar, DocVQA, 2021, arXiv 2007.00398 | primary | Sep 2026 | https://arxiv.org/abs/2007.00398 |
| 14 | 5 | Speech encoding: 30 s → 1,500 tokens | Radford et al., Whisper, 2022, arXiv 2212.04356 | primary | Sep 2026 | https://arxiv.org/abs/2212.04356 |
| 14 | 6 | Tiling at 512 px; per-image token budgets | Vendor vision documentation | vendor | Sep 2026 | https://docs.claude.com/en/docs/build-with-claude/vision |
| 14 | 7 | Patch counts; tile counts and tokens; corpus ratio; tag-error and validation probabilities; per-image cost | `labs/ch14-multimodal/derive.py` | derived | Sep 2026 | labs/ch14-multimodal/derive.py |
| 14 | 8 | 256 tokens per tile; per-character error rates; corpus page counts | Illustrative | illustrative | Sep 2026 | — |
| 14 | 9 | Identifier accuracy on industrial drawings and scans | None published at plant resolutions | open | Sep 2026 | — |
| 14 | C | Cost-optimization checklist measured on a claims agent: 10-claim eval, 2 trials per configuration | Anthropic, "Cost Optimization on the Claude API," Claude Cookbook, Aug 2026 (Lehrburger) | vendor | Sep 2026 | https://platform.claude.com/cookbook/cost-optimization-cost-optimization |
| 15 | 1 | List prices: frontier 1.25 / 0.125 / 10; small 0.25 / 0.025 / 2 | OpenAI GPT-5 and GPT-5-mini pricing | vendor | Sep 2026 | https://developers.openai.com/api/docs/pricing |
| 15 | 2 | Cache minimum ~1,024 tokens; 5-min / 1-h lifetimes; Anthropic 1.25× / 2× write surcharge; automatic caching at OpenAI and Google | Vendor caching documentation | vendor | Sep 2026 | https://docs.claude.com/en/docs/build-with-claude/prompt-caching |
| 15 | 3 | Batch APIs at ~50% | Vendor pricing documentation | vendor | Sep 2026 | https://docs.claude.com/en/docs/about-claude/pricing |
| 15 | 4 | RouteLLM: >85% MT-Bench, 45% MMLU, 35% GSM8K at 95% quality | Ong et al., 2024, arXiv 2406.18665 | primary | Sep 2026 | https://arxiv.org/abs/2406.18665 |
| 15 | 5 | FrugalGPT: up to 98% | Chen, Zaharia, Zou, 2023, arXiv 2305.05176 | primary | Sep 2026 | https://arxiv.org/abs/2305.05176 |
| 15 | 6 | ~35% at <2% loss on realistic traffic; skill does not transfer | RouterArena-style evaluations | analyst | Sep 2026 | needs fetch |
| 15 | 7 | ~30% within a family | Bedrock intelligent prompt routing | vendor | Sep 2026 | https://docs.aws.amazon.com/bedrock/latest/userguide/ |
| 15 | 8 | GPT-4 launch pricing $30 / $60 (8K), Mar 2023 | OpenAI announcement, historical | vendor | Sep 2026 | https://openai.com/index/ |
| 15 | 9 | Inference mechanics behind the prices | Pope et al. 2022; Kwon et al. 2023 (ch10) | primary | Sep 2026 | https://arxiv.org/abs/2309.06180 |
| 15 | 10 | FOCUS token billing | FinOps Foundation | primary | Sep 2026 | https://www.finops.org/framework/ |
| 15 | 11 | Blended prices; break-evens; batch blending; routing costs and degradation; crossover; trajectory ratios | `labs/ch15-economics/derive.py` | derived | Sep 2026 | labs/ch15-economics/derive.py |
| 15 | 12 | $4,365 compute; $0.009 per query; 30% hard share; 50% small-model failure on hard | ch10, ch37; illustrative | derived / illustrative | Sep 2026 | — |
| 15 | 13 | The plant's routed share and retention | Unmeasured until the golden set runs | open | Sep 2026 | — |
| 15 | C | Cost-optimization checklist measured on a claims agent: 10-claim eval, 2 trials per configuration | Anthropic, "Cost Optimization on the Claude API," Claude Cookbook, Aug 2026 (Lehrburger) | vendor | Sep 2026 | https://platform.claude.com/cookbook/cost-optimization-cost-optimization |
| 16 | 1 | Agent = Model + Harness; component derivation | LangChain, "The Anatomy of an Agent Harness," Mar 2026 | practitioner | Sep 2026 | https://python.langchain.com/docs/ |
| 16 | 2 | Every harness component encodes an assumption about what the model cannot do | Anthropic, "Effective Harnesses for Long-Running Agents," Nov 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering |
| 16 | 3 | Guides/sensors × computational/inferential; steering loop | Böckeler, martinfowler.com, Apr 2026 | practitioner | Sep 2026 | https://martinfowler.com/articles/exploring-gen-ai/ |
| 16 | 4 | Workflow patterns; simplest solution first | Anthropic, "Building Effective Agents," Dec 2024 | vendor | Sep 2026 | https://www.anthropic.com/engineering/building-effective-agents |
| 16 | 5 | pass^k; GPT-4o retail pass^1 60.4%, airline 42.0%; retail pass^8 < 25% | Yao et al., τ-bench, 2024, arXiv 2406.12045 | primary | Sep 2026 | https://arxiv.org/abs/2406.12045 |
| 16 | 6 | Opus 4.5 SEAL → Claude Code 45.9% → 55.4% (SWE-bench Pro); Grok 4 +14–16 pp (Verified) | "Stop Comparing LLM Agents Without Disclosing the Harness," 2026, arXiv 2605.23950 | preprint / analyst | Sep 2026 | https://arxiv.org/abs/2605.23950 |
| 16 | 7 | Single model 62.3–70.2% across scaffolds | Epoch AI monitoring | analyst | Sep 2026 | https://epoch.ai/ |
| 16 | 8 | ~1M lines, ~1,500 PRs, 3→7 engineers, 5 months | OpenAI, "Harness engineering," Feb 2026 | vendor | Sep 2026 | https://openai.com/index/ |
| 16 | 8a | SWE-bench Verified: 500 human-validated tasks | Chowdhury et al., OpenAI, "Introducing SWE-bench Verified," Aug 2024 | primary | Sep 2026 | https://openai.com/index/ |
| 16 | 8b | AgentDojo 629 cases | Debenedetti et al. 2024 (ch28) | primary | Sep 2026 | https://arxiv.org/abs/2406.13352 |
| 16 | 9 | Open harness comparison from source code | Darú, Harness Engineering (2026) | practitioner | Sep 2026 | needs fetch |
| 16 | 10 | Independence curves; Wilson intervals at 20/50/100/200; 84.1% needed for pass^8 = 25%; 59% relative drop; expected attempts; 0.95^11 = 57%, 0.99^11 = 90% | `labs/ch16-thesis/derive.py` | derived | Sep 2026 | labs/ch16-thesis/derive.py |
| 16 | 11 | Scenario parameters (2,000/day, 6,000/4,000/400 tokens, eleven calls, P-101 in Z3) | This chapter | illustrative / scenario | Sep 2026 | — |
| 16 | 12 | No controlled scaffold comparison on an industrial workload | Search, Sep 2026 | open | Sep 2026 | — |
| 17 | 1 | Task clarity and completion criteria for agents | Anthropic, "Building Effective Agents," Dec 2024 | vendor | Sep 2026 | https://www.anthropic.com/engineering/building-effective-agents |
| 17 | 2 | Acceptance criteria first; guardrails | OpenAI, "A Practical Guide to Building Agents," 2025 | vendor | Sep 2026 | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf |
| 17 | 3 | Contact humans with tool calls; launch/pause/resume | HumanLayer, 12-Factor Agents | practitioner | Sep 2026 | https://github.com/humanlayer/12-factor-agents |
| 17 | 4 | Intent-based outcome specification | Nielsen, 2023 (ch00) | practitioner | Sep 2026 | https://www.nngroup.com/articles/ai-paradigm/ |
| 17 | 5 | Webhooks and triggers as first-class task entry | Anthropic, Managed Agents, May 2026 | vendor | Sep 2026 | https://docs.claude.com/en/docs/agents-and-tools/managed-agents/overview |
| 17 | 6 | Behaviour scenarios as executable specifications | Cucumber / Gherkin documentation | practitioner | Sep 2026 | https://cucumber.io/docs/gherkin/ |
| 17 | 7 | Ask-or-guess costs and break-evens; clarification rates; coverage; intent-validation residual | `labs/ch17-task-entry/derive.py` | derived | Sep 2026 | labs/ch17-task-entry/derive.py |
| 17 | 8 | $2 clarification; $0.02 / $6 / $150; 10% slip; intake mix; 2% off-scope rate | Illustrative (costs from ch26) | illustrative | Sep 2026 | — |
| 17 | 9 | Clarification and under-specification rates on industrial channels | None published | open | Sep 2026 | — |
| 18 | 1 | Right altitude; context as a finite resource | Anthropic, "Effective Context Engineering for AI Agents," Sep 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| 18 | 2 | Examples for structure; prompt-engineering practice | Anthropic prompt-engineering documentation | vendor | Sep 2026 | https://www.anthropic.com/engineering |
| 18 | 3 | Tool descriptions written for the model | Anthropic, "Writing Effective Tools for Agents," 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering/writing-tools-for-agents |
| 18 | 4 | Project guide file, short and iterated | Anthropic, "Claude Code: Best Practices," 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering |
| 18 | 5 | Progressive disclosure of instructions | Anthropic, "Agent Skills," 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering |
| 18 | 6 | Own your prompts; own your context window | HumanLayer, 12-Factor Agents | practitioner | Sep 2026 | https://github.com/humanlayer/12-factor-agents |
| 18 | 7 | Instruction-following failure rates | Zhou et al., IFEval, 2023, arXiv 2311.07911 | primary | Sep 2026 | https://arxiv.org/abs/2311.07911 |
| 18 | 8 | Formatting sensitivity: large accuracy swings from spurious prompt features | Sclar et al., 2023, arXiv 2310.11324 | primary | Sep 2026 | https://arxiv.org/abs/2310.11324 |
| 18 | 8a | AGENTS.md convention | agents.md (open convention) | practitioner | Sep 2026 | https://agents.md/ |
| 18 | 8b | Architectural constraints as guides enforced by tooling; ~1,500 PRs by seven engineers | OpenAI, "Harness engineering," Feb 2026 | vendor | Sep 2026 | https://openai.com/index/ |
| 18 | 8c | Architecture decision records | Nygard, "Documenting Architecture Decisions," 2011 | practitioner | Sep 2026 | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions |
| 18 | 9 | Guides as a component | Böckeler, Apr 2026 | practitioner | Sep 2026 | https://martinfowler.com/articles/exploring-gen-ai/ |
| 18 | 10 | Prefix composition, costs, example and rule arithmetic, pairing share, drift loss | `labs/ch18-guides/derive.py` | derived | Sep 2026 | labs/ch18-guides/derive.py |
| 18 | 11 | Element sizes; 30 tokens per rule; 250 per example; 99% hit rate; 8% violation rate | Illustrative | illustrative | Sep 2026 | — |
| 18 | 12 | Per-rule compliance on industrial guides | None published | open | Sep 2026 | — |
| 19 | 1 | Context as a finite resource; compaction; note-taking; sub-agents; just-in-time retrieval | Anthropic, "Effective Context Engineering for AI Agents," Sep 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| 19 | 2 | KV-cache hit rate as the primary metric; append-only; mask tools; ~100:1 input–output ratio | Manus, "Context Engineering for AI Agents," Jul 2025 | practitioner | Sep 2026 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| 19 | 3 | In-sandbox filtering of tool results | Anthropic, "Code Execution with MCP," Nov 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering/code-execution-with-mcp |
| 19 | 4 | Positional and effective-length evidence | Liu et al. 2023; Modarressi et al. 2025 (ch05) | primary | Sep 2026 | https://arxiv.org/abs/2307.03172 |
| 19 | 5 | Degradation with input length across models | Chroma, "Context Rot," 2025 | practitioner | Sep 2026 | https://research.trychroma.com/context-rot |
| 19 | 5a | Poisoning, distraction, confusion, clash as named failure modes | Breunig, "How Long Contexts Fail," 2025 | practitioner | Sep 2026 | https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html |
| 19 | 5b | Lead agent and sub-agents with summaries | Anthropic, "How We Built Our Multi-Agent Research System," 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering/multi-agent-research-system |
| 19 | 6 | Own your context window | HumanLayer, 12-Factor Agents | practitioner | Sep 2026 | https://github.com/humanlayer/12-factor-agents |
| 19 | 7 | Window by iteration; tokens per task; savings; chunk fractions; trimming ratios; costs | `labs/ch19-context/derive.py` | derived | Sep 2026 | labs/ch19-context/derive.py |
| 19 | 8 | 1,500 tokens/iteration; budget allocation; 100 rows × 80 tokens; 22-iteration task | Illustrative / scenario | illustrative | Sep 2026 | — |
| 19 | 9 | Compaction fidelity on industrial tasks | None published | open | Sep 2026 | — |
| 19 | C | Cost-optimization checklist measured on a claims agent: 10-claim eval, 2 trials per configuration | Anthropic, "Cost Optimization on the Claude API," Claude Cookbook, Aug 2026 (Lehrburger) | vendor | Sep 2026 | https://platform.claude.com/cookbook/cost-optimization-cost-optimization |
| 20 | 1 | Contextual retrieval: −49% / −67% top-20 failures | Anthropic, "Introducing Contextual Retrieval," Sep 2024 | vendor | Sep 2026 | https://www.anthropic.com/news/contextual-retrieval |
| 20 | 2 | Reciprocal rank fusion | Cormack, Clarke, Buettcher, SIGIR 2009 | primary | Sep 2026 | https://doi.org/10.1145/1571941.1572114 |
| 20 | 3 | Cross-encoder re-ranking | Nogueira & Cho, 2019, arXiv 1901.04085 | primary | Sep 2026 | https://arxiv.org/abs/1901.04085 |
| 20 | 4 | Graph-augmented retrieval | Edge et al., "From Local to Global: A Graph RAG Approach," 2024, arXiv 2404.16130 | primary | Sep 2026 | https://arxiv.org/abs/2404.16130 |
| 20 | 4a | Learned sparse retrieval | Formal et al., SPLADE, 2021, arXiv 2107.05720 | primary | Sep 2026 | https://arxiv.org/abs/2107.05720 |
| 20 | 4b | Late interaction | Khattab & Zaharia, ColBERT, SIGIR 2020, arXiv 2004.12832 | primary | Sep 2026 | https://arxiv.org/abs/2004.12832 |
| 20 | 5 | BM25 | Robertson & Zaragoza, 2009 (ch02) | primary | Sep 2026 | https://doi.org/10.1561/1500000019 |
| 20 | 6 | Pipelines, chunkers, retrievers | LangChain and LlamaIndex documentation | vendor | Sep 2026 | https://python.langchain.com/docs/ |
| 20 | 7 | RAG for engineers | Huyen, *AI Engineering*, 2025 | practitioner | Sep 2026 | https://www.oreilly.com/library/view/ai-engineering/9781098166298/ |
| 20 | 8 | Chunk sizes; stale rates and counts; RRF scores; re-ranker latency; graph size; tokens at k | `labs/ch20-retrieval/derive.py` | derived | Sep 2026 | labs/ch20-retrieval/derive.py |
| 20 | 9 | 20,000 documents; 400 revisions/month; 10 ms per re-rank; 62% governance baseline; 7,600 refused | Illustrative / scenario | illustrative | Sep 2026 | — |
| 20 | 10 | Precision/recall on Portuguese industrial procedures with current models | None published | open | Sep 2026 | — |
| 21 | 1 | Workflows, activities, event history, replay, signals, timers, retry policies | Temporal documentation | vendor | Sep 2026 | https://docs.temporal.io/ |
| 21 | 2 | Isolated microVM sessions; managed memory; tool gateway | AWS Bedrock AgentCore documentation | vendor | Sep 2026 | https://docs.aws.amazon.com/bedrock-agentcore/ |
| 21 | 3 | Idempotency keys for safe retries | Stripe API documentation | vendor | Sep 2026 | https://docs.stripe.com/api/idempotent_requests |
| 21 | 4 | Sagas and compensation | Garcia-Molina & Salem, "Sagas," SIGMOD 1987 | primary | Sep 2026 | https://doi.org/10.1145/38713.38742 |
| 21 | 5 | Exponential backoff with jitter | Google SRE book, "Handling Overload"; AWS Architecture Blog on jitter | practitioner | Sep 2026 | https://ai.google.dev/gemini-api/docs/pricing |
| 21 | 6 | Launch/pause/resume; unify execution and business state | HumanLayer, 12-Factor Agents | practitioner | Sep 2026 | https://github.com/humanlayer/12-factor-agents |
| 21 | 7 | Git and progress file as checkpoints | Anthropic, "Effective Harnesses for Long-Running Agents," Nov 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering |
| 21 | 8 | Compounding failure rates; retry success; redo fraction; duplicate-write arithmetic; backoff schedule; held-worker cost | `labs/ch21-control-plane/derive.py` | derived | Sep 2026 | labs/ch21-control-plane/derive.py |
| 21 | 9 | Thirteen calls, one crash per 500 tasks, 2% ambiguous timeouts, 14 h 20 m wait, $0.05 per vCPU-hour | Scenario and assumptions | illustrative / scenario | Sep 2026 | — |
| 21 | 10 | Resume correctness and duplicate rates on production engines for agent workloads | None found | open | Sep 2026 | — |
| 22 | 1 | Workflows vs agents; five patterns; simplest solution first | Anthropic, "Building Effective Agents," Dec 2024 | vendor | Sep 2026 | https://www.anthropic.com/engineering/building-effective-agents |
| 22 | 2 | Single/multi-agent orchestration; guardrails | OpenAI, "A Practical Guide to Building Agents," 2025 | vendor | Sep 2026 | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf |
| 22 | 3 | ReAct: +34 / +10 points absolute on ALFWorld / WebShop; CoT beats ReAct on HotpotQA | Yao et al., "ReAct," 2022, arXiv 2210.03629 | primary | Sep 2026 | https://arxiv.org/abs/2210.03629 |
| 22 | 4 | Reflexion: HumanEval pass@1 80% → 91% (GPT-4); ALFWorld 130/134 vs 108/134; MBPP slight regression; WebShop no gain | Shinn et al., "Reflexion," 2023, arXiv 2303.11366 | primary | Sep 2026 | https://arxiv.org/abs/2303.11366 |
| 22 | 5 | Self-Refine: ~20 points absolute average improvement | Madaan et al., "Self-Refine," 2023, arXiv 2303.17651 | primary | Sep 2026 | https://arxiv.org/abs/2303.17651 |
| 22 | 6 | Plan-and-execute separation | Wang et al., "Plan-and-Solve Prompting," 2023, arXiv 2305.04091 | primary | Sep 2026 | https://arxiv.org/abs/2305.04091 |
| 22 | 7 | Sensor output as positive prompt injection | Böckeler, martinfowler.com, Apr 2026 | practitioner | Sep 2026 | https://martinfowler.com/articles/exploring-gen-ai/ |
| 22 | 8 | Compact errors; own control flow; launch/pause/resume | HumanLayer, 12-Factor Agents | practitioner | Sep 2026 | https://github.com/humanlayer/12-factor-agents |
| 22 | 9 | Repair-cap table; task-level rates; context growth; runaway cost | `labs/ch22-loop/derive.py` | derived | Sep 2026 | labs/ch22-loop/derive.py |
| 22 | 10 | Frontier fresh-input price $1.25/M | Vendor pricing, Sep 2026 (ch37) | vendor | Sep 2026 | https://docs.claude.com/en/docs/about-claude/pricing |
| 22 | 11 | p = 0.60, q = 0.50, growth 1,500 tokens/iteration, eleven steps | Assumptions for the arithmetic | illustrative / scenario | Sep 2026 | — |
| 22 | 12 | Effect sizes on industrial workloads | None found | open | Sep 2026 | — |
| 23 | 1 | RouteLLM: >85% MT-Bench, 45% MMLU, 35% GSM8K at 95% quality | Ong et al., 2024, arXiv 2406.18665 | primary | Sep 2026 | https://arxiv.org/abs/2406.18665 |
| 23 | 2 | FrugalGPT cascades: up to 98% | Chen, Zaharia, Zou, 2023, arXiv 2305.05176 | primary | Sep 2026 | https://arxiv.org/abs/2305.05176 |
| 23 | 3 | ~35% at <2% loss on realistic traffic; no transfer to unfamiliar tasks | RouterArena-style evaluations | analyst | Sep 2026 | needs fetch |
| 23 | 4 | ~30% within a family | Bedrock intelligent prompt routing | vendor | Sep 2026 | https://docs.aws.amazon.com/bedrock/latest/userguide/ |
| 23 | 5 | Gateway functions; self-hosting; ownership changes | LiteLLM, Portkey, OpenRouter, Helicone documentation | vendor | Sep 2026 | https://docs.litellm.ai/ |
| 23 | 6 | Deprecation cadences and aliases | Vendor deprecation policies | vendor | Sep 2026 | https://developers.openai.com/api/docs/deprecations |
| 23 | 7 | Routing as a workflow pattern | Anthropic, "Building Effective Agents," Dec 2024 | vendor | Sep 2026 | https://www.anthropic.com/engineering/building-effective-agents |
| 23 | 8 | List prices | OpenAI GPT-5 / GPT-5-mini pricing (ch15) | vendor | Sep 2026 | https://developers.openai.com/api/docs/pricing |
| 23 | 9 | Per-query and per-task costs; cascade costs; availability; effort-vs-tier savings | `labs/ch23-routing/derive.py` | derived | Sep 2026 | labs/ch23-routing/derive.py |
| 23 | 10 | 12% escalation; 18-minute outage; 99% on-site availability; 5–20 ms overhead | Illustrative | illustrative | Sep 2026 | — |
| 23 | 11 | The plant's routed share and retention per class | Unmeasured until the golden set runs | open | Sep 2026 | — |
| 23 | C | Cost-optimization checklist measured on a claims agent: 10-claim eval, 2 trials per configuration | Anthropic, "Cost Optimization on the Claude API," Claude Cookbook, Aug 2026 (Lehrburger) | vendor | Sep 2026 | https://platform.claude.com/cookbook/cost-optimization-cost-optimization |
| 24 | 1 | Four memory classes for language agents | Sumers, Yao, Narasimhan, Griffiths, "CoALA," 2023, arXiv 2309.02427 | primary | Sep 2026 | https://arxiv.org/abs/2309.02427 |
| 24 | 2 | Reflection over a memory stream | Park et al., "Generative Agents," 2023, arXiv 2304.03442 | primary | Sep 2026 | https://arxiv.org/abs/2304.03442 |
| 24 | 3 | Tiered memory management by the model | Packer et al., "MemGPT," 2023, arXiv 2310.08560 | primary | Sep 2026 | https://arxiv.org/abs/2310.08560 |
| 24 | 4 | Model-writable memory directory; background filing pass | Anthropic memory tool documentation; Managed Agents memory, 2025–2026 | vendor | Sep 2026 | https://docs.claude.com/en/docs/agents-and-tools/managed-agents/overview |
| 24 | 5 | Memory in open coding agents | Darú, Harness Engineering (2026) | practitioner | Sep 2026 | needs fetch |
| 24 | 6 | Personal-data retention and rights | LGPD (ch36) | primary | Sep 2026 | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm |
| 24 | 7 | Budget; recurrence probabilities; consolidation volumes; store sizes; review-error arithmetic | `labs/ch24-memory/derive.py` | derived | Sep 2026 | labs/ch24-memory/derive.py |
| 24 | 8 | p = 0.2 retrieval; 0.3 candidates per episode; 70% acceptance; 1/1,000 review error; 30-day text retention | Illustrative | illustrative | Sep 2026 | — |
| 24 | 9 | Proposer and reviewer error rates on industrial consolidation | None published | open | Sep 2026 | — |
| 25 | 1 | MCP: JSON-RPC 2.0; stdio and streamable HTTP; tools, resources, prompts, sampling; lifecycle | Model Context Protocol specification, 2024–2026 | primary | Sep 2026 | https://modelcontextprotocol.io/specification |
| 25 | 2 | MCP security best practices; tool poisoning; least privilege | MCP security best practices, 2025 | primary | Sep 2026 | https://modelcontextprotocol.io/specification/draft/basic/security_best_practices |
| 25 | 3 | Tool descriptions written for the model; small distinct sets | Anthropic, "Writing Effective Tools for Agents," 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering/writing-tools-for-agents |
| 25 | 4 | Code execution with MCP: 150,000 → 2,000 tokens (98.7%) | Anthropic, "Code Execution with MCP," Nov 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering/code-execution-with-mcp |
| 25 | 5 | Ephemeral sandboxes; microVM session isolation; configurable egress | E2B documentation; AWS AgentCore; Anthropic Managed Agents | vendor | Sep 2026 | https://docs.aws.amazon.com/bedrock-agentcore/ |
| 25 | 6 | Indirect injection; adaptive attacks defeat prompt-level defences | Greshake et al., 2023, arXiv 2302.12173; Nasr et al., 2025 | primary | Sep 2026 | https://arxiv.org/abs/2302.12173 |
| 25 | 7 | MCP gateways and secret injection | Docker MCP Gateway, MintMCP, Lunar.dev, Astrix documentation | vendor | Sep 2026 | https://docs.docker.com/ai/mcp-gateway/ |
| 25 | 8 | Computer-use models; browser automation | Anthropic computer use documentation; Playwright | vendor / practitioner | Sep 2026 | https://docs.claude.com/en/docs/agents-and-tools/tool-use/computer-use-tool |
| 25 | 9 | Tools are structured outputs | HumanLayer, 12-Factor Agents | practitioner | Sep 2026 | https://github.com/humanlayer/12-factor-agents |
| 25 | 10 | Schema surface, code-execution scenario figures, risk-class counts, exposure ratio, reliability | `labs/ch25-tools/derive.py` | derived | Sep 2026 | labs/ch25-tools/derive.py |
| 25 | 11 | 90 tokens per schema; 15-minute TTL; 180-day key; 0.2–1.0 s startup | Illustrative | illustrative | Sep 2026 | — |
| 25 | 12 | Wrong-tool and injection catch rates on industrial tool sets | None published | open | Sep 2026 | — |
| 25 | C | Cost-optimization checklist measured on a claims agent: 10-claim eval, 2 trials per configuration | Anthropic, "Cost Optimization on the Claude API," Claude Cookbook, Aug 2026 (Lehrburger) | vendor | Sep 2026 | https://platform.claude.com/cookbook/cost-optimization-cost-optimization |
| 26 | 1 | Sensors; computational/inferential; sensor messages as positive prompt injection | Böckeler, martinfowler.com, Apr 2026 | practitioner | Sep 2026 | https://martinfowler.com/articles/exploring-gen-ai/ |
| 26 | 2 | Architectural constraints and observability as sensors; ~1,500 merged PRs, seven engineers, five months | OpenAI, "Harness engineering," Feb 2026 | vendor | Sep 2026 | https://openai.com/index/ |
| 26 | 3 | End-to-end tests decide completion | Anthropic, "Effective Harnesses for Long-Running Agents," Nov 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering |
| 26 | 4 | Grader biases (position, verbosity, self-enhancement); >80% agreement on structured tasks | Zheng et al., NeurIPS 2023, arXiv 2306.05685 | primary | Sep 2026 | https://arxiv.org/abs/2306.05685 |
| 26 | 5 | Behaviour scenarios (Given / When / Then) as executable specifications | Cucumber / Gherkin documentation | practitioner | Sep 2026 | https://cucumber.io/docs/gherkin/ |
| 26 | 6 | Verification chapter grounded in open harnesses | Darú, Harness Engineering (2026) | practitioner | Sep 2026 | needs fetch |
| 26 | 7 | Layered detection; ordering cost; false-positive bound; coverage; escapes | `labs/ch26-sensors/derive.py` | derived | Sep 2026 | labs/ch26-sensors/derive.py |
| 26 | 8 | Per-sensor detection rates, failure rates, costs; $0.02 / $6 / $150; eleven criteria; MP-0417 rev 7 | Design assumptions and scenario | illustrative / scenario | Sep 2026 | — |
| 26 | 9 | κ ≥ 0.6 retirement threshold | Practitioner convention | practitioner | Sep 2026 | — |
| 26 | 10 | Per-sensor rates on real industrial artifacts | None published | open | Sep 2026 | — |
| 27 | 1 | Grader agreement 85% vs 81%; position, verbosity, self-enhancement biases | Zheng et al., NeurIPS 2023, arXiv 2306.05685 | primary | Sep 2026 | https://arxiv.org/abs/2306.05685 |
| 27 | 2 | Frontier judges >50% error on hard bias items; no judge uniformly reliable | JudgeBiasBench; RAND judge study, 2026 | analyst | Sep 2026 | needs fetch |
| 27 | 3 | Isolated-context outcome grading | Anthropic, Managed Agents outcomes, 2026 | vendor | Sep 2026 | https://docs.claude.com/en/docs/agents-and-tools/managed-agents/overview |
| 27 | 4 | SWE-bench; Verified subset of 500 | Jimenez et al., 2023, arXiv 2310.06770; Chowdhury et al., 2024 | primary | Sep 2026 | https://arxiv.org/abs/2310.06770 |
| 27 | 5 | τ-bench; pass^k; retail figures | Yao et al., 2024, arXiv 2406.12045 | primary | Sep 2026 | https://arxiv.org/abs/2406.12045 |
| 27 | 6 | AgentDojo: 97 tasks, 629 cases; utility and attack figures | Debenedetti et al., NeurIPS 2024, arXiv 2406.13352 | primary | Sep 2026 | https://arxiv.org/abs/2406.13352 |
| 27 | 7 | GAIA: 466 questions, three levels; humans ~92% vs GPT-4 with plugins ~15% | Mialon et al., 2023, arXiv 2311.12983 | primary | Sep 2026 | https://arxiv.org/abs/2311.12983 |
| 27 | 8 | Reproducible evaluation; CI integration | UK AI Security Institute, Inspect AI documentation | primary | Sep 2026 | https://inspect.aisi.org.uk/ |
| 27 | 9 | Cohen's κ; Krippendorff's α; paired bootstrap | Cohen 1960; Krippendorff 2004; Efron 1979 (ch12) | primary | Sep 2026 | https://doi.org/10.1177/001316446002000104 |
| 27 | 10 | Grader costs; κ example and SE; gate costs; half-width | `labs/ch27-graders/derive.py` | derived | Sep 2026 | labs/ch27-graders/derive.py |
| 27 | 11 | 1,200/120 tokens per grading call; a minute per item; ceiling 0.79; κ 0.71 / 0.58 / 0.66; gate example | Illustrative | illustrative | Sep 2026 | — |
| 27 | 12 | Grader κ on industrial Portuguese criteria | None published | open | Sep 2026 | — |
| 27 | C | Cost-optimization checklist measured on a claims agent: 10-claim eval, 2 trials per configuration | Anthropic, "Cost Optimization on the Claude API," Claude Cookbook, Aug 2026 (Lehrburger) | vendor | Sep 2026 | https://platform.claude.com/cookbook/cost-optimization-cost-optimization |
| 28 | 1 | Prompt injection is LLM01 and excessive agency LLM06 in the 2025 list | OWASP GenAI Security Project, Top 10 for LLM Applications 2025 | primary | Sep 2026 | https://genai.owasp.org/ |
| 28 | 2 | Indirect prompt injection defined and demonstrated | Greshake et al., 2023, arXiv 2302.12173 | primary | Sep 2026 | https://arxiv.org/abs/2302.12173 |
| 28 | 3 | AgentDojo: 4 environments, 74 tools, 97 user tasks, 27 injection tasks, 629 cases; attacks succeed <25% against best agents; deterministic checks | Debenedetti et al., NeurIPS 2024, arXiv 2406.13352 | primary | Sep 2026 | https://arxiv.org/abs/2406.13352 |
| 28 | 4 | CaMeL: 77% of tasks with provable security vs 84% undefended on AgentDojo | Debenedetti et al., "Defeating Prompt Injections by Design," 2025, arXiv 2503.18813 (latest version) | primary | Sep 2026 | https://arxiv.org/abs/2503.18813 |
| 28 | 5 | Twelve published defenses broken by adaptive attacks, ASR > 90% | Nasr et al., "The Attacker Moves Second," 10 Oct 2025 | primary | Sep 2026 | https://arxiv.org/abs/2510.09023 |
| 28 | 6 | Prompt Guard 2 86M: 81.2% attack-prevention rate on AgentDojo at 3% utility cost | Meta, LlamaFirewall paper, 2025 | vendor | Sep 2026 | https://arxiv.org/abs/2505.03574 |
| 28 | 7 | Agents Rule of Two statement and its status as a supplement to least privilege | Meta AI blog, "Agents Rule of Two," 31 Oct 2025 | vendor / primary | Sep 2026 | https://ai.meta.com/blog/practical-ai-agent-security/ |
| 28 | 8 | Lethal trifecta | Willison, simonwillison.net, 2025 | practitioner | Sep 2026 | https://simonwillison.net/ |
| 28 | 9 | OPA: Rego, deployment modes, decision logs, CNCF graduated | Open Policy Agent documentation | vendor | Sep 2026 | https://www.openpolicyagent.org/docs/ |
| 28 | 10 | Cedar: typed, analyzable policies | Cedar language specification; AWS Verified Permissions docs | vendor | Sep 2026 | https://docs.cedarpolicy.com/ |
| 28 | 11 | Dynamic secrets and leases | HashiCorp Vault documentation | vendor | Sep 2026 | https://developer.hashicorp.com/vault/docs |
| 28 | 12 | Zones and conduits; SIL and deterministic safety logic | IEC 62443; IEC 61508 / 61511 | primary (standards; cited by concept) | Sep 2026 | https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards |
| 28 | 13 | LGPD automated-decision rights; NIST AI RMF functions; ISO/IEC 42001 controls | LGPD Art. 20; NIST AI RMF 1.0 (2023); ISO/IEC 42001:2023 | primary | Sep 2026 | https://www.nist.gov/itl/ai-risk-management-framework |
| 28 | 14 | Annex III obligations from 2 Dec 2027 | Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744 | primary | Sep 2026 | https://eur-lex.europa.eu/eli/reg/2026/1744/oj |
| 28 | 15 | MCP security best practices: least-privilege scopes | Model Context Protocol specification, 2025 | primary | Sep 2026 | https://modelcontextprotocol.io/specification |
| 28 | 16 | Harness permission comparison from source code | Darú, Harness Engineering, ch. 07 (2026) | practitioner | Sep 2026 | needs fetch |
| 28 | 17 | Eleven tool calls per task; latency targets 10 ms / 30 ms p99; credential TTLs | Scenario and design targets | illustrative until Lab 28 | Sep 2026 | — |
| 28 | 18 | Delegation intersection rule; policy-authoring error rate | This chapter | proposal / open | Sep 2026 | — |
| 29 | 1 | GenAI span attributes (provider, model, token counts, operation) | OpenTelemetry semantic conventions for generative AI | primary / vendor | Sep 2026 | https://opentelemetry.io/docs/specs/semconv/gen-ai/ |
| 29 | 2 | Self-hostable LLM tracing backends ingesting OpenTelemetry | Langfuse and Arize Phoenix documentation | vendor | Sep 2026 | https://langfuse.com/docs |
| 29 | 3 | Chained timestamps | Haber & Stornetta, "How to Time-Stamp a Digital Document," 1991 | primary | Sep 2026 | https://doi.org/10.1007/BF00196791 |
| 29 | 4 | Observability wired into the loop | OpenAI, "Harness engineering," Feb 2026 | vendor | Sep 2026 | https://openai.com/index/ |
| 29 | 5 | Logs, metrics, traces; alerting practice | Google SRE book | practitioner | Sep 2026 | https://ai.google.dev/gemini-api/docs/pricing |
| 29 | 6 | Evidence mapping to LGPD, NIST AI RMF, ISO/IEC 42001, EU AI Act Art. 12 | As cited in ch28 (primary) | primary | Sep 2026 | — |
| 29 | 7 | Records per task; volumes; sampling probabilities; tag-presence arithmetic; verification, replay, export times | `labs/ch29-observability/derive.py` | derived | Sep 2026 | labs/ch29-observability/derive.py |
| 29 | 8 | 600 B per record; 4 chars/token; 1,500 tasks/month; 1 ms per record read; 10⁶ hashes/s; 6% permit omissions; retention windows | Scenario estimates | illustrative / scenario | Sep 2026 | — |
| 29 | 9 | Audit completeness and replay time on production harnesses | None published | open | Sep 2026 | — |
| 30 | 1 | Coordinator–specialist design; ~4× and ~15× token multipliers; failures met | Anthropic, "How We Built Our Multi-Agent Research System," Jun 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering/multi-agent-research-system |
| 30 | 2 | A2A: agent cards, tasks, messages, lifecycle; Linux Foundation stewardship | Agent2Agent protocol specification, 2025–2026 | primary | Sep 2026 | https://a2a-protocol.org/latest/specification/ |
| 30 | 3 | MCP as the tool protocol | Model Context Protocol specification (ch25) | primary | Sep 2026 | https://modelcontextprotocol.io/specification |
| 30 | 4 | MAST: 14 failure modes in 3 categories across open frameworks | Cemri et al., "Why Do Multi-Agent LLM Systems Fail?," 2025, arXiv 2503.13657 | primary | Sep 2026 | https://arxiv.org/abs/2503.13657 |
| 30 | 5 | Orchestrator–workers pattern | Anthropic, "Building Effective Agents," Dec 2024 | vendor | Sep 2026 | https://www.anthropic.com/engineering/building-effective-agents |
| 30 | 6 | Dynamic workflow composition on agent platforms | Vendor platform documentation | vendor | Sep 2026 | https://docs.claude.com/en/docs/agents-and-tools/managed-agents/overview |
| 30 | 7 | Multipliers applied to the scenario; costs; break-even; speedup; intersection; carve-out | `labs/ch30-multi-agent/derive.py` | derived | Sep 2026 | labs/ch30-multi-agent/derive.py |
| 30 | 8 | 40-second sub-tasks; 10 s coordination; 20% / 15% miss rates; $150 per failure; caps | Illustrative | illustrative | Sep 2026 | — |
| 30 | 9 | Single-vs-multi pass rates and multipliers on industrial tasks | None published | open | Sep 2026 | — |
| 30 | C | Cost-optimization checklist measured on a claims agent: 10-claim eval, 2 trials per configuration | Anthropic, "Cost Optimization on the Claude API," Claude Cookbook, Aug 2026 (Lehrburger) | vendor | Sep 2026 | https://platform.claude.com/cookbook/cost-optimization-cost-optimization |
| 31 | 1 | Durable waits, signals, timers | Temporal documentation (ch21) | vendor | Sep 2026 | https://docs.temporal.io/ |
| 31 | 2 | Human intervention as a guardrail for high-risk actions | OpenAI, "A Practical Guide to Building Agents," 2025 | vendor | Sep 2026 | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf |
| 31 | 3 | Contact humans with tool calls; launch/pause/resume | HumanLayer, 12-Factor Agents | practitioner | Sep 2026 | https://github.com/humanlayer/12-factor-agents |
| 31 | 4 | `input-required` state; outcomes | Anthropic, Managed Agents documentation, 2026 | vendor | Sep 2026 | https://docs.claude.com/en/docs/agents-and-tools/managed-agents/overview |
| 31 | 5 | Automation bias; vigilance; misuse and disuse of automation | Parasuraman & Riley, Human Factors, 1997 | primary | Sep 2026 | https://doi.org/10.1518/001872097778543886 |
| 31 | 6 | Human as an inferential sensor | Böckeler, Apr 2026 | practitioner | Sep 2026 | https://martinfowler.com/articles/exploring-gen-ai/ |
| 31 | 7 | Reviews per risk class; hours; gate cost; queue waits; STP; fatigue model; seeded counts | `labs/ch31-human-in-the-loop/derive.py` | derived | Sep 2026 | labs/ch31-human-in-the-loop/derive.py |
| 31 | 8 | Review rates; 6 minutes; $60/h; accuracy decay; 20 s floor; 2% seeds; 8% rejections; timers | Illustrative | illustrative | Sep 2026 | — |
| 31 | 9 | Reviewer catch rates and fatigue curves on industrial queues | None published | open | Sep 2026 | — |
| 32 | 1 | Harness, not model, as the improvement lever | OpenAI, "Harness Engineering," Feb 2026 | vendor | Sep 2026 | https://openai.com/index/ |
| 32 | 2 | Optimization of prompts and pipelines against a metric with splits | Khattab et al., "DSPy," 2023, arXiv 2310.03714 | primary | Sep 2026 | https://arxiv.org/abs/2310.03714 |
| 32 | 3 | Measured lever-by-lever gains; levers do not always compound | Anthropic, Claude Cookbook cost optimization, Aug 2026 (ch15) | vendor | Sep 2026 | https://github.com/anthropics/claude-cookbooks |
| 32 | 4 | Steering loop; sensor/guide framing | Böckeler, Apr 2026; Darú, 2026 | practitioner | Sep 2026 | https://martinfowler.com/articles/exploring-gen-ai/ |
| 32 | 5 | Metric gaming | Goodhart, 1975; Manheim & Garrabrant, "Categorizing Variants of Goodhart's Law," 2018, arXiv 1803.04585 | primary | Sep 2026 | https://arxiv.org/abs/1803.04585 |
| 32 | 6 | Paired bootstrap; power at 300 and 1,000 items | ch12 (Efron 1979) | primary / derived | Sep 2026 | https://doi.org/10.1214/aos/1176344552 |
| 32 | 7 | Cluster scores; expected gain; branch costs; ladder; curves | `labs/ch32-self-improving/derive.py` | derived | Sep 2026 | labs/ch32-self-improving/derive.py |
| 32 | 8 | 120 rejections; 2,100 events; cluster counts; 92% compliance; 20% holdout; 3 merges/week; curves; week-nine figures | Illustrative | illustrative | Sep 2026 | — |
| 32 | 9 | Improvement curves on industrial harnesses | None published | open | Sep 2026 | — |
| 33 | 1 | Risk categories for LLM and agentic applications | OWASP Top 10 for LLM Applications; OWASP agentic guidance, 2025–2026 | practitioner | Sep 2026 | https://genai.owasp.org/ |
| 33 | 2 | Multi-agent failure taxonomy | Cemri et al., MAST, 2025 (ch30) | primary | Sep 2026 | https://arxiv.org/abs/2503.13657 |
| 33 | 3 | GenAI risk categories | NIST AI 600-1, July 2024 | primary | Sep 2026 | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf |
| 33 | 4 | Indirect injection; adaptive attacks | Greshake et al. 2023; Nasr et al. 2025 (ch28) | primary | Sep 2026 | https://arxiv.org/abs/2302.12173 |
| 33 | 5 | Automation bias | Parasuraman & Riley 1997 (ch31) | primary | Sep 2026 | https://doi.org/10.1518/001872097778543886 |
| 33 | 6 | Mode-specific mechanisms and figures | Chapters 01–32 as cross-referenced in each entry | derived | Sep 2026 | — |
| 33 | 7 | Mode list; families; detection split; consequence weights; before/after per thousand | `labs/ch33-failure-catalogue/derive.py` | derived / illustrative | Sep 2026 | labs/ch33-failure-catalogue/derive.py |
| 33 | 8 | Per-mode rates on industrial deployments | None published | open | Sep 2026 | — |
| 37 | 1 | Frontier $1.25 / $0.125 / $10; small $0.25 / $0.025 / $2 per M tokens | OpenAI GPT-5 and GPT-5-mini list prices | vendor | Sep 2026 | https://developers.openai.com/api/docs/pricing |
| 37 | 2 | Cache read ~90% off; Anthropic write surcharge 1.25× / 2×; batch ~50% | OpenAI, Anthropic, Google pricing documentation | vendor | Sep 2026 | https://openai.com/index/ |
| 37 | 3 | RouteLLM: >85% MT-Bench, 45% MMLU, 35% GSM8K at 95% GPT-4 quality | Ong et al., RouteLLM, 2024, arXiv 2406.18665 | primary | Sep 2026 | https://arxiv.org/abs/2406.18665 |
| 37 | 4 | FrugalGPT up to 98% | Chen, Zaharia, Zou, FrugalGPT, 2023, arXiv 2305.05176 | primary | Sep 2026 | https://arxiv.org/abs/2305.05176 |
| 37 | 5 | ~35% savings at <2% loss on realistic traffic | RouterArena-style independent evaluations | analyst | Sep 2026 | needs fetch |
| 37 | 6 | H100 on-demand $2.99 (RunPod), ~$6.16 (CoreWeave); reserved $1.84–2.23 | Vendor pricing pages | vendor | Sep 2026 | https://docs.claude.com/en/docs/about-claude/pricing |
| 37 | 7 | Operations 1.3–5× raw GPU cost | Analyst estimates | analyst | Sep 2026 | — |
| 37 | 8 | Agents ~4× chat tokens; multi-agent ~15× | Anthropic, "How we built our multi-agent research system," 2025 | vendor | Sep 2026 | https://www.anthropic.com/engineering/multi-agent-research-system |
| 37 | 9 | ~5% rapid revenue acceleration; majority stalled | MIT Project NANDA, "The GenAI Divide," Jul 2025 (300+ initiatives; 52 interviews; 153 surveys — Fortune summary Aug 2025) | analyst | Sep 2026 | https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo |
| 37 | 10 | ~6% high performers (>5% EBIT) | McKinsey, The State of AI in 2025, Nov 2025 | analyst | Sep 2026 | https://www.mckinsey.com/ |
| 37 | 11 | FOCUS 1.4 ratified 4 Jun 2026; token billing supported; FinOps for AI as a framework category | FinOps Foundation | primary | Sep 2026 | https://www.finops.org/framework/ |
| 37 | 11a | SLMs serve most agent subtasks at 10–30× lower cost | Belcak et al., arXiv 2506.02153, Jun 2025 | primary | Sep 2026 | https://arxiv.org/abs/2506.02153 |
| 37 | 11b | Oversight formula inputs: 1,500 tasks, STP 20%/70%, 6 min, $60/h | This chapter | illustrative | Sep 2026 | — |
| 37 | 12 | All configuration totals, savings, break-evens, sensitivities | `labs/ch37-economics/derive.py` | derived | Sep 2026 | labs/ch37-economics/derive.py |
| 37 | 13 | Scenario volumes and token sizes; oversight loaded cost and allocation; first-year magnitudes | Scenario (ch16); illustrative | illustrative | Sep 2026 | — |
| 37 | 14 | No audited industrial cost-per-resolved-task figure in the public record | Search, Sep 2026 | open | Sep 2026 | — |
| 37 | C | Cost-optimization checklist measured on a claims agent: 10-claim eval, 2 trials per configuration | Anthropic, "Cost Optimization on the Claude API," Claude Cookbook, Aug 2026 (Lehrburger) | vendor | Sep 2026 | https://platform.claude.com/cookbook/cost-optimization-cost-optimization |