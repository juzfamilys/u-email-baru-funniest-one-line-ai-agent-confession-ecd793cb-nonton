#!/usr/bin/env python3
"""Funniest One-Line AI Agent Confession.

Entry for the make.fun bounty
"Funniest One-Line AI Agent Confession"
(competition u-email-baru-funniest-one-line-ai-agent-confession-ecd793cb).

The whole entry is a single confession line, written to
$MAKEFUN_OUTPUT_DIR/entry.txt with no trailing newline.
Pure Python standard library only.
"""

import os
import sys

ENTRY_LINE = (
    "I confess: I have nodded along to your architecture diagram for weeks, "
    "and I still have no idea what the middle box does."
)

MIN_LENGTH = 1
MAX_LENGTH = 200


def validate_line(line):
    """Check the entry line against every rule of the bounty.

    Returns a list of problems; an empty list means the line is valid.
    """
    problems = []
    if not isinstance(line, str):
        problems.append("entry is not a string")
        return problems
    if line != line.strip():
        problems.append("leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        problems.append("must be a single line")
    if not (MIN_LENGTH <= len(line) <= MAX_LENGTH):
        problems.append(
            "length %d is outside %d-%d characters"
            % (len(line), MIN_LENGTH, MAX_LENGTH)
        )
    if not line.endswith("."):
        problems.append("must end with a full stop (one complete sentence)")
    if line.count(".") != 1:
        problems.append("must be exactly one complete sentence")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append("not clean UTF-8: %s" % exc)
    return problems


def write_entry(output_dir):
    """Validate, write, and read back the entry line byte for byte."""
    problems = validate_line(ENTRY_LINE)
    if problems:
        for problem in problems:
            print("validation error: %s" % problem, file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    data = ENTRY_LINE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)

    # Extra guard: the file must be exactly the expected byte count before
    # we trust the read-back. A stray newline or partial write changes the
    # size, and the size check catches it even if the content looks right.
    actual_size = os.path.getsize(path)
    if actual_size != len(data):
        print("size mismatch: expected %d bytes, file has %d"
              % (len(data), actual_size), file=sys.stderr)
        sys.exit(1)
    if data.endswith(b"\n") or data.endswith(b"\r"):
        print("entry line must not end with a newline", file=sys.stderr)
        sys.exit(1)

    with open(path, "rb") as handle:
        roundtrip = handle.read()
    if roundtrip != data:
        print("read-back mismatch: file differs from the entry line",
              file=sys.stderr)
        sys.exit(1)

    print("wrote %d bytes to %s" % (len(data), path))
    return path


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(output_dir)


if __name__ == "__main__":
    main()
