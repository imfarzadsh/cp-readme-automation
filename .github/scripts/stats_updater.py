import os

# پسوندهای معتبر فایل‌های کد برای شمارش مسائل
VALID_EXTENSIONS = (".py", ".cpp", ".cc", ".c", ".java", ".js", ".ts", ".go", ".rs")

def count_files_recursive(folder):
    """شمارش بازگشتی تمام فایل‌های کد در پوشه و زیرپوشه‌ها"""
    if not os.path.exists(folder):
        return 0
    count = 0
    for _, _, files in os.walk(folder):
        for f in files:
            if f.endswith(VALID_EXTENSIONS):
                count += 1
    return count

def update_readme_section(readme_path, content_to_insert):
    """تزریق آمار بین تگ‌های مشخص‌شده <!-- START_STATS --> و <!-- END_STATS --> در فایل README"""
    if not os.path.exists(readme_path):
        return
    
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- START_STATS -->"
    end_tag = "<!-- END_STATS -->"

    start_idx = content.find(start_tag)
    end_idx = content.find(end_tag)

    if start_idx != -1 and end_idx != -1:
        new_content = (
            content[:start_idx + len(start_tag)] +
            "\n\n" + content_to_insert + "\n\n" +
            content[end_idx:]
        )
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)

def main():
    # اسکن خودکار پوشه‌های اصلی سطح اول (به جز پوشه‌های سیستمی)
    ignore_dirs = {".git", ".github", "venv", "__pycache__", "examples"}
    root_dirs = [d for d in os.listdir(".") if os.path.isdir(d) and d not in ignore_dirs]

    grand_total = 0
    platform_summary_rows = []

    for platform in sorted(root_dirs):
        platform_path = platform
        platform_total = 0
        
        # اسکن زیرپوشه‌های هر پلتفرم (مثلاً دسته‌بندی‌های CSES یا ریت‌های Codeforces)
        subdirs = sorted([d for d in os.listdir(platform_path) if os.path.isdir(os.path.join(platform_path, d)) and not d.startswith('.')])
        
        if not subdirs:
            continue

        platform_table_rows = []
        for idx, sub in enumerate(subdirs, start=1):
            sub_full_path = os.path.join(platform_path, sub)
            count = count_files_recursive(sub_full_path)
            platform_total += count

            status = "🟢 Active" if count > 0 else "⏳ Planned"
            link = f"[Go to Folder](./{sub})" if count > 0 else "—"

            platform_table_rows.append(f"| {idx} | {sub} | {count} | {status} | {link} |")

            # بروزرسانی ریدمیِ خودِ زیرپوشه (اگر تگ داشته باشد)
            sub_readme_content = f"### Subfolder: {sub}\n\nSolved Problems: **{count}**\n"
            update_readme_section(os.path.join(sub_full_path, "README.md"), sub_readme_content)

        # ساخت جدول برای ریدمیِ خودِ پلتفرم (مثلاً CSES/README.md)
        platform_rows_str = "\n".join(platform_table_rows)
        platform_md = f"Total Solved: **{platform_total}**\n\n"
        platform_md += "| # | Category / Level | Solved | Status | Directory Link |\n"
        platform_md += "| :---: | :--- | :---: | :---: | :---: |\n"
        platform_md += platform_rows_str
        
        update_readme_section(os.path.join(platform_path, "README.md"), platform_md)

        grand_total += platform_total
        platform_summary_rows.append(f"| 📂 **[{platform}](./{platform}/)** | **{platform_total}** |")

    # بروزرسانی ریدمی اصلی (Root README.md)
    summary_rows_str = "\n".join(platform_summary_rows)
    root_md = f"""## 📊 Overall Progress Dashboard

| Platform | Total Solved |
| :--- | :---: |
{summary_rows_str}
| 🔥 **Grand Total** | **{grand_total}** |"""
    
    update_readme_section("README.md", root_md.strip())

if __name__ == "__main__":
    main()