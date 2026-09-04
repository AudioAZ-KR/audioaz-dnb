#!/bin/bash
# 통합 배포: 빌드 → 테스트 → 로컬 채널 → 본체 push → 홈페이지 사본 push → 라이브 검증
# 사용: tools/deploy.sh "커밋 메시지"   (메시지 없으면 커밋 생략하고 기존 커밋만 push)
set -euo pipefail
cd "$(dirname "$0")/.."
BASE="$(pwd)"
HP="$HOME/Projects/AudioAZ/audioazpro-site"

echo "── 1/6 빌드·테스트"
python3 build.py
python3 tests/run_tests.py >/dev/null && echo "  테스트 ALL PASS"
VER=$(grep -o 'BETA v[0-9][0-9.]*' index.html | head -1 | sed 's/.*BETA //')
echo "  버전: $VER"

echo "── 2/6 로컬 채널"
cp index.html "$HOME/.dbdesigner/designer.html"
cp src/arraycalc_gen.py "$HOME/.dbdesigner/arraycalc_gen.py"
cp index.html "$HOME/Downloads/AudioAZ System Designer BETA $VER.html"

echo "── 4/6 본체 push"
if [ "${1:-}" != "" ]; then
  git add -A && git -c user.name="AudioAZ" -c user.email="leogudwns@gmail.com" commit -m "$1" || echo "  (변경 없음)"
fi
git fetch origin && git push origin main

echo "── 5/6 홈페이지 push (staging 워크플로 — main 직접 push 금지 규칙)"
cd "$HP"
CURBR=$(git rev-parse --abbrev-ref HEAD)
git checkout -- tools/system-designer.html 2>/dev/null || true   # 미커밋 사본 폐기(전환 후 재생성)
git fetch origin
git checkout -q staging 2>/dev/null || git checkout -qb staging origin/staging
git pull --rebase -q origin staging
cd - >/dev/null && python3 tools/make_site_copy.py >/dev/null && cd "$HP"   # 브랜치 전환 후 사본 재생성
git add tools/system-designer.html
git -c user.name="AudioAZ" -c user.email="leogudwns@gmail.com" commit -m "sync: system-designer $VER" || echo "  (변경 없음)"
git push origin staging
# staging에 도구 파일 외 다른 미검증 변경이 없을 때만 자동 라이브 승격
OTHERS=$(git diff --name-only origin/main..staging | grep -v '^tools/system-designer.html$' || true)
if [ -z "$OTHERS" ]; then
  "$HOME/Projects/AudioAZ/promote-to-live.sh" >/dev/null && echo "  staging→main 승격 완료"
else
  echo "  ⚠️ staging에 다른 변경 있음 — 라이브 승격은 수동으로 (promote-to-live.sh):"
  echo "$OTHERS" | sed 's/^/    /'
fi
git checkout -q "$CURBR" 2>/dev/null || true

echo "── 6/6 라이브 검증 (최대 5분)"
for i in $(seq 1 30); do
  A=$(curl -s "https://audioaz-kr.github.io/audioaz-dnb/?nc=$RANDOM" | grep -c "$VER</span>" || true)
  B=$(curl -s "https://audioazpro.com/tools/system-designer.html?nc=$RANDOM" | grep -c "$VER</span>" || true)
  [ "$A" -ge 1 ] && [ "$B" -ge 1 ] && { echo "✅ 두 사이트 모두 $VER 라이브"; exit 0; }
  sleep 10
done
echo "⚠️ 5분 내 반영 확인 실패 — 수동 확인 필요 (github.io=$A, audioazpro=$B)"; exit 1
