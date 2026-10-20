#!/usr/bin/env python3
"""Pipeline status for every chapter: registry / draft / lint / verify / redteam / lab."""
import os, re, subprocess, glob, sys
rows=[]
for path in sorted(glob.glob("book/part*/ch*.md")):
    n=re.search(r"ch(\d\d)",path).group(1); title=open(path).readline().strip("# \n")
    txt=open(path).read(); drafted=len(txt.split())>800
    reg=os.path.exists(f"book/registry/ch{n}.md") and "not started" not in open(f"book/registry/ch{n}.md").read()
    ver=os.path.exists(f"book/registry/ch{n}-verify.md"); red=os.path.exists(f"book/registry/ch{n}-redteam.md")
    labs=glob.glob(f"labs/ch{n}-*/results/run.txt"); lab="ok" if labs and "exit=0" in open(labs[0]).read() or (labs and ("REPRODUCED" in open(labs[0]).read() or "written" in open(labs[0]).read())) else ("—" if not labs else "?")
    lint="—"
    if drafted:
        floor="6000" if "/part2/" in path else "4500"
        args=[sys.executable,"scripts/lint_chapter.py",path,"--min",floor,"--max","12000"]
        if "/part0/" in path: args=[sys.executable,"scripts/lint_chapter.py",path,"--prose","--min","3000","--max","4000"]
        r=subprocess.run(args,capture_output=True,text=True); lint="pass" if r.returncode==0 else "FAIL"
    rows.append((n,title[:44],"y" if reg else "—","y" if drafted else "—",lint,"y" if ver else "—","y" if red else "—",lab))
print(f"{'ch':>2} {'title':44} {'reg':>3} {'draft':>5} {'lint':>4} {'ver':>3} {'red':>3} {'lab':>3}")
for r in rows: print(f"{r[0]:>2} {r[1]:44} {r[2]:>3} {r[3]:>5} {r[4]:>4} {r[5]:>3} {r[6]:>3} {r[7]:>3}")
done=sum(1 for r in rows if r[3]=="y"); print(f"\n{done}/{len(rows)} drafted; {sum(1 for r in rows if r[5]=='y')} verified; {sum(1 for r in rows if r[7]=='ok')} labs reproducing")

import subprocess,sys,os
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),'update_map.py')])
