#!/usr/bin/env python3
"""소스(src/) → index.html 번들 조립.
사용: python3 build.py            # 빌드+검증
      python3 build.py --check    # 현재 index.html이 소스와 일치하는지만 확인
빌드 후: git add -A && git commit && git push → Netlify 자동배포 + 설치본 복사는 deploy.sh 참고
"""
import os,sys,re
HERE=os.path.dirname(os.path.abspath(__file__))
def read(p): return open(os.path.join(HERE,p),encoding="utf-8").read()
ui=read("src/ui.html")
parts={"@@DBSD_SQLJS@@":read("src/sqljs_glue.js"),
       "@@DBSD_WASM@@":read("src/wasm_payload.txt"),
       "@@DBSD_WEBGEN@@":read("src/web_gen.js")}
out=ui
for tk,body in parts.items():
    assert out.count(tk)==1, "token missing: "+tk
    out=out.replace(tk,body,1)
# ── 안전검증 (과거 wasm 소실 사고 방지) ──
assert len(out)>1_400_000, "번들이 너무 작음 — wasm 소실 의심: %d"%len(out)
vers=set(re.findall(r"BETA v(\d+\.\d+)",out))
assert len(vers)==1, "버전 문자열 불일치: %s"%vers
assert out.count("DBSD-WEBGEN-START")==1 and "window.DBSD_WEBGEN" in out
tgt=os.path.join(HERE,"index.html")
if "--check" in sys.argv:
    cur=open(tgt,encoding="utf-8").read()
    print("일치" if cur==out else "불일치 — build.py 실행 필요"); sys.exit(0 if cur==out else 1)
open(tgt,"w",encoding="utf-8").write(out)
print("✅ index.html 빌드 완료: %d bytes · v%s"%(len(out),vers.pop()))
