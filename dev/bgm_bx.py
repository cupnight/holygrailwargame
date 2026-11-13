"""비스트 Ⅲ/R 위기의 바깥(전투가 아닌) 배경음악 두 곡을 코드로 만든다 (11-13).
  bxseal  봉인 중 — BB전 곡(B장조 · 161BPM · 전자음)과 닮은 결: 반짝이는 아르페지오 · 넓은 패드 · 서브 베이스 · 가벼운 리듬 · 가끔 끊기는 글리치
  bxdesc  강림 뒤 — 키아라전 곡(117BPM)과 닮은 결: G 프리지안 도미넌트의 이국적인 선율 · 합창 같은 패드 · 종 · 낮은 북 · 지속음
앞부분(도입)은 한 번만, 뒤의 본문은 반복된다. 본문을 두 번 그려 두 번째 것을 반복 구간으로 써서 잔향까지 이어지게 한다.
사용: python3 bgm_bx.py <출력 폴더>  → 마지막 줄들에 소리 목록 항목을 찍는다"""
import sys, os, subprocess, wave
import numpy as np
from scipy.signal import lfilter, butter, fftconvolve, sosfilt

SR = 48000
rng = np.random.default_rng(7)
mtof = lambda m: 440.0 * 2 ** ((m - 69) / 12)

# ---------- 기본 소리 ----------
def polyblep(t, dt):
    y = np.zeros_like(t)
    m = t < dt; x = t[m] / dt; y[m] = x + x - x * x - 1
    m = t > 1 - dt; x = (t[m] - 1) / dt; y[m] = x * x + x + x + 1
    return y

def osc(kind, f, n, det=0.0, ph=None):
    f = f * (2 ** (det / 1200))
    dt = f / SR
    t = (np.arange(n) * dt + (rng.random() if ph is None else ph)) % 1.0
    if kind == 'saw': return 2 * t - 1 - polyblep(t, dt)
    if kind == 'sq':
        s = np.where(t < .5, 1.0, -1.0); s += polyblep(t, dt); s -= polyblep((t + .5) % 1, dt); return s
    if kind == 'tri': return 2 * np.abs(2 * t - 1) - 1
    return np.sin(2 * np.pi * t)

def adsr(n, a, d, s, r, sus=None):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    sus = n - a - d - r if sus is None else int(sus * SR)
    sus = max(0, sus)
    e = np.concatenate([np.linspace(0, 1, max(a, 1)), np.linspace(1, s, max(d, 1)), np.full(sus, s), np.linspace(s, 0, max(r, 1))])
    if len(e) < n: e = np.concatenate([e, np.zeros(n - len(e))])
    return e[:n]

def lp(x, fc, order=2):
    if np.ndim(fc):   # 시간에 따라 바뀌는 차단 주파수: 조각마다 계수를 바꾸며 상태를 이어 간다
        from scipy.signal import sosfilt_zi
        out = np.empty_like(x); zi = None; B = 1024
        for i in range(0, len(x), B):
            f = float(np.clip(fc[min(i, len(fc) - 1)], 30, SR * .45))
            sos = butter(order, f / (SR / 2), 'low', output='sos')
            if zi is None: zi = sosfilt_zi(sos) * 0
            out[i:i + B], zi = sosfilt(sos, x[i:i + B], zi=zi)
        return out
    sos = butter(order, min(fc, SR * .45) / (SR / 2), 'low', output='sos'); return sosfilt(sos, x)
def hp(x, fc, order=2):
    sos = butter(order, fc / (SR / 2), 'high', output='sos'); return sosfilt(sos, x)
def bp(x, lo, hi, order=2):
    sos = butter(order, [lo / (SR / 2), min(hi, SR * .45) / (SR / 2)], 'band', output='sos'); return sosfilt(sos, x)

def reverb_ir(sec, damp=4000, pre=.012):
    n = int(sec * SR); t = np.arange(n) / SR
    ir = rng.standard_normal((2, n)) * np.exp(-6.9 * t / sec)
    ir = np.stack([lp(ir[0], damp), lp(ir[1], damp)])
    ir[:, :int(pre * SR)] = 0
    return ir / np.sqrt((ir ** 2).sum(axis=1, keepdims=True))

def add(buf, x, at, pan=0.0, g=1.0):
    """buf (2,N)에 모노 x를 at초에 pan(-1~1)으로 더한다"""
    i = int(at * SR); j = min(buf.shape[1], i + len(x))
    if j <= i: return
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[0, i:j] += x[:j - i] * l * g; buf[1, i:j] += x[:j - i] * r * g

def wet(buf, ir, mix):
    out = np.stack([fftconvolve(buf[0], ir[0])[:buf.shape[1]], fftconvolve(buf[1], ir[1])[:buf.shape[1]]])
    return out * mix

# ---------- 악기 ----------
def kick(g=1.0):
    n = int(.42 * SR); t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t * 28); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7.5) * g + lp(rng.standard_normal(n), 3000) * np.exp(-t * 90) * .15 * g
def hat(open_=False, g=1.0):
    n = int((.22 if open_ else .05) * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7000, 4) * np.exp(-t * (14 if open_ else 70)) * g
def clap(g=1.0):
    n = int(.3 * SR); t = np.arange(n) / SR; x = bp(rng.standard_normal(n), 900, 5000)
    env = np.exp(-t * 18);
    for k in (0, .011, .022): env += np.where((t > k) & (t < k + .008), 1.0, 0) * .6
    return x * env * .5 * g
def taiko(g=1.0):
    n = int(1.4 * SR); t = np.arange(n) / SR
    f = 62 + 40 * np.exp(-t * 12); body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    skin = lp(rng.standard_normal(n), 900) * np.exp(-t * 22) * .5
    return (body + skin) * g
def pluck(m, dur, g=1.0, bright=6000):
    n = int(dur * SR); f = mtof(m)
    x = (osc('sq', f, n, ph=0) * .5 + osc('saw', f, n, 7, ph=0) * .5)
    t = np.arange(n) / SR
    x = lp(x * np.exp(-t * 9), bright) * adsr(n, .002, .05, .5, .05)
    return x * g
def bell(m, dur, g=1.0, ratio=3.5, idx=2.4):
    n = int(dur * SR); t = np.arange(n) / SR; f = mtof(m)
    mod = np.sin(2 * np.pi * f * ratio * t) * idx * np.exp(-t * 2.2)
    return np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 1.6) * adsr(n, .003, .1, .9, .4) * g
def pad(ms, dur, g=1.0, cut=2400, a=1.2, r=1.6):
    n = int(dur * SR); x = np.zeros(n)
    for m in ms:
        for d in (-11, 0, 9): x += osc('saw', mtof(m), n, d)
    x = lp(x / (len(ms) * 3), cut, 2)
    return x * adsr(n, a, .5, .8, r) * g
def choir(ms, dur, g=1.0, a=1.6, r=2.0, vowel='a'):
    F = {'a': [(800, 1.0), (1150, .5), (2900, .25)], 'o': [(500, 1.0), (800, .45), (2830, .15)], 'u': [(350, 1.0), (600, .3), (2700, .1)]}[vowel]
    n = int(dur * SR); t = np.arange(n) / SR; src = np.zeros(n)
    for m in ms:
        for d in (-8, -3, 4, 10):
            vib = 1 + .004 * np.sin(2 * np.pi * (5.1 + rng.random()) * t + rng.random() * 6)
            ph = 2 * np.pi * np.cumsum(mtof(m) * (2 ** (d / 1200)) * vib) / SR
            src += (2 * ((ph / (2 * np.pi)) % 1) - 1)
    out = np.zeros(n)
    for fc, w in F: out += bp(src, fc * .86, fc * 1.14) * w
    breath = bp(rng.standard_normal(n), 900, 3500) * .02
    return (out / (len(ms) * 2) + breath) * adsr(n, a, .6, .85, r) * g
def sub(m, dur, g=1.0):
    n = int(dur * SR); return osc('sin', mtof(m), n, ph=0) * adsr(n, .01, .1, .9, .08) * g
def drone(m, dur, g=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(osc('saw', mtof(m) * k, n, d) for k, d in ((1, -4), (1, 5), (2, 0), (1.5, 3)))
    x = lp(x, 900 + 500 * np.sin(2 * np.pi * .07 * t) ** 2)
    return x * adsr(n, 2.5, 1, .9, 2.5) * g * .25

def finish(buf, name, ls, le, outdir, target=-18.4):
    peak = np.abs(buf).max(); buf = buf / (peak + 1e-9) * .9
    w = os.path.join(outdir, name + '.wav')
    ww = wave.open(w, 'wb'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(SR)
    ww.writeframes((np.clip(buf.T, -1, 1) * 32767).astype('<i2').tobytes()); ww.close()
    I = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', w, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float([l for l in I.split('\n') if l.strip().startswith('I:')][-1].split()[1]); G = target - I
    out = os.path.join(outdir, name + '.mp3')
    subprocess.run(['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', w, '-af', f'volume={G}dB,alimiter=limit=0.89:level=false:attack=2:release=60', '-ar', '48000', '-b:a', '160k', out]); os.remove(w)
    print(f'"{name}":{{"d":{buf.shape[1] / SR:.2f},"ls":{ls:.3f},"le":{le:.3f}}}')

# ---------- 봉인: BB전과 닮은 결 ----------
def seal(outdir):
    bpm = 160; b = 60 / bpm; bar = 4 * b
    # B장조: G#m - E - B - F#  /  G#m - E - C#m - F#
    prog = [(56, [56, 59, 63]), (52, [52, 56, 59]), (47, [59, 63, 66]), (54, [54, 58, 61]),
            (56, [56, 59, 63]), (52, [52, 56, 59]), (49, [49, 52, 56]), (54, [54, 58, 61])]
    intro_bars, body_bars = 4, 32
    total = (intro_bars + 2 * body_bars) * bar + 3
    dry = np.zeros((2, int(total * SR))); sendv = np.zeros_like(dry)
    def section(t0, bars, intro=False):
        for k in range(bars):
            at = t0 + k * bar; root, ch = prog[k % 8]; part = k // 8  # 0~3
            # 패드: 넓게, 박자마다 숨 쉬듯(사이드체인처럼)
            p = pad([m + 12 for m in ch], bar + .2, .5 if not intro else .35 + .1 * k, cut=2200 + 600 * (part % 2), a=.05, r=.3)
            duck = np.ones(len(p)); tt = np.arange(len(p)) / SR
            for q in range(4): duck *= 1 - .55 * np.exp(-np.clip(tt - q * b, 0, None) * 9) * (tt >= q * b)
            add(sendv, p * duck, at, -.3, .7); add(sendv, p * duck, at, .3, .7)
            if intro: continue
            # 서브 베이스: 8분 음표 옥타브 왕복
            for q in range(8):
                add(dry, sub(root - 12 + (12 if q % 2 else 0) * (part >= 2), b / 2 * .9, .55), at + q * b / 2)
            # 반짝이는 아르페지오: 16분, 화음 위아래
            if part != 1 or k % 8 >= 4:
                seq = [ch[0] + 24, ch[1] + 24, ch[2] + 24, ch[1] + 36, ch[2] + 24, ch[1] + 24, ch[0] + 36, ch[2] + 24]
                for q in range(16):
                    m = seq[q % 8]
                    if part == 3 and q % 4 == 3: m += 12
                    x = pluck(m, b / 4 * 1.6, .32, 5200 + 2000 * ((q % 4) == 0))
                    add(dry, x, at + q * b / 4, (-.5 if q % 2 else .5), .8); add(sendv, x, at + q * b / 4, 0, .35)
            # 리듬: 반박자 느낌의 킥 · 하이햇 · 2 · 4박 손뼉
            if part >= 1:
                for q in (0, 2): add(dry, kick(.9), at + q * b)
                if part >= 2: add(dry, kick(.6), at + 3.5 * b)
                for q in range(8): add(dry, hat(q % 2 == 1, .18 if q % 2 else .12), at + q * b / 2, .25)
                for q in (1, 3): add(dry, clap(.55), at + q * b, -.1); add(sendv, clap(.3), at + q * b)
            # 리드: 짧은 장난스러운 모티프 (두 마디에 한 번)
            if part in (1, 3) and k % 2 == 0:
                mot = [(0, 75, .5), (.5, 78, .5), (1, 80, .25), (1.25, 78, .25), (1.5, 75, 1), (3, 73, .75)]
                for st, m, d in mot:
                    n = int(d * b * SR); x = (osc('sq', mtof(m), n) * .6 + osc('tri', mtof(m + 12), n) * .4)
                    x = lp(x, 4200) * adsr(n, .005, .08, .6, .06) * .16
                    add(dry, x, at + st * b, .1); add(sendv, x, at + st * b, 0, .5)
            # 글리치: 여덟 마디 끝에 한 번, 마지막 박을 잘게 되풀이
            if k % 8 == 7:
                i0 = int((at + 3 * b) * SR); sl = int(b / 8 * SR)
                for ch_ in (dry, sendv):
                    piece = ch_[:, i0 - sl:i0].copy()
                    for r_ in range(8): ch_[:, i0 + r_ * sl:i0 + (r_ + 1) * sl] = piece * (1 - r_ / 10)
    section(0, intro_bars, intro=True)
    t1 = intro_bars * bar
    section(t1, body_bars); section(t1 + body_bars * bar, body_bars)
    # 도입의 상승음
    n = int(intro_bars * bar * SR); tt = np.arange(n) / SR
    sw = lp(rng.standard_normal(n), 400 + 6000 * (tt / tt[-1]) ** 2) * (tt / tt[-1]) ** 2 * .25
    add(sendv, sw, 0)
    mix = dry + sendv * .55 + wet(sendv, reverb_ir(2.2, 5000), .45) + wet(dry, reverb_ir(1.1, 6000), .12)
    ls, le = t1 + body_bars * bar, t1 + 2 * body_bars * bar
    mix = mix[:, :int((le + .5) * SR)]
    finish(mix, 'bxseal', ls, le, outdir)

# ---------- 강림: 키아라전과 닮은 결 ----------
def descend(outdir):
    bpm = 117; b = 60 / bpm; bar = 4 * b
    # G 프리지안 도미넌트(G Ab B C D Eb F): Gm(add b2) - Ab - Gm - Fm / Eb - D - Cm - D
    prog = [(43, [55, 58, 62]), (44, [56, 60, 63]), (43, [55, 59, 62]), (41, [53, 56, 60]),
            (39, [55, 58, 63]), (38, [54, 57, 62]), (36, [55, 60, 63]), (38, [54, 57, 62])]
    scale = [55, 56, 59, 60, 62, 63, 65, 67, 68, 71, 72, 74, 75]
    intro_bars, body_bars = 4, 16
    total = (intro_bars + 2 * body_bars) * bar + 4
    dry = np.zeros((2, int(total * SR))); sendv = np.zeros_like(dry)
    mel = [(0, 67, 1.5), (1.5, 68, .5), (2, 67, 1), (3, 63, 1), (4, 62, 2), (6, 63, 1), (7, 59, 1),
           (8, 60, 1.5), (9.5, 62, .5), (10, 63, 1), (11, 65, 1), (12, 67, 3), (15, 68, 1)]
    def section(t0, bars, intro=False):
        for k in range(bars):
            at = t0 + k * bar; root, ch = prog[k % 8]; part = k // 8
            add(sendv, choir(ch, bar + .4, .55 if not intro else .3 + .08 * k, a=.9, r=1.2, vowel='a' if k % 2 == 0 else 'o'), at, 0, 1)
            if k % 2 == 0: add(dry, drone(root - 12 if root > 40 else root, 2 * bar + .5, .9), at, 0)
            if intro:
                add(sendv, bell(79, 4.0, .35, 1.4, 1.2), at, .4); continue
            # 낮은 북: 1박 크게, 3박 반 작게 / 둘째 판부터 8분 장식
            add(dry, taiko(1.0), at); add(sendv, taiko(.3), at)
            add(dry, taiko(.55), at + 2.5 * b, .15)
            if part == 1:
                for q in (1, 3): add(dry, taiko(.35), at + q * b + b / 2, -.2)
                for q in range(8): add(dry, hat(False, .07), at + q * b / 2, .3)
            # 종 · 싱잉볼: 마디마다
            add(sendv, bell(ch[2] + 12, 3.5, .32, 1.4, 1.1), at + .02, -.4)
            if k % 2 == 1: add(sendv, bell(ch[0] + 24, 2.5, .18, 3.5, 2.6), at + 2 * b, .45)
            # 시타르 같은 뜯는 소리: 음계를 오르내리는 16분 꾸밈
            if part == 1 or k % 4 >= 2:
                for q in range(8):
                    m = scale[(k * 3 + [0, 2, 4, 2, 5, 4, 2, 1][q]) % len(scale)]
                    n = int(b / 2 * 1.8 * SR); tt = np.arange(n) / SR
                    x = osc('saw', mtof(m), n) * np.exp(-tt * 7)
                    x = bp(x, 400, 3800) + lp(osc('saw', mtof(m) * 1.005, n), 2000) * np.exp(-tt * 9) * .4
                    add(dry, x * .1, at + q * b / 2, .35 * (1 if q % 2 else -1)); add(sendv, x * .08, at + q * b / 2)
            # 선율(목소리처럼): 두 마디 묶음
            if k % 2 == 0:
                for st, m, d in mel:
                    if st >= 8 and k % 4 == 2: m += 0
                    n = int(d * b * SR + .25 * SR); tt = np.arange(n) / SR
                    vib = 1 + .006 * np.sin(2 * np.pi * 5.4 * tt) * np.clip(tt * 2, 0, 1)
                    ph = 2 * np.pi * np.cumsum(mtof(m + (12 if part == 1 else 0)) * vib) / SR
                    x = np.sin(ph) * .6 + np.sin(2 * ph) * .25 + np.sin(3 * ph) * .1
                    x = x * adsr(n, .06, .2, .8, .25) * .2
                    add(dry, x, at + st * b, -.05, .7); add(sendv, x, at + st * b, 0, .8)
    section(0, intro_bars, intro=True)
    t1 = intro_bars * bar
    section(t1, body_bars); section(t1 + body_bars * bar, body_bars)
    mix = dry + sendv * .5 + wet(sendv, reverb_ir(3.2, 3800, .02), .6) + wet(dry, reverb_ir(1.4, 5000), .15)
    ls, le = t1 + body_bars * bar, t1 + 2 * body_bars * bar
    mix = mix[:, :int((le + .5) * SR)]
    finish(mix, 'bxdesc', ls, le, outdir)

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    seal(out); descend(out)
