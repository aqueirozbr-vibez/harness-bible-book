#!/usr/bin/env python3
"""Deterministic checks for a Harness Bible chapter. Exit 1 on any failure.

Checks: the nine layer headings exist in order; numbers in body text carry a
citation or tier tag on the same line; banned phrases; word count within the
budget given by --min/--max; at least two mermaid blocks; a Layer 9 table.
"""
import re, sys, argparse

LAYERS = ["Intuition","Mechanism","Worked numbers","Measurement","Failure","The frontier","Industrial application","Decision aids","Sources"]
BANNED = ["essentially","basically","simply put","rapidly evolving","it is important to note","in this chapter we will","!"]
CITE = re.compile(r"\([^()]*(?:\d{4}|illustrative|vendor|primary|analyst|derived|open|practitioner|scenario)[^()]*\)", re.I)
NUM = re.compile(r"(?<![\w./-])\d[\d,]*(?:\.\d+)?\s?(?:%|×|x|ms|s|GB|KB|MB|TB|K|M|B|pp|tokens?|USD|\$)?(?![\w/-])")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("--min",type=int,default=5000); ap.add_argument("--max",type=int,default=12000); ap.add_argument("--prose",action="store_true",help="prose-only chapter: no layers, mermaid, or sources table required; no numbered/boxed content allowed")
    a=ap.parse_args(); text=open(a.path,encoding="utf-8").read(); fails=[]
    if a.prose:
        body=re.sub(r"```.*?```","",text,flags=re.S); wc=len(body.split())
        if wc<a.min or wc>a.max: fails.append(f"word count {wc} outside [{a.min},{a.max}]")
        low=body.lower()
        for b in BANNED:
            if b in low: fails.append(f"banned phrase: {b!r}")
        if re.search(r"^\s*(\||\d+\.\s|[-*]\s|#{2,}\s)", body, re.M): fails.append("prose-only chapter contains a table, list, or subsection heading")
        if "```mermaid" in text: fails.append("prose-only chapter contains a diagram")
        if not re.search(r"^\*Sources", body, re.M): fails.append("closing *Sources* note missing")
        print(("FAIL — "+"; ".join(fails)) if fails else f"PASS — {wc} words (prose-only)"); sys.exit(1 if fails else 0)
    # layers in order
    pos=-1
    for L in LAYERS:
        m=re.search(r"^##\s+\S+\s+"+re.escape(L), text, re.M)
        if not m: fails.append(f"missing layer heading: {L}"); continue
        if m.start()<pos: fails.append(f"layer out of order: {L}")
        pos=m.start()
    # word count excluding code blocks and tables
    body=re.sub(r"```.*?```","",text,flags=re.S); body=re.sub(r"\$\$.*?\$\$","",body,flags=re.S); body=re.sub(r"\$(?!\d)[^$\n]*?\$(?!\d)","",body); body=re.sub(r"^\|.*$","",body,flags=re.M)
    wc=len(body.split()); tbl=len(" ".join(re.findall(r"^\|.*$", re.sub(r"```.*?```","",text,flags=re.S), flags=re.M)).split()); wc_total=wc+tbl
    if wc_total<a.min or wc_total>a.max: fails.append(f"word count {wc_total} (prose {wc} + tables {tbl}) outside [{a.min},{a.max}]")
    # banned phrases
    low=body.lower()
    for b in BANNED:
        if b in low: fails.append(f"banned phrase: {b!r}")
    # mermaid
    if len(re.findall(r"```mermaid",text))<2: fails.append("fewer than two mermaid diagrams")
    # sources table
    if not re.search(r"\|\s*#\s*\|\s*Claim", text): fails.append("Layer 9 sources table missing")
    # uncited numbers in prose (skip headings, tables, code, and figure/table numbering)
    paras=re.split(r"\n\s*\n", body)
    for i,para in enumerate(paras,1):
        s=para.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("*"): continue
        s2=re.sub(r"(Figure|Table|Lab|Layer|Chapter|Section|ch|Part|Equation|Eq\.)\s*\d+(\.\d+)?","",s)
        s2=re.sub(r"\b\d{1,2}\.\d{1,2}\b","",s2)  # section refs
        s2=re.sub(r"\$[^$]*\$","",s2)  # inline math
        if NUM.search(s2) and not CITE.search(s2):
            fails.append(f"paragraph {i}: number without source/tier: {s[:90]}")
    if fails:
        print("\n".join(fails)); print(f"\nFAIL — {len(fails)} issue(s), {wc_total} words"); sys.exit(1)
    print(f"PASS — {wc_total} words (prose {wc} + tables {tbl}; code excluded)"); sys.exit(0)
if __name__=="__main__": main()
