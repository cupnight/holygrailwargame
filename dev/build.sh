#!/bin/sh
# main의 public/index.html에서 복구 작업을 차례로 다시 쌓는다: sh dev/build.sh
set -e
cd "$(dirname "$0")"
git show main:public/index.html > base.html
mkdir -p build; cp base.html build/game.html
python3 al_apply.py build/game.html            # ⓪ 속성·취향
python3 inject3.py batch3 3차 build/game.html   # ① BB·멜트릴리스·패션립
python3 cls_apply.py build/game.html           # ① 새 클래스 셋
