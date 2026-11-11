#!/bin/sh
# main의 public/index.html에서 복구 작업을 차례로 다시 쌓는다: sh dev/build.sh
set -e
cd "$(dirname "$0")"
git show main:public/index.html > base.html
mkdir -p build; cp base.html build/game.html
python3 al_apply.py build/game.html            # ⓪ 속성·취향
python3 inject3.py batch3 3차 build/game.html   # ① BB·멜트릴리스·패션립
python3 cls_apply.py build/game.html           # ① 새 클래스 셋
python3 inject3.py batch4 4차 build/game.html   # ③ 스즈카 고젠 · 타마모 캣
python3 extras4.py build/game.html             # ③ 성향 말투 · 마성 · 매료 마안 · 낮잠
python3 bx_patch.py build/game.html            # ② 비스트 위기
python3 bxe_apply.py build/game.html           # ② 키아라 패배 뒤 에필로그
python3 rel_apply.py build/game.html          # ④ 관계 대사 · 짝 대사
python3 faces_apply.py build/game.html         # ④ 얼굴 135칸
python3 sw_apply.py build/game.html            # ⑤ 에필로그 애정 전환
python3 moon_apply.py build/game.html          # BB · 멜트 · 립 전용 소환 길
python3 sfx_apply.py build/game.html           # 소환 연출: 문 캔서 · 얼터 에고
python3 sfx_bb.py build/game.html              # 소환 연출: BB 전용(가로채는 소환)
