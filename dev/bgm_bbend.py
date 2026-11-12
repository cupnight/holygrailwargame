"""BB가 성배를 달로 가져간 결말(⑤ 달로 간 잔)의 결말 음악 (11-12, 사용자 제공 곡 「last piece again · peaceful」, C 장조 96 BPM · 3분 48초).
- end_f.mp3 : 결과 화면 배경음악. 처음 26초는 잔잔한 도입, 26.5초에 본 곡이 들어온다. 곡이 끝나고 울림이 잦아든 223.0초에서
  본 곡이 들어오기 직전(26.3초, 아직 조용한 자리)으로 되감는다 — 조용한 곳끼리 잇기 때문에 이음매가 들리지 않는다.
- j_end_f.mp3 : 결말 연출 · 연출을 껐을 때 울리는 짧은 판. 본 곡이 들어오는 26.3초부터 12초, 끝 2.5초는 서서히 줄인다.
사용: python3 bgm_bbend.py <원곡.wav> <소리 폴더>  → 마지막 줄에 소리 목록 항목"""
import sys, subprocess, os, numpy as np, wave
SR = 48000; LS, LE, TAIL = 26.3, 223.0, .5
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
X = np.frombuffer(raw, '<i2').reshape(-1, 2).T.astype(float) / 32768; OUT = sys.argv[2]
def enc(Y, name, lufs):
    w = os.path.join(OUT, name + '.wav'); ww = wave.open(w, 'wb'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes((np.clip(Y.T, -1, 1) * 32767).astype('<i2').tobytes()); ww.close()
    I = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', w, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float([l for l in I.split('\n') if l.strip().startswith('I:')][-1].split()[1])
    subprocess.run(['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', w, '-af', f'volume={lufs - I}dB,alimiter=limit=0.89:level=false:attack=2:release=60', '-ar', '48000', '-b:a', '160k', os.path.join(OUT, name + '.mp3')]); os.remove(w)
    return Y.shape[1] / SR
Y = X[:, :int((LE + TAIL) * SR)]
d = enc(Y, 'end_f', -18.0)
a = int(LS * SR); n = int(12 * SR); J = X[:, a:a + n].copy(); f = int(2.5 * SR); J[:, -f:] *= np.linspace(1, 0, f) ** 1.5
enc(J, 'j_end_f', -16.0)
print(f'"end_f":{{"d":{d:.2f},"ls":{LS},"le":{LE}}}')
