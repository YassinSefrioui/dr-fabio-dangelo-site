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
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import slugs as S  # noqa: E402

BASE = S.BASE
LANGS = S.LANGS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lastmod(key, lang):
    return date.fromtimestamp(
        os.path.getmtime(os.path.join(ROOT, S.path(key, lang)))).isoformat()


def child_sitemap(lang):
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for key in S.SLUGS:
        out.append("  <url>")
        out.append("    <loc>%s</loc>" % S.url(key, lang))
        out.append("    <lastmod>%s</lastmod>" % lastmod(key, lang))
        for alt in LANGS:
            out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                       % (alt, S.url(key, alt)))
        out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>'
                   % S.url(key, "es"))
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
    # The slug map is the source of truth; every file it names must exist, and
    # no .html file may exist that the map does not name — otherwise a page is
    # either missing or silently absent from the sitemap and hreflang cluster.
    expected = {S.path(k, L) for k in S.SLUGS for L in LANGS}
    actual = set()
    for lang in LANGS:
        d = os.path.join(ROOT, S.folder(lang).rstrip("/") or ".")
        actual |= {S.folder(lang) + f for f in os.listdir(d) if f.endswith(".html")}
    if expected != actual:
        for p in sorted(expected - actual):
            print("in slugs.py but missing on disk: %s" % p, file=sys.stderr)
        for p in sorted(actual - expected):
            print("on disk but not in slugs.py: %s" % p, file=sys.stderr)
        return 1

    total = 0
    newest = date.min
    for lang in LANGS:
        with open(os.path.join(ROOT, "sitemap-%s.xml" % lang), "w", encoding="utf-8") as fh:
            fh.write(child_sitemap(lang))
        total += len(S.SLUGS)
        newest = max(newest, max(date.fromisoformat(lastmod(k, lang)) for k in S.SLUGS))
        print("sitemap-%s.xml — %d URLs" % (lang, len(S.SLUGS)))

    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(index_sitemap(newest.isoformat()))
    print("sitemap.xml — 4 child sitemaps, %d URLs total" % total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
