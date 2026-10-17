"""Generates the static SVG sections of the profile README into ../assets/.

Run:  pip install fonttools brotli && python scripts/generate_assets.py
Edit the content below, re-run, commit the SVGs.
"""
import re
from math import cos, sin, radians
from deco import *

OUT = ROOT / "assets"
ICONS = ROOT / "scripts" / "icons"
W = 830


def save(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")
    print(f"{name:28s} {len(svg)/1024:6.1f} KB")


# ---------------------------------------------------------------- header
def header():
    H = 270
    d = Doc(W)
    name = "AMRUTHA PEKETI"
    ns = fit(name, "poster", 76, 720, 4)
    d.text(W / 2 + 2, 120, name, "poster", ns, IVORY, "middle", 4)
    role = "Full-Stack Engineer · RAG & LLM Systems · Hyperledger Fabric"
    tag = "AI that remembers. Blockchain that can't lie."
    d.text(W / 2, 178, role, "decob", fit(role, "decob", 20, 740, 1.5), GOLD, "middle", 1.5)
    d.text(W / 2, 216, tag, "deco", fit(tag, "deco", 18, 740, 1), IVORY, "middle", 1)
    save("header.svg", d.render(H, "Amrutha Peketi", f"{role}. {tag}"))


# ---------------------------------------------------------------- about
def about():
    d = Doc(W)
    d.title_bar(66, "ABOUT")
    para = ("Software engineer with hands-on experience across full-stack development, AI integrations, and "
            "blockchain. I build systems that hold up in production: retrieval-augmented incident resolution on "
            "Gemini, and Hyperledger Fabric supply chains that anyone can verify. B.Tech CSE student at SRKR "
            "Engineering College (IoT, Cybersecurity & Blockchain), graduating 2027.")
    y = 112
    for ln in wrap(para, "deco", 16, 730):
        d.text(50, y, ln, "deco", 16, IVORY)
        y += 27
    y += 14
    tiles = [("200+", "LeetCode problems solved"), ("8.82", "CGPA, B.Tech CSE"),
             ("2×", "First-place wins")]
    tw, gap = 230, 20
    for i, (num, lab) in enumerate(tiles):
        x = 50 + i * (tw + gap)
        d.raw(f'<rect x="{x}" y="{y}" width="{tw}" height="100" rx="10" fill="{NAVY2}" stroke="{GOLD_D}"/>')
        d.text(x + tw / 2, y + 44, num, "decob", 32, GOLD, "middle")
        for j, ln in enumerate(wrap(lab, "deco", 12.5, tw - 28, 0.8)):
            d.text(x + tw / 2, y + 68 + j * 16, ln, "deco", 12.5, MUTED, "middle", 0.8)
    H = y + 100 + 34
    save("about.svg", d.render(H, "About Amrutha Peketi", para))


# ---------------------------------------------------------------- experience
def experience():
    d = Doc(W)
    d.title_bar(66, "EXPERIENCE")
    jobs = [
        ("AI Intern", "Stikbook", "May 2026 - Jun 2026", [
            "Built ML recommendation models and pipelines with Python, Scikit-learn, and REST APIs in Agile sprints.",
            "Engineered data preprocessing pipelines and worked with cross-functional teams on production AI features.",
            "Evaluated model performance metrics to iterate on recommendation accuracy for end users."]),
        ("Freelance Frontend Engineer", "Startup", "Feb 2026 - May 2026", [
            "Built the marketplace frontend for 10+ service categories with Next.js, React, and Tailwind CSS, deployed on Vercel.",
            "Integrated secure REST APIs and managed state with an object-oriented component architecture.",
            "Shipped real-time search and interactive filters to speed up discovery and booking."]),
    ]
    y = 108
    d.raw(f'<line x1="62" y1="{y}" x2="62" y2="__END__" stroke="{GOLD_D}" stroke-width="1.5"/>')
    line_idx = len(d.parts) - 1
    for role, org, when, bullets in jobs:
        d.diamond(62, y - 5, 6, GOLD)
        d.text(86, y, role, "decob", 19, IVORY)
        y += 24
        d.text(86, y, f"{org}  ·  {when}", "deco", 13.5, GOLD, ls=1)
        y += 12
        for b in bullets:
            lines = wrap(b, "deco", 14.5, 690)
            y += 22
            d.diamond(92, y - 5, 2.6, GOLD_D)
            for j, ln in enumerate(lines):
                d.text(106, y, ln, "deco", 14.5, IVORY)
                if j < len(lines) - 1:
                    y += 21
        y += 40
    H = y - 6
    d.parts[line_idx] = d.parts[line_idx].replace("__END__", str(H - 40))
    save("experience.svg", d.render(H, "Experience", "AI Intern at Stikbook; Freelance Frontend Engineer"))


# ---------------------------------------------------------------- tech stack
def icon_inner(name):
    s = (ICONS / f"{name}.svg").read_text()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.sub(r"^.*?<svg[^>]*>", "", s, count=1, flags=re.S).rsplit("</svg>", 1)[0]
    inner = re.sub(r"<title>.*?</title>", "", inner)
    inner = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{name}-{m.group(1)}"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{name}-{m.group(1)})", inner)
    inner = re.sub(r'(xlink:href|href)="#([^"]+)"', lambda m: f'{m.group(1)}="#{name}-{m.group(2)}"', inner)
    return vb, inner


GROUPS = [
    ("Languages", [("java", "Java", None), ("python", "Python", None), ("c", "C", None),
                   ("cpp", "C++", None), ("postgresql", "SQL", None)]),
    ("Frontend", [("react", "React", None), ("nextjs", "Next.js", None), ("typescript", "TypeScript", None),
                  ("tailwind", "Tailwind", None), ("html", "HTML5", None), ("css", "CSS3", None)]),
    ("Backend & Data", [("node", "Node.js", None), ("express", "Express", None), ("mongodb", "MongoDB", None),
                        ("prisma", "Prisma", None), ("flask", "Flask", None)]),
    ("AI & Cloud", [("si_googlegemini", "Gemini", "#8E75B2"), ("aws", "AWS", None), ("docker", "Docker", None),
                    ("vercel", "Vercel", None), ("git", "Git", None), ("github", "GitHub", None)]),
    ("Blockchain & Security", [("hyperledger", "Hyperledger\nFabric", None), ("si_ipfs", "IPFS", "#2A9AA3"),
                               ("si_wireshark", "Wireshark", "#1679A7")]),
]


def stack():
    d = Doc(W)
    d.title_bar(66, "TECH STACK")
    y, x0, pitch = 104, 215, 88
    for gi, (gname, items) in enumerate(GROUPS):
        ty = y + gi * 96
        gl = wrap(gname.upper(), "decob", 12, 150, 2)
        for j, ln in enumerate(gl):
            d.text(50, ty + 28 + (j - (len(gl) - 1) / 2) * 16, ln, "decob", 12, GOLD, ls=2)
        for i, (icon, label, fill) in enumerate(items):
            x = x0 + i * pitch
            d.raw(f'<rect x="{x}" y="{ty}" width="46" height="46" rx="9" fill="#f8f5ec" stroke="{GOLD_D}"/>')
            if icon == "hyperledger":
                c = (x + 23, ty + 23)
                pts = " ".join(f"{c[0]+16*cos(radians(60*k+30)):.1f},{c[1]+16*sin(radians(60*k+30)):.1f}" for k in range(6))
                d.raw(f'<polygon points="{pts}" fill="none" stroke="{IVORY}" stroke-width="2.4"/>')
                d.text(c[0], c[1] + 5, "HF", "decob", 13, IVORY, "middle")
            else:
                vb, inner = icon_inner(icon)
                fa = f' fill="{fill}"' if fill else ""
                d.raw(f'<svg x="{x+9}" y="{ty+9}" width="28" height="28" viewBox="{vb}"{fa}>{inner}</svg>')
            for j, ln in enumerate(label.split("\n")):
                d.text(x + 23, ty + 62 + j * 13, ln, "deco", 11.5, MUTED, "middle")
    H = y + len(GROUPS) * 96 + 4
    save("stack.svg", d.render(H, "Tech stack",
         "Java, Python, C, C++, SQL; React, Next.js, TypeScript, Tailwind CSS, HTML5, CSS3; Node.js, Express, MongoDB, Prisma, Flask; Gemini, AWS, Docker, Vercel, Git, GitHub; Hyperledger Fabric, IPFS, Wireshark"))


# ---------------------------------------------------------------- achievements
ACH = [
    ("1ST", "Prakalp 2026  ·  Winner", "Ramachandra Engineering College, Eluru",
     "First place for an automated SOC threat-detection solution."),
    ("SIH", "Smart India Hackathon 2025  ·  National Finalist", "Smart India Hackathon",
     "Selected nationally for AyuSetu, a blockchain platform that records supply chain provenance end to end."),
    ("1ST", "E-Summit 2026  ·  Winner", "VIT Bhimavaram",
     "First place for innovation in decentralized system architectures."),
    ("PUB", "ICRCESM 2025  ·  Research publication", "International conference paper",
     "Published a research paper on food redistribution technology platforms."),
    ("EXE", "Executive Body Member  ·  2025 - Present", "Association of Computer Engineers",
     "Organized 5+ technical hackathons and workshops that engaged 200+ students across campus."),
]


def achievements():
    d = Doc(W)
    d.title_bar(66, "ACHIEVEMENTS")
    y = 96
    for badge, title, meta, desc in ACH:
        dl = wrap(desc, "deco", 14.5, 600)
        h = 24 + 20 + 20 + len(dl) * 21 + 12
        d.raw(f'<rect x="40" y="{y}" width="750" height="{h}" rx="10" fill="{NAVY2}" stroke="{GOLD_D}" stroke-opacity=".8"/>')
        cy = y + h / 2
        d.raw(f'<circle cx="94" cy="{cy}" r="29" fill="{GOLD}"/><circle cx="94" cy="{cy}" r="24" fill="none" stroke="{NAVY}" stroke-width="1.2"/>')
        d.text(94, cy + 5.5, badge, "decob", 15, NAVY, "middle", 1)
        ty = y + 32
        d.text(144, ty, title, "decob", 16, IVORY)
        d.text(144, ty + 20, meta, "deco", 12.5, GOLD, ls=1)
        for j, ln in enumerate(dl):
            d.text(144, ty + 44 + j * 21, ln, "deco", 14.5, IVORY)
        y += h + 12
    H = y + 22
    save("achievements.svg", d.render(H, "Achievements", " ".join(f"{t}. {m}. {s}" for _, t, m, s in ACH)))


# ---------------------------------------------------------------- projects
PROJECTS = [
    ("project-hindsight.svg", "Hindsight", "AI-powered operational memory and incident resolution platform", "2026",
     ["Gemini LLMs and RAG on Node.js, Prisma, and PostgreSQL automate real-time incident resolution as a production-grade cloud service.",
      "pgvector semantic search with cosine similarity across incident logs cut resolution time by 40%.",
      "Server-Sent Events stream generated answers live, secured with token-based JWT authentication."],
     ["Gemini", "RAG", "Node.js", "Prisma", "PostgreSQL", "pgvector", "SSE", "JWT"]),
    ("project-ayusetu.svg", "AyuSetu", "Blockchain supply chain traceability platform", "2025  ·  SIH national finalist",
     ["Hyperledger Fabric network across multi-org nodes records immutable, tamper-resistant supply chain provenance.",
      "Smart contracts enforce automated quality gates based on DNA tests and moisture thresholds.",
      "IPFS holds lab certificates off-chain, and cryptographic QR codes give consumers real-time provenance checks."],
     ["Hyperledger Fabric", "Smart Contracts", "IPFS", "Node.js", "QR provenance"]),
    ("project-homefinder.svg", "HomeFinder", "Full-stack rental and valuation platform", "2026",
     ["Multi-tier real estate platform on React, TypeScript, Node.js, Express, and MongoDB with JWT authentication.",
      "Flask microservice running an XGBoost regression model predicts dynamic rent at 80% accuracy.",
      "Responsive Tailwind CSS and shadcn/ui workflows over RESTful pipelines tuned for low latency."],
     ["React", "TypeScript", "Node.js", "MongoDB", "Flask", "XGBoost", "Tailwind"]),
]


def project(fname, name, sub, when, bullets, chips):
    d = Doc(W)
    d.text(44, 60, name, "decob", 27, IVORY)
    d.text(W - 44, 58, when, "deco", 13, MUTED, "end", 1)
    d.text(44, 86, sub.upper(), "deco", 12.5, GOLD, ls=2)
    d.raw(f'<line x1="44" y1="102" x2="{W-44}" y2="102" stroke="{GOLD_D}" stroke-opacity=".7"/>')
    y = 130
    for b in bullets:
        lines = wrap(b, "deco", 15, 700)
        d.diamond(50, y - 5, 3, GOLD)
        for ln in lines:
            d.text(66, y, ln, "deco", 15, IVORY)
            y += 22
        y += 6
    y += 6
    x = 44
    for c in chips:
        cw = width(c, "deco", 12.5, 0.5) + 22
        if x + cw > W - 44:
            x, y = 44, y + 34
        d.raw(f'<rect x="{x}" y="{y-17}" width="{cw:.1f}" height="26" rx="13" fill="none" stroke="{GOLD_D}"/>')
        d.text(x + cw / 2, y, c, "deco", 12.5, IVORY, "middle", 0.5)
        x += cw + 8
    y += 38
    label = "VIEW REPOSITORY"
    lw = width(label, "decob", 12, 2.5)
    d.text(W - 44 - 24, y, label, "decob", 12, GOLD, "end", 2.5)
    ax = W - 44 - 16
    d.raw(f'<path d="M{ax} {y-4} H{ax+14} M{ax+9} {y-9} L{ax+14} {y-4} L{ax+9} {y+1}" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    H = y + 30
    save(fname, d.render(H, name, f"{sub}. " + " ".join(bullets), frame=True))


def section(fname, label):
    d = Doc(W)
    d.title_bar(40, label, 6, 16)
    save(fname, d.render(62, label, label, frame=False))


# ---------------------------------------------------------------- contact
def contact():
    d = Doc(W)
    d.title_bar(66, "LET'S BUILD SOMETHING")
    d.text(W / 2, 114, "Open to SDE, Full Stack Developer, and AI Engineer roles.", "deco", 17, IVORY, "middle")
    d.text(W / 2, 148, "amruthapeketi05@gmail.com", "decob", 15, GOLD, "middle", 1.5)
    save("contact.svg", d.render(180, "Contact", "Open to SDE, Full Stack Developer, and AI Engineer roles. amruthapeketi05@gmail.com"))
    for label in ("LINKEDIN", "GITHUB", "LEETCODE", "EMAIL"):
        b = Doc(190)
        b.text(95, 30, label, "decob", 13, IVORY, "middle", 3)
        save(f"btn-{label.lower()}.svg", b.render(46, label, label, frame=False, bg=NAVY))


if __name__ == "__main__":
    header(); about(); experience(); stack()
    section("title-projects.svg", "FEATURED PROJECTS")
    for p in PROJECTS:
        project(*p)
    achievements(); contact()
