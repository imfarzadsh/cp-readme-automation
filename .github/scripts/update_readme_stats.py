#!/usr/bin/env python3
"""
Updates every README.md in the repo with a stats block placed between:

    <!-- REPO-STATS:START -->
    <!-- REPO-STATS:END -->

(If the markers don't exist, the block is appended to the end of the README.)

Layouts:
  1) Root README
       - total solved per extension
       - table: Platforms | Solved Count | Directory Link   (top-level folders)
       - table: last 5 pushed code files
  2) README in a folder that has sub-folders
       - total solved per extension
       - table: Category | Solved Count | Directory Link
  3) README in a folder with no sub-folders
       - total solved per extension
       - table: Number | Problem | Directory Link
         (file names look like [Index]-[ProblemID]-[ProblemName].ext,
          only ProblemName is shown)
"""
import os
import re
import subprocess
from collections import Counter
from urllib.parse import quote

START = "<!-- REPO-STATS:START -->"
END = "<!-- REPO-STATS:END -->"
README_RE = re.compile(r"^readme([-_.][a-z0-9_-]+)?\.(md|markdown)$", re.IGNORECASE)
RECENT_LIMIT = 5

# Extensions counted as "solved" code files. Add/remove as you like.
CODE_EXTS = {
    ".cpp", ".cc", ".c", ".h", ".hpp", ".py", ".java", ".js", ".ts",
    ".cs", ".go", ".rs", ".kt", ".rb", ".php", ".swift", ".sql",
    ".scala", ".dart", ".sh",
}


# ---------------------------------------------------------------- helpers
def tracked_files():
    out = subprocess.check_output(["git", "-c", "core.quotepath=false", "ls-files", "-z"])
    return [p for p in out.decode("utf-8", "replace").split("\0") if p and os.path.isfile(p)]


def is_readme(path):
    return bool(README_RE.match(os.path.basename(path)))


def is_hidden(path):
    return any(part.startswith(".") for part in path.split("/"))


def ext_of(path):
    return os.path.splitext(path)[1].lower()


def esc(text):
    return text.replace("|", "\\|")


def link(target, from_folder, is_dir):
    rel = os.path.relpath(target, from_folder or ".").replace(os.sep, "/")
    url = quote(rel, safe="/")
    if is_dir:
        url += "/"
    return f"[Open]({url})"


def problem_name(path):
    """[Index]-[ProblemID]-[ProblemName].ext  ->  ProblemName"""
    stem = os.path.splitext(os.path.basename(path))[0]
    parts = stem.split("-", 2)
    return parts[2] if len(parts) == 3 and parts[2] else stem


def sort_key(path):
    base = os.path.basename(path)
    m = re.match(r"\d+", base)
    return (int(m.group()) if m else float("inf"), base.lower())


def summary_line(files):
    counts = Counter(ext_of(f).lstrip(".") for f in files)
    parts = " · ".join(f"`{e}`: {n}" for e, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
    line = f"**Total Solved: {len(files)}**"
    return f"{line} — {parts}" if parts else line


def recent_code_files(valid, limit=RECENT_LIMIT):
    """Most recently added/modified/renamed code files, newest first."""
    proc = subprocess.Popen(
        ["git", "-c", "core.quotepath=false", "log", "--diff-filter=AMR",
         "--name-only", "--pretty=format:"],
        stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
    )
    found = []
    for line in proc.stdout:
        name = line.rstrip("\n")
        if name and name in valid and name not in found:
            found.append(name)
            if len(found) == limit:
                break
    proc.terminate()
    proc.wait()
    return found


# ---------------------------------------------------------------- blocks
def folder_table(folder, scoped, subs, first_header):
    prefix = folder + "/" if folder else ""
    rows = [f"| {first_header} | Solved Count | Directory Link |", "| --- | ---: | --- |"]
    for name in subs:
        sub_path = prefix + name
        count = sum(1 for f in scoped if f.startswith(sub_path + "/"))
        rows.append(f"| {esc(name)} | {count} | {link(sub_path, folder, True)} |")
    return rows


def file_table(folder, scoped):
    rows = ["| Number | Problem | Directory Link |", "| ---: | --- | --- |"]
    for i, f in enumerate(sorted(scoped, key=sort_key), start=1):
        rows.append(f"| {i:04d} | {esc(problem_name(f))} | {link(f, folder, False)} |")
    return rows


def build_block(folder, code, recent):
    prefix = folder + "/" if folder else ""
    scoped = [f for f in code if f.startswith(prefix)]
    subs = sorted({f[len(prefix):].split("/")[0] for f in scoped if "/" in f[len(prefix):]},
                  key=str.lower)

    out = [START, "", "## 📊 Stats", "", summary_line(scoped), ""]

    if subs:
        out += folder_table(folder, scoped, subs, "Platforms" if not folder else "Category")
        out.append("")
        if not folder and recent:
            out += [f"### 🕒 Last {len(recent)} pushed solutions", "",
                    "| Problem | Directory Link |", "| --- | --- |"]
            for f in recent:
                out.append(f"| {esc(problem_name(f))} | {link(f, folder, False)} |")
            out.append("")
    else:
        direct = [f for f in scoped if "/" not in f[len(prefix):]]
        out += file_table(folder, direct)
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
    code = [f for f in files
            if not is_hidden(f) and not is_readme(f) and ext_of(f) in CODE_EXTS]
    recent = recent_code_files(set(code))

    for readme in [f for f in files if is_readme(f) and not is_hidden(f)]:
        folder = os.path.dirname(readme)
        update_readme(readme, build_block(folder, code, recent))


if __name__ == "__main__":
    main()