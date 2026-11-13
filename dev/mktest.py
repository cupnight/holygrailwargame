"""테스트용 HTML 한 장 만들기: 로비 하늘 · 초상화를 파일 안에 넣어, 내려받아 바로 열어도 그림이 나오게 한다(소리는 빠짐).
사용: python3 dev/mktest.py public/index.html dev/build/test.html"""
import sys, os, base64, re, json
src, out = sys.argv[1], sys.argv[2]
A = os.path.join(os.path.dirname(os.path.abspath(src)), 'assets')
s = open(src, encoding='utf-8').read(); miss = []
du = lambda p: 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
# 얼굴 모음(CSS)
n = len(re.findall(r"url\(assets/portraits/faces72\.webp(\?v=\d+)?\)", s))
s = re.sub(r"url\(assets/portraits/faces72\.webp(\?v=\d+)?\)", 'url(' + du(os.path.join(A, 'portraits', 'faces72.webp')) + ')', s)
if not n: miss.append('faces72')
# 일러스트 초상화
P = {f[:-5]: du(os.path.join(A, 'portraits', f)) for f in os.listdir(os.path.join(A, 'portraits')) if f.endswith('.webp') and f != 'faces72.webp'}
o = "--img:url(assets/portraits/${id}.webp)"
if o in s: s = s.replace(o, "--img:url(${(window.__PORT||{})[id]||'assets/portraits/'+id+'.webp'})")
else: miss.append('portrait tpl')
# 로비 하늘
L = {f[:-5]: du(os.path.join(A, 'lobby', f)) for f in os.listdir(os.path.join(A, 'lobby')) if f.endswith('.webp')}
o = "im.src='assets/lobby/'+B.f+'.webp'"
if o in s: s = s.replace(o, "im.src=(window.__LOBBY||{})[B.f]||'assets/lobby/'+B.f+'.webp'")
else: miss.append('lobby')
pre = '<script>window.__PORT=' + json.dumps(P) + ';window.__LOBBY=' + json.dumps(L) + ';</script>\n'
s = s.replace('<body>\n', '<body>\n' + pre, 1)
open(out, 'w', encoding='utf-8').write(s)
print('test miss', miss, 'portraits', len(P), 'lobby', len(L), 'MB', round(len(s.encode()) / 1e6, 1))
