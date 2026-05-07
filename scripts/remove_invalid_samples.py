#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Set


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)


def extract_invalid_sample_ids(validation_report: Dict[str, Any]) -> Set[str]:
    invalid_ids: Set[str] = set()

    results = validation_report.get("results", [])
    if not isinstance(results, list):
        raise ValueError("validation_report['results'] must be a list.")

    for r in results:
        if not isinstance(r, dict):
            continue

        sample_id = str(r.get("sample_id", "")).strip()
        if not sample_id:
            continue

        if r.get("is_valid") is False:
            invalid_ids.add(sample_id)

    return invalid_ids


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove invalid samples from rendered_repaired JSON based on validation report."
    )

    parser.add_argument(
        "--rendered-repaired",
        default="./data/privacy_benchmark_rendered_repaired.json",
        help="Path to rendered_repaired JSON file. This file will be overwritten.",
    )

    parser.add_argument(
        "--validation-report",
        default="./data/privacy_benchmark_validation_report.json",
        help="Path to validation report JSON file.",
    )

    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create a .bak backup before overwriting.",
    )

    args = parser.parse_args()

    rendered_path = Path(args.rendered_repaired)
    report_path = Path(args.validation_report)

    if not rendered_path.exists():
        raise FileNotFoundError(f"Rendered repaired file not found: {rendered_path}")

    if not report_path.exists():
        raise FileNotFoundError(f"Validation report not found: {report_path}")

    rendered_data = load_json(rendered_path)
    validation_report = load_json(report_path)

    if not isinstance(rendered_data, list):
        raise ValueError("Rendered repaired file must be a top-level JSON array.")

    if not isinstance(validation_report, dict):
        raise ValueError("Validation report must be a top-level JSON object.")

    invalid_ids = extract_invalid_sample_ids(validation_report)

    print(f"Loaded rendered samples: {len(rendered_data)}")
    print(f"Invalid sample_ids from validation report: {len(invalid_ids)}")

    kept_samples: List[Dict[str, Any]] = []
    removed_samples: List[Dict[str, Any]] = []

    for sample in rendered_data:
        if not isinstance(sample, dict):
            kept_samples.append(sample)
            continue

        sample_id = str(sample.get("sample_id", "")).strip()

        if sample_id in invalid_ids:
            removed_samples.append(sample)
        else:
            kept_samples.append(sample)

    print(f"Samples removed: {len(removed_samples)}")
    print(f"Samples kept: {len(kept_samples)}")

    if removed_samples:
        print("\nFirst removed sample_ids:")
        for sample in removed_samples[:20]:
            print(f"  {sample.get('sample_id')}")

    if not args.no_backup:
        backup_path = rendered_path.with_suffix(rendered_path.suffix + ".bak")
        shutil.copy2(rendered_path, backup_path)
        print(f"\nBackup saved to: {backup_path}")

    save_json(kept_samples, rendered_path)

    print(f"\nOverwritten cleaned file: {rendered_path}")


if __name__ == "__main__":
    main()