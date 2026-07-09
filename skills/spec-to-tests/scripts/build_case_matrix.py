#!/usr/bin/env python3
"""Build a canonical candidate test matrix from an XMind file or parsed JSON."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path
from typing import Any

from parse_xmind import parse_xmind


LEVEL_RULES: list[tuple[str, tuple[str, ...], str]] = [
    (
        "unit",
        (
            "最大值",
            "最小值",
            "默认值",
            "字段名",
            "映射",
            "枚举",
            "参数",
            "payload",
            "必填",
            "显隐",
            "显示",
            "隐藏",
            "校验",
            "权限判断",
            "状态计算",
        ),
        "偏字段规则、参数映射或纯逻辑校验，优先下沉到 unit。",
    ),
    (
        "component",
        (
            "表单",
            "弹窗",
            "Drawer",
            "Modal",
            "联动",
            "评分",
            "回显",
            "新增/编辑",
            "列表列",
            "筛选",
        ),
        "偏组件/表单/局部交互，适合 component 测试。",
    ),
    (
        "API",
        (
            "接口",
            "请求",
            "响应",
            "错误码",
            "鉴权",
            "权限接口",
            "保存参数",
            "提交参数",
        ),
        "偏接口契约、请求响应或服务层行为，适合 API/integration 测试。",
    ),
    (
        "e2e",
        (
            "导出",
            "树",
            "跨页面",
            "审批",
            "流程",
            "下载",
            "上传",
            "hover",
            "跳转",
            "提交审核",
            "驳回",
            "列表可见",
            "详情可见",
        ),
        "涉及真实页面、多区域联动或浏览器级行为，适合 e2e。",
    ),
]

PRIORITY_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("P0", ("主流程", "核心", "冒烟", "提交", "保存成功", "审批", "创建成功")),
    ("P1", ("异常", "失败", "校验", "权限", "边界", "驳回", "禁用")),
    ("P2", ("展示", "查询", "筛选", "导出", "回显")),
]

LOW_SIGNAL_TITLES = {
    "文件编号",
    "文件名称",
    "版本号",
    "状态",
    "创建人",
    "创建时间",
    "更新时间",
    "操作",
}

HIGH_SIGNAL_KEYWORDS = (
    "校验",
    "搜索",
    "查询",
    "导出",
    "新增",
    "编辑",
    "删除",
    "提交",
    "审批",
    "驳回",
    "启用",
    "禁用",
    "上传",
    "下载",
    "联动",
    "二次确认",
    "回显",
    "必填",
    "默认",
    "限制",
    "提示",
    "刷新",
    "重复",
    "不可编辑",
    "成功",
    "失败",
)

GENERIC_PATH_PREFIXES = ("步骤", "预期", "前置")
ACTION_PREFIXES = ("点击", "查看", "切换", "选择", "输入")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a canonical test matrix from XMind.")
    parser.add_argument("input_path", help="Path to .xmind or parsed .json file")
    parser.add_argument(
        "--format",
        choices=("yaml", "csv", "json", "markdown"),
        default="yaml",
        help="Output format",
    )
    parser.add_argument(
        "--module-root",
        default="tests",
        help="Root directory used when suggesting file paths",
    )
    parser.add_argument("--id-prefix", default="XM", help="Stable id prefix for generated rows")
    return parser.parse_args()


def load_sheets(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".xmind":
        return parse_xmind(path, max_depth=8)
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(text: str) -> str:
    cleaned = []
    for char in text.strip().lower():
        if char.isalnum():
            cleaned.append(char)
        elif char in (" ", "-", "_", "/", "."):
            cleaned.append("-")
    slug = "".join(cleaned).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "module"


def normalize_title(title: str) -> str:
    normalized = title.strip()
    for prefix in GENERIC_PATH_PREFIXES:
        if normalized.startswith(f"{prefix}：") or normalized.startswith(f"{prefix}:"):
            normalized = re.split("[:：]", normalized, maxsplit=1)[1].strip()
            break
    for prefix in ACTION_PREFIXES:
        if normalized.startswith(prefix) and len(normalized) > len(prefix) + 1:
            normalized = normalized[len(prefix) :].strip()
            break
    return normalized


def classify_level(text: str) -> tuple[str, str]:
    for level, keywords, reason in LEVEL_RULES:
        if any(keyword in text for keyword in keywords):
            return level, reason
    return "component", "缺少更具体的需求权威，默认先作为组件/局部交互候选。"


def classify_priority(text: str) -> str:
    for priority, keywords in PRIORITY_RULES:
        if any(keyword in text for keyword in keywords):
            return priority
    return "P2"


def data_requirement_for(level: str) -> str:
    if level == "unit":
        return "none"
    if level in {"component", "API"}:
        return "mock"
    if level == "e2e":
        return "real-env"
    return "fixture"


def is_leaf(node: dict[str, Any]) -> bool:
    return not node.get("children")


def is_low_signal_leaf(node: dict[str, Any]) -> bool:
    title = (node.get("title") or "").strip()
    if not title or node.get("notes") or node.get("labels"):
        return False
    if title in LOW_SIGNAL_TITLES:
        return True
    if len(title) > 30:
        return False
    return not any(keyword in title for keyword in HIGH_SIGNAL_KEYWORDS)


def summarize_titles(titles: list[str]) -> str:
    if len(titles) <= 3:
        return "、".join(titles)
    return f"{titles[0]}、{titles[1]}等{len(titles)}项"


def guess_feature(sheet_name: str, path_titles: list[str]) -> str:
    for title in reversed(path_titles):
        normalized = normalize_title(title)
        if normalized and len(normalized) >= 2 and len(normalized) <= 24:
            return slugify(normalized)
    return slugify(sheet_name)


def planned_file(module_root: str, feature: str, level: str) -> str:
    if level == "e2e":
        return f"{module_root}/e2e/{feature}/{feature}.spec.ts"
    if level == "unit":
        return f"{module_root}/unit/{feature}/{feature}.test.ts"
    if level == "API":
        return f"{module_root}/api/{feature}/{feature}.test.ts"
    if level == "manual":
        return ""
    return f"{module_root}/component/{feature}/{feature}.test.tsx"


def make_row(
    row_id: str,
    scenario: str,
    path_titles: list[str],
    notes: str | None,
    module_root: str,
    sheet_name: str,
    reason_override: str | None = None,
) -> dict[str, Any]:
    text = " ".join(filter(None, [scenario, notes or "", *path_titles]))
    level, reason = classify_level(text)
    feature = guess_feature(sheet_name, path_titles)
    return {
        "id": row_id,
        "source": "xmind",
        "requirementRef": "",
        "xmindRef": " > ".join([*path_titles, scenario]),
        "scenario": scenario,
        "precondition": "",
        "action": notes or "",
        "expected": "",
        "priority": classify_priority(text),
        "recommendedLevel": level,
        "dataRequirement": data_requirement_for(level),
        "assertionAuthority": "needs-confirmation",
        "reason": reason_override or reason,
        "plannedFile": planned_file(module_root, feature, level),
        "automationStatus": "planned",
        "openQuestions": ["只有 XMind 来源，需用需求文档或人工确认业务断言。"],
    }


def collect_rows(
    sheet_name: str,
    node: dict[str, Any],
    path_titles: list[str],
    module_root: str,
    rows: list[dict[str, Any]],
    id_prefix: str,
) -> None:
    title = (node.get("title") or "").strip()
    if not title:
        return

    current_path = [*path_titles, normalize_title(title)]
    if is_leaf(node):
        row_id = f"{id_prefix}-{len(rows) + 1:03d}"
        rows.append(make_row(row_id, normalize_title(title), path_titles, node.get("notes"), module_root, sheet_name))
        return

    children = node.get("children", [])
    low_signal = [
        normalize_title(child.get("title") or "")
        for child in children
        if is_leaf(child) and is_low_signal_leaf(child)
    ]
    if len(low_signal) >= 2:
        row_id = f"{id_prefix}-{len(rows) + 1:03d}"
        scenario = f"{normalize_title(title)}展示正确（{summarize_titles(low_signal)}）"
        rows.append(
            make_row(
                row_id,
                scenario,
                path_titles,
                None,
                module_root,
                sheet_name,
                "同组低风险字段/列展示合并为一条候选用例，避免 XMind 叶子节点机械平铺。",
            )
        )

    for child in children:
        if len(low_signal) >= 2 and is_leaf(child) and is_low_signal_leaf(child):
            continue
        collect_rows(sheet_name, child, current_path, module_root, rows, id_prefix)


def build_matrix(sheets: list[dict[str, Any]], module_root: str, id_prefix: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for sheet in sheets:
        root = sheet.get("root")
        if not root:
            continue
        for child in root.get("children", []):
            collect_rows(sheet.get("sheet", "Sheet"), child, [], module_root, rows, id_prefix)
    return rows


def yaml_scalar(value: Any) -> str:
    if isinstance(value, list):
        return ""
    text = str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def emit_yaml(rows: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for row in rows:
        lines.append("-")
        for key, value in row.items():
            if isinstance(value, list):
                if value:
                    lines.append(f"  {key}:")
                    for item in value:
                        lines.append(f"    - {yaml_scalar(item)}")
                else:
                    lines.append(f"  {key}: []")
            else:
                lines.append(f"  {key}: {yaml_scalar(value)}")
    return "\n".join(lines) + ("\n" if lines else "")


def emit_markdown(rows: list[dict[str, Any]]) -> str:
    headers = ["id", "source", "scenario", "priority", "recommendedLevel", "assertionAuthority", "plannedFile"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def emit_csv(rows: list[dict[str, Any]]) -> str:
    headers = [
        "id",
        "source",
        "requirementRef",
        "xmindRef",
        "scenario",
        "precondition",
        "action",
        "expected",
        "priority",
        "recommendedLevel",
        "dataRequirement",
        "assertionAuthority",
        "reason",
        "plannedFile",
        "automationStatus",
        "openQuestions",
    ]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        flattened = dict(row)
        flattened["openQuestions"] = " / ".join(row.get("openQuestions", []))
        writer.writerow(flattened)
    return output.getvalue()


def main() -> int:
    args = parse_args()
    sheets = load_sheets(Path(args.input_path))
    rows = build_matrix(sheets, args.module_root, args.id_prefix)
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif args.format == "csv":
        sys.stdout.write(emit_csv(rows))
    elif args.format == "markdown":
        sys.stdout.write(emit_markdown(rows))
    else:
        sys.stdout.write(emit_yaml(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
