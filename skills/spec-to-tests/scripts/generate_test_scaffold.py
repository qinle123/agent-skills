#!/usr/bin/env python3
"""Generate test scaffolds from the canonical test matrix schema."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml as _yaml  # type: ignore[import]
except ImportError:
    _yaml = None  # type: ignore[assignment]


VALID_LEVELS = {"unit", "component", "API", "e2e", "manual"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate test scaffolds from a canonical matrix.")
    parser.add_argument("matrix_path", help="Path to matrix yaml/json/csv")
    parser.add_argument("--project-root", default=".", help="Project root used for plannedFile paths")
    parser.add_argument("--test-framework", choices=("vitest", "jest"), default="vitest")
    parser.add_argument("--e2e-framework", choices=("playwright", "cypress"), default="playwright")
    parser.add_argument("--ui-framework", choices=("react", "vue", "other"), default="react")
    parser.add_argument("--write", action="store_true", help="Create files instead of dry-run")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
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
        raise ValueError("Matrix must be a list")
    return [validate_row(dict(row)) for row in data if isinstance(row, dict)]


def validate_row(row: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in ("id", "scenario", "recommendedLevel", "plannedFile") if not row.get(key)]
    if missing:
        raise ValueError(f"Matrix row missing required fields {missing}: {row}")
    level = str(row["recommendedLevel"])
    if level not in VALID_LEVELS:
        raise ValueError(f"Invalid recommendedLevel '{level}' in {row.get('id')}")
    return row


def group_by_file(rows: Iterable[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row.get("recommendedLevel") == "manual":
            continue
        planned_file = str(row.get("plannedFile", "")).strip()
        if not planned_file:
            continue
        grouped.setdefault(planned_file, []).append(row)
    return grouped


def js_string(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace("'", "\\'")


def feature_name(path: Path) -> str:
    return path.stem.replace(".spec", "").replace(".test", "")


def pascal_case(text: str) -> str:
    parts = []
    token = []
    for char in text:
        if char.isalnum():
            token.append(char)
        elif token:
            parts.append("".join(token))
            token = []
    if token:
        parts.append("".join(token))
    return "".join(part.capitalize() for part in parts) or "Feature"


def resolve_level(rows: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        level = str(row["recommendedLevel"])
        counts[level] = counts.get(level, 0) + 1
    return max(counts, key=lambda key: counts[key])


def test_name(row: dict[str, Any]) -> str:
    return f"[{row['id']}] {row['scenario']}"


def render_todo_rows(rows: list[dict[str, Any]], call: str) -> str:
    return "\n".join(f"  {call}('{js_string(test_name(row))}');" for row in rows)


def runner_import(test_framework: str) -> str:
    return "import { describe, it } from 'vitest';\n\n" if test_framework == "vitest" else ""


def component_import(ui_framework: str, test_framework: str) -> str:
    lines = []
    if test_framework == "vitest":
        lines.append("import { describe, it } from 'vitest';")
    if ui_framework == "react":
        lines.append("import { render } from '@testing-library/react';")
    elif ui_framework == "vue":
        lines.append("import { mount } from '@vue/test-utils';")
    return "\n".join(lines) + ("\n\n" if lines else "")


def render_test_file(
    file_path: Path,
    rows: list[dict[str, Any]],
    level: str,
    test_framework: str,
    e2e_framework: str,
    ui_framework: str,
) -> str:
    feature = js_string(feature_name(file_path))

    if level == "e2e":
        if e2e_framework == "playwright":
            return (
                "import { test } from '@playwright/test';\n\n"
                f"test.describe('{feature}', () => {{\n"
                f"{render_todo_rows(rows, 'test.todo')}\n"
                "});\n"
            )
        return (
            f"describe('{feature}', () => {{\n"
            f"{render_todo_rows(rows, 'it.todo')}\n"
            "});\n"
        )

    if level == "component":
        return (
            f"{component_import(ui_framework, test_framework)}"
            f"describe('{feature}', () => {{\n"
            f"{render_todo_rows(rows, 'it.todo')}\n"
            "});\n"
        )

    return (
        f"{runner_import(test_framework)}"
        f"describe('{feature}', () => {{\n"
        f"{render_todo_rows(rows, 'it.todo')}\n"
        "});\n"
    )


def render_page_object(file_path: Path) -> str:
    class_name = f"{pascal_case(feature_name(file_path))}Page"
    return (
        "import type { Page } from '@playwright/test';\n\n"
        f"export class {class_name} {{\n"
        "  static PATH = '/';\n\n"
        "  constructor(private readonly page: Page) {}\n"
        "}\n"
    )


def render_fixture_file(file_path: Path) -> str:
    feature = feature_name(file_path)
    return (
        f"// Test data helpers for {feature}.\n"
        "// Keep data setup explicit and independent between cases.\n"
    )


def support_files(file_path: Path, level: str) -> list[tuple[Path, str]]:
    if level != "e2e":
        return []
    feature = feature_name(file_path)
    directory = file_path.parent
    return [
        (directory / f"{feature}.page.ts", render_page_object(file_path)),
        (directory / f"{feature}.fixture.ts", render_fixture_file(file_path)),
    ]


def maybe_write(path: Path, content: str, write: bool, overwrite: bool) -> str:
    if path.exists() and not overwrite:
        return f"skip  {path}"
    if not write:
        return f"plan  {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"write {path}"


def main() -> int:
    args = parse_args()
    rows = load_matrix(Path(args.matrix_path))
    project_root = Path(args.project_root).resolve()
    actions: list[str] = []

    for planned_file, file_rows in group_by_file(rows).items():
        level = resolve_level(file_rows)
        target = (project_root / planned_file).resolve()
        content = render_test_file(
            target,
            file_rows,
            level,
            args.test_framework,
            args.e2e_framework,
            args.ui_framework,
        )
        actions.append(maybe_write(target, content, args.write, args.overwrite))
        for support_path, support_content in support_files(target, level):
            actions.append(maybe_write(support_path, support_content, args.write, args.overwrite))

    for action in actions:
        print(action)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
