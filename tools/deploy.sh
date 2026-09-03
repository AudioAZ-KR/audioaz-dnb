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
VER=$(grep -o 'BETA v[0-9]*\.[0-9]*' index.html | head -1 | sed 's/.*BETA //')
echo "  버전: $VER"

echo "── 2/6 로컬 채널"
cp index.html "$HOME/.dbdesigner/designer.html"
cp src/arraycalc_gen.py "$HOME/.dbdesigner/arraycalc_gen.py"
cp index.html "$HOME/Downloads/AudioAZ System Designer BETA $VER.html"

echo "── 3/6 홈페이지 사본 생성"
python3 tools/make_site_copy.py

echo "── 4/6 본체 push"
if [ "${1:-}" != "" ]; then
  git add -A && git -c user.name="AudioAZ" -c user.email="leogudwns@gmail.com" commit -m "$1" || echo "  (변경 없음)"
fi
git fetch origin && git push origin main

echo "── 5/6 홈페이지 push"
cd "$HP"
git add tools/system-designer.html
git -c user.name="AudioAZ" -c user.email="leogudwns@gmail.com" commit -m "sync: system-designer $VER" || echo "  (변경 없음)"
git fetch origin && git pull --rebase -q origin main && git push origin main

echo "── 6/6 라이브 검증 (최대 5분)"
for i in $(seq 1 30); do
  A=$(curl -s "https://audioaz-kr.github.io/audioaz-dnb/?nc=$RANDOM" | grep -c "$VER</span>" || true)
  B=$(curl -s "https://audioazpro.com/tools/system-designer.html?nc=$RANDOM" | grep -c "$VER</span>" || true)
  [ "$A" -ge 1 ] && [ "$B" -ge 1 ] && { echo "✅ 두 사이트 모두 $VER 라이브"; exit 0; }
  sleep 10
done
echo "⚠️ 5분 내 반영 확인 실패 — 수동 확인 필요 (github.io=$A, audioazpro=$B)"; exit 1
