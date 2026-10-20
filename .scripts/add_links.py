#!/usr/bin/env python3
"""Add a Link column to every chapter's Sources table. URLs only where stated without guessing."""
import glob,re,collections,json
KNOWN=json.load(open("scripts/known_links.json"))
def link_for(src):
    m=re.search(r"arXiv[: ]?(\d{4}\.\d{4,5})",src)
    if m: return f"https://arxiv.org/abs/{m.group(1)}","official"
    m=re.search(r"labs/(ch\d\d-[\w-]+)/derive\.py",src)
    if m: return f"labs/{m.group(1)}/derive.py","repo"
    low=src.lower()
    if low.startswith("illustrative") or "none published" in low or "unmeasured" in low or low.startswith("this chapter"): return "—","none"
    for k,u,kind in KNOWN:
        if k.lower() in low: return u,kind
    if re.search(r"\(ch\d\d\)|^ch\d\d|chapters? \d\d",low): return "—","cross-ref"
    return "needs fetch","needs"
stats=collections.Counter(); needs=[]
for f in sorted(glob.glob("book/part*/ch*.md")):
    t=open(f).read(); ch=re.search(r"ch(\d\d)",f).group(1)
    if len(t.split())<800 or ch=="00": continue
    m=re.search(r"(## \d\d?\.9 Sources\n)(.*)",t,re.S); head,body=m.group(1),m.group(2); out=[]
    for line in body.splitlines():
        if line.startswith("| #") and "Link" not in line: line=line.rstrip("|").rstrip()+" | Link |"
        elif re.match(r"^\|---\|---\|---\|---\|---\|$",line): line="|---|---|---|---|---|---|"
        elif line.startswith("| ") and not line.startswith("| #") and not line.startswith("|---"):
            cells=[c.strip() for c in line.strip("|").split("|")]
            if len(cells) in (5,6):
                cells=cells[:5]; url,kind=link_for(cells[2]); stats[kind]+=1
                if kind=="needs": needs.append((ch,cells[2][:80]))
                line=f"| {' | '.join(cells)} | {url} |"
        out.append(line)
    open(f,'w').write(t[:m.start()]+head+"\n".join(out))
print(dict(stats)); print("needs fetch:",len(needs)); [print(" ",n) for n in needs]
