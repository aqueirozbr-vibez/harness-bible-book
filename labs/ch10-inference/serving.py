def serving_model(params: float, bytes_per_param: float, kv_bytes_per_token: float, gpus: int,
                  gpu_mem_gb: float, bw_per_gpu: float, flops_per_gpu: float, ctx_tokens: int, usd_per_gpu_hour: float):
    """Bandwidth/compute/memory model of decode for a dense model served tensor-parallel across `gpus`."""
    weight_bytes = params * bytes_per_param
    bw = bw_per_gpu * gpus; flops = flops_per_gpu * gpus
    floor_s = weight_bytes / bw                                   # decode time per token at batch 1
    compute_s = 2 * params / flops                                # compute time per token
    crossover = max(1, round(floor_s / compute_s))                # batch where compute time = memory time
    free_bytes = gpus * gpu_mem_gb * 1e9 - weight_bytes
    max_seqs = max(0, int(free_bytes / (kv_bytes_per_token * ctx_tokens)))
    batch = min(max_seqs, crossover)
    tps = batch / floor_s if batch else 0.0
    return {"weights_GB": weight_bytes / 1e9, "decode_floor_ms": floor_s * 1e3, "batch_crossover": crossover,
            "free_GB": free_bytes / 1e9, "max_concurrent_seqs": max_seqs, "decode_tps_at_max_batch": tps,
            "usd_per_M_tokens": {u: (usd_per_gpu_hour * gpus) / (tps * u * 3600) * 1e6 if tps else float("inf") for u in (0.1, 0.4, 0.7)}}

def speculative_gain(alpha: float, k: int) -> float:
    """Expected tokens accepted per verification pass with draft length k and per-token acceptance alpha."""
    return (1 - alpha ** (k + 1)) / (1 - alpha)

def prefill_seconds(params: float, prompt_tokens: int, flops: float, utilization: float) -> float:
    return 2 * params * prompt_tokens / (flops * utilization)
