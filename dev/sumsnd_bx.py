"""비스트 Ⅲ/R 연출 소리 (11-12). 모두 직접 합성. 결말 둘은 결말 음악(j_end_d) 앞에 효과를 붙인 판.
사용: python3 sumsnd_bx.py <소리 폴더(j_end_d.mp3가 있는 곳)> <출력 폴더> [이름,이름 — 이것만 만듦]"""
import sys, os, subprocess, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
SR = 48000; rng = np.random.default_rng(5)
SRC, OUT = sys.argv[1], sys.argv[2]
def T(d): return np.arange(int(d * SR)) / SR
def buf(d): return np.zeros((2, int(d * SR)))
def put(B, x, at, pan=0., g=1.):
    i = int(at * SR); n = min(len(x), B.shape[1] - i)
    if n <= 0: return
    B[0, i:i + n] += x[:n] * g * np.sqrt(.5 * (1 - pan)); B[1, i:i + n] += x[:n] * g * np.sqrt(.5 * (1 + pan))
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def bell(f, d):
    x = T(d * 4); m = 2.0 * np.exp(-x / (d * .4)); return np.sin(2 * np.pi * f * x + m * np.sin(2 * np.pi * f * 3.5 * x)) * np.exp(-x / d)
def soft(f, d):  # 부드러운 종 (하모닉 적음)
    x = T(d * 3); return (np.sin(2 * np.pi * f * x) + .3 * np.sin(4 * np.pi * f * x)) * np.exp(-x / d) * np.minimum(1, x / .004)
def pad(freqs, d, att, rel, det=.004, bright=1800):
    x = T(d); y = np.zeros(len(x))
    for f in freqs:
        for k in (-1, 0, 1):
            ph = 2 * np.pi * f * (1 + det * k) * x + rng.random() * 6
            y += (2 * ((ph / (2 * np.pi)) % 1) - 1) * .3
    y = lp(y, bright); e = np.minimum(1, x / att) * np.minimum(1, (d - x) / rel); return y * e / len(freqs)
def noise(d): return rng.standard_normal(int(d * SR))
def env(d, a, r): x = T(d); return np.minimum(1, x / max(a, 1e-4)) * np.exp(-np.maximum(0, x - a) / r)
def sweep(f0, f1, d, shape='exp'):
    x = T(d); f = f0 * (f1 / f0) ** (x / d) if shape == 'exp' else f0 + (f1 - f0) * x / d; return np.sin(2 * np.pi * np.cumsum(f) / SR)
def whoosh(d, lo, hi, g=1.):
    n = int(d * SR); s = noise(d); y = np.zeros(n); seg = 2400; u = np.linspace(0, 1, n)
    for k in range(0, n, seg): f = lo * (hi / lo) ** u[k]; y[k:k + seg] = bp(s[k:k + seg], f * .7, min(f * 1.4, 20000), 1)
    return y * np.sin(np.pi * u) ** 1.5 * g
def crush(x, bits=5, hold=6): y = np.repeat(x[::hold], hold)[:len(x)]; q = 2 ** (bits - 1); return np.round(y * q) / q
def thump(f=55, d=.8): x = T(d); return np.sin(2 * np.pi * f * x * (1 + .6 * np.exp(-x / .04))) * np.exp(-x / (d * .4))
def crackle(d, g=1.):
    n = int(d * SR); z = bp(noise(d), 700, 7000); gate = np.zeros(n); k = 0
    while k < n: L = int(rng.uniform(.012, .06) * SR); gate[k:k + L] = rng.random() < .65; k += L
    e = np.minimum(1, np.arange(n) / (.02 * SR)) * np.minimum(1, (n - np.arange(n)) / (.08 * SR)); return z * gate * e * g
def reverb(B, sec=2.2, wet=.3):
    n = int(sec * SR); x = np.arange(n) / SR; out = np.zeros_like(B)
    for c in range(2):
        ir = rng.standard_normal(n) * np.exp(-x / (sec / 6.9)); ir = lp(ir, 7000); ir /= np.sqrt((ir ** 2).sum()); out[c] = B[c] + wet * fftconvolve(B[c], ir)[:B.shape[1]]
    return out
def rd(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 's16le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, '<i2').reshape(-1, 2).T.astype(float) / 32768
def save(name, B, lufs=-16.5):
    import wave
    B = B / (np.abs(B).max() + 1e-9) * .89; w = os.path.join(OUT, name + '.wav')
    ww = wave.open(w, 'wb'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes((np.clip(B.T, -1, 1) * 32767).astype('<i2').tobytes()); ww.close()
    I = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', w, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float([l for l in I.split('\n') if l.strip().startswith('I:')][-1].split()[1]); G = lufs - I
    subprocess.run(['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', w, '-af', f'volume={G}dB,alimiter=limit=0.89:level=false:attack=2:release=60', '-ar', '48000', '-b:a', '160k', os.path.join(OUT, name + '.mp3')]); os.remove(w); print(name, round(B.shape[1] / SR, 2))
# 11-12 2판: 사용자가 준 키아라 전투곡(kiara.mp3)의 말을 따른다 — G 프리지안(G · A♭ · B♭ · C · D · E♭ · F), 낮은 G · D 지속음이 무겁게 깔리고(150Hz 아래 몫이 큼),
# 선율은 A♭→G 반음 내림이 중심, 저음에 C#(삼전음)이 섞임, 80 BPM(한 박 0.75초 · 셋잇단 0.25초). 곡의 소리는 쓰지 않고 조성 · 음정 · 무게만 따른다
GOLD = [587.33, 880, 1174.66, 783.99]          # 금빛 성배: D · A · D · G (곡의 조에 맞춰 F# 뺌)
MOON = [233.08, 277.18, 349.23, 523.25]        # 달: B♭ 단조 add9 (BB 소환과 같은 화음 · G 프리지안과 음을 나눔)
SWEET = [196.0, 207.65, 261.63, 311.13, 392.0] # 키아라: G 위의 A♭ 장3화음(G · A♭ · C · E♭ · G) — 달콤하게 어긋난 소리
REST = [98.0, 146.83, 196.0, 293.66]          # 풀림: G · D 빈 5도
DRONE = [49.0, 98.0, 146.83]                  # 바닥에 깔리는 G · D
AB, G4 = 415.3, 392.0                          # 키아라의 동기: A♭ → G
def choir(freqs, d, att, rel, vow=((730, 1.0, 90), (1090, .55, 110), (2440, .25, 170))):  # '아' 소리 결의 합창 패드
    x = T(d); y = np.zeros(len(x))
    for f in freqs:
        for k in (-1, 0, 1):
            fm = f * (1 + .006 * k) * (1 + .004 * np.sin(2 * np.pi * (5.1 + .3 * k) * x + rng.random() * 6))
            ph = np.cumsum(fm) / SR; y += (2 * (ph % 1) - 1) * .3
    o = sum(g * bp(y, max(60, c - w), c + w) for c, g, w in vow) + .15 * lp(y, 400)
    return o * np.minimum(1, x / att) * np.minimum(1, (d - x) / rel) / len(freqs)
def drone(d, att, rel, g=1.):  # 무거운 바닥: 아주 낮은 G와 그 위의 G · D, 천천히 숨 쉬듯
    x = T(d); y = np.sin(2 * np.pi * 49 * x) * .35 + pad(DRONE[1:], d, .01, .01, det=.002, bright=700) * 1.2
    return y * (1 + .15 * np.sin(2 * np.pi * .33 * x)) * np.minimum(1, x / att) * np.minimum(1, (d - x) / rel) * g * .5   # 곡보다 저음이 넘치지 않게(150Hz 아래 몫 60% 안팎)
def motif(B, at, oct=1, g=.14, step=.75, pan=0.):  # A♭ → G, 한 박 간격
    put(B, bell(AB * oct, 1.4), at, pan, g); put(B, bell(G4 * oct, 2.0), at + step, pan, g * 1.1)
def pulse(B, a, b, g=.06, f=(196.0, 207.65)):  # 셋잇단(0.25초)으로 짧게 뜯는 G · A♭ — 긴장이 차오르는 자리
    t0, k = a, 0
    while t0 < b:
        u = (t0 - a) / max(.01, b - a); put(B, soft(f[k % 2] * 2, .18) * (1 - .3 * (k % 3 != 0)), t0, (-1) ** k * .3, g * (.4 + .6 * u)); t0 += .25; k += 1

def seal(nb):
    d = 6.3 if nb else 6.7; B = buf(d); x = T(d)
    put(B, (np.sin(2 * np.pi * 55 * x) + .4 * np.sin(2 * np.pi * 110 * x)) * ss(x / .6) * (1 - ss((x - d + .8) / .8)), 0, 0, .25)
    for i, f in enumerate(GOLD): put(B, soft(f * 2, 1.4), .3 + i * .07, (-1) ** i * .4, .08)
    put(B, pad(GOLD[:3], d - .4, .6, 1.2, bright=2400) * (1 - (ss((x[:int((d - .4) * SR)] - 1.4) / 1.0) if nb else 0)), .2, 0, .22)
    if not nb:
        put(B, bell(MOON[3] * 2, 1.2), .3, .3, .12)
        for i in range(12): z = sweep(700 + 60 * i, 1500 + 80 * i, .07) * env(.07, .005, .03); put(B, z, 1.1 + i * .1, ((i * 7) % 5 - 2) / 2.5, .14)
        wb = np.sin(2 * np.pi * 880 * T(.3) + 3 * np.sin(2 * np.pi * 9 * T(.3))) * np.sin(np.pi * T(.3) / .3); put(B, wb, 2.22, 0, .12)
        put(B, bp(noise(.06), 1800, 4500) * env(.06, .001, .02) * 1.5, 2.6, 0, .5); put(B, thump(70, .5), 2.6, 0, .6)
        for i, f in enumerate(MOON): put(B, bell(f * 2, 1.4), 2.62 + i * .01, (i - 1.5) / 2, .14)
    whis = bp(noise(.9), 2000, 5000) * np.sin(np.pi * T(.9) / .9) ** 2; put(B, whis, 1.0 if nb else 2.25, .4, .25)
    if nb:
        t0 = 1.4
        while t0 < 2.5: put(B, hp(noise(.01), 4000) * env(.01, .001, .003), t0, rng.uniform(-.8, .8), .25 * (1 - (t0 - 1.4) / 1.2)); t0 += rng.uniform(.01, .04)
        put(B, soft(110, 1.6), 2.0, 0, .3)
    return reverb(B, 2.4, .32)

def desc():
    d = 7.8; B = buf(d); x = T(d)
    put(B, drone(2.6, .5, .3), 0, 0, .35)
    put(B, choir([98.0, 103.83, 146.83], 2.2, .8, .6), .4, 0, .5)          # 수녀가 나타난다 (낮은 합창 · G 위의 A♭)
    for i, f in enumerate([587.33, 783.99, 880, 1174.66, 1567.98]): put(B, soft(f, .8), 1.2 + i * .15, (i - 2) / 3, .1)   # 잔이 오른다
    pulse(B, 1.25, 2.5, .07)
    rv = hp(noise(.7), 1500) * (T(.7) / .7) ** 3; put(B, rv, 1.9, 0, .3)                 # 거꾸로 차오름
    put(B, thump(49, 1.2), 2.6, 0, .45)
    put(B, choir(SWEET, 5.2, .25, 2.2), 2.6, 0, .75); put(B, pad(SWEET[1:4], 5.2, .25, 2.2, bright=2400), 2.6, 0, .25)
    for i, f in enumerate(SWEET): put(B, bell(f * 2, 1.6), 2.62 + i * .03, (i - 2) / 2.5, .1)
    put(B, drone(5.2, .3, 2.0), 2.6, 0, .4)
    for k in range(3): put(B, whoosh(.7, 300, 2400, .25), 3.0 + k * .18, (-1) ** k * .6)
    z = crush(bp(noise(.3), 1200, 8000) * env(.3, .002, .1), 3, 10); put(B, z, 4.25, -.3, .35); put(B, z[::-1].copy(), 4.38, .3, .25)
    g = sweep(140, 38, .6) * env(.6, .01, .25); put(B, crush(g, 4, 8) * .6 + g * .4, 4.22, 0, .45)   # 그림자가 뒤틀린다
    motif(B, 4.2, 2, .12)                                                                     # 이름이 고쳐 쓰이는 순간 A♭ → G
    put(B, bell(98.0, 2.6) * .6, 4.6, 0, .25); put(B, soft(49.0, 3.2), 4.6, 0, .14); put(B, soft(196.0, 2.6), 4.6, 0, .14); put(B, soft(138.59, 2.4), 4.62, 0, .12)   # 비스트 Ⅲ/R: 무거운 G와 C#
    return reverb(B, 2.8, .35)

def karma():
    d = 2.2; B = buf(d); put(B, crackle(1.0, .6), 0, 0); put(B, np.sign(np.sin(2 * np.pi * 60 * T(1.0))) * .12 * env(1.0, .02, .5), 0)
    sw = sweep(2200, 220, 1.0) * np.sin(np.pi * T(1.0)) ** 1.5; put(B, sw, .3, 0, .2)
    z = crush(bp(noise(.08), 1500, 9000) * env(.08, .001, .03), 3, 12)
    for at in (.1, .55, .9): put(B, z, at, rng.uniform(-.6, .6), .5)
    put(B, bell(233.08, 1.2), 1.0, 0, .2); return reverb(B, 1.8, .25)

def bin_(full):
    d = 6.6 if full else 2.5; B = buf(d); x = T(d)
    put(B, choir(SWEET[:4], d - .1, .9 if full else .3, .8 if full else .5), .05, 0, .5)
    put(B, drone(d, .5 if full else .1, .6), 0, 0, .35)
    a0 = .6 if full else .05
    for i, f in enumerate([392.0, 415.3, 523.25, 622.25, 783.99, 830.61]): put(B, soft(f, .9), a0 + i * (.08 if full else .04), (i - 2.5) / 3, .12)
    if full: put(B, choir([49.0 * 2, 69.3 * 2, 98.0 * 2], 4.6, .5, 2.0), 1.3, 0, .45); motif(B, 1.3, 1, .14); pulse(B, 2.8, 4.4, .05)
    else: put(B, bell(AB, .5), .15, 0, .12); put(B, bell(G4, 1.0), .4, 0, .14)
    return reverb(B, 2.2, .3)

def brk(full):
    d = 1.6 if full else 1.2; B = buf(d); n = 60 if full else 32
    for k in range(n): at = rng.random() ** 1.5 * (.7 if full else .45); f = rng.choice(SWEET) * rng.choice([2, 4]); put(B, soft(f, .18), at, rng.uniform(-.9, .9), .08 * (1 - at))
    put(B, whoosh(.9 if full else .6, 400, 5000, .35), 0, 0); put(B, thump(60, .4), 0, 0, .3); return reverb(B, 1.6, .3)

def p2():
    d = 4.1; B = buf(d); put(B, thump(49, .7), .28, 0, .8); put(B, bell(AB * 2, 1.0), .28, 0, .15)
    for i in range(5): put(B, sweep(900 - i * 60, 220, .7) * env(.7, .02, .35), .32 + i * .04, (i - 2) / 3, .08)
    for i in range(5): put(B, sweep(220, 900 + i * 60, .7) * env(.7, .5, .2)[::-1].copy() * np.sin(np.pi * T(.7) / .7), 1.0 + i * .04, (2 - i) / 3, .08)
    pulse(B, 1.0, 1.75, .08)
    put(B, choir(SWEET, 2.3, .05, 1.3), 1.7, 0, .6); put(B, drone(2.3, .05, 1.3), 1.7, 0, .35); put(B, bell(G4 * 2, 1.6), 1.72, 0, .12)
    return reverb(B, 2.0, .3)

def end_moon(v):  # ⑤ 달로 간 잔 (2판, 갈래별): 효과 뒤 결말 음악. 음악은 도시 불빛이 다시 켜질 때(TK) 들어온다
    music = rd(os.path.join(SRC, 'j_end_d.mp3')); TK = {'me': 7.9, 'live': 6.6, 'nobb': 5.8, 'voice': 6.2}[v]; d = TK + .2 + music.shape[1] / SR; B = buf(d)
    for k in range(40): put(B, soft(rng.choice(SWEET) * 4, .25), .3 + rng.random() ** 1.4 * 1.3, rng.uniform(-.8, .8), .05)   # 꽃잎으로 흩어짐
    def blip(f, dd=.07): x = T(dd); return np.sign(np.sin(2 * np.pi * f * x)) * .5 * np.exp(-x / (dd * .35))
    def ticks(a, b_, g=.05):
        t0 = a
        while t0 < b_: put(B, bp(noise(.012), 2500, 7000) * env(.012, .001, .004), t0, rng.uniform(-.3, .3), g); t0 += rng.uniform(.05, .09)
    if v in ('me', 'voice'):   # ① 끼어드는 방송: 지직 → 장난스러운 세 음 → 자막이 찍힘
        put(B, crackle(.35, .9), .1, 0); put(B, np.sign(np.sin(2 * np.pi * 60 * T(.3))) * .1 * env(.3, .01, .1), .1)
        for i, f in enumerate([932.33, 1396.91, 1864.66]): put(B, blip(f, .12), .5 + i * .11, (i - 1) * .4, .2)
        ticks(.55, 1.15 if v == 'me' else 1.05)
        if v == 'me': put(B, crush(bp(noise(.1), 1500, 9000) * env(.1, .001, .03), 3, 10), 1.75, 0, .4)
        else: put(B, crackle(.3, 1.2), 1.2, 0); put(B, crush(bp(noise(.18), 800, 9000) * env(.18, .001, .05), 2, 14), 1.33, 0, .7)
    if v == 'me':
        put(B, pad(MOON, 4.0, .8, 1.2, bright=2000), 1.6, 0, .3)
        sh = sum(np.sin(2 * np.pi * np.cumsum(f * (1 + .6 * T(2.2) / 2.2)) / SR) for f in (880, 1108.73, 1396.91)) * np.sin(np.pi * T(2.2) / 2.2) ** 2 / 3; put(B, sh, 3.2, 0, .1)
        put(B, bell(1864.66, 1.2), 5.45, 0, .12); ticks(5.7, 6.6, .035)
        put(B, soft(466.16, 2.0), 7.2, 0, .14); put(B, soft(698.46, 1.6), 7.25, 0, .07)                   # 한 박자 뒤 진심 한 줄
    elif v == 'live':
        put(B, pad(MOON, 2.5, .8, .6, bright=1800), 1.6, 0, .25)
        put(B, lp(noise(1.2), 160) * np.sin(np.pi * T(1.2) / 1.2) * 3, 2.3, 0, .35); put(B, thump(46, .8), 2.4, 0, .4)   # 그림자가 번진다
        for i in range(6): put(B, whoosh(.5, 120, 700, .5), 2.9 + i * .1, (i - 2.5) / 3)                       # 감싸 오른다
        for k in range(70): at = 3.6 + rng.random() * 1.9; put(B, blip(587.33 * 2 ** ((at - 3.6) / 1.9 * 1.5 + rng.choice([0, .25, .58])), .05), at, rng.uniform(-.6, .6), .07)   # 빛 조각이 줄지어 올라감
        put(B, bell(1864.66, 1.2), 5.6, 0, .12)
    elif v == 'nobb':
        put(B, pad(GOLD[:3], 3.0, .8, 1.0, bright=2000), 1.6, 0, .25)
        for k in range(55): at = 2.4 + rng.random() * 2.0; put(B, soft(587.33 * 2 ** ((at - 2.4) / 2.0 * 1.5 + rng.choice([0, .58, 1])), .15), at, rng.uniform(-.6, .6), .06)
        put(B, bell(1864.66, 1.2), 4.7, 0, .12)
    else:
        for i, f in enumerate([466.16, 554.37]): put(B, crush(soft(f, .5), 4, 6), 1.9 + i * .35, 0, .12)        # 끊긴 목소리 자리
        ticks(1.9, 2.6, .04); put(B, crackle(.25, .5), 2.3, 0)
        rv = hp(noise(.4), 2000) * (T(.4) / .4) ** 2; put(B, rv, 2.6, 0, .25); put(B, bell(1864.66, 1.2), 3.05, 0, .12)
    for i, f in enumerate([587.33, 783.99, 880, 1174.66, 1567.98]): put(B, soft(f, 1.0), TK - .5 + i * .18, (i - 2) / 3, .07)   # ④ 불빛이 다시 켜짐
    B = reverb(B, 2.4, .3); put(B, music[0], TK + .2, -1, 1.414); put(B, music[1], TK + .2, 1, 1.414); return B

def end_dream():
    music = rd(os.path.join(SRC, 'j_end_d.mp3')); d = 4.2 + music.shape[1] / SR; B = buf(d)
    put(B, choir(SWEET[:4], 4.6, 1.6, 1.0), 0, 0, .5); put(B, drone(4.6, 1.6, 1.0), 0, 0, .3)
    for k in range(6): put(B, thump(45, .3), .6 + k * (.55 + k * .12), 0, .3 * (1 - k / 7))     # 느려지는 박동
    t0 = .9
    while t0 < 4.0: put(B, hp(noise(.008), 2500) * env(.008, .0005, .002), t0, rng.uniform(-.9, .9), .1); t0 += .02 + .25 * abs(t0 - 2.2) / 1.8 * rng.random()
    t0 = 5.0
    while t0 < 6.1: put(B, bp(noise(.02), 1500, 5000) * env(.02, .001, .006), t0, .2, .4); t0 += rng.uniform(.05, .11)
    put(B, bell(2093, .6), 6.15, .3, .15)
    B = reverb(B, 2.2, .3); put(B, music[0], 4.2, -1, 1.414); put(B, music[1], 4.2, 1, 1.414); return B

def kp():  # ⑦ 조각이 빠져나와 손에 내려앉고, 지켜보던 시선이 끊긴다
    d = 6.7; B = buf(d); x = T(d)
    gz = T(2.45); gaze = (np.sin(2 * np.pi * 1661 * gz) + .5 * np.sin(2 * np.pi * 1663.5 * gz)) * (.6 + .4 * np.sin(2 * np.pi * 5 * gz)) * ss(gz / .6)
    put(B, gaze, .2, .2, .05); put(B, drone(2.5, .5, .08), .1, 0, .35); put(B, choir([98.0, 103.83], 2.45, .6, .08), .15, 0, .25)
    put(B, whoosh(.5, 600, 3000, .3), .45, 0); put(B, thump(80, .4), .58, 0, .35)
    for i, f in enumerate(SWEET): put(B, bell(f * 2, 1.0), .6 + i * .04, (i - 2) / 2.5, .08)
    put(B, choir(SWEET[1:4], 1.2, .3, .6), .9, 0, .25)
    put(B, whoosh(.65, 3000, 500, .35), 1.8, 0)
    put(B, thump(60, .5), 2.42, 0, .5); put(B, soft(587.33, 1.4), 2.43, 0, .2); put(B, soft(783.99, 1.2), 2.45, .2, .12)
    sn = crush(bp(noise(.12), 1500, 9000) * env(.12, .001, .03), 3, 8); put(B, sn, 2.6, 0, .55); put(B, sweep(2400, 300, .4) * env(.4, .002, .12), 2.6, 0, .12)
    put(B, pad(REST, 3.8, .3, 2.0, bright=1600), 2.8, 0, .3); put(B, bell(1174.66, 1.2), 3.45, 0, .08)
    return reverb(B, 2.2, .3)

def free():  # ⑧ 가시 실이 하나씩 끊어지고 제 빛깔로 피어난다
    d = 6.4; B = buf(d); x = T(d)
    put(B, bp(noise(1.2), 300, 900) * np.sin(np.pi * T(1.2) / 1.2) * (1 + .5 * np.sin(2 * np.pi * 7 * T(1.2))), .1, 0, .18)
    put(B, sweep(180, 260, 1.1) * env(1.1, .5, .6) * .5, .2, 0, .2)
    put(B, choir([98.0, 103.83, 138.59], 2.0, .4, .12), .2, 0, .4); put(B, drone(2.05, .4, .1), .2, 0, .3)
    for i, at in enumerate([1.55, 1.95, 1.35, 1.75, 2.05, 1.25, 1.65, 1.45, 1.85]):
        z = bp(noise(.05), 2000, 8000) * env(.05, .001, .012); pl = np.sin(2 * np.pi * (700 + 90 * i) * T(.3)) * np.exp(-T(.3) / .05)
        put(B, z, at, ((i * 5) % 9 - 4) / 5, .4); put(B, pl, at, ((i * 5) % 9 - 4) / 5, .12)
    put(B, thump(55, .7), 2.28, 0, .55)
    for i, f in enumerate([440, 659.25, 880, 1318.5]): put(B, bell(f, 1.6), 2.3 + i * .03, (i - 1.5) / 2, .1)
    put(B, whoosh(1.0, 400, 6000, .35), 2.25, 0); put(B, pad([220, 329.63, 440, 554.37], 3.9, .1, 2.0, bright=3200), 2.3, 0, .3)
    for k in range(14): put(B, soft(rng.choice([1760, 2217.5, 2637, 3520]), .2), 2.35 + rng.random() * .8, rng.uniform(-.9, .9), .05)
    return reverb(B, 2.4, .32)

def conf(v):  # ⑨ 봉인이 갈라짐: conf 고백 · force 찢어짐 · unseal 풀기
    d = {'force': 6.4, 'unseal': 6.3}.get(v, 6.9); B = buf(d); x = T(d); brk = 2.3 if v == 'force' else 2.8
    put(B, pad(MOON, d - .3, .5, 1.4, bright=1600) * (1 - (ss((x[:int((d - .3) * SR)] - brk) / .3) * .7 if v != 'unseal' else 0)), .1, 0, .3)
    if v == 'unseal':
        for i in range(12): put(B, soft(rng.choice(MOON) * 4, .7), 1.0 + i * .08, ((i * 7) % 5 - 2) / 2.5, .07)
        put(B, whoosh(1.6, 500, 3000, .2), 1.0, 0)
        for i, f in enumerate(GOLD): put(B, soft(f, 1.8), 2.0 + i * .08, (i - 1.5) / 2, .1)
        put(B, pad(GOLD[:3], 4.1, .5, 2.0, bright=2200), 2.0, 0, .25)
        return reverb(B, 2.6, .35)
    a0 = .6 if v == 'force' else 1.0
    if v == 'force': put(B, sweep(45, 90, brk - .5) * ss(T(brk - .5) / (brk - .5)) * .8, .5, 0, .4)
    t0 = a0
    while t0 < brk - .05:
        g = .1 + .5 * ((t0 - a0) / (brk - a0)) ** 2; put(B, hp(noise(.03), 2500) * env(.03, .001, .01), t0, rng.uniform(-.7, .7), g); t0 += rng.uniform(.03, .2) * (1.2 - (t0 - a0) / (brk - a0))
    put(B, thump(50, 1.0), brk, 0, .8); put(B, bp(noise(.4), 1200, 9000) * env(.4, .002, .12), brk, 0, .6)
    for k in range(30): put(B, soft(rng.choice(MOON) * rng.choice([4, 8]), .25), brk + rng.random() ** 1.5 * .7, rng.uniform(-.9, .9), .05)
    put(B, choir(SWEET, d - brk, .2, 1.3), brk + .05, 0, .6); put(B, drone(d - brk, .2, 1.3), brk + .05, 0, .35)
    if v == 'conf': motif(B, brk + .9, 2, .1)
    pulse(B, a0 + .4, brk - .1, .05)
    for i, f in enumerate(SWEET): put(B, bell(f * 2, 1.5), brk + .06 + i * .03, (i - 2) / 2.5, .08)
    if v == 'force': put(B, whoosh(.9, 200, 3000, .5), brk - .05, 0)
    return reverb(B, 2.6, .33)

def order():  # ⑩ 종 두 번 · 공문 · 도장
    d = 4.6; B = buf(d)
    def toll(at, g):
        for f, a, dd in [(196, 1, 2.4), (392.4, .5, 1.8), (466.9, .35, 1.4), (587.3, .25, 1.0), (98, .4, 2.8)]: put(B, soft(f, dd) * a, at, 0, g)
    toll(.15, .3); toll(.85, .25)
    put(B, bp(noise(.35), 1500, 6000) * np.sin(np.pi * T(.35) / .35) ** 2, .4, .3, .15)
    put(B, thump(70, .35), 1.55, 0, .7); put(B, bp(noise(.06), 300, 3000) * env(.06, .001, .02), 1.55, 0, .5)
    put(B, pad([98, 146.83, 207.65], 2.9, .1, 1.6, bright=900), 1.56, 0, .25)
    return reverb(B, 2.4, .3)

def np_():  # ⑪ 키아라와의 격돌에 겹치는 단맛 (격돌 소리 위에 얹는다)
    d = 3.0; B = buf(d); x = T(d)
    put(B, choir(SWEET, 2.6, .9, .9), 0, 0, .4); motif(B, 1.26, 2, .08, .5)
    for k in range(10): put(B, soft(rng.choice(SWEET) * 2, .5), .1 + k * .09, rng.uniform(-.5, .9), .04)
    for i, f in enumerate(SWEET): put(B, bell(f * 2, 1.2), 1.26 + i * .02, .4, .07)
    for k in range(18): put(B, soft(rng.choice(SWEET) * 4, .2), 1.5 + rng.random() * .9, rng.uniform(-.9, .3), .035)
    return reverb(B, 2.0, .3)

os.makedirs(OUT, exist_ok=True)
ONLY = sys.argv[3].split(',') if len(sys.argv) > 3 else None
if ONLY:
    F = {'j_bx_karma': karma, 'j_bx_brk': lambda: brk(True), 'j_bx_brk_s': lambda: brk(False), 'j_end_bxm_me': lambda: end_moon('me'), 'j_end_bxm_live': lambda: end_moon('live'), 'j_end_bxm_nobb': lambda: end_moon('nobb'), 'j_end_bxm_voice': lambda: end_moon('voice'), 'j_end_bxdream': end_dream, 'j_bx_seal': lambda: seal(False), 'j_bx_empty': lambda: seal(True), 'j_bx_in': lambda: bin_(True), 'j_bx_in_s': lambda: bin_(False), 'j_bx_p2': p2, 'j_bx_kp': kp, 'j_bx_free': free, 'j_bx_conf': lambda: conf('conf'), 'j_bx_tear': lambda: conf('force'), 'j_bx_open': lambda: conf('unseal'), 'j_bx_order': order, 'j_bx_np': np_, 'j_bx_desc': desc}
    for n in ONLY: save(n, F[n](), -21.0 if n == 'j_bx_np' else -16.0 if n.startswith('j_end') else -16.5)   # 격돌 소리 위에 얹는 단맛은 작게
    raise SystemExit
save('j_bx_seal', seal(False)); save('j_bx_empty', seal(True)); save('j_bx_desc', desc()); save('j_bx_karma', karma())
save('j_bx_in', bin_(True)); save('j_bx_in_s', bin_(False)); save('j_bx_brk', brk(True)); save('j_bx_brk_s', brk(False)); save('j_bx_p2', p2())
[save(f'j_end_bxm_{v}', end_moon(v), -16.0) for v in ('me', 'live', 'nobb', 'voice')]; save('j_end_bxdream', end_dream(), -16.0)
