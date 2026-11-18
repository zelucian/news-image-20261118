"""Deliver the pre-rendered image using only the Python standard library."""

import os
from pathlib import Path
import shutil


def main():
    source = Path(__file__).resolve().with_name("entry.png")
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output.mkdir(parents=True, exist_ok=True)
    destination = output / "entry.png"
    if source.resolve() != destination.resolve():
        shutil.copyfile(source, destination)


if __name__ == "__main__":
    main()
