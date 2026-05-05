"""MkDocs hook: inject a "recent updates" section into the homepage."""

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
import subprocess
import re


def _git_log(commits: int = 15) -> str:
    try:
        return subprocess.check_output(
            [
                "git",
                "log",
                f"--max-count={commits}",
                "--oneline",
                "--name-only",
                "--date=short",
                '--format=@@@%ad@@@%s@@@%H@@@',
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.SubprocessError, FileNotFoundError):
        return ""


def _path_to_url(path: str) -> str:
    """Convert a docs/ file path to a relative MkDocs URL from the homepage."""
    if not path.startswith("docs/"):
        return ""
    url = path.removeprefix("docs/")
    if url.endswith(".md"):
        url = url.removesuffix(".md")
        if url == "index":
            return "./"
        elif url.endswith("/index"):
            url = url.removesuffix("/index") or "."
        return f"./{url}/"
    # Non-md files served as-is at site root
    return f"./{url}"


def _parse_git_log(raw: str) -> list[dict]:
    """Parse git log output into a list of {date, subject, sha, files} dicts.

    The custom format looks like:
        @@@2026-05-05@@@subject here@@@abclongsha@@@
        docs/foo.md
        docs/bar/baz.md

    """
    if not raw.strip():
        return []

    commits = []
    blocks = re.split(r"\n(?=@@@)", raw.strip())

    for block in blocks:
        lines = block.strip().split("\n")
        header = lines[0]
        m = re.match(r"^@@@(.+?)@@@(.+?)@@@(.+?)@@@$", header)
        if not m:
            continue

        date, subject, sha = m.group(1), m.group(2).strip(), m.group(3)

        # Gather docs/ files (excluding admin/)
        files = []
        for fpath in lines[1:]:
            fpath = fpath.strip()
            if not fpath or not fpath.startswith("docs/"):
                continue
            if fpath.startswith("docs/admin/"):
                continue
            url = _path_to_url(fpath)
            if url:
                files.append((fpath.removeprefix("docs/"), url))

        if files:
            commits.append({
                "date": date,
                "subject": subject,
                "sha": sha,
                "files": files,
            })

    return commits


def _build_updates_html(commits: list[dict]) -> str:
    """Build pre-rendered HTML for the recent-updates section."""
    if not commits:
        return '<p class="updates-empty">暂无更新记录。</p>'

    GITHUB = "https://github.com/biostatcn/clinical-ai-stat"
    parts = ['<div class="updates-list">']

    for c in commits:
        commit_url = f"{GITHUB}/commit/{c['sha']}"
        parts.append(f'<h3>{c["date"]}</h3>')
        parts.append("<ul>")
        parts.append(
            f'<li><strong><a href="{commit_url}">{c["subject"]}</a></strong><ul>'
        )

        max_files = 5
        for name, url in c["files"][:max_files]:
            parts.append(f'<li><a href="{url}"><code>{name}</code></a></li>')

        remaining = len(c["files"]) - max_files
        if remaining > 0:
            parts.append(f"<li>… 还有 {remaining} 个文件</li>")

        parts.append("</ul></li>")
        parts.append("</ul>")

    parts.append("</div>")
    return "\n".join(parts)


def on_page_markdown(
    markdown: str,
    page: Page,
    config: MkDocsConfig,
    **kwargs,
) -> str:
    """Inject recent-updates section into the homepage."""
    if page.file.src_uri != "index.md":
        return markdown

    placeholder = "<!-- recent-updates -->"
    if placeholder not in markdown:
        return markdown

    raw = _git_log(commits=15)
    commits = _parse_git_log(raw)
    updates = _build_updates_html(commits)

    section = (
        "\n\n---\n\n"
        "## 最近更新\n\n"
        f"{updates}\n\n"
        "---\n"
    )

    return markdown.replace(placeholder, section)
