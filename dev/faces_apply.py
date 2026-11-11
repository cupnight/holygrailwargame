"""④ 얼굴 아틀라스 135칸: FACE_IDS · CSS 줄 수 · 캐시 꼬리표. 사용: python3 faces_apply.py <game.html>"""
import sys, os, re
D0 = os.path.dirname(os.path.abspath(__file__)); ids = open(os.path.join(D0, 'face_ids.txt')).read().strip()
n = len(ids.split(',')); rows = (n + 11) // 12
for P in sys.argv[1:]:
    s = open(P, encoding='utf-8').read()
    s, a = re.subn(r"const FACE_IDS='[^']*'", "const FACE_IDS='" + ids + "'", s)
    s, b = re.subn(r"url\(assets/portraits/faces72\.webp(\?v=\d+)?\) no-repeat;background-size:1200% \d+%", f"url(assets/portraits/faces72.webp?v={n}) no-repeat;background-size:1200% {rows*100}%", s)
    open(P, 'w', encoding='utf-8').write(s); print(os.path.basename(P), 'FACE_IDS', a, 'css', b, 'cells', n)
