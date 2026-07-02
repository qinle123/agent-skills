#!/usr/bin/env python3
"""Reconcile a requirement matrix with an XMind candidate matrix."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

try:
    import yaml as _yaml  # type: ignore[import]
except ImportError:
    _yaml = None  # type: ignore[assignment]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare requirement and XMind test matrices.")
    parser.add_argument("requirement_matrix", help="Canonical requirement matrix yaml/json/csv")
    parser.add_argument("xmind_matrix", help="Canonical XMind candidate matrix yaml/json/csv")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--threshold", type=float, default=0.28)
    return parser.parse_args()


def load_matrix(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
    elif suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            data = list(csv.DictReader(handle))
    else:
        if _yaml is None:
            raise RuntimeError("pyyaml is required for yaml matrices")
        data = _yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Matrix must be a list: {path}")
    return [dict(row) for row in data if isinstance(row, dict)]


def text_for(row: dict[str, Any]) -> str:
    parts = [
        row.get("scenario", ""),
        row.get("precondition", ""),
        row.get("action", ""),
        row.get("expected", ""),
        row.get("requirementRef", ""),
        row.get("xmindRef", ""),
    ]
    return " ".join(str(part) for part in parts if part)


def tokens(text: str) -> set[str]:
    normalized = re.sub(r"\s+", "", text.lower())
    chunks = set(re.findall(r"[a-z0-9_]{2,}", text.lower()))
    for index in range(max(len(normalized) - 1, 0)):
        chunks.add(normalized[index : index + 2])
    return {chunk for chunk in chunks if chunk.strip()}


def similarity(left: dict[str, Any], right: dict[str, Any]) -> float:
    left_scenario = str(left.get("scenario", "")).strip()
    right_scenario = str(right.get("scenario", "")).strip()
    if left_scenario and right_scenario:
        if left_scenario == right_scenario:
            return 1.0
        if left_scenario in right_scenario or right_scenario in left_scenario:
            return 0.75

    left_tokens = tokens(text_for(left))
    right_tokens = tokens(text_for(right))
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def best_match(row: dict[str, Any], candidates: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, float]:
    best_row = None
    best_score = 0.0
    for candidate in candidates:
        score = similarity(row, candidate)
        if score > best_score:
            best_row = candidate
            best_score = score
    return best_row, best_score


def authority_conflict(requirement_row: dict[str, Any], xmind_row: dict[str, Any]) -> bool:
    expected_left = str(requirement_row.get("expected", "")).strip()
    expected_right = str(xmind_row.get("expected", "")).strip()
    if not expected_left or not expected_right:
        return False
    return expected_left != expected_right and similarity(
        {"scenario": expected_left}, {"scenario": expected_right}
    ) < 0.2


def reconcile(
    requirement_rows: list[dict[str, Any]],
    xmind_rows: list[dict[str, Any]],
    threshold: float,
) -> dict[str, Any]:
    covered = []
    missing_in_xmind = []
    conflicts = []
    matched_xmind_ids: set[str] = set()

    for requirement_row in requirement_rows:
        match, score = best_match(requirement_row, xmind_rows)
        if match is not None and score >= threshold:
            matched_xmind_ids.add(str(match.get("id", "")))
            item = {"requirement": requirement_row, "xmind": match, "score": round(score, 3)}
            if authority_conflict(requirement_row, match):
                conflicts.append(item)
            else:
                covered.append(item)
        else:
            missing_in_xmind.append(requirement_row)

    xmind_only = [
        row for row in xmind_rows if str(row.get("id", "")) not in matched_xmind_ids
    ]

    merged = []
    for item in covered:
        row = dict(item["requirement"])
        row["source"] = "requirement+xmind"
        row["xmindRef"] = item["xmind"].get("xmindRef", "")
        row["assertionAuthority"] = row.get("assertionAuthority") or "confirmed"
        merged.append(row)
    merged.extend(missing_in_xmind)
    merged.extend(xmind_only)

    return {
        "covered": covered,
        "missingInXmind": missing_in_xmind,
        "xmindOnly": xmind_only,
        "conflicts": conflicts,
        "mergedMatrix": merged,
    }


def row_label(row: dict[str, Any]) -> str:
    return f"{row.get('id', '')} {row.get('scenario', '')}".strip()


def render_markdown(result: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Coverage Diff")
    lines.append("")

    lines.append("## Covered")
    if result["covered"]:
        for item in result["covered"]:
            lines.append(
                f"- {row_label(item['requirement'])} <= {row_label(item['xmind'])} "
                f"(score {item['score']})"
            )
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Missing In XMind")
    if result["missingInXmind"]:
        for row in result["missingInXmind"]:
            lines.append(f"- {row_label(row)}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## XMind Only / Needs Confirmation")
    if result["xmindOnly"]:
        for row in result["xmindOnly"]:
            lines.append(f"- {row_label(row)}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Possible Conflicts")
    if result["conflicts"]:
        for item in result["conflicts"]:
            lines.append(
                f"- {row_label(item['requirement'])} conflicts with {row_label(item['xmind'])}"
            )
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Suggested Next Step")
    lines.append("- Review XMind-only and conflict rows before marking assertions as confirmed.")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    requirement_rows = load_matrix(Path(args.requirement_matrix))
    xmind_rows = load_matrix(Path(args.xmind_matrix))
    result = reconcile(requirement_rows, xmind_rows, args.threshold)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
