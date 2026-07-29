#!/usr/bin/env python3
"""Fail the build if anything credential-shaped has been committed.

CLAUDE.md is explicit that the connection and its Application Password live in
the local Claude config, never in the repo. This is the automated backstop for
that rule. Deliberately dependency-free so CI needs no third-party action.
"""
import re
import subprocess
import sys
from pathlib import Path

# Six groups of four alphanumerics is the WordPress Application Password shape.
# Requiring at least two digits across the match keeps ordinary English prose
# ("they were sent from your last note") from tripping it.
WP_APP_PASSWORD = re.compile(r"\b[A-Za-z0-9]{4}(?: [A-Za-z0-9]{4}){5}\b")

# A named credential assigned a literal value. Placeholders in angle brackets
# and the documented <paste-password> form are allowed through.
# Note: bare "token" is deliberately NOT a keyword. In this project "token" means
# a DESIGN token (colour, spacing, gradient), which appears constantly in the build
# records, so it would be a permanent false positive. Only an auth-qualified token
# (access_token, api_token, bearer token, etc.) counts as credential-shaped.
ASSIGNMENT = re.compile(
    r"""(?ix)
    \b (api[_-]?key | secret | passwd | password | authorization
        | (?:access|api|auth|bearer|refresh|oauth|session|csrf)[_-]?token)
    \s* [:=] \s*
    ['"]? (?P<value> [^\s'"<>]{8,}) ['"]?
    """
)

PLACEHOLDER = re.compile(
    r"""(?ix) ^( .*\.\.\. | \*+ | x+ | your[_-].* | <.*> | \$\{?\w+\}?
    | %\w+% | paste.* | changeme | example.* | none | null | true | false )$"""
)

SKIP_DIRS = {".git", "__pycache__", "node_modules"}
SKIP_PATHS = {Path(".github/scripts/check_secrets.py")}
TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".yml", ".yaml", ".py", ".sh",
    ".js", ".jsx", ".ts", ".css", ".html", ".svg", ".csv", "",
}


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files", "-z"], capture_output=True, text=True, check=True
    ).stdout
    for name in out.split("\0"):
        if not name:
            continue
        path = Path(name)
        if SKIP_DIRS & set(path.parts) or path in SKIP_PATHS:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main():
    findings = []

    for path in tracked_files():
        if path.name == ".env" or path.name.startswith(".env."):
            findings.append((path, 0, "a .env file is tracked; it must stay untracked"))
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue

        for n, line in enumerate(lines, 1):
            for match in WP_APP_PASSWORD.finditer(line):
                if sum(c.isdigit() for c in match.group()) >= 2:
                    findings.append(
                        (path, n, "looks like a WordPress Application Password")
                    )

            match = ASSIGNMENT.search(line)
            if match and not PLACEHOLDER.match(match.group("value")):
                findings.append(
                    (path, n, f"credential assigned a literal value: {match.group(1)}")
                )

    if findings:
        print("Possible secrets committed:\n")
        for path, n, why in findings:
            where = f"{path}:{n}" if n else str(path)
            print(f"  {where}: {why}")
        print(
            "\nIf a real credential reached the repo, revoke it in wp-admin first, "
            "then purge it from history. Rewriting the commit is not enough on its own."
        )
        return 1

    print("No secrets found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
