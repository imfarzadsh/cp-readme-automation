# 🚀 CP README Automation

> An automated, multi-level statistics tracker and dashboard generator for Competitive Programming and Problem-Solving repositories using GitHub Actions and Python.

[![GitHub Actions Status](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/cp-readme-automation/update-readme.yml?branch=main&style=flat-square&logo=githubactions&logoColor=white)](https://github.com/YOUR_USERNAME/cp-readme-automation/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

---

## 🌟 Overview

Keeping track of solved problems across platforms like **LeetCode**, **CSES**, and **Codeforces** can become messy. **CP README Automation** solves this by automatically scanning your repository directory structure, counting your solution files, and dynamically updating multi-level markdown tables and statistics inside your `README.md` files upon every push.

No manual updates required—just push your code and let the automation handle the rest!

---

## 📊 Overall Progress Dashboard

<!-- REPO-STATS:START -->

### 📊 Stats

| Metric | Value |
| --- | ---: |
| Files (total) | 10 |
| Files in this folder | 2 |
| Files in sub-folders | 8 |
| Sub-folders | 8 |
| Lines (text files) | 198 |
| Total size | 6.1 KB |

| Extension | Files | Lines | Size |
| --- | ---: | ---: | ---: |
| `.cpp` | 4 | 0 | 0 B |
| `.py` | 3 | 137 | 4.1 KB |
| `(no ext)` | 1 | 21 | 1.0 KB |
| `.txt` | 1 | 2 | 93 B |
| `.yml` | 1 | 38 | 857 B |

<!-- REPO-STATS:END -->

---

## 📂 Repository Structure

```text
cp-readme-automation/
├── .github/
│   ├── workflows/
│   │   └── update-readme.yml    # GitHub Actions workflow for auto-syncing
│   └── scripts/
│       └── stats_updater.py     # Core Python script for recursive scanning & table injection
├── examples/                    # Example structure showing how platforms & categories organize
│   ├── CSES/
│   └── Codeforces/
├── README.md                    # Root-level general dashboard & documentation
├── requirements.txt             # Project dependencies
└── LICENSE                      # MIT License
```

---

## ⚙️ How It Works

1. **Recursive Scanning:** The Python script (`stats_updater.py`) scans all first-level directories (platforms) and their subfolders (categories/ratings).
2. **File Counting:** It counts valid code files (`.py`, `.cpp`, `.cc`, `.c`, `.java`, `.js`, `.ts`, `.go`, `.rs`) recursively.
3. **Markdown Injection:** It looks for specific HTML comment tags (`<!-- START_STATS -->` and `<!-- END_STATS -->`) in your `README.md` files and injects the updated statistics tables.
4. **Automated Commit:** GitHub Actions detects the changes made by the script and automatically commits and pushes them back to your repository.

---

## 🚀 Quick Start / Usage

Want to use this system for your own problem-solving repository? Follow these steps:

1. **Use Template or Fork:** Click **Use this template** (or fork this repository) to create your own copy.
2. **Organize Your Folders:** Create top-level folders for each platform (e.g., `CSES`, `Codeforces`, `LeetCode`) and subfolders for categories or ratings (e.g., `Introductory Problems`, `1200`).
3. **Add Tags to READMEs:** Ensure your `README.md` files (at the root, inside each platform folder, and optionally inside subfolders) contain the target tags:
   ```markdown
   <!-- START_STATS -->
   <!-- END_STATS -->
   ```
4. **Configure Workflow Permissions:**
   * Go to your repository **Settings** -> **Actions** -> **General**.
   * Scroll down to **Workflow permissions** and select **Read and write permissions**.
   * Click **Save**.
5. **Push Solutions:** Add your solution files inside your category folders and push to GitHub. The automation will run automatically and update all your tables!

---

## 🛠️ Supported File Extensions

By default, the script counts files with the following extensions:
`.py`, `.cpp`, `.cc`, `.c`, `.java`, `.js`, `.ts`, `.go`, `.rs`

You can easily customize this list by editing `VALID_EXTENSIONS` inside `.github/scripts/stats_updater.py`.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).