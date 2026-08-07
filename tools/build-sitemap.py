#!/usr/bin/env python3
"""Regenerate sitemap.xml and the four per-language child sitemaps.

Run from the document root after adding, removing or editing pages:

    python3 tools/build-sitemap.py

Every URL is emitted in canonical form (https://www. host, directory URL for
the homepages) with a <lastmod> taken from the file's modification time and
the full five-tag hreflang cluster as <xhtml:link> alternates, mirroring the
on-page cluster.
"""

import os
import re
import sys
from datetime import date, datetime

BASE = "https://www.drfabiodangelo.com/"
LANGS = ("es", "en", "fr", "it")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def folder(lang):
    """Directory a language lives in, relative to the document root."""
    return "" if lang == "es" else lang + "/"


def url_for(lang, page):
    """Canonical URL: homepages are directory URLs, never .../index.html."""
    return BASE + folder(lang) + ("" if page == "index.html" else page)


def lastmod(lang, page):
    path = os.path.join(ROOT, folder(lang), page)
    return date.fromtimestamp(os.path.getmtime(path)).isoformat()


def pages_for(lang):
    d = os.path.join(ROOT, folder(lang).rstrip("/") or ".")
    return sorted(f for f in os.listdir(d) if f.endswith(".html"))


def child_sitemap(lang, pages):
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for page in pages:
        out.append("  <url>")
        out.append("    <loc>%s</loc>" % url_for(lang, page))
        out.append("    <lastmod>%s</lastmod>" % lastmod(lang, page))
        for alt in LANGS:
            out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                       % (alt, url_for(alt, page)))
        out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>'
                   % url_for("es", page))
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def index_sitemap(stamp):
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for lang in LANGS:
        out.append("  <sitemap>")
        out.append("    <loc>%ssitemap-%s.xml</loc>" % (BASE, lang))
        out.append("    <lastmod>%s</lastmod>" % stamp)
        out.append("  </sitemap>")
    out.append("</sitemapindex>")
    return "\n".join(out) + "\n"


def main():
    # Every language folder must hold the same page set, or the hreflang
    # alternates written below would point at URLs that do not exist.
    sets = {lang: set(pages_for(lang)) for lang in LANGS}
    if len({frozenset(v) for v in sets.values()}) != 1:
        for lang in LANGS:
            extra = sets[lang] - set.intersection(*sets.values())
            if extra:
                print("%s has pages no other language has: %s"
                      % (lang, ", ".join(sorted(extra))), file=sys.stderr)
        return 1

    total = 0
    newest = date.min
    for lang in LANGS:
        pages = pages_for(lang)
        path = os.path.join(ROOT, "sitemap-%s.xml" % lang)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(child_sitemap(lang, pages))
        total += len(pages)
        newest = max(newest, max(date.fromisoformat(lastmod(lang, p)) for p in pages))
        print("sitemap-%s.xml — %d URLs" % (lang, len(pages)))

    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(index_sitemap(newest.isoformat()))
    print("sitemap.xml — 4 child sitemaps, %d URLs total" % total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
