"""BB 전용 소환 소리(9.5초): 기본 소환(j_summon) 앞 2.6초 → 가로채기(어긋남) → 1.3초 늦춘 문 캔서 소리(sumsnd2 moon). 사용: python3 sumsnd_bb.py <j_summon.mp3> <moon.wav> <out.wav>"""
import sys, subprocess, numpy as np, wave
SR=48000
def rd(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-f','s16le','-ac','2','-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(raw,'<i2').reshape(-1,2).T.astype(float)/32768
base, moon = rd(sys.argv[1]), rd(sys.argv[2]); SH=int(1.3*SR); moon=np.pad(moon,((0,0),(SH,0))); N=moon.shape[1]; base=np.pad(base,((0,0),(0,max(0,N-base.shape[1]))))[:, :N]
t=np.arange(N)/SR; ss=lambda x: (lambda y: y*y*(3-2*y))(np.clip(x,0,1))
gB=1-ss((t-2.58)/.3); gM=ss((t-2.6)/.6)
out=base*gB*.9+moon*gM
# 가로채는 순간: 기본 소리 1.15~1.27초 조각을 깎아서 짧게 되풀이
seg=base[:, int(2.42*SR):int(2.56*SR)]; pos=2.62; L=.07; rng=np.random.default_rng(3)
while pos<3.1 and L>.012:
    n=int(L*SR); q=np.round(np.repeat(seg[:, :n:5],5,axis=1)[:, :n]*8)/8; i=int(pos*SR); out[:, i:i+n]+=q*.8*np.linspace(1,.3,n); pos+=L+.01; L*=.8
# 지시봉을 톡: 2.72초 높은 딱
x=np.arange(int(.12*SR))/SR; tick=(np.sin(2*np.pi*3200*x)+.5*np.sin(2*np.pi*5100*x))*np.exp(-x/.012); i=int(4.02*SR); out[:, i:i+len(x)]+=tick*.35
# 치직: 2.58~3.25초 띄엄띄엄 끊기는 잡음 + 낮은 웅 소리, 앞서 2.18 · 2.44초에 짧은 예고
def crackle(at,dur,g):
    n=int(dur*SR); z=rng.standard_normal((2,n)); from scipy.signal import butter,sosfilt
    z=sosfilt(butter(2,[700,7000],'band',fs=SR,output='sos'),z); gate=np.zeros(n); k=0
    while k<n: L=int(rng.uniform(.012,.06)*SR); gate[k:k+L]=rng.random()<.65; k+=L
    e=np.minimum(1,np.arange(n)/(.02*SR))*np.minimum(1,(n-np.arange(n))/(.08*SR)); i=int(at*SR); out[:, i:i+n]+=z*gate*e*g
    hum=np.sign(np.sin(2*np.pi*60*np.arange(n)/SR))*.25*e*gate; out[:, i:i+n]+=hum*g*.5
crackle(2.58,.67,.55); crackle(2.16,.07,.3); crackle(2.42,.06,.3)
out=out/np.abs(out).max()*.89
w=wave.open(sys.argv[3],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out.T,-1,1)*32767).astype('<i2').tobytes()); w.close(); print(sys.argv[3])
