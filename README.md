# AudioAZ d&b System Designer — 소스
- `index.html` — 배포 번들(생성물). 직접 수정 금지, build.py로 조립.
- `src/ui.html` — UI+베뉴에디터 (WEBGEN 3종은 @@토큰@@)
- `src/web_gen.js` — 브라우저 .dbpr 생성기 (arraycalc_gen.py의 1:1 JS 미러 — 항상 함께 수정!)
- `src/arraycalc_gen.py` — 파이썬 마스터 생성기 (설치본 ~/.dbdesigner/과 동기)
- `src/sqljs_glue.js`, `src/wasm_payload.txt` — sql.js (수정할 일 없음)
- `src/server.py`, `src/r1_assets.json` — 로컬 앱 서버

## 워크플로
1. src/ 수정 (버전 배지 2곳: ui.html의 v1.XX)
2. `python3 build.py`
3. `python3 tests/run_tests.py` (골든+패리티)
4. 설치본 반영: `cp index.html ~/.dbdesigner/designer.html && cp src/arraycalc_gen.py ~/.dbdesigner/`
5. `git add -A && git commit && git push` → Netlify 자동배포(~15초)

## 절대 규칙
- FlyingFrames 관련 수정은 ArrayCalc 실측 검증 없이 배포 금지(크래시 전례 2회)
- 파이썬↔JS 생성기 동시 수정(패리티)
- 제3자 파일(타 엔지니어 .dbpr·R1) 데이터를 번들에 임베드 금지
