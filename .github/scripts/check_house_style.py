#!/usr/bin/env python3
"""Enforce the CLAUDE.md house style on the copy that ships to the site.

Scoped deliberately to design/content/. The rule is "no em dashes, no en dashes,
no double hyphens in prose", and the internal working documents (sitemap.md,
the build log) use em dashes as structural separators rather than prose, so
sweeping the whole repo would flag nearly a hundred harmless separators and
train everyone to ignore the check.

Code spans and fenced blocks are stripped first, so CLI flags and CSS
var(--token) references do not register as double hyphens.
"""
import re
import sys
from pathlib import Path

TARGET_DIR = Path("design/content")

BANNED = {
    "—": "em dash",
    "–": "en dash",
}
DOUBLE_HYPHEN = re.compile(r"(?<![\w-])--(?![\w-])")

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")


def prose_lines(text):
    """Yield (line number, line) for prose only, code stripped out."""
    in_fence = False
    for n, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield n, INLINE_CODE.sub("", line)


def main():
    if not TARGET_DIR.is_dir():
        print(f"{TARGET_DIR} does not exist; nothing to check.")
        return 0

    findings = []
    checked = 0

    for path in sorted(TARGET_DIR.rglob("*.md")):
        checked += 1
        text = path.read_text(encoding="utf-8")
        for n, line in prose_lines(text):
            for char, name in BANNED.items():
                if char in line:
                    findings.append((path, n, name, line.strip()))
            if DOUBLE_HYPHEN.search(line):
                findings.append((path, n, "double hyphen", line.strip()))

    if findings:
        print("House style violations in client copy:\n")
        for path, n, what, line in findings:
            print(f"  {path}:{n}: {what}")
            print(f"      {line[:100]}")
        print(
            "\nCLAUDE.md: no em dashes, no en dashes, no double hyphens in prose. "
            "Use a comma, a full stop, or rewrite the sentence."
        )
        return 1

    print(f"House style clean across {checked} file(s) in {TARGET_DIR}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
