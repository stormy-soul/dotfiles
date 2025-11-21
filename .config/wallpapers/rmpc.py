import os
import re
import json
import argparse
from pathlib import Path
from typing import Optional, Union

error_buffer = []

def extract(file: Path) -> Optional[dict]:
    try:
        with open(file, "r") as data:
            scheme = json.loads(data.read())
        return scheme['colors']
    except Exception:
        return None

def paint(colors: list[str], theme: Path):
    if len(colors) < 2:
        error_buffer.append("not enough colors")

    steps = ["0", "100"]
    data = theme.read_text()

    pattern = r"bar_color:\s*Gradient\(\{.*?\}\)"
    gradient = "Gradient({\n"
    for color, step in zip(colors, steps):
        gradient += f"\t\t\t\t\t{step}: \"{color}\",\n"
    gradient += "\t\t\t\t})"

    new_data, count = re.subn(pattern, f"bar_color: {gradient}", data, flags=re.DOTALL)

    if count == 0:
        error_buffer.append(f"gradient not found in {str(theme)}")
    theme.write_text(new_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cache", help="Pywal directory. default = ~/.cache/wal/")
    parser.add_argument("-r", "--rmpc", help="RMPC theme directory. default = ~/.config/rmpc/themes/")
    parser.add_argument("-t", "--theme", help="RMPC theme name.")
    args= parser.parse_args()

    pywal_cache = Path(args.cache) if args.cache else Path("/home/nadun/.cache/wal/")
    pywal_json = pywal_cache / "colors.json"
    rmpc_path = Path(args.rmpc) if args.rmpc else Path("/home/nadun/.config/rmpc/themes/")
    rmpc_theme = rmpc_path / f"{args.theme}"

    colors = []

    if os.path.exists(pywal_json):
        scheme = extract(pywal_json)

        for name, color in scheme.items():
            colors.append(color)    

    usable_colors = colors[6], colors[7]
    paint(usable_colors, rmpc_theme)
