# -*- coding: utf-8 -*-
"""Canonical slug map for the site.

Spanish lives at the document root and keeps its own slugs; English, French
and Italian sit in /en/, /fr/ and /it/ on localised filenames. Every page in
the site is identified here by a language-neutral key, and the four columns
give the filename that key resolves to in each language.

This is the single source of truth for:
  * the hreflang cluster on every page (key -> four URLs)
  * the language switcher
  * sitemap generation (tools/build-sitemap.py)
  * the 301 redirects from the old Spanish-slug paths (tools/build-htaccess.py)

Adding a page means adding one row here and creating the four files.
"""

LANGS = ("es", "en", "fr", "it")

# key: (es, en, fr, it)
SLUGS = {
    "home":            ("index.html", "index.html", "index.html", "index.html"),
    "about":           ("quienes-somos.html", "about.html", "a-propos.html", "chi-sono.html"),
    "spare":           ("spare-method.html", "spare-method.html", "methode-spare.html", "metodo-spare.html"),
    "conditions":      ("que-tratamos.html", "conditions-we-treat.html", "pathologies-traitees.html", "patologie-trattate.html"),
    "surgery":         ("cirugia.html", "surgical-procedures.html", "chirurgie.html", "chirurgia.html"),
    "faq":             ("preguntas-frecuentes.html", "faq.html", "questions-frequentes.html", "domande-frequenti.html"),
    "contact":         ("contacto.html", "contact.html", "contact.html", "contatti.html"),
    "results":         ("resultados.html", "results.html", "resultats.html", "risultati.html"),
    "tightrope":       ("tecnica-tightrope.html", "tightrope-technique.html", "technique-tightrope.html", "tecnica-tightrope.html"),
    "legal":           ("aviso-legal.html", "legal-notice.html", "mentions-legales.html", "note-legali.html"),
    "privacy":         ("politica-privacidad.html", "privacy-policy.html", "politique-confidentialite.html", "informativa-privacy.html"),
    "cookies":         ("politica-cookies.html", "cookie-policy.html", "politique-cookies.html", "informativa-cookie.html"),

    # podiatry services cluster
    "services":        ("servicios.html", "services.html", "services.html", "servizi.html"),
    "cryo":            ("crioterapia.html", "cryotherapy.html", "cryotherapie.html", "crioterapia.html"),
    "physio":          ("fisioterapia-podologica.html", "podiatric-physiotherapy.html", "physiotherapie-podologique.html", "fisioterapia-podologica.html"),
    "laser":           ("laser-terapia.html", "laser-therapy.html", "laserotherapie.html", "laser-terapia.html"),
    "infrared":        ("luz-infrarroja.html", "infrared-light.html", "lumiere-infrarouge.html", "luce-infrarossa.html"),
    "pedicure":        ("pedicura.html", "pedicure.html", "pedicure.html", "pedicure.html"),
    "chiropody-delux": ("quiropodia-delux.html", "delux-chiropody.html", "chiropodie-delux.html", "podologia-delux.html"),
    "chiropody-aesth": ("quiropodia-estetica.html", "aesthetic-chiropody.html", "chiropodie-esthetique.html", "podologia-estetica.html"),
    "tens":            ("tens.html", "tens.html", "tens.html", "tens.html"),
    "nail-fungus":     ("tratamiento-hongos-unas.html", "nail-fungus-treatment.html", "traitement-mycose-ongles.html", "trattamento-micosi-unghie.html"),
    "warts":           ("tratamiento-verrugas.html", "wart-treatment.html", "traitement-verrues.html", "trattamento-verruche.html"),

    # per-condition pages (Task 3.1), children of "conditions"
    "c-bunion":        ("cirugia-juanete-barcelona.html", "bunion-surgery-barcelona.html", "chirurgie-hallux-valgus-barcelone.html", "chirurgia-alluce-valgo-barcellona.html"),
    "c-bunionette":    ("juanete-de-sastre.html", "bunionette-tailors-bunion.html", "bunionette-oignon-de-tailleur.html", "bunionette-alluce-del-sarto.html"),
    "c-hammertoe":     ("dedos-en-martillo.html", "hammer-toe.html", "orteils-en-marteau.html", "dita-a-martello.html"),
    "c-morton":        ("neuroma-de-morton.html", "mortons-neuroma.html", "nevrome-de-morton.html", "neuroma-di-morton.html"),
    "c-metatarsalgia": ("metatarsalgia.html", "metatarsalgia.html", "metatarsalgie.html", "metatarsalgia.html"),
    "c-brachy":        ("braquimetatarsia.html", "brachymetatarsia.html", "brachymetatarsie.html", "brachimetatarsia.html"),
}

CONDITION_KEYS = [k for k in SLUGS if k.startswith("c-")]

BASE = "https://www.drfabiodangelo.com/"


def slug(key, lang):
    return SLUGS[key][LANGS.index(lang)]


def folder(lang):
    return "" if lang == "es" else lang + "/"


def path(key, lang):
    """Repo-relative file path, e.g. 'en/about.html'."""
    return folder(lang) + slug(key, lang)


def url(key, lang):
    """Canonical absolute URL; homepages are directory URLs."""
    s = slug(key, lang)
    return BASE + folder(lang) + ("" if s == "index.html" else s)


def key_for(path_):
    """Reverse lookup: repo-relative path -> key. Raises on unknown paths."""
    lang = path_.split("/")[0] if "/" in path_ else "es"
    name = path_.split("/")[-1]
    for k in SLUGS:
        if slug(k, lang) == name:
            return k
    raise KeyError(path_)
