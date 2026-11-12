"""키아라 전투 배경음악(11-12, 사용자 제공 곡): 반복 구간을 정하고 이음매를 미리 섞어 둔 뒤 다른 배경음악과 같은 크기·형식으로 맞춘다.
반복: 16.41초 → 40.39초 (8마디, 약 24초). 반복 끝 0.35초는 반복 시작 직전 소리로 서서히 바뀌게 섞어 두어, 되감을 때 이음매가 들리지 않는다.
사용: python3 bgm_kiara.py <원곡.mp3> <출력.mp3>  → 마지막 줄에 소리 목록 항목을 찍는다"""
import sys, subprocess, numpy as np, os
SR = 48000; LS, LE, XF, TAIL = 16.41, 40.39, .35, .5
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
X = np.frombuffer(raw, '<i2').reshape(-1, 2).T.astype(float) / 32768
a, b, n = int(LE * SR), int(LS * SR), int(XF * SR)
u = np.linspace(0, 1, n); gi, go = np.sin(u * np.pi / 2), np.cos(u * np.pi / 2)
mix = X[:, a - n:a] * go + X[:, b - n:b] * gi
Y = np.concatenate([X[:, :a - n], mix, X[:, b:b + int(TAIL * SR)]], axis=1)
w = sys.argv[2] + '.wav'; import wave
ww = wave.open(w, 'wb'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes((np.clip(Y.T, -1, 1) * 32767).astype('<i2').tobytes()); ww.close()
I = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', w, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float([l for l in I.split('\n') if l.strip().startswith('I:')][-1].split()[1]); G = -17.4 - I   # 검은 성배 보스 곡(boss)과 같은 크기
subprocess.run(['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', w, '-af', f'volume={G}dB,alimiter=limit=0.89:level=false:attack=2:release=60', '-ar', '48000', '-b:a', '160k', sys.argv[2]]); os.remove(w)
print(f'"kiara":{{"d":{Y.shape[1] / SR:.2f},"ls":{LS},"le":{LE}}}')
