#!/usr/bin/env python3
"""LoRA fine-tuning wrapper with progress tracking and structured logs.

Wraps `python -m mlx_lm.lora` to add:
  - tqdm progress bar (step / total, loss, speed)
  - Structured JSONL metrics  → llm/logs/<timestamp>/metrics.jsonl
  - Config snapshot           → llm/logs/<timestamp>/config.yaml
  - Run summary               → llm/logs/<timestamp>/summary.json
  - Symlink llm/logs/latest   → latest run directory

Usage:
    uv run python llm/scripts/train.py
    uv run python llm/scripts/train.py --config llm/configs/lora_config.yaml
"""

import argparse
import datetime
import json
import os
import re
import shutil
import signal
import subprocess
import sys
from pathlib import Path

from tqdm import tqdm
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGS_DIR  = REPO_ROOT / "llm" / "logs"
DEFAULT_CONFIG = REPO_ROOT / "llm" / "configs" / "lora_config.yaml"

# ── mlx-lm output patterns ───────────────────────────────────────────────────
# Iter 50: Train loss 2.500, Learning Rate 1.000e-04, It/sec 8.2, Tokens/sec 4200.0
_TRAIN_RE = re.compile(
    r"Iter\s+(\d+):\s+Train loss\s+([\d.]+)"
    r"(?:.*?Learning Rate\s+([\d.e+\-]+))?"
    r"(?:.*?It/sec\s+([\d.]+))?"
    r"(?:.*?Tokens/sec\s+([\d.]+))?"
)
# Iter 200: Val loss 1.800, Val took 5.3s
_VAL_RE   = re.compile(r"Iter\s+(\d+):.*?Val loss\s+([\d.]+)")
# Saved adapter weights to ...
_SAVE_RE  = re.compile(r"Saved.*?to\s+(.+)")


def parse_line(line: str) -> dict | None:
    line = line.rstrip()
    if not line:
        return None

    m = _TRAIN_RE.search(line)
    if m:
        rec: dict = {
            "type":       "train",
            "step":       int(m.group(1)),
            "train_loss": float(m.group(2)),
        }
        if m.group(3):
            rec["lr"] = float(m.group(3))
        if m.group(4):
            rec["it_per_sec"] = float(m.group(4))
        if m.group(5):
            rec["tokens_per_sec"] = float(m.group(5))
        return rec

    m = _VAL_RE.search(line)
    if m:
        return {"type": "val", "step": int(m.group(1)), "val_loss": float(m.group(2))}

    m = _SAVE_RE.search(line)
    if m:
        return {"type": "save", "path": m.group(1).strip()}

    return None


def setup_log_dir(config_path: Path) -> Path:
    ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = LOGS_DIR / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    # Copy config snapshot
    shutil.copy(config_path, run_dir / "config.yaml")

    # Update symlink llm/logs/latest → this run
    latest = LOGS_DIR / "latest"
    if latest.is_symlink() or latest.exists():
        latest.unlink()
    latest.symlink_to(run_dir.name)

    return run_dir


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--config", type=Path, default=DEFAULT_CONFIG,
        help="Path to lora_config.yaml",
    )
    args = ap.parse_args()

    config_path = args.config if args.config.is_absolute() else REPO_ROOT / args.config
    if not config_path.exists():
        sys.exit(f"Config not found: {config_path}")

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    num_iters   = int(cfg.get("iters", 2000))
    report_every = int(cfg.get("steps_per_report", 50))

    # ── Setup ─────────────────────────────────────────────────────────────────
    run_dir     = setup_log_dir(config_path)
    metrics_log = run_dir / "metrics.jsonl"
    summary     = {"config": str(config_path), "run_dir": str(run_dir),
                   "num_iters": num_iters, "start": datetime.datetime.now().isoformat()}

    print(f"Logs → {run_dir}")
    print(f"Training {num_iters} iters, reporting every {report_every} steps\n")

    # ── Launch mlx-lm.lora ────────────────────────────────────────────────────
    cmd = [sys.executable, "-m", "mlx_lm", "lora", "--config", str(config_path)]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=REPO_ROOT,
    )

    # State for progress bar postfix
    last_train_loss = float("nan")
    last_val_loss   = float("nan")
    last_ips        = float("nan")

    bar = tqdm(
        total=num_iters,
        unit="iter",
        desc="Training",
        dynamic_ncols=True,
    )

    all_metrics: list[dict] = []
    raw_log = run_dir / "stdout.log"

    def _flush(metrics: list[dict]) -> None:
        with open(metrics_log, "a", encoding="utf-8") as lf:
            for m in metrics:
                lf.write(json.dumps(m, ensure_ascii=False) + "\n")

    def _handle_sigint(sig, frame):
        print("\nInterrupted — saving summary ...")
        proc.terminate()
        _finish()
        sys.exit(1)

    def _finish():
        bar.close()
        _flush(all_metrics)
        summary["end"] = datetime.datetime.now().isoformat()
        summary["final_train_loss"] = last_train_loss
        summary["final_val_loss"]   = last_val_loss
        with open(run_dir / "summary.json", "w") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"\nRun saved → {run_dir}")

    signal.signal(signal.SIGINT, _handle_sigint)

    pending: list[dict] = []
    with open(raw_log, "w", encoding="utf-8") as raw_f:
        for line in proc.stdout:
            raw_f.write(line)
            raw_f.flush()

            rec = parse_line(line)
            if rec is None:
                # Print unrecognized lines (errors, warnings, etc.)
                stripped = line.rstrip()
                if stripped:
                    tqdm.write(stripped)
                continue

            rec["ts"] = datetime.datetime.now().isoformat()
            all_metrics.append(rec)
            pending.append(rec)

            if rec["type"] == "train":
                step = rec["step"]
                last_train_loss = rec["train_loss"]
                if "it_per_sec" in rec:
                    last_ips = rec["it_per_sec"]
                bar.n = step
                bar.set_postfix(
                    train=f"{last_train_loss:.3f}",
                    val=f"{last_val_loss:.3f}",
                    ips=f"{last_ips:.1f}",
                    refresh=True,
                )
                bar.refresh()

            elif rec["type"] == "val":
                last_val_loss = rec["val_loss"]
                bar.set_postfix(
                    train=f"{last_train_loss:.3f}",
                    val=f"{last_val_loss:.3f}",
                    ips=f"{last_ips:.1f}",
                    refresh=True,
                )
                tqdm.write(
                    f"  ✓ Step {rec['step']:>5} | "
                    f"train {last_train_loss:.3f}  val {last_val_loss:.3f}"
                )

            elif rec["type"] == "save":
                tqdm.write(f"  💾 Saved → {rec['path']}")

            # Batch-flush every 100 records
            if len(pending) >= 100:
                _flush(pending)
                pending.clear()

    proc.wait()
    if pending:
        _flush(pending)

    _finish()


if __name__ == "__main__":
    main()
