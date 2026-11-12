"""비스트 Ⅲ/R 연출 소리 (11-12). 모두 직접 합성. 결말 둘은 결말 음악(j_end_d) 앞에 효과를 붙인 판.
사용: python3 sumsnd_bx.py <소리 폴더(j_end_d.mp3가 있는 곳)> <출력 폴더>"""
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
GOLD = [587.33, 739.99, 880, 1174.66]          # 금빛 성배: D 장조
MOON = [233.08, 277.18, 349.23, 523.25]        # 달: B♭ 단조 add9 (BB 소환과 같은 화음)
SWEET = [277.18, 349.23, 415.3, 523.25, 622.25]  # 키아라: D♭ 장조 maj7 add9 — 달콤하고 불안한

def seal(nb):
    d = 4.4 if nb else 4.8; B = buf(d); x = T(d)
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
    put(B, (np.sin(2 * np.pi * 46 * x) + .5 * np.sin(2 * np.pi * 69 * x)) * ss(x / .5) * (1 - ss((x - 2.5) / .3)), 0, 0, .3)
    put(B, pad([138.59, 207.65, 277.18], 2.2, .8, .6, bright=900), .4, 0, .35)          # 수녀가 나타난다 (낮은 합창 결)
    for i, f in enumerate([587.33, 739.99, 880, 1174.66, 1479.98]): put(B, soft(f, .8), 1.2 + i * .15, (i - 2) / 3, .1)   # 잔이 오른다
    rv = hp(noise(.7), 1500) * (T(.7) / .7) ** 3; put(B, rv, 1.9, 0, .3)                 # 거꾸로 차오름
    put(B, thump(48, 1.2), 2.6, 0, .8)
    put(B, pad(SWEET, 5.2, .25, 2.2, bright=3000), 2.6, 0, .55)
    for i, f in enumerate(SWEET): put(B, bell(f * 2, 1.6), 2.62 + i * .03, (i - 2) / 2.5, .1)
    for k in range(3): put(B, whoosh(.7, 300, 2400, .25), 3.0 + k * .18, (-1) ** k * .6)
    z = crush(bp(noise(.3), 1200, 8000) * env(.3, .002, .1), 3, 10); put(B, z, 4.25, -.3, .35); put(B, z[::-1].copy(), 4.38, .3, .25)
    g = sweep(140, 38, .6) * env(.6, .01, .25); put(B, crush(g, 4, 8) * .6 + g * .4, 4.22, 0, .45)   # 그림자가 뒤틀린다
    put(B, bell(138.59, 2.6) * .6, 4.6, 0, .35); put(B, soft(69.3, 3.2), 4.6, 0, .35)
    return reverb(B, 2.8, .35)

def karma():
    d = 2.2; B = buf(d); put(B, crackle(1.0, .6), 0, 0); put(B, np.sign(np.sin(2 * np.pi * 60 * T(1.0))) * .12 * env(1.0, .02, .5), 0)
    sw = sweep(2200, 220, 1.0) * np.sin(np.pi * T(1.0)) ** 1.5; put(B, sw, .3, 0, .2)
    z = crush(bp(noise(.08), 1500, 9000) * env(.08, .001, .03), 3, 12)
    for at in (.1, .55, .9): put(B, z, at, rng.uniform(-.6, .6), .5)
    put(B, bell(233.08, 1.2), 1.0, 0, .2); return reverb(B, 1.8, .25)

def bin_(full):
    d = 5.2 if full else 1.8; B = buf(d); x = T(d)
    put(B, pad(SWEET[:3], d - .1, .9 if full else .3, .8 if full else .5, bright=1600), .05, 0, .4)
    put(B, (np.sin(2 * np.pi * 41 * x)) * ss(x / .5) * (1 - ss((x - d + .6) / .6)), 0, 0, .3)
    a0 = .6 if full else .05
    for i, f in enumerate([277.18, 349.23, 415.3, 523.25, 698.46, 830.61]): put(B, soft(f, .9), a0 + i * (.08 if full else .04), (i - 2.5) / 3, .12)
    if full: put(B, pad([69.3, 103.83, 138.59], 3.2, .5, 1.5, bright=700), 1.3, 0, .45); put(B, bell(554.37, 1.5), 1.3, 0, .15)
    else: put(B, bell(554.37, 1.0), .15, 0, .14)
    return reverb(B, 2.2, .3)

def brk(full):
    d = 1.6 if full else 1.2; B = buf(d); n = 60 if full else 32
    for k in range(n): at = rng.random() ** 1.5 * (.7 if full else .45); f = rng.choice(SWEET) * rng.choice([2, 4]); put(B, soft(f, .18), at, rng.uniform(-.9, .9), .08 * (1 - at))
    put(B, whoosh(.9 if full else .6, 400, 5000, .35), 0, 0); put(B, thump(60, .4), 0, 0, .3); return reverb(B, 1.6, .3)

def p2():
    d = 2.7; B = buf(d); put(B, thump(52, .6), .28, 0, .7); put(B, bell(622.25, 1.0), .28, 0, .15)
    for i in range(5): put(B, sweep(900 - i * 60, 220, .7) * env(.7, .02, .35), .32 + i * .04, (i - 2) / 3, .08)
    for i in range(5): put(B, sweep(220, 900 + i * 60, .7) * env(.7, .5, .2)[::-1].copy() * np.sin(np.pi * T(.7) / .7), 1.0 + i * .04, (2 - i) / 3, .08)
    put(B, pad(SWEET, 1.0, .05, .6, bright=2800), 1.7, 0, .45); return reverb(B, 2.0, .3)

def end_moon():
    music = rd(os.path.join(SRC, 'j_end_d.mp3')); d = 4.6 + music.shape[1] / SR; B = buf(d); x = T(4.8)
    for k in range(40): put(B, soft(rng.choice(SWEET) * 2, .25), .3 + rng.random() ** 1.4 * 1.3, rng.uniform(-.8, .8), .06)
    put(B, soft(1174.66, 1.4), 1.2, 0, .12); put(B, pad(MOON, 3.6, .8, 1.2, bright=2000), 1.4, 0, .35)
    sh = sum(np.sin(2 * np.pi * f * T(2.4) * (1 + .5 * T(2.4) / 2.4)) for f in (1760, 2217, 2637)) * np.sin(np.pi * T(2.4) / 2.4) ** 2 / 3; put(B, sh, 3.0, 0, .12)
    put(B, bell(1864.66, 1.0), 5.3, 0, .1)
    B = reverb(B, 2.4, .3); put(B, music[0], 4.6, -1, 1.414); put(B, music[1], 4.6, 1, 1.414); return B

def end_dream():
    music = rd(os.path.join(SRC, 'j_end_d.mp3')); d = 4.2 + music.shape[1] / SR; B = buf(d)
    put(B, pad(SWEET, 4.6, 1.6, 1.0, bright=1400), 0, 0, .4)
    for k in range(6): put(B, thump(45, .3), .6 + k * (.55 + k * .12), 0, .3 * (1 - k / 7))     # 느려지는 박동
    t0 = .9
    while t0 < 4.0: put(B, hp(noise(.008), 2500) * env(.008, .0005, .002), t0, rng.uniform(-.9, .9), .1); t0 += .02 + .25 * abs(t0 - 2.2) / 1.8 * rng.random()
    t0 = 5.0
    while t0 < 6.1: put(B, bp(noise(.02), 1500, 5000) * env(.02, .001, .006), t0, .2, .4); t0 += rng.uniform(.05, .11)
    put(B, bell(2093, .6), 6.15, .3, .15)
    B = reverb(B, 2.2, .3); put(B, music[0], 4.2, -1, 1.414); put(B, music[1], 4.2, 1, 1.414); return B

os.makedirs(OUT, exist_ok=True)
save('j_bx_seal', seal(False)); save('j_bx_empty', seal(True)); save('j_bx_desc', desc()); save('j_bx_karma', karma())
save('j_bx_in', bin_(True)); save('j_bx_in_s', bin_(False)); save('j_bx_brk', brk(True)); save('j_bx_brk_s', brk(False)); save('j_bx_p2', p2())
save('j_end_bxmoon', end_moon(), -16.0); save('j_end_bxdream', end_dream(), -16.0)
