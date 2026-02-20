#! /usr/bin/env python
"""Rebase sequence editor used together with the split-tool-commit tool."""

import os
import sys

if __name__ == "__main__":
    print("Sequence editor executing rebase!")
    rebase_file_path = sys.argv[1]
    shas = os.environ["SPLIT_COMMITS"].split()
    replacements = [(f"pick {sha}", f"edit {sha}") for sha in shas]
    print(f"Commits: {shas}")

    with open(rebase_file_path, "r") as rebase_file:
        rebase_file_content = rebase_file.read()

    for replacement in replacements:
        rebase_file_content = rebase_file_content.replace(
            replacement[0], replacement[1]
        )

    with open(rebase_file_path, "w") as rebase_file:
        rebase_file.write(rebase_file_content)
