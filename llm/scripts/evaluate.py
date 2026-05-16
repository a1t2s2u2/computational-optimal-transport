#!/usr/bin/env python3
"""Post-training evaluation: compute perplexity on the validation set.

Usage:
    python llm/scripts/evaluate.py \
        --model llm/models/Qwen3-14B-4bit \
        --adapter llm/adapters/qwen3-14b-ot \
        --data llm/data/valid.jsonl

Prints per-example loss and mean perplexity. Lower perplexity = better fit.
Compare base model (no --adapter) vs fine-tuned to measure improvement.
"""

import argparse
import json
import math
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def main() -> None:
    try:
        import mlx.core as mx
        from mlx_lm import load
        from mlx_lm.utils import get_model_path
    except ImportError:
        sys.exit("mlx_lm not found. Run: pip install mlx-lm>=0.21.0")

    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="Path to MLX model directory")
    ap.add_argument("--adapter", default=None, help="Path to LoRA adapter (optional)")
    ap.add_argument(
        "--data",
        default=os.path.join(REPO_ROOT, "llm", "data", "valid.jsonl"),
        help="Path to validation JSONL",
    )
    ap.add_argument(
        "--max-examples", type=int, default=None, help="Limit number of examples"
    )
    args = ap.parse_args()

    model_path = os.path.join(REPO_ROOT, args.model) if not os.path.isabs(args.model) else args.model
    data_path = os.path.join(REPO_ROOT, args.data) if not os.path.isabs(args.data) else args.data

    print(f"Loading model: {model_path}")
    adapter_path = None
    if args.adapter:
        adapter_path = os.path.join(REPO_ROOT, args.adapter) if not os.path.isabs(args.adapter) else args.adapter
        print(f"Loading adapter: {adapter_path}")

    model, tokenizer = load(model_path, adapter_path=adapter_path)

    with open(data_path, "r", encoding="utf-8") as f:
        examples = [json.loads(line) for line in f]

    if args.max_examples:
        examples = examples[: args.max_examples]

    print(f"Evaluating {len(examples)} examples ...\n")

    total_loss = 0.0
    total_tokens = 0
    losses = []

    for i, ex in enumerate(examples):
        messages = ex.get("messages", [])
        # Apply chat template to get full prompt+response text
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=False
        )
        # Tokenize
        input_ids = tokenizer.encode(text, return_tensors=None)
        tokens = mx.array(input_ids)

        # Compute loss over the full sequence (causal LM style)
        # For a rough perplexity estimate we use the model's forward pass.
        # Only count loss on the assistant turn tokens.
        # Simpler: compute full sequence loss (includes prompt, over-estimates).
        n = len(tokens)
        if n < 2:
            continue

        inputs = tokens[:-1][None]  # (1, n-1)
        targets = tokens[1:][None]  # (1, n-1)

        logits = model(inputs)
        # Cross-entropy loss
        vocab_size = logits.shape[-1]
        log_probs = mx.log_softmax(logits, axis=-1)
        # Gather target log-probs
        idx = targets[..., None]
        token_log_probs = mx.take_along_axis(log_probs, idx, axis=-1).squeeze(-1)
        loss = -token_log_probs.mean().item()
        losses.append(loss)
        total_loss += loss * (n - 1)
        total_tokens += n - 1

        if (i + 1) % 20 == 0:
            running_ppl = math.exp(total_loss / total_tokens)
            print(f"  [{i+1}/{len(examples)}] running perplexity: {running_ppl:.2f}")

    if not losses:
        print("No examples evaluated.")
        return

    mean_loss = total_loss / total_tokens
    perplexity = math.exp(mean_loss)
    print(f"\nMean loss:   {mean_loss:.4f}")
    print(f"Perplexity:  {perplexity:.2f}")
    print(f"Examples:    {len(losses)}")
    print(f"Tokens:      {total_tokens}")


if __name__ == "__main__":
    main()
