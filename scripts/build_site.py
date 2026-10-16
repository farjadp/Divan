#!/usr/bin/env python3
"""Build the Divan guide site into site/ from the Markdown that already exists.

Single source of truth: README*.md and docs/*.md. Nothing on the site is written twice.

    python3 scripts/build_site.py            # writes site/
    python3 scripts/build_site.py --out dist # elsewhere

Requires: pip install markdown
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover
    sys.exit("python-markdown is required: pip install markdown")

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/farjadp/Divan"
BLOB = REPO_URL + "/blob/main/"

# --------------------------------------------------------------------------- content model

# README H2 sections, in the order they appear. The English README has one extra section
# ("Repository layout"); the translations do not.
SECTION_KEYS_EN = ["problem", "team", "loop", "install", "facts", "fd", "why", "limits",
                   "layout", "contributing", "about", "licence"]
SECTION_KEYS_TR = ["problem", "team", "loop", "install", "facts", "fd", "why", "limits",
                   "contributing", "about", "licence"]

LANGS = {
    #  code: (html lang, dir, README file, url prefix)
    "en": ("en", "ltr", "README.md", ""),
    "fa": ("fa", "rtl", "README.fa.md", "fa/"),
    "ar": ("ar", "rtl", "README.ar.md", "ar/"),
    "zh": ("zh-CN", "ltr", "README.zh-CN.md", "zh/"),
}

# Pages in reading order. kind: "home" | "readme" (one README section) | "doc" (English file)
PAGES = [
    ("index", "home", None),
    ("install", "readme", "install"),
    ("team", "readme", "team"),
    ("loop", "readme", "loop"),
    ("three-facts", "readme", "facts"),
    ("feature-definition", "readme", "fd"),
    ("method", "doc", "docs/method.md"),
    ("adapting", "doc", "docs/adapting.md"),
    ("case-study", "doc", "docs/case-studies/taghvim.md"),
    ("limits", "readme", "limits"),
    ("layout", "readme", "layout"),
    ("contributing", "readme", "contributing"),
    ("about", "readme", "about"),
]
GROUPS = [
    ("start", ["index", "install"]),
    ("method", ["team", "loop", "three-facts", "feature-definition", "method"]),
    ("reference", ["adapting", "case-study", "limits", "layout", "contributing", "about"]),
]

UI = {
    "en": {
        "name": "Divan", "start": "Start", "method": "Method", "reference": "Reference",
        "onpage": "On this page", "prev": "Previous", "next": "Next", "menu": "Contents",
        "edit": "Edit this page on GitHub", "english_only": "This page is available in English only.",
        "tagline": "A product team of AI agents, built around one human who decides.",
        "sub": "Seven specialised roles for Claude Code. Three gates where you approve. Agents never release.",
        "cards": [("New here?", "Start with the problem Divan solves and the team it gives you.", "team"),
                  ("Have a repo?", "Adapt the kit to an existing project without breaking its rules.", "adapting"),
                  ("Want proof?", "Read the first real adaptation, on a live product.", "case-study")],
        "footer": "MIT licence. Divan is independent and not affiliated with Anthropic.",
        "labels": {"index": "Why Divan", "install": "Install", "team": "The team", "loop": "The loop",
                   "three-facts": "Three facts", "feature-definition": "Feature definition",
                   "method": "The method", "adapting": "Adapting to a repo",
                   "case-study": "Case study: Taghvim", "limits": "Honest limits",
                   "layout": "Repository layout", "contributing": "Contributing", "about": "About the author"},
    },
    "fa": {
        "name": "دیوان", "start": "شروع", "method": "روش", "reference": "مرجع",
        "onpage": "در این صفحه", "prev": "قبلی", "next": "بعدی", "menu": "فهرست",
        "edit": "ویرایش این صفحه در گیت‌هاب", "english_only": "این صفحه فقط به انگلیسی موجود است.",
        "tagline": "یک تیم محصول از ایجنت‌های هوش مصنوعی، ساخته‌شده حول یک انسان که تصمیم می‌گیرد.",
        "sub": "هفت نقش تخصصی برای Claude Code. سه دروازه که تو تأیید می‌کنی. ایجنت‌ها هرگز منتشر نمی‌کنند.",
        "cards": [("تازه‌واردی؟", "از مسئله‌ای که دیوان حل می‌کند و تیمی که به تو می‌دهد شروع کن.", "team"),
                  ("پروژهٔ موجود داری؟", "کیت را با پروژهٔ جاافتاده تطبیق بده، بدون شکستن قانون‌هایش.", "adapting"),
                  ("مدرک می‌خواهی؟", "اولین تطبیق واقعی را روی یک محصول زنده بخوان.", "case-study")],
        "footer": "مجوز MIT. دیوان پروژه‌ای مستقل است و به Anthropic وابسته نیست.",
        "labels": {"index": "چرا دیوان", "install": "نصب", "team": "تیم", "loop": "چرخهٔ کار",
                   "three-facts": "سه واقعیت", "feature-definition": "تعریف فیچر",
                   "method": "روش (انگلیسی)", "adapting": "تطبیق با پروژهٔ موجود (انگلیسی)",
                   "case-study": "نمونهٔ واقعی: تقویم (انگلیسی)", "limits": "محدودیت‌ها",
                   "layout": "ساختار مخزن (انگلیسی)", "contributing": "مشارکت", "about": "دربارهٔ سازنده"},
    },
    "ar": {
        "name": "ديوان", "start": "ابدأ", "method": "المنهج", "reference": "مراجع",
        "onpage": "في هذه الصفحة", "prev": "السابق", "next": "التالي", "menu": "المحتويات",
        "edit": "حرّر هذه الصفحة على GitHub", "english_only": "هذه الصفحة متاحة بالإنجليزية فقط.",
        "tagline": "فريق منتج من وكلاء الذكاء الاصطناعي، مبنيّ حول إنسان واحد يتخذ القرار.",
        "sub": "سبعة أدوار متخصصة لـ Claude Code. ثلاث بوابات توافق فيها أنت. الوكلاء لا يُطلقون أبداً.",
        "cards": [("جديد هنا؟", "ابدأ بالمشكلة التي يحلّها ديوان والفريق الذي يمنحك إياه.", "team"),
                  ("لديك مستودع؟", "كيّف العُدّة مع مشروع قائم دون خرق قواعده.", "adapting"),
                  ("تريد دليلاً؟", "اقرأ أول تكييف حقيقي على منتج حيّ.", "case-study")],
        "footer": "رخصة MIT. ديوان مشروع مستقل وغير تابع لـ Anthropic.",
        "labels": {"index": "لماذا ديوان", "install": "التثبيت", "team": "الفريق", "loop": "الدورة",
                   "three-facts": "ثلاث حقائق", "feature-definition": "تعريف الميزات",
                   "method": "المنهج (إنجليزي)", "adapting": "التكييف مع مستودع قائم (إنجليزي)",
                   "case-study": "دراسة حالة: تقويم (إنجليزي)", "limits": "حدود صريحة",
                   "layout": "بنية المستودع (إنجليزي)", "contributing": "المساهمة", "about": "عن المؤلف"},
    },
    "zh": {
        "name": "Divan", "start": "开始", "method": "方法", "reference": "参考",
        "onpage": "本页内容", "prev": "上一页", "next": "下一页", "menu": "目录",
        "edit": "在 GitHub 上编辑此页", "english_only": "此页面目前仅有英文版。",
        "tagline": "由 AI 智能体组成的产品团队，围绕一位做决定的人而构建。",
        "sub": "为 Claude Code 提供七个专门角色。三道由你审批的关卡。智能体从不发布。",
        "cards": [("初次了解？", "从 Divan 要解决的问题和它给你的团队开始。", "team"),
                  ("已有代码库？", "在不破坏现有规则的前提下，把工具包适配到现有项目。", "adapting"),
                  ("想看证据？", "阅读在一个真实产品上的首次适配。", "case-study")],
        "footer": "MIT 许可证。Divan 是独立项目，与 Anthropic 无关。",
        "labels": {"index": "为什么是 Divan", "install": "安装", "team": "团队", "loop": "功能循环",
                   "three-facts": "三个事实", "feature-definition": "功能定义",
                   "method": "方法（英文）", "adapting": "适配现有代码库（英文）",
                   "case-study": "案例：Taghvim（英文）", "limits": "坦诚的局限",
                   "layout": "仓库结构（英文）", "contributing": "参与贡献", "about": "关于作者"},
    },
}
LANG_NAMES = {"en": "English", "fa": "فارسی", "ar": "العربية", "zh": "中文"}

# --------------------------------------------------------------------------- markdown helpers

H2 = re.compile(r"^## (.+?)\s*$", re.M)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def split_readme(text: str, keys: list) -> tuple:
    """Return (preamble, {key: (title, body)})."""
    text = re.sub(r"^</?div[^>]*>\s*$", "", text, flags=re.M)   # the RTL wrapper
    matches = list(H2.finditer(text))
    preamble = text[: matches[0].start()] if matches else text
    sections = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end].strip("\n")
        if i < len(keys):
            sections[keys[i]] = (m.group(1).strip(), body)
    return preamble, sections


def status_quote(preamble: str) -> str:
    lines = [l for l in preamble.splitlines()]
    out, inside = [], False
    for l in lines:
        if l.startswith(">"):
            out.append(l)
            inside = True
        elif inside:
            break
    return "\n".join(out)


def first_fence(md: str) -> str:
    m = re.search(r"```\w*\n(.*?)```", md, re.S)
    return m.group(1).strip() if m else ""


def rewrite_links(md: str, root: str, lang_prefix: str) -> str:
    """Point repo-relative links at site pages (same language) or GitHub."""
    page = lambda slug: root + lang_prefix + slug + "/"
    repl = {
        "docs/method.md": page("method"),
        "docs/adapting.md": page("adapting"),
        "docs/case-studies/taghvim.md": page("case-study"),
        "case-studies/taghvim.md": page("case-study"),
        "CONTRIBUTING.md": BLOB + "CONTRIBUTING.md",
        "LICENSE": BLOB + "LICENSE",
        "assets/NOTICE-lucide.txt": BLOB + "assets/NOTICE-lucide.txt",
        "#about": page("about"),
        "#about-the-author": page("about"),
    }
    def sub(m):
        target = m.group(1)
        base, _, frag = target.partition("#")
        if target in repl:
            return "](" + repl[target] + ")"
        if base in repl:
            return "](" + repl[base] + "#" + frag + ")"
        return m.group(0)
    md = re.sub(r"\]\(([^)\s]+)\)", sub, md)
    md = md.replace('src="assets/', 'src="' + root + 'assets/')
    return md


def render(md: str) -> tuple:
    """Return (html, toc_tokens)."""
    engine = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"],
                               extension_configs={"toc": {"toc_depth": "2-3"}})
    out = engine.convert(md)
    return out, engine.toc_tokens


# --------------------------------------------------------------------------- html

def esc(s: str) -> str:
    return html.escape(s, quote=True)


def toc_html(tokens: list, ui: dict) -> str:
    items = []
    for t in tokens:
        items.append('<li><a href="#%s">%s</a></li>' % (t["id"], esc(t["name"])))
        for c in t.get("children", []):
            items.append('<li class="sub"><a href="#%s">%s</a></li>' % (c["id"], esc(c["name"])))
    if len(items) < 2:
        return ""
    return '<nav class="toc" aria-label="%s"><p class="eyebrow">%s</p><ul>%s</ul></nav>' % (
        esc(ui["onpage"]), esc(ui["onpage"]), "".join(items))


def nav_html(lang: str, current: str, root: str) -> str:
    ui = UI[lang]
    prefix = LANGS[lang][3]
    parts = []
    for gkey, slugs in GROUPS:
        links = []
        for s in slugs:
            href = root + prefix + ("" if s == "index" else s + "/")
            cls = ' class="on" aria-current="page"' if s == current else ""
            links.append('<li><a href="%s"%s>%s</a></li>' % (href, cls, esc(ui["labels"][s])))
        parts.append('<section><h2 class="eyebrow">%s</h2><ul>%s</ul></section>' % (esc(ui[gkey]), "".join(links)))
    return "".join(parts)


def lang_switch(current_lang: str, slug: str, root: str) -> str:
    out = []
    for code in LANGS:
        prefix = LANGS[code][3]
        href = root + prefix + ("" if slug == "index" else slug + "/")
        on = ' aria-current="true"' if code == current_lang else ""
        out.append('<a href="%s" lang="%s" hreflang="%s"%s>%s</a>' % (href, LANGS[code][0], LANGS[code][0], on, LANG_NAMES[code]))
    return "".join(out)


def page_html(lang: str, slug: str, title: str, body: str, toc: str, sources: list, depth: int,
              english_only: bool, description: str) -> str:
    ui = UI[lang]
    html_lang, direction, _, prefix = LANGS[lang]
    root = "../" * depth
    order = [p[0] for p in PAGES]
    i = order.index(slug)
    prev_slug = order[i - 1] if i > 0 else None
    next_slug = order[i + 1] if i + 1 < len(order) else None

    def link(s):
        return root + prefix + ("" if s == "index" else s + "/")

    pager = '<nav class="pager" aria-label="pager">'
    pager += ('<a class="prev" href="%s"><span class="eyebrow">%s</span>%s</a>' % (link(prev_slug), esc(ui["prev"]), esc(ui["labels"][prev_slug]))) if prev_slug else "<span></span>"
    pager += ('<a class="next" href="%s"><span class="eyebrow">%s</span>%s</a>' % (link(next_slug), esc(ui["next"]), esc(ui["labels"][next_slug]))) if next_slug else "<span></span>"
    pager += "</nav>"

    edit = "".join('<a href="%s%s">%s</a>' % (BLOB, s, esc(ui["edit"]) if n == 0 else esc(s)) for n, s in enumerate(sources))
    note = '<p class="note" lang="%s" dir="%s">%s</p>' % (html_lang, direction, esc(ui["english_only"])) if english_only else ""
    body_attrs = ' lang="en" dir="ltr"' if english_only and lang != "en" else ""
    fonts = "IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500"
    if lang in ("fa", "ar"):
        fonts += "&family=Vazirmatn:wght@400;500;700"
    if lang == "zh":
        fonts += "&family=Noto+Sans+SC:wght@400;500;700"

    full_title = ui["name"] if slug == "index" else "%s · %s" % (title, ui["name"])
    return """<!doctype html>
<html lang="{html_lang}" dir="{dir}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://farjadp.github.io/Divan/assets/banner.svg">
<meta property="og:type" content="website">
<link rel="icon" href="{root}assets/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={fonts}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="mast">
  <a class="brand" href="{home}"><img src="{root}assets/logo.svg" alt="" width="28" height="28">{name}<span class="version">v0.1 · early</span></a>
  <div class="mast-right">
    <nav class="langs" aria-label="Language">{langs}</nav>
    <a class="gh" href="{repo}">GitHub</a>
  </div>
</header>
<div class="shell">
  <aside class="side">
    <details class="drawer" open>
      <summary>{menu}</summary>
      <nav class="chapters" aria-label="{menu}">{chapters}</nav>
    </details>
  </aside>
  <main id="content" class="main">
    {note}
    <article class="prose"{body_attrs}>
      <h1>{title}</h1>
      {body}
    </article>
    {pager}
    <p class="edit">{edit}</p>
  </main>
  <aside class="rail">{toc}</aside>
</div>
<footer class="foot"><span>{footer}</span><a href="https://farjadp.info">farjadp.info</a></footer>
<script>(function(){{var d=document.querySelector(".drawer");if(d&&!matchMedia("(min-width: 780px)").matches)d.removeAttribute("open");}})();</script>
</body>
</html>
""".format(html_lang=html_lang, dir=direction, full_title=esc(full_title), description=esc(description),
           root=root, fonts=fonts, home=root + prefix, name=esc(ui["name"]), langs=lang_switch(lang, slug, root),
           repo=REPO_URL, menu=esc(ui["menu"]), chapters=nav_html(lang, slug, root), note=note,
           body_attrs=body_attrs, title=esc(title), body=body, pager=pager, edit=edit, toc=toc,
           footer=esc(ui["footer"]))


# --------------------------------------------------------------------------- build

def build(out_dir: Path) -> int:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    shutil.copytree(ROOT / "assets", out_dir / "assets")
    shutil.copy(ROOT / "site-src" / "style.css", out_dir / "style.css")
    shutil.copy(ROOT / "site-src" / "404.html", out_dir / "404.html")

    readmes = {}
    for code, (_, _, fname, _) in LANGS.items():
        keys = SECTION_KEYS_EN if code == "en" else SECTION_KEYS_TR
        readmes[code] = split_readme(read(fname), keys)
    en_pre, en_sections = readmes["en"]

    count = 0
    for code, (_, _, fname, prefix) in LANGS.items():
        ui = UI[code]
        preamble, sections = readmes[code]
        for slug, kind, src in PAGES:
            depth = (1 if prefix else 0) + (0 if slug == "index" else 1)
            root = "../" * depth
            english_only = False
            sources = []
            if kind == "home":
                title = ui["tagline"]
                install_cmd = first_fence(sections["install"][1])
                cards = "".join(
                    '<a class="card" href="%s"><b>%s</b><span>%s</span></a>' % (root + prefix + target + "/", esc(h), esc(t))
                    for h, t, target in ui["cards"])
                md = status_quote(preamble) + "\n\n"
                md += "```bash\n" + install_cmd + "\n```\n\n"
                md += '<div class="cards">' + cards + "</div>\n\n"
                md += "## %s\n\n%s\n\n## %s\n\n%s\n" % (sections["problem"][0], sections["problem"][1],
                                                        sections["why"][0], sections["why"][1])
                md = '<p class="lead">%s</p>\n\n' % esc(ui["sub"]) + md
                description = ui["sub"]
                sources = [fname]
            elif kind == "readme":
                if src in sections:
                    title, md = sections[src]
                    sources = [fname]
                else:  # only the English README has it
                    title, md = en_sections[src]
                    english_only = code != "en"
                    sources = ["README.md"]
                description = ui["tagline"]
            else:  # doc
                text = read(src)
                m = re.match(r"# (.+)\n", text)
                title = m.group(1).strip() if m else slug
                md = text[m.end():] if m else text
                english_only = code != "en"
                sources = [src]
                description = title + " · " + UI["en"]["tagline"]
            md = rewrite_links(md, root, prefix)
            body, toc_tokens = render(md)
            toc = toc_html(toc_tokens, ui)
            page = page_html(code, slug, title, body, toc, sources, depth, english_only, description)
            target = out_dir / prefix / ("" if slug == "index" else slug) / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(page, encoding="utf-8")
            count += 1
    return count


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "site"), help="output directory (default: site/)")
    args = ap.parse_args()
    out = Path(args.out).resolve()
    n = build(out)
    print("built %d pages into %s" % (n, out.relative_to(ROOT) if out.is_relative_to(ROOT) else out))


if __name__ == "__main__":
    main()
