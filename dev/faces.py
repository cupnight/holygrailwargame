"""신규 서번트 얼굴: 240px 일러스트 webp + 72px 도트 아틀라스 칸. 사용: python3 dev/faces.py [--preview]
기존 아틀라스 칸은 픽셀 그대로 옮기고, 새 칸만 원본에서 만든다. 칸 순서는 id 알파벳순(FACE_IDS)."""
import sys, os, re
from PIL import Image
from collections import Counter
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CROPS = {'bb': (655, 475, 290), 'kiara': (660, 445, 290), 'meltryllis': (655, 395, 290), 'passionlip': (655, 480, 290), 'suzuka': (670, 470, 290), 'tamamocat': (685, 455, 290), 'emiya_alter': (598, 350, 310)}
P = lambda *a: os.path.join(ROOT, *a)

def dot72(src):
    """셀 최빈색 + 어두운 선 우선 + 고립점 정리 + 투명 유지"""
    W = src.size[0]; n = 72; px = src.load(); out = Image.new('RGBA', (n, n)); op = out.load()
    for j in range(n):
        for i in range(n):
            x0, x1 = int(i * W / n), max(int(i * W / n) + 1, int((i + 1) * W / n)); y0, y1 = int(j * W / n), max(int(j * W / n) + 1, int((j + 1) * W / n))
            cs = [px[x, y] for y in range(y0, y1) for x in range(x0, x1)]
            op_ = [c for c in cs if c[3] >= 128]
            if len(op_) * 2 < len(cs): op[i, j] = (0, 0, 0, 0); continue
            lum = lambda c: .299 * c[0] + .587 * c[1] + .114 * c[2]
            dark = [c for c in op_ if lum(c) < 70]
            if len(dark) * 4 >= len(op_):  # 어두운 선이 지나가면 선을 남긴다
                c = min(dark, key=lum); op[i, j] = (c[0], c[1], c[2], 255); continue
            q = Counter((c[0] >> 3, c[1] >> 3, c[2] >> 3) for c in op_).most_common(1)[0][0]
            m = [c for c in op_ if (c[0] >> 3, c[1] >> 3, c[2] >> 3) == q]
            op[i, j] = (sum(c[0] for c in m) // len(m), sum(c[1] for c in m) // len(m), sum(c[2] for c in m) // len(m), 255)
    # 고립점 정리: 이웃 8칸이 모두 나와 다르고 서로 비슷하면 이웃의 최빈색으로
    d = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])
    cp = out.copy(); cq = cp.load()
    for j in range(1, n - 1):
        for i in range(1, n - 1):
            c = cq[i, j]; nb = [cq[i + a, j + b] for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]
            if all(d(c, x) > 90 for x in nb):
                mc = Counter(nb).most_common(1)[0]
                if mc[1] >= 5: op[i, j] = mc[0]
    return out

if __name__ == '__main__':
    src = open(P('dev/build/game.html'), encoding='utf-8').read() if os.path.exists(P('dev/build/game.html')) else open(P('public/index.html'), encoding='utf-8').read()
    old = open(P('dev/face_ids.txt')).read().strip().split(',') if os.path.exists(P('dev/face_ids.txt')) else re.search(r"const FACE_IDS='([^']*)'", open(P('dev/base.html'), encoding='utf-8').read()).group(1).split(',')   # 지금 아틀라스의 칸 차례
    atlas = Image.open(P('public/assets/portraits/faces72.webp')).convert('RGBA')
    cell = lambda k: atlas.crop(((k % 12) * 72, (k // 12) * 72, (k % 12) * 72 + 72, (k // 12) * 72 + 72))
    cells = {i: cell(k) for k, i in enumerate(old)}
    for i, (x, y, s) in CROPS.items():
        im = Image.open(P(f'public/assets/sprites/{i}_portrait.png')).convert('RGBA').crop((x, y, x + s, y + s))
        im.resize((240, 240), Image.LANCZOS).save(P(f'public/assets/portraits/{i}.webp'), 'WEBP', quality=88)
        cells[i] = dot72(im)
    ids = sorted(cells); rows = (len(ids) + 11) // 12
    out = Image.new('RGBA', (12 * 72, rows * 72), (0, 0, 0, 0))
    for k, i in enumerate(ids): out.paste(cells[i], ((k % 12) * 72, (k // 12) * 72))
    out.save(P('public/assets/portraits/faces72.webp'), 'WEBP', lossless=True, method=6, quality=100)
    if '--preview' in sys.argv:
        pv = Image.new('RGBA', (len(CROPS) * 220, 220), (40, 37, 52, 255))
        for k, i in enumerate(CROPS): pv.paste(cells[i].resize((216, 216), Image.NEAREST), (k * 220, 2), cells[i].resize((216, 216), Image.NEAREST))
        pv.save('/tmp/claude-0/-home-claude/3b7fc538-eed0-54bc-a02e-74418e7d1e17/scratchpad/faces_preview.png')
    open(P('dev/face_ids.txt'), 'w').write(','.join(ids))
    print('cells', len(ids), 'rows', rows)
