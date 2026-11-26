"""Office Artifacts: The One-Line Placard.

Writes a single-line museum placard for an ordinary office object,
treated as an ancient artifact, to the entry file.

Stdlib only. The output path is resolved from the ENTRY_OUTPUT
environment variable, else OUTPUT_DIR / MAKEFUN_OUTPUT_DIR, else
/output/entry.txt.
"""

import os


ENTRY = (
    "Sticky note, c. 1500 BCE. Papyrus and beeswax. "
    "Reads: 'Do not move the grain.' "
    "Earliest known passive-aggressive memo. "
    "Gift of the Break Room."
)


def resolve_output_path():
    if os.environ.get("ENTRY_OUTPUT"):
        return os.environ["ENTRY_OUTPUT"]
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    return "/output/entry.txt"


def validate_entry():
    """Guard: the placard must be one line, 1-180 non-whitespace chars,
    valid UTF-8. Raises ValueError otherwise; never alters the text."""
    encoded = ENTRY.encode("utf-8")  # raises UnicodeEncodeError if invalid
    if not (1 <= len(ENTRY.strip()) <= 180):
        raise ValueError("placard must be 1-180 non-whitespace characters")
    if "\n" in ENTRY or "\r" in ENTRY:
        raise ValueError("placard must be a single line")
    if len(encoded) == 0:
        raise ValueError("placard must not be empty")


def main():
    validate_entry()
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
