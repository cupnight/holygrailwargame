"""소환 연출 소리 · 문 캔서(moon) · 얼터 에고(ego). 모두 직접 합성 (11-12 시안)
연출 시간표: 0~2.8초 모임 · 2.8초 터짐 · 3~5.7초 이름 · 5.7~6.65초 날아가 내려앉음 · 8.2초
사용: python3 sumsnd2.py <moon|ego> <out.wav>"""
import sys, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
SR = 48000; DUR = 8.2; N = int(SR * DUR)
rng = np.random.default_rng(11)
t = np.arange(N) / SR

def env(a, d, length):  # 빠른 시작 · 지수 감쇠
    n = int(length * SR); x = np.arange(n) / SR
    e = np.minimum(1, x / max(a, 1e-4)) * np.exp(-np.maximum(0, x - a) / max(d, 1e-4)); return e

def put(buf, sig, at, pan=0.0, g=1.0):
    i = int(at * SR); n = min(len(sig), N - i)
    if n <= 0: return
    l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan))
    buf[0, i:i + n] += sig[:n] * g * l; buf[1, i:i + n] += sig[:n] * g * r

def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def crush(x, bits=5, hold=6):
    y = np.repeat(x[::hold], hold)[:len(x)]; q = 2 ** (bits - 1); return np.round(y * q) / q
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def bell(f, d, n=None):
    L = d * 4; x = np.arange(int(L * SR)) / SR
    m = 2.0 * np.exp(-x / (d * .4)); return np.sin(2 * np.pi * f * x + m * np.sin(2 * np.pi * f * 3.5 * x)) * np.exp(-x / d)
def reverb(buf, sec=2.2, wet=.28):
    n = int(sec * SR); x = np.arange(n) / SR; out = np.zeros_like(buf)
    for c in range(2):
        ir = rng.standard_normal(n) * np.exp(-x / (sec / 6.9)); ir = lp(ir, 7000); ir /= np.sqrt((ir ** 2).sum())
        out[c] = buf[c] + wet * fftconvolve(buf[c], ir)[:N]
    return out
def whoosh(at, dur, lo, hi, g):  # 날아가는 바람
    n = int(dur * SR); x = np.linspace(0, 1, n); s = rng.standard_normal(n)
    y = np.zeros(n); seg = 2400
    for k in range(0, n, seg):
        f = lo * (hi / lo) ** x[k]; y[k:k + seg] = bp(s[k:k + seg], f * .7, min(f * 1.4, 20000), 1)
    return y * np.sin(np.pi * x) ** 1.5 * g

def moon():
    B = np.zeros((2, N))
    # 낮은 바탕음과 달빛 화음(B♭ 단조 add9), 모일수록 커진다
    rise = ss(t / 2.8) * (t < 2.8) + (t >= 2.8) * np.exp(-np.maximum(0, t - 2.8) / 1.4)
    drone = (np.sin(2 * np.pi * 55 * t) + .4 * np.sin(2 * np.pi * 110 * t + .3)) * (.15 + .5 * rise) * (t < 2.78)
    put(B, drone, 0, 0, .35)
    for f, p in [(233.08, -.3), (277.18, .3), (349.23, -.1), (523.25, .2)]:
        tri = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * f * t * (1 + .002 * np.sin(2 * np.pi * .3 * t))))
        put(B, tri * rise * (t < 2.78) * .07 + tri * (t >= 2.8) * np.exp(-np.maximum(0, t - 2.8) / 2.2) * .05, 0, p)
    # 데이터 삐삐: 짧은 네모파, 점점 촘촘하게 (비트를 깎은 소리)
    pent = [1046.5, 1174.7, 1396.9, 1568, 1864.7, 2093, 2349.3, 2793.8]
    tt = .4
    while tt < 2.7:
        f = pent[rng.integers(len(pent))]; L = .03 + rng.random() * .04; x = np.arange(int(L * SR)) / SR
        sq = np.sign(np.sin(2 * np.pi * f * x)) * np.exp(-x / (L * .5))
        put(B, crush(sq, 4, 4), tt, rng.uniform(-.8, .8), .09 + .1 * ss(tt / 2.8)); tt += .22 * (1 - .8 * ss(tt / 2.6)) + rng.random() * .05
    # 올라가는 소리 (반쯤 깎음)
    x = t[t < 2.75]; ph = 2 * np.pi * np.cumsum(200 * (8 ** (x / 2.75))) / SR
    sw = np.sin(ph) * ss(x / 2.75) ** 2; put(B, .6 * sw + .4 * crush(sw, 5, 8), 0, 0, .12)
    # 어긋남: 2.45~2.77초 짧은 조각을 점점 빠르게 되풀이
    mix = B[:, int(2.3 * SR):int(2.42 * SR)].copy(); pos = 2.45; L = .09
    while pos < 2.76:
        n = int(L * SR); put(B, crush(mix[0, :n], 6, 3) * 1.6, pos, -.4); put(B, crush(mix[1, :n], 6, 3) * 1.6, pos, .4); pos += L; L *= .72
        if L < .012: break
    B[:, int(2.77 * SR):int(2.8 * SR)] *= np.linspace(1, 0, int(.03 * SR))   # 터지기 직전 0.03초 비움
    # 터짐: 낮은 쿵 · 깎인 잡음 · 종 화음 · 다시 쓰는 '지직' 세 번
    x = np.arange(int(1.2 * SR)) / SR; thump = np.sin(2 * np.pi * (35 * x + 30 * (1 - np.exp(-x / .08)) * .08)) * np.exp(-x / .35)
    put(B, thump, 2.8, 0, .9)
    nz = rng.standard_normal(int(.9 * SR)) * env(.002, .18, .9); put(B, crush(hp(nz, 300), 5, 10), 2.8, -.2, .35); put(B, crush(hp(nz[::-1].copy(), 300), 5, 10) * env(.002, .18, .9), 2.8, .2, .35)
    for k, (f, p) in enumerate([(932.33, -.5), (1108.7, .5), (1396.9, -.2), (2093, .3), (466.16, 0)]):
        put(B, bell(f, 1.1 + .3 * k), 2.8 + k * .012, p, .16)
    for at in (2.8, 2.95, 3.06):
        z = rng.standard_normal(int(.07 * SR)) * env(.001, .03, .07); put(B, crush(bp(z, 1500, 9000), 3, 12), at, rng.uniform(-.7, .7), .5)
    # 가라앉는 데이터: 내려가는 삐삐
    for k in range(10):
        f = pent[-1 - (k % len(pent))] / (1 + k * .05); L = .05; x = np.arange(int(L * SR)) / SR
        put(B, crush(np.sign(np.sin(2 * np.pi * f * x)) * np.exp(-x / .02), 4, 4), 3.2 + k * .16, (-1) ** k * .5, .06 * (1 - k / 12))
    # 날아감 · 내려앉음
    put(B, whoosh(5.75, .95, 400, 2600, .25), 5.75, .2)
    x = np.arange(int(.25 * SR)) / SR; tok = np.sin(2 * np.pi * 180 * x * np.exp(-x * 4)) * np.exp(-x / .05)
    put(B, tok, 6.62, 0, .5); put(B, crush(bell(1864.7, .25), 5, 4), 6.64, .3, .12)
    return reverb(B, 2.2, .3)

def ego():
    B = np.zeros((2, N))
    rise = ss(t / 2.8)
    # 세 여신의 목소리: 어긋난 세 음이 미끄러져 하나의 화음(A · E · A)으로 합쳐진다
    for (f0, f1, p) in [(207.65, 220.0, -.6), (311.13, 329.63, .6), (466.16, 440.0, 0)]:
        fr = np.where(t < 2.8, f0 + (f1 - f0) * ss(t / 2.7), f1)
        vib = 1 + .004 * np.sin(2 * np.pi * 5.2 * t) * (1 - ss((t - 2.6) / .4))
        ph = 2 * np.pi * np.cumsum(fr * vib) / SR
        v = (np.sin(ph) + .3 * np.sin(2 * ph) + .12 * np.sin(3 * ph))
        amp = np.where(t < 2.8, .15 + .55 * rise, 1.0) * np.where(t < 2.8, 1, np.exp(-np.maximum(0, t - 2.8) / 2.0) * 1.2)
        put(B, v * amp, 0, p, .07)
    # 물: 느리게 일렁이는 잡음
    nz = rng.standard_normal(N); water = bp(nz, 250, 1400) * (.4 + .6 * np.sin(2 * np.pi * .4 * t) ** 2) * (.2 + .8 * rise) * np.where(t < 2.78, 1, np.exp(-np.maximum(0, t - 2.8) / .6))
    put(B, water, 0, 0, .12)
    # 물방울: 높이가 뚝 떨어지는 짧은 울림, 점점 잦아진다
    def drop(f):
        L = .18; x = np.arange(int(L * SR)) / SR; fr = f * (1 + 1.6 * np.exp(-x / .012)); return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-x / .05)
    tt = .3
    while tt < 2.75:
        put(B, drop(rng.uniform(700, 1700)), tt, rng.uniform(-.8, .8), .12 + .1 * rise[int(tt * SR)]); tt += .25 * (1 - .75 * ss(tt / 2.6)) + rng.random() * .08
    B[:, int(2.77 * SR):int(2.8 * SR)] *= np.linspace(1, 0, int(.03 * SR))
    # 터짐: 깊은 쿵 · 물보라 · 유리 조각
    x = np.arange(int(1.4 * SR)) / SR; put(B, np.sin(2 * np.pi * 45 * x * (1 + .5 * np.exp(-x / .05))) * np.exp(-x / .45), 2.8, 0, .85)
    sp = rng.standard_normal(int(1.2 * SR)); splash = lp(sp, 3500) * env(.004, .25, 1.2); put(B, splash, 2.8, -.25, .45); put(B, lp(sp[::-1].copy(), 3500) * env(.004, .25, 1.2), 2.8, .25, .45)
    for k in range(46):
        at = 2.8 + rng.random() ** 1.6 * .7; f = rng.uniform(2200, 7500); L = rng.uniform(.06, .35); x = np.arange(int(L * SR)) / SR
        put(B, np.sin(2 * np.pi * f * x) * np.exp(-x / (L * .35)) * (1 - (at - 2.8) / .9), at, rng.uniform(-.9, .9), .07)
    for f, p in [(440, -.4), (659.25, .4), (880, 0), (1318.5, .2)]:
        put(B, bell(f, 1.6), 2.82, p, .13)
    # 번지는 물결: 물방울 메아리
    for k in range(5): put(B, drop(1100 - k * 90), 3.15 + k * .32, (-1) ** k * .5, .14 * (1 - k / 6))
    put(B, whoosh(5.75, .95, 300, 2000, .22), 5.75, -.2)
    put(B, drop(520), 6.62, 0, .45)
    return reverb(B, 2.6, .34)

kind, out = sys.argv[1], sys.argv[2]
B = {'moon': moon, 'ego': ego}[kind]()
B = B / (np.abs(B).max() + 1e-9) * .89
import wave
w = wave.open(out, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(B.T, -1, 1) * 32767).astype('<i2').tobytes()); w.close(); print(out)
