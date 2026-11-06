"""Builds index.html (the playable, offline file) from src/orbita-viva.html.

The source file is the version published as a Claude artifact: it has no
<!doctype>, <head> or <body> and loads three.js from a CDN. This script adds
the page skeleton (charset, viewport for phones) and inlines vendor/three.min.js
so the game works offline and on GitHub Pages.

Usage: python3 tools/build_standalone.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "orbita-viva.html"
THREE = ROOT / "vendor" / "three.min.js"
OUT = ROOT / "index.html"
CDN_TAG = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
HEAD = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<meta name="theme-color" content="#0b1226">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
"""


def main():
    html = SRC.read_text(encoding="utf-8")
    three = THREE.read_text(encoding="utf-8").replace("</script", "<\\/script")
    if html.count(CDN_TAG) != 1:
        raise SystemExit("No encontré la etiqueta de three.js en el archivo fuente")
    html = html.replace(CDN_TAG, "<script>/* three.js r128 · MIT License · https://threejs.org */\n" + three + "\n</script>")
    html = html.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    html = HEAD + html
    end_style = html.index("</style>") + len("</style>")
    html = html[:end_style] + "\n</head>\n<body>" + html[end_style:] + "\n</body>\n</html>\n"
    OUT.write_text(html, encoding="utf-8")
    print(f"index.html: {len(html) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
