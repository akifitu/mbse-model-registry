"""Export model registry outputs."""

from __future__ import annotations

from csv import DictWriter
from html import escape
from pathlib import Path
from typing import Iterable, Mapping

from .analysis import RegistryResult


def export_reports(result: RegistryResult, export_dir: Path | str) -> None:
    """Write report artifacts."""
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    _write_text(export_path / "model-summary.md", _render_summary_markdown(result))
    _write_csv(export_path / "model-catalog.csv", result.package_rows)
    _write_csv(export_path / "repo-coverage.csv", result.coverage_rows)
    _write_text(export_path / "model-dashboard.html", _render_dashboard_html(result))


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _write_csv(path: Path, rows: Iterable[Mapping[str, str]]) -> None:
    row_list = list(rows)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = DictWriter(handle, fieldnames=list(row_list[0].keys()))
        writer.writeheader()
        writer.writerows(row_list)


def _render_summary_markdown(result: RegistryResult) -> str:
    summary = result.summary
    packages = "\n".join(
        f"- {row['title']} ({row['domain']}) | repositories: {row['linked_repositories']}"
        for row in result.package_rows
    ) or "- None"
    errors = "\n".join(f"- {item}" for item in result.errors) or "- None"
    warnings = "\n".join(f"- {item}" for item in result.warnings) or "- None"
    return (
        "# Model Registry Summary\n\n"
        f"- Model packages: {summary['package_count']}\n"
        f"- Domains: {summary['domain_count']}\n"
        f"- Linked repositories: {summary['linked_repository_count']}\n"
        f"- Unique view types: {summary['view_type_count']}\n"
        f"- Errors: {summary['error_count']}\n"
        f"- Warnings: {summary['warning_count']}\n\n"
        "## Package Catalog\n\n"
        f"{packages}\n\n"
        "## Errors\n\n"
        f"{errors}\n\n"
        "## Warnings\n\n"
        f"{warnings}\n"
    )


def _render_dashboard_html(result: RegistryResult) -> str:
    summary = result.summary
    cards = [
        ("Packages", str(summary["package_count"])),
        ("Domains", str(summary["domain_count"])),
        ("Repositories", str(summary["linked_repository_count"])),
        ("View Types", str(summary["view_type_count"])),
    ]
    card_html = "\n".join(
        f"<article class=\"card\"><span>{escape(label)}</span><strong>{escape(value)}</strong></article>"
        for label, value in cards
    )
    package_table = _render_table(
        result.package_rows,
        ["id", "title", "domain", "requirement_count", "interface_count"],
        "No model packages available.",
    )
    coverage_table = _render_table(
        result.coverage_rows,
        ["repository", "package_count", "view_count"],
        "No repository coverage available.",
    )
    warnings = "".join(f"<li>{escape(item)}</li>" for item in (result.warnings or ["None"]))
    errors = "".join(f"<li>{escape(item)}</li>" for item in (result.errors or ["None"]))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MBSE Model Registry</title>
  <style>
    :root {{
      --bg: #f0f3f7;
      --panel: rgba(255,255,255,0.9);
      --ink: #1f2a3d;
      --muted: #617089;
      --accent: #2563eb;
      --line: rgba(31,42,61,0.12);
      --shadow: 0 18px 40px rgba(31, 42, 61, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background: linear-gradient(180deg, #f4f7fb, #e7edf5);
    }}
    main {{
      width: min(1100px, calc(100% - 28px));
      margin: 0 auto;
      padding: 28px 0 54px;
    }}
    .hero, section, .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
      border-radius: 24px;
    }}
    .hero {{
      padding: 28px;
      background: linear-gradient(135deg, rgba(37,99,235,0.95), rgba(30,64,175,0.95));
      color: #f7fbff;
    }}
    h1, h2 {{
      margin: 0 0 12px;
      font-family: "Georgia", serif;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin: 18px 0;
    }}
    .card {{
      padding: 20px;
      min-height: 116px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .card span {{
      color: var(--muted);
      text-transform: uppercase;
      font-size: 0.84rem;
      letter-spacing: 0.07em;
    }}
    .card strong {{
      color: var(--accent);
      font-size: 1.9rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 18px;
    }}
    section {{
      padding: 22px;
      overflow: hidden;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.94rem;
    }}
    th, td {{
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      text-transform: uppercase;
      font-size: 0.8rem;
      letter-spacing: 0.06em;
    }}
    ul {{
      margin: 0;
      padding-left: 20px;
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>MBSE Model Registry</h1>
      <p>Architecture-view and model-package catalog for a multi-repository systems engineering portfolio.</p>
    </section>
    <div class="metrics">{card_html}</div>
    <div class="grid">
      <section>
        <h2>Model Packages</h2>
        {package_table}
      </section>
      <section>
        <h2>Repository Coverage</h2>
        {coverage_table}
      </section>
      <section>
        <h2>Warnings</h2>
        <ul>{warnings}</ul>
      </section>
      <section>
        <h2>Errors</h2>
        <ul>{errors}</ul>
      </section>
    </div>
  </main>
</body>
</html>
"""


def _render_table(rows: Iterable[Mapping[str, str]], columns: list[str], empty_message: str) -> str:
    row_list = list(rows)
    if not row_list:
        return f"<p>{escape(empty_message)}</p>"
    header_html = "".join(f"<th>{escape(column.replace('_', ' '))}</th>" for column in columns)
    body_html = []
    for row in row_list:
        body_html.append(
            "<tr>" + "".join(f"<td>{escape(str(row.get(column, '')))}</td>" for column in columns) + "</tr>"
        )
    return f"<table><thead><tr>{header_html}</tr></thead><tbody>{''.join(body_html)}</tbody></table>"
