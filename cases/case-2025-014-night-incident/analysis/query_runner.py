#!/usr/bin/env python3
"""
Toy SIEM query runner for CASE-2025-014.

Reads synthetic JSONL telemetry and supports:
- search by field=value;
- count grouped by a field;
- timeline by an entity field.

This script does not write files and does not send data anywhere.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

CASE_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SOURCES = [
    CASE_ROOT / "02-telemetry" / "edr-events.jsonl",
    CASE_ROOT / "02-telemetry" / "idp-events.jsonl",
    CASE_ROOT / "02-telemetry" / "proxy-events.jsonl",
    CASE_ROOT / "02-telemetry" / "dns-events.jsonl",
]


def iter_events(paths: Iterable[Path]) -> Iterable[dict[str, Any]]:
    for path in paths:
        if not path.exists():
            continue

        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    yield json.loads(line)


def match(event: dict[str, Any], filters: list[str]) -> bool:
    for item in filters:
        if "=" not in item:
            return False

        key, _, value = item.partition("=")
        key = key.strip()
        value = value.strip()

        actual = event.get(key)

        if actual is None:
            return False

        if isinstance(actual, str):
            if value.lower() not in actual.lower():
                return False
        elif str(actual).lower() != value.lower():
            return False

    return True


def cmd_search(args: argparse.Namespace) -> int:
    count = 0

    for event in (item for item in iter_events(DEFAULT_SOURCES) if match(item, args.filter)):
        print(json.dumps(event, ensure_ascii=False))
        count += 1

        if args.limit and count >= args.limit:
            break

    print(f"--- {count} events ---", file=sys.stderr)
    return 0


def cmd_count(args: argparse.Namespace) -> int:
    counter: Counter[Any] = Counter()

    for event in (item for item in iter_events(DEFAULT_SOURCES) if match(item, args.filter)):
        counter[event.get(args.by, "<missing>")] += 1

    for value, total in counter.most_common(args.top):
        print(f"{total:6d}  {value}")

    return 0


def cmd_timeline(args: argparse.Namespace) -> int:
    events = list(iter_events(DEFAULT_SOURCES))
    events.sort(key=lambda event: event.get("ts", ""))

    for event in events:
        if args.entity_key and args.entity_value:
            actual = str(event.get(args.entity_key, "")).lower()

            if actual != args.entity_value.lower():
                continue

        timestamp = event.get("ts", "?")
        kind = event.get("kind", "event")
        print(f"{timestamp}  {kind:14s}  {json.dumps(event, ensure_ascii=False)}")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Synthetic SIEM query runner for CASE-2025-014"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search events by field filters")
    search.add_argument(
        "filter",
        nargs="*",
        help="Field filter in the form key=value",
    )
    search.add_argument("--limit", type=int, default=0)
    search.set_defaults(function=cmd_search)

    count = subparsers.add_parser("count", help="Count events grouped by a field")
    count.add_argument("by", help="Field used for grouping")
    count.add_argument("filter", nargs="*", help="Field filters: key=value")
    count.add_argument("--top", type=int, default=20)
    count.set_defaults(function=cmd_count)

    timeline = subparsers.add_parser("timeline", help="Print a timeline for one entity")
    timeline.add_argument("--entity-key", help="Field name, for example host or user")
    timeline.add_argument("--entity-value", help="Exact value for the selected field")
    timeline.set_defaults(function=cmd_timeline)

    args = parser.parse_args(argv)
    return args.function(args)


if __name__ == "__main__":
    raise SystemExit(main())
