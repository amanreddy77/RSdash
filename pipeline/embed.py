import json, math
d = json.load(open('out/data.json'))
s = json.load(open('out/series.json'))
F = ['s','n','sec','ind','p','d1','m3','m12','rs','dl','whd','to','bd','rb','vhi','vma']
rnd = lambda v: round(v, 1) if isinstance(v, float) else v
stocks = [[(1 if r[k] else 0) if k == 'rb' else rnd(r[k]) for k in F] for r in d['stocks']]
ind = [{k: i[k] for k in ('name','sec','n','avg','chg','w1','m1')} for i in d['industries']]
sec = [{k: i[k] for k in ('name','n','avg','chg')} for i in d['sectors']]
data = dict(asof=d['asof'], universe=d['universe'], breadth=d['breadth'], sectors=sec, industries=ind, f=F, s=stocks)

def enc(arr):
    # [leadingNulls, firstValue, then weekly change in basis points; null = missing week]
    lead = 0
    while lead < len(arr) and arr[lead] is None: lead += 1
    if lead == len(arr): return [lead]
    out = [lead, arr[lead]]
    prev = arr[lead]
    for x in arr[lead+1:]:
        if x is None: out.append(None); continue
        out.append(round((x / prev - 1) * 100000)); prev = x
    return out

ser = dict(dates=s['dates'], bench=s['bench'], c={k: enc(v) for k, v in s['close'].items()}, r=s['rating'])
blob = json.dumps(dict(d=data, sr=ser), separators=(',', ':'))
assert '</' not in blob
open('out/embed.js', 'w').write(blob)
print('embedded payload', round(len(blob) / 1e6, 2), 'MB')

# round-trip check: decode and compare to original closes
def dec(e):
    lead = e[0]; out = [None] * lead
    if len(e) == 1: return out
    x = e[1]; out.append(x)
    for v in e[2:]:
        if v is None: out.append(None); continue
        x = x * (1 + v / 100000); out.append(x)
    return out
worst = 0
for k, v in s['close'].items():
    r = dec(ser['c'][k])
    for a, b in zip(v, r):
        if a is not None and b is not None: worst = max(worst, abs(b / a - 1))
print('max reconstruction error %.4f%%' % (worst * 100))
