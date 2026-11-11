# 4차(스즈카 · 캣) 추가 규칙: 성향 · 해체 말투 · 마성 · 매료 마안 · 캣의 낮잠
import sys
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read(); miss = []
    def R(o, n, opt=False):
        global s
        k = s.count(o)
        if k != 1:
            if not opt: miss.append((o[:60], k))
            return
        s = s.replace(o, n)
    # 공식 성향
    R("bb:'CE',meltryllis:'LG',passionlip:'LB',", "bb:'CE',meltryllis:'LG',passionlip:'LB',suzuka:'NE',tamamocat:'CG',")
    # 해체로 말하는 서번트 (기준 파일에는 이 표가 없다)
    R('const CAS_V=new Set(["meltryllis", ', 'const CAS_V=new Set(["suzuka", "meltryllis", ', opt=True)
    # 마성: 천마의 딸 · 여우 꼬리의 분신
    R("const DEMONIC={ibaraki:1,shuten:1,raikou:1,medusa:1,tamamo:1};", "const DEMONIC={ibaraki:1,shuten:1,raikou:1,medusa:1,tamamo:1,suzuka:1,tamamocat:1};")
    # 마안(매료): 남성 서번트에게 더 잘 듣는다 (방해 값 +55%)
    R("  function SV(h,kind){ return skillsOf(h).filter(x=>x.k===kind).reduce((a,x)=>a+RANKV[x.r],0); }",
      "  function SV(h,kind){ return skillsOf(h).filter(x=>x.k===kind).reduce((a,x)=>a+RANKV[x.r],0); }\n"
      "  // 마안(매료): 상대가 남성 서번트면 방해가 더 잘 듣는다\n"
      "  const charmX=(h,o)=>{ if(!h||!o||o.fem) return 0; const k=skillsOf(h).find(x=>x.n==='마안(매료)'); return k?RANKV[k.r]*.6:0; };")
    R("let sab=SV(h,'sabotage')*1.1, eSab=SV(eh2,'sabotage')*1.1;", "let sab=SV(h,'sabotage')*1.1+charmX(h,eh2), eSab=SV(eh2,'sabotage')*1.1+charmX(eh2,h);")
    R("const sabOf=x=>{ const o=x.o; let v=SV(x.h,'sabotage')*1.1;", "const sabOf=x=>{ const o=x.o; let v=SV(x.h,'sabotage')*1.1+charmX(x.h,o.h);")
    # 캣의 낮잠: 보구를 쓴 다음 합은 합 −30, 그 뒤 두 합 동안 체력 +8, 그동안 보구 봉인
    R("const FX_KO={field:'영역',wall:'방벽',sup:'보조',counter:'받아치기',holmes:'간파',pig:'변이',self:'강화',rev:'되돌림'};",
      "const FX_KO={field:'영역',wall:'방벽',sup:'보조',counter:'받아치기',holmes:'간파',pig:'변이',self:'강화',rev:'되돌림',nap:'낮잠'};\n"
      "  const NAP_P=30, NAP_H=8;")
    R("if(f.type==='pig') return own?0:f.ehap;", "if(f.type==='pig') return own?0:f.ehap;\n    if(f.type==='nap') return own&&b.round===f.start?-NAP_P:0;")
    R("const npNoNP=(b,side)=>{ const pg=fxGet(b,npOther(side),'pig'), su=fxGet(b,npOther(side),'sup'); return !!(pg&&pg.lock)||!!(su&&(SUP_SP[su.id]||{}).ban); };",
      "const npNoNP=(b,side)=>{ const pg=fxGet(b,npOther(side),'pig'), su=fxGet(b,npOther(side),'sup'); return !!(pg&&pg.lock)||!!(su&&(SUP_SP[su.id]||{}).ban)||!!fxGet(b,side,'nap'); };")
    R("if(npRole(h)==='S'&&!fxGet(b,'me','self')) fxL(b).push({side:'me',type:'self',id:h.id,left:99,age:0});",
      "if(npRole(h)==='S'&&!fxGet(b,'me','self')) fxL(b).push({side:'me',type:'self',id:h.id,left:99,age:0});\n"
      "    if(h.id==='tamamocat'&&!fxGet(b,'me','nap')) fxL(b).push({side:'me',type:'nap',id:h.id,start:b.round+1,left:4,age:0});")
    R("if(npRole(H_BY[e.hero])==='S'&&!fxGet(b,'en','self')) fxL(b).push({side:'en',type:'self',id:e.hero,left:99,age:0});",
      "if(npRole(H_BY[e.hero])==='S'&&!fxGet(b,'en','self')) fxL(b).push({side:'en',type:'self',id:e.hero,left:99,age:0});\n"
      "    if(e.hero==='tamamocat'&&!fxGet(b,'en','nap')) fxL(b).push({side:'en',type:'nap',id:e.hero,start:b.round+1,left:4,age:0});")
    R("      if(f.type==='rev'){ if(b.round>=f.start) fxDrop(b,f); continue; }",
      "      if(f.type==='rev'){ if(b.round>=f.start) fxDrop(b,f); continue; }\n"
      "      if(f.type==='nap'){ const me=f.side==='me', who=me?h.name:pName(b.e);\n"
      "        if(b.round<f.start) log(`${who}${J(who,이)} 보구를 다 쓰고 그 자리에 드러누웠다. 다음 합은 낮잠이다.`,me?'loss':'war');\n"
      "        else if(b.round===f.start) log(`${who}${J(who,이)} 기지개를 켜며 일어났다. 두 합 동안 상처가 아문다.`,me?'war':'loss');\n"
      "        else { if(me){ if(w.hp>0) w.hp=clamp(w.hp+NAP_H); } else if(b.e.hp>0) b.e.hp=clamp(b.e.hp+NAP_H); log(`낮잠 덕분에 ${who}의 상처가 아문다. 체력 +${NAP_H}`,me?'war':'loss'); }\n"
      "        f.age++; f.left--; if(f.left<=0) fxDrop(b,f); continue; }")
    # NPC끼리의 싸움
    R("if(x.h.id==='karna') x.p.kavacha=1; };", "if(x.h.id==='karna') x.p.kavacha=1; if(x.h.id==='tamamocat'&&!get(x,'nap')) x.fx.push({type:'nap',id:x.h.id,start:0,left:4,age:0}); };")
    R("const noNP=x=>{ const pg=get(x.o,'pig'), su=get(x.o,'sup'); return !!(pg&&pg.lock)||!!(su&&(SUP_SP[su.id]||{}).ban); };",
      "const noNP=x=>{ const pg=get(x.o,'pig'), su=get(x.o,'sup'); return !!(pg&&pg.lock)||!!(su&&(SUP_SP[su.id]||{}).ban)||!!get(x,'nap'); };")
    R("else if(f.type==='rev') v+=f.v;", "else if(f.type==='rev') v+=f.v; else if(f.type==='nap'){ if(f.start===r) v-=NAP_P; }")
    R("        if(f.type==='counter'||f.type==='rev'){ if(r>=f.start) drop(x,f); continue; }",
      "        if(f.type==='counter'||f.type==='rev'){ if(r>=f.start) drop(x,f); continue; }\n"
      "        if(f.type==='nap'){ if(!f.start) f.start=r+1; else if(r>f.start&&x.p.hp>0) x.p.hp=clamp(x.p.hp+NAP_H*K); f.left--; if(f.left<=0) drop(x,f); continue; }")
    open(p, 'w', encoding='utf-8').write(s); print(p[-22:], 'miss', miss)
