"""키아라에게 진 결말(⑥ 단꿈)의 결말 음악 (11-12, 사용자 제공 곡 「bad end · melancholic」, D 단조 · 약 80 BPM · 3분 33초). (원곡은 용량 때문에 저장소에 두지 않는다)
- end_g.mp3 : 결과 화면 배경음악. 곡이 끝나고 울림이 잦아든 208.0초에서 곡이 시작하기 직전(0.45초, 무음)으로 되감는다 — 조용한 곳끼리 잇는다.
- j_end_g.mp3 : 연출을 껐을 때 울리는 짧은 판. 처음 12초, 끝 2.5초는 서서히 줄인다.
사용: python3 bgm_badend.py <원곡> <소리 폴더>"""
import sys, subprocess, os, numpy as np, wave
SR = 48000; LS, LE, TAIL = .45, 208.0, .5
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
X = np.frombuffer(raw, '<i2').reshape(-1, 2).T.astype(float) / 32768; OUT = sys.argv[2]
def enc(Y, name, lufs):
    w = os.path.join(OUT, name + '.wav'); ww = wave.open(w, 'wb'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes((np.clip(Y.T, -1, 1) * 32767).astype('<i2').tobytes()); ww.close()
    I = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', w, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float([l for l in I.split('\n') if l.strip().startswith('I:')][-1].split()[1])
    subprocess.run(['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', w, '-af', f'volume={lufs - I}dB,alimiter=limit=0.89:level=false:attack=2:release=60', '-ar', '48000', '-b:a', '160k', os.path.join(OUT, name + '.mp3')]); os.remove(w)
    return Y.shape[1] / SR
d = enc(X[:, :int((LE + TAIL) * SR)], 'end_g', -18.0)
a = int(LS * SR); n = int(12 * SR); J = X[:, a:a + n].copy(); f = int(2.5 * SR); J[:, -f:] *= np.linspace(1, 0, f) ** 1.5
enc(J, 'j_end_g', -16.0)
print(f'"end_g":{{"d":{d:.2f},"ls":{LS},"le":{LE}}}')
