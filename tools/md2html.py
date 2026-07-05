#!/usr/bin/env python3
"""docs-template/ の Markdown 正本から、規格書スタイルのHTML(人向け配布物)を生成する。

使い方:
  python3 tools/md2html.py docs-template/standards/governance.md \
      -o docs-template/standards/governance.html \
      --docno STD-AIDEV-003 --rev 1.0 --date 2026-07-04 --lead "承認用の配布文書"

規程④(フォーマット規則): HTMLは生成物。編集は必ずmd側で行い、本スクリプトで再生成する。
対応するMarkdownの範囲: 見出し(h1-h3)・段落・箇条書き・表・引用・コードフェンス・
太字・インラインコード・リンク・生HTML(<details>等)・水平線。
"""
import argparse
import html
import re
from pathlib import Path

CSS = """
:root {
  --paper: #F4F5F1; --card: #FFFFFF; --ink: #1C2622; --muted: #5D6B63;
  --line: #D9DED6; --line-strong: #2A3630;
  --red: #C43A2E; --green: #1E7A46; --blue: #2B5FAB;
  --serif: "Hiragino Mincho ProN", "Yu Mincho", "YuMincho", "Noto Serif JP", serif;
  --sans: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic", "YuGothic", "Noto Sans JP", sans-serif;
  --mono: "SF Mono", "SFMono-Regular", Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root {
    --paper: #141917; --card: #1D2421; --ink: #E8ECE7; --muted: #96A49B;
    --line: #303B35; --line-strong: #C6D0C9;
    --red: #E06A5C; --green: #4DAE7C; --blue: #6E9BD8;
  }
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: var(--sans); font-size: 14.5px; line-height: 2.0; color: var(--ink); background: var(--paper); }
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
.page { max-width: 860px; margin: 0 auto; padding: 36px 28px 72px; }
.crumb { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; font-family: var(--mono); font-size: 11px; letter-spacing: .06em; color: var(--muted); margin-bottom: 34px; }
.crumb a { color: var(--muted); }
.crumb a:hover { color: var(--blue); }
.eyebrow { font-family: var(--mono); font-size: 11px; letter-spacing: .22em; color: var(--muted); margin-bottom: 14px; }
h1 { font-family: var(--serif); font-weight: 600; font-size: clamp(24px, 4vw, 34px); letter-spacing: .05em; line-height: 1.4; }
.doc-lead { margin-top: 10px; color: var(--muted); font-size: 14.5px; }
.titleblock { margin: 26px 0 40px; display: grid; grid-template-columns: repeat(5, minmax(0,1fr)); border: 1.5px solid var(--line-strong); background: var(--card); }
.titleblock .cell { padding: 9px 14px 7px; border-left: 1px solid var(--line); min-width: 0; }
.titleblock .cell:first-child { border-left: none; }
.titleblock .k { display: block; font-family: var(--mono); font-size: 9.5px; letter-spacing: .16em; color: var(--muted); margin-bottom: 2px; }
.titleblock .v { font-size: 12px; font-weight: 600; overflow-wrap: anywhere; }
.titleblock .v.mono { font-family: var(--mono); font-weight: 500; }
@media (max-width: 760px) {
  .titleblock { grid-template-columns: 1fr 1fr; }
  .titleblock .cell { border-top: 1px solid var(--line); }
  .titleblock .cell:nth-child(-n+2) { border-top: none; }
  .titleblock .cell:nth-child(odd) { border-left: none; }
  .titleblock .cell:nth-child(even) { border-left: 1px solid var(--line); }
}
main h2 { font-family: var(--serif); font-weight: 600; font-size: 21px; letter-spacing: .06em; margin: 52px 0 16px; padding-bottom: 8px; border-bottom: 1px solid var(--line); }
main h3 { font-size: 15px; font-weight: 700; margin: 30px 0 10px; }
main p { margin: 12px 0; }
main ul { margin: 12px 0; padding-left: 1.5em; }
main li { margin: 5px 0; }
main blockquote { border-left: 3px solid var(--green); background: var(--card); padding: 8px 16px; margin: 12px 0; font-size: 13px; color: var(--muted); }
main .tblwrap { overflow-x: auto; border: 1px solid var(--line); background: var(--card); margin: 14px 0; }
main table { border-collapse: collapse; width: 100%; }
main th { text-align: left; font-family: var(--mono); font-weight: 500; font-size: 10.5px; letter-spacing: .12em; color: var(--muted); padding: 10px 16px 8px; border-bottom: 1.5px solid var(--line-strong); white-space: nowrap; }
main td { padding: 9px 16px; border-bottom: 1px solid var(--line); font-size: 13.5px; line-height: 1.9; vertical-align: top; }
main tr:last-child td { border-bottom: none; }
main pre { background: var(--card); border: 1px solid var(--line); padding: 14px 18px; overflow-x: auto; font-family: var(--mono); font-size: 12.5px; line-height: 1.8; margin: 14px 0; }
main code { font-family: var(--mono); font-size: .92em; background: var(--card); border: 1px solid var(--line); border-radius: 3px; padding: 0 5px; }
main pre code { border: none; padding: 0; background: none; }
main hr { border: none; border-top: 1px solid var(--line); margin: 32px 0; }
main details { background: var(--card); border: 1px solid var(--line); padding: 10px 16px; margin: 14px 0; }
main summary { cursor: pointer; font-weight: 600; font-size: 13px; }
footer { margin-top: 64px; padding-top: 18px; border-top: 1.5px solid var(--line-strong); font-family: var(--mono); font-size: 10.5px; color: var(--muted); letter-spacing: .06em; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
""".strip()


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    return s


def render_table(rows: list[str]) -> str:
    parsed = []
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        parsed.append(cells)
    has_header = len(parsed) >= 2 and all(re.fullmatch(r":?-{3,}:?", c) for c in parsed[1])
    out = ['<div class="tblwrap"><table>']
    body = parsed
    if has_header:
        out.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in parsed[0]) + "</tr></thead>")
        body = parsed[2:]
    out.append("<tbody>")
    for cells in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def render_body(md: str) -> tuple[str, str]:
    """(title, body_html) を返す。最初の h1 をタイトルとして抜き出す。"""
    lines = md.splitlines()
    out: list[str] = []
    title = ""
    para: list[str] = []
    i = 0

    def flush_para():
        nonlocal para
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_para()
            fence: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                fence.append(lines[i])
                i += 1
            out.append("<pre><code>" + html.escape("\n".join(fence)) + "</code></pre>")
            i += 1
            continue
        if stripped.startswith("|"):
            flush_para()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(render_table(rows))
            continue
        if stripped.startswith("# ") and not title:
            title = stripped[2:].strip()
            i += 1
            continue
        if stripped.startswith("### "):
            flush_para()
            out.append(f"<h3>{inline(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            flush_para()
            out.append(f"<h2>{inline(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            flush_para()
            out.append(f"<h2>{inline(stripped[2:])}</h2>")
        elif stripped.startswith("> "):
            flush_para()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote>{inline(' '.join(q for q in quote if q))}</blockquote>")
            continue
        elif stripped.startswith("- "):
            flush_para()
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ul>")
            continue
        elif re.fullmatch(r"-{3,}|\*{3,}", stripped):
            flush_para()
            out.append("<hr>")
        elif stripped.startswith("<"):
            flush_para()
            out.append(line)
        elif stripped == "":
            flush_para()
        else:
            para.append(stripped)
        i += 1

    flush_para()
    return title, "\n".join(out)


PAGE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<div class="page">
<nav class="crumb"><a href="{back}">← ポータル</a><span>{contact}</span></nav>
<header>
  <div class="eyebrow">{eyebrow}</div>
  <h1>{title}</h1>
  <p class="doc-lead">{lead}</p>
  <div class="titleblock" role="table" aria-label="文書管理情報">
    <div class="cell"><span class="k">文書番号</span><span class="v mono">{docno}</span></div>
    <div class="cell"><span class="k">版</span><span class="v mono">{rev}</span></div>
    <div class="cell"><span class="k">発行日</span><span class="v mono">{date}</span></div>
    <div class="cell"><span class="k">承認</span><span class="v">{approval}</span></div>
    <div class="cell"><span class="k">正本</span><span class="v mono">{source}</span></div>
  </div>
</header>
<main>
{body}
</main>
<footer>
  <span>GENERATED: tools/md2html.py ・ 編集は正本({source})側で行う</span>
  <span>{docno} ・ REV {rev} ・ {date}</span>
</footer>
</div>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="変換するMarkdownファイル(正本)")
    ap.add_argument("-o", "--output", required=True, help="出力するHTMLファイル(生成物)")
    ap.add_argument("--docno", default="STD-AIDEV-XXX", help="文書番号")
    ap.add_argument("--rev", default="1.0", help="版")
    ap.add_argument("--date", required=True, help="発行日(YYYY-MM-DD)")
    ap.add_argument("--approval", default="main へのマージ", help="承認方法")
    ap.add_argument("--lead", default="", help="タイトル下の1行説明")
    ap.add_argument("--eyebrow", default="INTERNAL IT STANDARD ・ GENERATED DOCUMENT", help="最上部のラベル")
    ap.add_argument("--back", default="index.html", help="ポータルへ戻るリンク先")
    ap.add_argument("--contact", default="問い合わせ: 情報システム(m_nakagawa@smilior.com)", help="問い合わせ先の表示")
    args = ap.parse_args()

    src = Path(args.input)
    title, body = render_body(src.read_text(encoding="utf-8"))
    page = PAGE.format(
        title=html.escape(title or src.stem),
        css=CSS,
        eyebrow=html.escape(args.eyebrow),
        lead=html.escape(args.lead),
        docno=html.escape(args.docno),
        rev=html.escape(args.rev),
        date=html.escape(args.date),
        approval=html.escape(args.approval),
        source=html.escape(src.name),
        back=html.escape(args.back),
        contact=html.escape(args.contact),
        body=body,
    )
    Path(args.output).write_text(page, encoding="utf-8")
    print(f"generated: {args.output} (from {args.input})")


if __name__ == "__main__":
    main()
