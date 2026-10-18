"""Daily screener snapshot from NSE end-of-day data.

Outputs out/screener.json with breadth, 52-week highs/lows, volume shockers,
circuit hits (upper/lower) and sector movers for the latest session.

Circuit hits are inferred from prices: a stock counts as an upper (lower) circuit when it
closed at the day's high (low) and its change matches an NSE price band (2/5/10/20%) within
0.15 points. NSE does not publish bands in the EOD file, so this is an approximation.
"""
import csv, json, os
import numpy as np
import pandas as pd

PX, OUT = 'px', 'out'
meta = {r['symbol']: r for r in csv.DictReader(open('master.csv'))}
rs = {s['s']: s['rs'] for s in json.load(open(f'{OUT}/data.json'))['stocks']}
asof = pd.read_csv(f'{PX}/nifty_500.csv', parse_dates=['Date'])['Date'].max()

rows = []
for sym, m in meta.items():
    f = f'{PX}/{sym.lower()}.csv'
    if not os.path.exists(f):
        continue
    df = pd.read_csv(f, usecols=['Date', 'High', 'Low', 'Close', 'Volume'], parse_dates=['Date'])
    df = df.dropna(subset=['Close']).drop_duplicates('Date').sort_values('Date').tail(300)
    if len(df) < 2 or df['Date'].iloc[-1] != asof:
        continue
    c, h, l, v = (df[k].to_numpy(float) for k in ('Close', 'High', 'Low', 'Volume'))
    d1 = (c[-1] / c[-2] - 1) * 100
    prev_h = h[-252:-1].max() if len(h) > 21 else np.nan
    prev_l = l[-252:-1].min() if len(l) > 21 else np.nan
    avg50 = v[-51:-1].mean() if len(v) > 21 else np.nan
    vx = v[-1] / avg50 if avg50 and avg50 > 0 else np.nan
    ema = lambda span: pd.Series(c).ewm(span=span, adjust=False).mean().iloc[-1]
    band = None
    for b in (2, 5, 10, 20):
        if abs(abs(d1) - b) <= 0.15:
            band = b
    up_c = band is not None and d1 > 0 and c[-1] >= h[-1]
    lo_c = band is not None and d1 < 0 and c[-1] <= l[-1]
    rows.append(dict(
        s=sym, sec=m['sector'], p=round(c[-1], 2), d1=round(d1, 2),
        hi=bool(len(h) >= 252 and h[-1] >= prev_h), lo=bool(len(l) >= 252 and l[-1] <= prev_l),
        vx=None if np.isnan(vx) else round(vx, 1), to=round(c[-1] * v[-1] / 1e7, 2),
        uc=band if up_c else None, lc=band if lo_c else None,
        e50=None if len(c) < 200 else bool(c[-1] > ema(50)), e200=None if len(c) < 200 else bool(c[-1] > ema(200)),
        rs=rs.get(sym),
    ))

df = pd.DataFrame(rows)
def pick(d, cols):
    # pandas turns missing values into NaN, which is not valid JSON; write them as null
    clean = lambda v: None if isinstance(v, float) and v != v else v
    return [{k: clean(v) for k, v in r.items()} for r in d[cols].to_dict('records')]
base = ['s', 'sec', 'p', 'd1', 'vx', 'to', 'rs']

hi = df[df.hi].sort_values('d1', ascending=False)
lo = df[df.lo].sort_values('d1')
# volume shockers: at least 3x the 50-day average volume, with at least Rs 1 crore traded
vs = df[(df.vx >= 3) & (df.to >= 1)].sort_values('vx', ascending=False)
uc = df[df.uc.notna()].sort_values('d1', ascending=False)
lc = df[df.lc.notna()].sort_values('d1')

sec = []
for name, g in df.groupby('sec'):
    sec.append(dict(name=name, n=int(len(g)), med=round(float(g.d1.median()), 2),
                    up=int((g.d1 > 0).sum()), dn=int((g.d1 < 0).sum())))
sec.sort(key=lambda x: -x['med'])
sec = [x for x in sec if x['n'] >= 10]

e = df.dropna(subset=['e50'])
out = dict(
    asof=str(asof.date()), tracked=int(len(df)),
    adv=int((df.d1 > 0).sum()), dec=int((df.d1 < 0).sum()), unch=int((df.d1 == 0).sum()),
    e50=round(float(e.e50.mean() * 100), 1), e200=round(float(e.e200.mean() * 100), 1),
    hi=pick(hi, base), lo=pick(lo, base), vs=pick(vs, base),
    uc=pick(uc, base + ['uc']), lc=pick(lc, base + ['lc']),
    top=sec[:8], worst=sec[::-1][:8],
)
json.dump(out, open(f'{OUT}/screener.json', 'w'), separators=(',', ':'), default=lambda o: None, allow_nan=False)
print({k: (len(v) if isinstance(v, list) else v) for k, v in out.items()})
print('top', [(x['name'], x['med']) for x in out['top'][:3]], 'worst', [(x['name'], x['med']) for x in out['worst'][:3]])
print('size', os.path.getsize(f'{OUT}/screener.json'))
