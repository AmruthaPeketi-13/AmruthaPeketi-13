import base64, io, html
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset

ROOT = Path(__file__).resolve().parent.parent
FD = ROOT / "assets" / "fonts"
FONTS = {
    "poster": dict(family="Abril Fatface", file="poster.woff2", weight=400),
    "hand": dict(family="Nothing You Could Do", file="hand.woff2", weight=400),
    "deco": dict(family="Josefin Sans", file="deco400.woff2", weight=400),
    "decob": dict(family="Josefin Sans", file="deco700.woff2", weight=700),
}
NAVY, NAVY2 = "#ffffff", "#f8f5ec"      # page background, soft card tint
GOLD, GOLD_D = "#96701a", "#e3d8b6"      # accent, light border
IVORY, MUTED = "#1b2a41", "#5f6b7a"      # main text, secondary text

_cache = {}


def _font(key):
    if key not in _cache:
        f = TTFont(FD / FONTS[key]["file"])
        _cache[key] = (f, f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _cache[key]


def width(text, key, size, ls=0):
    f, cmap, hmtx, upm = _font(key)
    w = 0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            print(f"warning: no glyph for {ch!r} in {key}")
            w += upm * 0.5
        else:
            w += hmtx[g][0]
    return w / upm * size + ls * len(text)


def wrap(text, key, size, maxw, ls=0):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if width(t, key, size, ls) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(text, key, size, maxw, ls=0):
    while width(text, key, size, ls) > maxw:
        size -= 1
    return size


def subset_b64(key, chars):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.notdef_outline = False
    opts.name_IDs = []
    f = TTFont(FD / FONTS[key]["file"])
    s = subset.Subsetter(opts)
    s.populate(text=chars + " ")
    s.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff2"
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def esc(t):
    return html.escape(t, quote=False)


class Doc:
    def __init__(self, w):
        self.w, self.parts, self.used = w, [], {}

    def raw(self, s):
        self.parts.append(s)

    def text(self, x, y, t, key, size, fill, anchor="start", ls=0, op=None):
        self.used.setdefault(key, set()).update(t)
        fam, wt = FONTS[key]["family"], FONTS[key]["weight"]
        extra = f' letter-spacing="{ls}"' if ls else ""
        extra += f' fill-opacity="{op}"' if op else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="\'{fam}\', serif" font-size="{size}" '
            f'font-weight="{wt}" fill="{fill}" text-anchor="{anchor}"{extra}>{esc(t)}</text>'
        )

    def diamond(self, cx, cy, r, fill=GOLD):
        self.raw(f'<path d="M{cx} {cy-r} L{cx+r} {cy} L{cx} {cy+r} L{cx-r} {cy} Z" fill="{fill}"/>')

    def brackets(self, h):
        w = self.w
        out = []
        for cx, cy, sx, sy in [(14, 14, 1, 1), (w - 14, 14, -1, 1), (14, h - 14, 1, -1), (w - 14, h - 14, -1, -1)]:
            out.append(f'<path d="M{cx} {cy+sy*34} L{cx} {cy} L{cx+sx*34} {cy}" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
            out.append(f'<path d="M{cx+sx*7} {cy+sy*24} L{cx+sx*7} {cy+sy*7} L{cx+sx*24} {cy+sy*7}" fill="none" stroke="{GOLD}" stroke-width="1" stroke-opacity=".7"/>')
        return "".join(out)

    def title_bar(self, y, label, ls=5, size=15):
        w = self.w
        tw = width(label, "decob", size, ls)
        x = (w - tw) / 2 + ls / 2
        self.text(w / 2 + ls / 2, y, label, "decob", size, GOLD, "middle", ls)
        self.diamond(x - 16, y - 5, 3.5)
        self.diamond(x + tw + 10, y - 5, 3.5)

    def render(self, h, title, desc, frame=True, bg=NAVY):
        css = []
        for key, chars in self.used.items():
            b64 = subset_b64(key, "".join(sorted(chars)))
            fam, wt = FONTS[key]["family"], FONTS[key]["weight"]
            css.append(
                f"@font-face{{font-family:'{fam}';font-weight:{wt};"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
            )
        head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{h}" viewBox="0 0 {self.w} {h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
            f"<style>{''.join(css)}</style>"
            f'<rect x="0.6" y="0.6" width="{self.w-1.2}" height="{h-1.2}" rx="14" fill="{bg}" stroke="{GOLD_D}" stroke-width="1.2"/>'
        )
        br = ""
        return head + "".join(self.parts) + br + "</svg>"
