#!/usr/bin/env python3
"""Switch an app's landing page from "Notify me" to the Google Play badge, once the app is in production.

Run from the repository root:  python3 _build/play_release.py filmdesk   (or filmtrail)
It does the same as the manual steps in PHAT-HANH-GOOGLE-PLAY.md: in the app's template it deletes every
[NOTIFY ME n/N] block and removes the comment lines around every [GOOGLE PLAY n/N] block, does the same for the
app's status chip on the home page, then rebuilds the site. Check the result with git diff before committing.
"""
import pathlib, re, runpy, sys

REPO = pathlib.Path(__file__).resolve().parent.parent
TARGETS = {
    # app: (template, marker number of its status chip in _build/home/home.html)
    "filmdesk": ("_build/filmdesk/template.html", "1/2"),
    "filmtrail": ("_build/filmtrail/landing.html", "2/2"),
}
NOTIFY = r"^[ \t]*<!-- \[NOTIFY ME {n}[^\]]*\][^\n]*\n.*?^[ \t]*<!-- \[/NOTIFY ME {n}[^\]]*\][^\n]*\n"
PLAY_OPEN = r"^[ \t]*<!-- \[GOOGLE PLAY {n}[^\]]*\][^\n]*\n"
PLAY_CLOSE = r"^[ \t]*\[/GOOGLE PLAY {n}[^\]]*\][^\n]*\n"


def switch(path, n=r"\d+/\d+"):
    """n: regex for the marker number; the default matches every block in the file."""
    p = REPO / path
    t = p.read_text(encoding="utf-8")
    before = t
    for pattern in (NOTIFY, PLAY_OPEN, PLAY_CLOSE):
        t = re.sub(pattern.format(n=n), "", t, flags=re.S | re.M)
    if t == before:
        sys.exit(f"{path}: no markers found (already switched?)")
    p.write_text(t, encoding="utf-8")
    print("switched", path)


if len(sys.argv) != 2 or sys.argv[1] not in TARGETS:
    sys.exit("usage: python3 _build/play_release.py filmdesk|filmtrail")
template, home_marker = TARGETS[sys.argv[1]]
site = (REPO / "_build" / "site.json").read_text(encoding="utf-8")
if "DIEN_PACKAGE" in site and sys.argv[1] == "filmtrail":
    sys.exit("_build/site.json: fill in filmtrail_play first")
missing = [c for c in ("en", "de", "fr", "zh-tw", "ja", "ko", "vi") if not (REPO / "assets" / "play-badge" / f"{c}.png").exists()]
if missing:
    sys.exit("assets/play-badge/: missing " + ", ".join(f"{c}.png" for c in missing) + " (see PHAT-HANH-GOOGLE-PLAY.md, step 1)")
switch(template)
switch("_build/home/home.html", re.escape(home_marker))
runpy.run_path(str(REPO / "_build" / "build_all.py"), run_name="__main__")
