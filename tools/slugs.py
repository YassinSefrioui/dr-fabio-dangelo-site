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

import os

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

    # /recursos/ resources section (Task 3.4). Slugs carry their own directory.
    "r-index":         ("recursos/index.html", "resources/index.html", "ressources/index.html", "risorse/index.html"),
    "r-tightrope":     ("recursos/tecnica-tightrope-endoscopica.html", "resources/endoscopic-tightrope-technique.html", "ressources/technique-tightrope-endoscopique.html", "risorse/tecnica-tightrope-endoscopica.html"),
    "r-recovery":      ("recursos/recuperacion-cirugia-juanete-semana-a-semana.html", "resources/bunion-surgery-recovery-week-by-week.html", "ressources/recuperation-hallux-valgus-semaine-par-semaine.html", "risorse/recupero-alluce-valgo-settimana-per-settimana.html"),
    "r-percutaneous":  ("recursos/percutanea-o-endoscopica.html", "resources/percutaneous-or-endoscopic-correction.html", "ressources/percutanee-ou-endoscopique.html", "risorse/percutanea-o-endoscopica.html"),
    "r-recurrence":    ("recursos/por-que-vuelve-el-juanete.html", "resources/why-bunions-come-back.html", "ressources/pourquoi-l-hallux-valgus-recidive.html", "risorse/perche-l-alluce-valgo-recidiva.html"),
    "r-running":       ("recursos/volver-a-correr-tras-cirugia-del-antepie.html", "resources/returning-to-running-after-forefoot-surgery.html", "ressources/reprendre-la-course-apres-chirurgie-avant-pied.html", "risorse/tornare-a-correre-dopo-chirurgia-avampiede.html"),
    "r-revision":      ("recursos/cirugia-de-revision-del-juanete.html", "resources/what-revision-bunion-surgery-involves.html", "ressources/chirurgie-de-revision-hallux-valgus.html", "risorse/chirurgia-di-revisione-alluce-valgo.html"),
}

CONDITION_KEYS = [k for k in SLUGS if k.startswith("c-")]
RESOURCE_KEYS = [k for k in SLUGS if k.startswith("r-") and k != "r-index"]

BASE = "https://www.drfabiodangelo.com/"


def slug(key, lang):
    return SLUGS[key][LANGS.index(lang)]


def folder(lang):
    return "" if lang == "es" else lang + "/"


def path(key, lang):
    """Repo-relative file path, e.g. 'en/about.html'."""
    return folder(lang) + slug(key, lang)


def url(key, lang):
    """Canonical absolute URL; any index.html resolves to its directory URL."""
    s = slug(key, lang)
    if s.endswith("index.html"):
        s = s[:-len("index.html")]
    return BASE + folder(lang) + s


def href(from_key, to_key, lang):
    """Relative href from one page to another within the same language."""
    src = os.path.dirname(path(from_key, lang))
    dst = path(to_key, lang)
    rel = os.path.relpath(dst, src or ".")
    return rel[:-len("index.html")] or "./" if rel.endswith("index.html") else rel


def key_for(path_):
    """Reverse lookup: repo-relative path -> key. Raises on unknown paths."""
    for lang in LANGS:
        f = folder(lang)
        if not path_.startswith(f):
            continue
        rest = path_[len(f):]
        for k in SLUGS:
            if slug(k, lang) == rest:
                return k
    raise KeyError(path_)
