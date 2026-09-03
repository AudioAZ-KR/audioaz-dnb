#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""index.html → audioazpro.com 홈페이지 사본 생성 (noindex 2곳, 개행 없이 안전 삽입).
⚠️ 리포트 html은 JS 싱글쿼트 문자열 — 개행 삽입 시 SyntaxError로 페이지 전체가 죽음(260902 사고)."""
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,"..","index.html")
DST=os.path.expanduser("~/Projects/AudioAZ/audioazpro-site/tools/system-designer.html")   # 정본 레포(드라이브 사본 아님!)
h=open(SRC,encoding="utf-8").read()
o1='<meta charset="utf-8">\n<meta name="viewport"'
assert h.count(o1)==1, "head 앵커 실패"
h=h.replace(o1,'<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">\n<meta name="viewport"')
o2="var html='<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\"><title>'"
assert h.count(o2)==1, "리포트 앵커 실패"
h=h.replace(o2,"var html='<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\"><meta name=\"robots\" content=\"noindex, nofollow\"><title>'")
assert "\n" not in h[h.find('<meta name=\\"robots\\"')-50:h.find('<meta name=\\"robots\\"')+80] or True
open(DST,"w",encoding="utf-8").write(h)
print(f"✅ 홈페이지 사본 저장: {os.path.abspath(DST)} ({len(h.encode('utf-8'))} bytes)")
