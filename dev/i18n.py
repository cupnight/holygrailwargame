"""게임 파일의 번역 사전(I18N_DICT)과 문장 틀(I18N_TPL)에 항목을 더한다."""
import json, re

def _blk(s, name):
    m = re.search(r'const ' + name + r'=(\{.*?\});\n', s, re.S)
    return m, json.loads(m.group(1))

def add(s, dict_items=(), tpl_items=(), overwrite=False):
    """dict_items/tpl_items: (ko, en, ja) 묶음. 이미 있는 번역은 overwrite가 아니면 그대로 둔다."""
    nd = nt = 0
    if dict_items:
        m, D = _blk(s, 'I18N_DICT')
        for ko, en, ja in dict_items:
            if ko in D['en'] and not overwrite: continue
            D['en'][ko] = en; D['ja'][ko] = ja; nd += 1
        s = s[:m.start(1)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
    if tpl_items:
        m, T = _blk(s, 'I18N_TPL')
        for ko, en, ja in tpl_items:
            for lang, v in (('en', en), ('ja', ja)):
                L = T[lang]; hit = [x for x in L if x[0] == ko]
                if hit:
                    if overwrite: hit[0][1] = v
                    continue
                L.append([ko, v]); nt += 1
        s = s[:m.start(1)] + json.dumps(T, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
    return s, nd, nt
