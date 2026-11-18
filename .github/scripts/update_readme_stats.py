#!/usr/bin/env python3
"""
For every README.md in the repo, compute stats about the files that live in the
same folder and all sub-folders, and write them between these markers:

    <!-- REPO-STATS:START -->
    <!-- REPO-STATS:END -->

If a README has no markers, the block is appended to the end of the file.
Only git-tracked files are counted (so .gitignore'd files, node_modules, etc.
are skipped automatically). README.md files themselves are not counted,
which prevents the action from changing its own numbers.
"""
import os
import re
import subprocess
from collections import defaultdict

START = "<!-- REPO-STATS:START -->"
END = "<!-- REPO-STATS:END -->"
README_NAMES = {"readme.md", "readme.markdown"}


def tracked_files():
    out = subprocess.check_output(["git", "ls-files", "-z"]).decode("utf-8", "replace")
    return [p for p in out.split("\0") if p and os.path.isfile(p)]


def is_readme(path):
    return os.path.basename(path).lower() in README_NAMES


def file_info(path):
    """Return (size_bytes, line_count or None for binary files)."""
    size = os.path.getsize(path)
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return size, None
    if b"\0" in data[:8000]:
        return size, None
    lines = data.count(b"\n")
    if data and not data.endswith(b"\n"):
        lines += 1
    return size, lines


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def ext_of(path):
    name = os.path.basename(path)
    ext = os.path.splitext(name)[1].lower()
    return ext if ext else "(no ext)"


def build_block(folder, files, info):
    prefix = folder + "/" if folder else ""
    scoped = [f for f in files if f.startswith(prefix) and not is_readme(f)]

    direct = [f for f in scoped if "/" not in f[len(prefix):]]
    nested = [f for f in scoped if "/" in f[len(prefix):]]

    dirs = set()
    for f in scoped:
        rel = f[len(prefix):]
        parts = rel.split("/")[:-1]
        for i in range(1, len(parts) + 1):
            dirs.add("/".join(parts[:i]))

    total_size = sum(info[f][0] for f in scoped)
    total_lines = sum(info[f][1] or 0 for f in scoped)

    by_ext = defaultdict(lambda: [0, 0, 0])  # files, lines, size
    for f in scoped:
        size, lines = info[f]
        row = by_ext[ext_of(f)]
        row[0] += 1
        row[1] += lines or 0
        row[2] += size

    out = [START, "", "### 📊 Stats", ""]
    out += [
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Files (total) | {len(scoped)} |",
        f"| Files in this folder | {len(direct)} |",
        f"| Files in sub-folders | {len(nested)} |",
        f"| Sub-folders | {len(dirs)} |",
        f"| Lines (text files) | {total_lines:,} |",
        f"| Total size | {human_size(total_size)} |",
        "",
    ]
    if by_ext:
        out += [
            "| Extension | Files | Lines | Size |",
            "| --- | ---: | ---: | ---: |",
        ]
        for ext, (n, lines, size) in sorted(by_ext.items(), key=lambda kv: (-kv[1][0], kv[0])):
            out.append(f"| `{ext}` | {n} | {lines:,} | {human_size(size)} |")
        out.append("")
    out.append(END)
    return "\n".join(out)


def update_readme(path, block):
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
        content = f.read()

    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if pattern.search(content):
        new = pattern.sub(lambda _m: block, content)
    else:
        sep = "" if content.endswith("\n\n") else ("\n" if content.endswith("\n") else "\n\n")
        new = content + sep + "\n" + block + "\n"

    if new != content:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print(f"updated: {path}")


def main():
    files = tracked_files()
    info = {f: file_info(f) for f in files if not is_readme(f)}
    for readme in [f for f in files if is_readme(f)]:
        folder = os.path.dirname(readme)
        update_readme(readme, build_block(folder, list(info), info))


if __name__ == "__main__":
    main()