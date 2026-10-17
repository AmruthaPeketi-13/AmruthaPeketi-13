"""Builds assets/activity.svg: a deco-styled contribution graph from your public GitHub data.

Run:  pip install fonttools brotli && python scripts/generate_activity.py YOUR_USERNAME
No token needed. It reads GitHub's public contributions fragment for the user.
"""
import re, sys, datetime as dt
from urllib.request import Request, urlopen
from deco import *

USER = sys.argv[1] if len(sys.argv) > 1 else "AmruthaPeketi-13"
W = 830
LEVELS = ["#e9e4d3", "#f0d98a", "#d9a93a", "#b07a12", "#6b4a08"]


def fetch(user):
    req = Request(f"https://github.com/users/{user}/contributions", headers={"User-Agent": "Mozilla/5.0"})
    return urlopen(req, timeout=30).read().decode("utf-8", "ignore")


def parse(page):
    cells = re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*?id="([^"]+)"[^>]*?data-level="(\d)"', page)
    tips = {}
    for tid, txt in re.findall(r'<tool-tip[^>]*?for="([^"]+)"[^>]*>([^<]*)</tool-tip>', page):
        m = re.match(r"(\d+) contribution", txt.strip())
        tips[tid] = int(m.group(1)) if m else 0
    days = [(dt.date.fromisoformat(d), int(lv), tips.get(i, 0)) for d, i, lv in cells]
    return sorted(days)


def streaks(days):
    best = cur = 0
    for _, _, c in days:
        cur = cur + 1 if c > 0 else 0
        best = max(best, cur)
    # current streak: count back from the latest day (a zero today does not break it)
    run, seq = 0, list(days)
    if seq and seq[-1][2] == 0:
        seq = seq[:-1]
    for _, _, c in reversed(seq):
        if c > 0:
            run += 1
        else:
            break
    return best, run


def build(days, user):
    d = Doc(W)
    d.title_bar(66, "CONTRIBUTION ACTIVITY")
    total = sum(c for _, _, c in days)
    active = sum(1 for _, _, c in days if c)
    best, current = streaks(days)
    pitch, cell, x0, y0 = 13.6, 11, 76, 122
    rp, ch = 22, 18
    first = days[0][0]
    sunday = first - dt.timedelta(days=(first.weekday() + 1) % 7)
    seen_month = None
    for day, lv, c in days:
        col = (day - sunday).days // 7
        row = (day.weekday() + 1) % 7
        x, y = x0 + col * pitch, y0 + row * rp
        d.raw(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{ch}" rx="3" fill="{LEVELS[lv]}"/>')
        if day.day <= 7 and day.month != seen_month and row == 0 or (seen_month is None):
            seen_month = day.month
            d.text(x, y0 - 10, day.strftime("%b").upper(), "deco", 10.5, MUTED, ls=1)
    for r, lab in ((1, "MON"), (3, "WED"), (5, "FRI")):
        d.text(x0 - 10, y0 + r * rp + 13, lab, "deco", 9.5, MUTED, "end", 1)
    ly = y0 + 7 * rp + 18
    d.text(W - 50 - 5 * 15 - 40, ly + 9, "LESS", "deco", 10, MUTED, "end", 1.5)
    for i, col in enumerate(LEVELS):
        d.raw(f'<rect x="{W-50-5*15-30+i*15}" y="{ly}" width="11" height="11" rx="2.5" fill="{col}"/>')
    d.text(W - 50 - 5 * 15 + 52, ly + 9, "MORE", "deco", 10, MUTED, "start", 1.5)
    d.text(50, ly + 9, f"github.com/{user}  ·  updated {dt.date.today().isoformat()}", "deco", 10.5, MUTED, ls=1)
    H = ly + 40
    return d.render(H, "Contribution activity", f"{total} contributions in the last year, {active} active days, longest streak {best} days.")


if __name__ == "__main__":
    days = parse(fetch(USER))
    if not days:
        sys.exit("No contribution data found; the page layout may have changed.")
    out = ROOT / "assets" / "activity.svg"
    out.write_text(build(days, USER), encoding="utf-8")
    print("wrote", out, f"({len(days)} days)")
