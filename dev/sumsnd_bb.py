"""BB 전용 소환 소리: 기본 소환(j_summon) 앞부분 → 1.35초 가로채기(어긋남) → 문 캔서 소리(sumsnd2 moon). 사용: python3 sumsnd_bb.py <j_summon.mp3> <moon.wav> <out.wav>"""
import sys, subprocess, numpy as np, wave
SR=48000
def rd(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-f','s16le','-ac','2','-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(raw,'<i2').reshape(-1,2).T.astype(float)/32768
base, moon = rd(sys.argv[1]), rd(sys.argv[2]); N=moon.shape[1]; base=np.pad(base,((0,0),(0,max(0,N-base.shape[1]))))[:, :N]
t=np.arange(N)/SR; ss=lambda x: (lambda y: y*y*(3-2*y))(np.clip(x,0,1))
gB=1-ss((t-1.30)/.45); gM=ss((t-1.30)/.6)
out=base*gB*.9+moon*gM
# 가로채는 순간: 기본 소리 1.15~1.27초 조각을 깎아서 짧게 되풀이
seg=base[:, int(1.15*SR):int(1.27*SR)]; pos=1.32; L=.07; rng=np.random.default_rng(3)
while pos<1.75 and L>.012:
    n=int(L*SR); q=np.round(np.repeat(seg[:, :n:5],5,axis=1)[:, :n]*8)/8; i=int(pos*SR); out[:, i:i+n]+=q*.8*np.linspace(1,.3,n); pos+=L+.01; L*=.8
# 지시봉을 톡: 2.72초 높은 딱
x=np.arange(int(.12*SR))/SR; tick=(np.sin(2*np.pi*3200*x)+.5*np.sin(2*np.pi*5100*x))*np.exp(-x/.012); i=int(2.72*SR); out[:, i:i+len(x)]+=tick*.35
out=out/np.abs(out).max()*.89
w=wave.open(sys.argv[3],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out.T,-1,1)*32767).astype('<i2').tobytes()); w.close(); print(sys.argv[3])
