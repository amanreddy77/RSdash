"""Compute relative-strength data for NSE stocks from end-of-day prices.

Inputs  : px/<symbol>.csv (daily OHLCV, split/bonus adjusted), master.csv (NSE classification)
Outputs : out/data.json   (stocks, sectors, industries, breadth)
          out/series.json (weekly closes per stock + benchmarks, weekly RS rating history)

RS Rating (1-99): percentile rank, across every stock with at least 63 sessions of history,
of a weighted relative-performance score:
    score = (2*C/C[63] + C/C[126] + C/C[189] + C/C[252]) / 5
(the latest quarter counts double, i.e. 40%, each earlier quarter 20%). When a stock has less
than a year of history, only the available quarters are used and the weights are re-normalised.
"""
import csv, json, math, os
import numpy as np
import pandas as pd

PX = 'px'
OUT = 'out'
os.makedirs(OUT, exist_ok=True)

BENCH = {'Nifty 500': 'nifty_500', 'Nifty 50': 'nifty_50', 'Nifty MidSmallcap 400': 'nifty_midsmallcap_400'}
LOOKBACK_ROWS = 1300         # ~3.5 years of sessions kept in memory
STALE_DAYS = 7               # skip stocks whose last print is older than this (suspended / delisted)


def load(path):
    df = pd.read_csv(path, usecols=['Date', 'High', 'Close', 'Volume'], parse_dates=['Date'])
    df = df.dropna(subset=['Close']).drop_duplicates('Date').set_index('Date').sort_index()
    return df


# ---------- benchmarks ----------
bench = {k: load(f'{PX}/{v}.csv')['Close'] for k, v in BENCH.items()}
cal = bench['Nifty 500'].index[-LOOKBACK_ROWS:]
asof = cal[-1]

# ---------- stocks ----------
meta = {r['symbol']: r for r in csv.DictReader(open('master.csv'))}
close, high, turn = {}, {}, {}
for sym, m in meta.items():
    f = f'{PX}/{sym.lower()}.csv'
    if not os.path.exists(f):
        continue
    df = load(f)
    if df.empty or (asof - df.index[-1]).days > STALE_DAYS:
        continue
    df = df[df.index >= cal[0]]
    if len(df) < 63:
        continue
    close[sym] = df['Close']
    high[sym] = df['High']
    turn[sym] = df['Close'] * df['Volume']

C = pd.DataFrame(close).reindex(cal).ffill(limit=5)
H = pd.DataFrame(high).reindex(cal).ffill(limit=5)
T = pd.DataFrame(turn).reindex(cal)
syms = list(C.columns)
print('stocks in universe:', len(syms), 'as of', asof.date())


# ---------- RS score / rating for every session ----------
def rs_score(C):
    parts, wts = [], []
    for lag, w in ((63, 2), (126, 1), (189, 1), (252, 1)):
        r = C / C.shift(lag)
        parts.append(r.fillna(0) * w)
        wts.append(r.notna() * w)
    num = sum(parts)
    den = sum(wts)
    s = num / den.replace(0, np.nan)
    s[C.shift(63).isna()] = np.nan          # need at least one full quarter
    return s


score = rs_score(C)
rating = score.rank(axis=1, pct=True)
rating = (rating * 98 + 1).round()          # 1..99

# ---------- per-stock metrics ----------
def ret(series, lag):
    s = series.dropna()
    if len(s) <= lag:
        return None
    return round((s.iloc[-1] / s.iloc[-1 - lag] - 1) * 100, 2)


b500 = bench['Nifty 500'].reindex(cal).ffill()
rows = []
breadth = dict(n=0, e21=0, e50=0, e200=0, near=0, nh=0, adv=0, dec=0)
for sym in syms:
    c = C[sym].dropna()
    h = H[sym].dropna()
    m = meta[sym]
    last = c.iloc[-1]
    rt = rating[sym]
    rs_now = rt.iloc[-1]
    if np.isnan(rs_now):
        continue
    rs_20 = rt.iloc[-21] if len(rt.dropna()) > 21 else np.nan

    hi52 = h.iloc[-252:].max()
    whd = (last / hi52 - 1) * 100

    rsl = (C[sym] / b500).dropna()
    rsl_hi_prev = rsl.iloc[-253:-1].max() if len(rsl) > 21 else np.nan
    blue = bool(len(rsl) >= 126 and rsl.iloc[-1] >= rsl_hi_prev)
    # blue dot within the last 5 sessions
    recent_blue = False
    if len(rsl) >= 130:
        for k in range(1, 6):
            seg = rsl.iloc[:len(rsl) - k + 1]
            if seg.iloc[-1] >= seg.iloc[-253:-1].max():
                recent_blue = True
                break
    price_hi_prev = c.iloc[-253:-1].max()
    leading = blue and last < price_hi_prev
    rs_vs_hi = (rsl.iloc[-1] / rsl.iloc[-252:].max() - 1) * 100
    rs_vs_ma = (rsl.iloc[-1] / rsl.iloc[-50:].mean() - 1) * 100   # 10-week ≈ 50 sessions

    to50 = T[sym].iloc[-50:].mean() / 1e7     # ₹ crore
    d1 = ret(c, 1)

    if len(c) >= 200:
        breadth['n'] += 1
        e = lambda span: c.ewm(span=span, adjust=False).mean().iloc[-1]
        breadth['e21'] += last > e(21)
        breadth['e50'] += last > e(50)
        breadth['e200'] += last > e(200)
        breadth['near'] += whd >= -15
        breadth['nh'] += last >= hi52
        breadth['adv'] += (d1 or 0) > 0
        breadth['dec'] += (d1 or 0) < 0

    rows.append(dict(
        s=sym, n=m['company'].replace(' Limited', '').replace(' LIMITED', '').replace(' Ltd.', '').replace(' Ltd', ''),
        sec=m['sector'], ind=m['basicIndustry'], mac=m['macro'],
        p=round(float(last), 2), d1=d1, w1=ret(c, 5), m1=ret(c, 21), m3=ret(c, 63), m6=ret(c, 126), m12=ret(c, 252),
        rs=int(rs_now), dl=None if np.isnan(rs_20) else int(rs_now - rs_20),
        whd=round(float(whd), 2), to=round(float(to50), 2),
        bd=2 if leading else (1 if blue else 0), rb=recent_blue,
        vhi=round(float(rs_vs_hi), 2), vma=round(float(rs_vs_ma), 2),
        hist=len(c),
    ))

print('rated stocks:', len(rows))
df = pd.DataFrame(rows)


# ---------- group aggregates ----------
def agg(key):
    out = []
    for name, g in df.groupby(key):
        prev = g['rs'] - g['dl'].fillna(0)
        out.append(dict(
            name=name, sec=g['sec'].iloc[0], n=int(len(g)),
            avg=round(float(g['rs'].mean()), 1), med=float(g['rs'].median()),
            chg=round(float(g['rs'].mean() - prev.mean()), 1),
            pct80=round(float((g['rs'] >= 80).mean() * 100), 1),
            near=round(float((g['whd'] >= -15).mean() * 100), 1),
            w1=round(float(g['w1'].median()), 2), m1=round(float(g['m1'].median()), 2),
        ))
    return sorted(out, key=lambda x: -x['avg'])


bt = breadth['n']
data = dict(
    asof=str(asof.date()),
    universe=len(rows),
    method='RS Rating = percentile (1-99) of (2*C/C63 + C/C126 + C/C189 + C/C252)/5 across all rated NSE stocks',
    breadth=dict(
        base=bt,
        e21=round(breadth['e21'] / bt * 100, 1), e50=round(breadth['e50'] / bt * 100, 1),
        e200=round(breadth['e200'] / bt * 100, 1), near=round(breadth['near'] / bt * 100, 1),
        nh=int(breadth['nh']), adv=int(breadth['adv']), dec=int(breadth['dec']),
        rs80=int((df['rs'] >= 80).sum()),
    ),
    sectors=agg('sec'),
    industries=agg('ind'),
    stocks=sorted(rows, key=lambda r: (-r['rs'], r['s'])),
)
json.dump(data, open(f'{OUT}/data.json', 'w'), separators=(',', ':'), allow_nan=False, default=lambda o: None)

# ---------- weekly series for charts ----------
wk_idx = C.resample('W-FRI').last().index
wk_dates = [d for d in wk_idx][-209:]
last_week_end = wk_dates[-1]


def weekly(s):
    w = s.resample('W-FRI').last()
    w = w.reindex(wk_dates)
    return w


series = dict(dates=[str(min(d, asof).date()) for d in wk_dates], bench={}, close={}, rating={})
for k in BENCH:
    series['bench'][k] = [round(float(x), 2) for x in weekly(bench[k].reindex(cal).ffill())]
rw = rating.resample('W-FRI').last().reindex(wk_dates)
for r in rows:
    sym = r['s']
    w = weekly(C[sym])
    series['close'][sym] = [None if np.isnan(x) else float(f'{x:.4g}') for x in w]
    series['rating'][sym] = [None if np.isnan(x) else int(x) for x in rw[sym].iloc[-157:]]
json.dump(series, open(f'{OUT}/series.json', 'w'), separators=(',', ':'), allow_nan=False)

print('breadth', data['breadth'])
print('top sectors', [(s['name'], s['avg']) for s in data['sectors'][:5]])
for k in ('data', 'series'):
    print(k, round(os.path.getsize(f'{OUT}/{k}.json') / 1e6, 2), 'MB')
