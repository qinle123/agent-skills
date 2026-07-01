#!/usr/bin/env python3
"""Parse an xmind file into structured markdown or JSON."""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any


NS = {"main": "urn:xmind:xmap:xmlns:content:2.0"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse XMind into JSON or markdown.")
    parser.add_argument("xmind_path", help="Path to the .xmind file")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--max-depth", type=int, default=8)
    return parser.parse_args()


def read_member(archive: zipfile.ZipFile, name: str) -> bytes | None:
    try:
        with archive.open(name) as handle:
            return handle.read()
    except KeyError:
        return None


def extract_json_notes(topic: dict[str, Any]) -> str | None:
    notes = topic.get("notes") or {}
    plain = notes.get("plain") or {}
    content = plain.get("content")
    if isinstance(content, str):
      content = content.strip()
      return content or None
    return None


def topic_from_json(topic: dict[str, Any], depth: int, max_depth: int) -> dict[str, Any]:
    node = {
        "title": str(topic.get("title", "")).strip(),
        "depth": depth,
        "notes": extract_json_notes(topic),
        "labels": topic.get("labels", []),
        "children": [],
    }
    if depth >= max_depth:
        return node

    for child in topic.get("children", {}).get("attached", []) or []:
        node["children"].append(topic_from_json(child, depth + 1, max_depth))
    return node


def parse_content_json(data: bytes, max_depth: int) -> list[dict[str, Any]]:
    payload = json.loads(data.decode("utf-8"))
    sheets = payload if isinstance(payload, list) else [payload]
    result = []
    for sheet in sheets:
        root_topic = sheet.get("rootTopic")
        if not root_topic:
            continue
        result.append(
            {
                "sheet": sheet.get("title", "Sheet"),
                "root": topic_from_json(root_topic, 0, max_depth),
            }
        )
    return result


def text_or_empty(node: ET.Element | None) -> str:
    if node is None or node.text is None:
        return ""
    return node.text.strip()


def extract_xml_notes(topic: ET.Element) -> str | None:
    note_node = topic.find("main:notes/main:plain", NS)
    content = text_or_empty(note_node)
    return content or None


def topic_from_xml(topic: ET.Element, depth: int, max_depth: int) -> dict[str, Any]:
    node = {
        "title": text_or_empty(topic.find("main:title", NS)),
        "depth": depth,
        "notes": extract_xml_notes(topic),
        "labels": [],
        "children": [],
    }
    if depth >= max_depth:
        return node

    children_root = topic.find("main:children/main:topics[@type='attached']", NS)
    if children_root is None:
        return node

    for child in children_root.findall("main:topic", NS):
        node["children"].append(topic_from_xml(child, depth + 1, max_depth))
    return node


def parse_content_xml(data: bytes, max_depth: int) -> list[dict[str, Any]]:
    root = ET.fromstring(data)
    result = []
    for sheet in root.findall("main:sheet", NS):
        root_topic = sheet.find("main:topic", NS)
        if root_topic is None:
            continue
        result.append(
            {
                "sheet": sheet.attrib.get("title", "Sheet"),
                "root": topic_from_xml(root_topic, 0, max_depth),
            }
        )
    return result


def parse_xmind(path: Path, max_depth: int) -> list[dict[str, Any]]:
    with zipfile.ZipFile(path) as archive:
        content_json = read_member(archive, "content.json")
        if content_json is not None:
            return parse_content_json(content_json, max_depth)

        content_xml = read_member(archive, "content.xml")
        if content_xml is not None:
            return parse_content_xml(content_xml, max_depth)

    raise ValueError("Unsupported xmind format: neither content.json nor content.xml found")


def render_markdown_topic(topic: dict[str, Any]) -> list[str]:
    depth = int(topic["depth"])
    indent = "  " * max(depth, 0)
    title = topic.get("title") or "(empty)"
    lines = [f"{indent}- {title}"]
    notes = topic.get("notes")
    if notes:
        lines.append(f"{indent}  note: {notes}")
    for child in topic.get("children", []):
        lines.extend(render_markdown_topic(child))
    return lines


def emit_markdown(sheets: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for sheet in sheets:
        lines.append(f"# {sheet['sheet']}")
        lines.extend(render_markdown_topic(sheet["root"]))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    path = Path(args.xmind_path)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    sheets = parse_xmind(path, args.max_depth)
    if args.format == "json":
        print(json.dumps(sheets, ensure_ascii=False, indent=2))
    else:
        print(emit_markdown(sheets), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
