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
python3 inject3.py batch5 5차 build/game.html   # 에미야[얼터]
python3 extras4.py build/game.html             # ③ 성향 말투 · 마성 · 매료 마안 · 낮잠
python3 bx_patch.py build/game.html            # ② 비스트 위기
python3 bxe_apply.py build/game.html           # ② 키아라 패배 뒤 에필로그
python3 rel_apply.py build/game.html          # ④ 관계 대사 · 짝 대사
python3 faces_apply.py build/game.html         # ④ 얼굴 135칸
python3 sw_apply.py build/game.html            # ⑤ 에필로그 애정 전환
python3 moon_apply.py build/game.html          # BB · 멜트 · 립 전용 소환 길
python3 sfx_apply.py build/game.html           # 소환 연출: 문 캔서 · 얼터 에고
python3 sfx_bb.py build/game.html              # 소환 연출: BB 전용(가로채는 소환)
python3 kiara_bgm_apply.py build/game.html       # 키아라 · BB 전투 배경음악
python3 ea_apply.py build/game.html              # 에미야[얼터]: 보구 특례 · 키아라 관계 대사
python3 fix1112_apply.py build/game.html         # 11-12 문의: 교회 의뢰 보상 · 죽마고우 → 지기
python3 alex_apply.py build/game.html            # 이스칸다르의 소원: 수육
python3 epi2_apply.py build/game.html            # 에필로그 시간 흐름: 일 · 달 · 해 구간
python3 bxach_apply.py build/game.html           # 비스트 위기 업적 17개 (11-13)
python3 ach_order_apply.py build/game.html       # 업적 화면: 업데이트된 순서 · 분류 순서 고정 (11-13)
python3 reg1113_apply.py build/game.html         # 갈림길 · 재촉 · 쉼 대사를 서번트 말투에 맞게 (11-13)
python3 bxscn_apply.py build/game.html           # 비스트 위기 화면 표시 · 시나리오 분리 (11-13)
python3 cxui_apply.py build/game.html            # 후반 위기 현판 (11-13)
python3 bxnun_apply.py build/game.html           # 비스트 위기: 수녀(키아라)의 소원 · 대사 · 이벤트 (11-13)
python3 epi1113_apply.py build/game.html          # 에필로그: 비스트 생의 검은 성배 사건 · 단꿈 생의 일상 사건 거르기 (11-13)
python3 bxabs_apply.py build/game.html           # 비스트: 봉인 중 흡수도 단서로 (11-13 · A안)
python3 cxmsg_apply.py build/game.html           # 비스트 유닛: 전투 종료 메시지 · 적 카드 · 정보창 문구 (11-13)
python3 fix1113_apply.py build/game.html         # 11-13 문의: 인질 구출전 대화 · 인질 날 결투장 겹침
python3 lobby_apply.py build/game.html            # 로비 새 배경 · 새 배치 (11-13)
python3 lbrec_apply.py build/game.html            # 로비: 기록 화면을 배경 위에 펼침 (A안 · 11-13)
python3 loading_apply.py build/game.html          # 로딩 화면: 성배에 금빛이 차오름 (11-13)
python3 bxfx_apply.py build/game.html            # 비스트 연출 ①~⑥: 봉인 · 빈 자리 · 강림 · 키아라 입장 · 단독현현 · 결말 (11-12 시안 → 11-13 연결)
python3 bxfx2_apply.py build/game.html           # 비스트 연출 ⑦~⑪: KP · 해방 · 봉인이 갈라짐 · 토벌령 · 격돌 (11-13 연결)
