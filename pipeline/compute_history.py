"""Daily history snapshots so the site can show any recent trading day.

Inputs  : px/<symbol>.csv (NSE EOD, split/bonus adjusted), master.csv, px/nifty_500.csv
Outputs : out/history/index.json        list of available dates (newest first)
          out/history/meta.json         symbol -> [name, sector, industry]
          out/history/<YYYY-MM-DD>.json one file per session:
              d  = dashboard snapshot (same shape as data.json, compact rows)
              sc = screener snapshot (same shape as screener.json)

Every metric is computed the way compute_rs.py / compute_screener.py compute it for the
latest day, but for each of the last HISTORY_SESSIONS sessions (default 126, ~6 months),
using only data up to that day. Work is vectorised across all stocks and dates.
"""
import csv
import json
import os

import numpy as np
import pandas as pd

PX, OUT = 'px', 'out'
SESSIONS = int(os.environ.get('HISTORY_SESSIONS', '126'))
# Optional freeze date: ignore every price after it
DATA_END = pd.Timestamp(os.environ['DATA_END']) if os.environ.get('DATA_END') else None
# Optional first snapshot day; when set it replaces the HISTORY_SESSIONS count
HISTORY_START = pd.Timestamp(os.environ['HISTORY_START']) if os.environ.get('HISTORY_START') else None
HIST = os.path.join(OUT, 'history')
os.makedirs(HIST, exist_ok=True)

FIELDS = ['s', 'p', 'd1', 'm3', 'm12', 'rs', 'dl', 'whd', 'to', 'bd', 'rb', 'vhi', 'vma']


def load(path, cols):
    df = pd.read_csv(path, usecols=['Date'] + cols, parse_dates=['Date'])
    df = df.dropna(subset=['Close']).drop_duplicates('Date').set_index('Date').sort_index()
    return df if DATA_END is None else df[df.index <= DATA_END]


b500_full = load(f'{PX}/nifty_500.csv', ['Close'])['Close']
if HISTORY_START is not None:
    SESSIONS = int((b500_full.index >= HISTORY_START).sum())
cal = b500_full.index[-(SESSIONS + 600):]          # 52-week windows + 252-session RS lookback
dates = cal[-SESSIONS:]
b500 = b500_full.reindex(cal).ffill()

meta = {r['symbol']: r for r in csv.DictReader(open('master.csv'))}
raw = {k: {} for k in ('C', 'H', 'L', 'V')}
for sym in meta:
    f = f'{PX}/{sym.lower()}.csv'
    if not os.path.exists(f):
        continue
    try:
        df = load(f, ['High', 'Low', 'Close', 'Volume'])
    except ValueError:
        continue
    df = df[df.index >= cal[0]]
    if df.empty:
        continue
    raw['C'][sym], raw['H'][sym], raw['L'][sym], raw['V'][sym] = df['Close'], df['High'], df['Low'], df['Volume']

Cr = pd.DataFrame(raw['C']).reindex(cal)
Hr = pd.DataFrame(raw['H']).reindex(cal)
Lr = pd.DataFrame(raw['L']).reindex(cal)
Vr = pd.DataFrame(raw['V']).reindex(cal)
syms = list(Cr.columns)
print('symbols', len(syms), '| sessions', len(dates), dates[0].date(), '->', dates[-1].date())

# ---------- dashboard metrics (as compute_rs.py) ----------
C = Cr.ffill(limit=5)
H = Hr.ffill(limit=5)
T = Cr * Vr
count = C.notna().cumsum()
seen = pd.DataFrame(np.where(Cr.notna(), cal.values[:, None], np.datetime64('NaT')), index=cal, columns=syms).ffill()
active = (seen.rsub(cal.values, axis=0) <= pd.Timedelta(days=7)) & seen.notna()


def rs_score(C):
    parts, wts = [], []
    for lag, w in ((63, 2), (126, 1), (189, 1), (252, 1)):
        r = C / C.shift(lag)
        parts.append(r.fillna(0) * w)
        wts.append(r.notna() * w)
    s = sum(parts) / sum(wts).replace(0, np.nan)
    s[C.shift(63).isna()] = np.nan
    return s


score = rs_score(C).where(active & (count >= 63))
rating = (score.rank(axis=1, pct=True) * 98 + 1).round()
dl = rating - rating.shift(20)
ret = {lag: (C / C.shift(lag) - 1) * 100 for lag in (1, 5, 21, 63, 252)}
hi52 = H.rolling(252, min_periods=1).max()
whd = (C / hi52 - 1) * 100
rsl = C.div(b500, axis=0)
rsl_n = rsl.notna().cumsum()
blue = (rsl_n >= 126) & (rsl >= rsl.shift(1).rolling(252, min_periods=21).max())
recent_blue = (blue.astype(float).rolling(5, min_periods=1).max() > 0) & (rsl_n >= 130)
leading = blue & (C < C.shift(1).rolling(252, min_periods=1).max())
vhi = (rsl / rsl.rolling(252, min_periods=1).max() - 1) * 100
vma = (rsl / rsl.rolling(50, min_periods=1).mean() - 1) * 100
to50 = T.rolling(50, min_periods=1).mean() / 1e7
E = {span: C.ewm(span=span, adjust=False).mean() for span in (21, 50, 200)}

# ---------- screener metrics (as compute_screener.py) ----------
prev_close = Cr.ffill().shift(1)
d1s = (Cr / prev_close - 1) * 100
h_n, l_n = Hr.notna().cumsum(), Lr.notna().cumsum()
new_hi = (h_n >= 252) & (Hr >= Hr.shift(1).rolling(251, min_periods=21).max())
new_lo = (l_n >= 252) & (Lr <= Lr.shift(1).rolling(251, min_periods=21).min())
vx = Vr / Vr.shift(1).rolling(50, min_periods=21).mean()
to_day = Cr * Vr / 1e7


def r2(v, nd=2):
    return None if v is None or (isinstance(v, float) and v != v) else round(float(v), nd)


def agg(df, key):
    out = []
    for name, g in df.groupby(key):
        prev = g['rs'] - g['dl'].fillna(0)
        out.append(dict(name=name, sec=g['sec'].iloc[0], n=int(len(g)),
                        avg=round(float(g['rs'].mean()), 1), med=float(g['rs'].median()),
                        chg=round(float(g['rs'].mean() - prev.mean()), 1),
                        pct80=round(float((g['rs'] >= 80).mean() * 100), 1),
                        near=round(float((g['whd'] >= -15).mean() * 100), 1),
                        w1=r2(g['w1'].median()), m1=r2(g['m1'].median())))
    return sorted(out, key=lambda x: -x['avg'])


sec_of = np.array([meta[s]['sector'] for s in syms])
ind_of = np.array([meta[s]['basicIndustry'] for s in syms])
written, used = [], set()
for D in dates:
    i = cal.get_loc(D)
    at = lambda M: M.iloc[i].to_numpy()
    rt, ok = at(rating), ~np.isnan(at(rating))
    # dashboard rows
    df = pd.DataFrame({
        's': syms, 'sec': sec_of, 'ind': ind_of, 'p': at(C), 'd1': at(ret[1]), 'w1': at(ret[5]), 'm1': at(ret[21]),
        'm3': at(ret[63]), 'm12': at(ret[252]), 'rs': rt, 'dl': at(dl), 'whd': at(whd), 'to': at(to50),
        'bd': np.where(at(leading), 2, np.where(at(blue), 1, 0)), 'rb': at(recent_blue).astype(int),
        'vhi': at(vhi), 'vma': at(vma), 'n200': at(count) >= 200,
        'e21': at(C) > at(E[21]), 'e50': at(C) > at(E[50]), 'e200': at(C) > at(E[200]), 'hi52': at(hi52),
    })[ok]
    df['rs'] = df['rs'].astype(int)
    b = df[df.n200]
    breadth = dict(base=int(len(b)), e21=round(float(b.e21.mean() * 100), 1), e50=round(float(b.e50.mean() * 100), 1),
                   e200=round(float(b.e200.mean() * 100), 1), near=round(float((b.whd >= -15).mean() * 100), 1),
                   nh=int((b.p >= b.hi52).sum()), adv=int((b.d1 > 0).sum()), dec=int((b.d1 < 0).sum()),
                   rs80=int((df.rs >= 80).sum()))
    df = df.sort_values(['rs', 's'], ascending=[False, True])
    rows = []
    for r in df.itertuples(index=False):
        rows.append([r.s, r2(r.p), r2(r.d1), r2(r.m3), r2(r.m12), int(r.rs), None if r.dl != r.dl else int(r.dl),
                     r2(r.whd), r2(r.to), int(r.bd), int(r.rb), r2(r.vhi), r2(r.vma)])
        used.add(r.s)
    d = dict(asof=str(D.date()), universe=int(len(df)), breadth=breadth,
             sectors=[{k: x[k] for k in ('name', 'n', 'avg', 'chg')} for x in agg(df, 'sec')],
             industries=[{k: x[k] for k in ('name', 'sec', 'n', 'avg', 'chg', 'w1', 'm1')} for x in agg(df, 'ind')],
             f=FIELDS, s=rows)

    # screener
    traded = ~np.isnan(at(Cr))
    sd = pd.DataFrame({'s': syms, 'sec': sec_of, 'p': at(Cr), 'd1': at(d1s), 'h': at(Hr), 'l': at(Lr),
                       'hi': at(new_hi), 'lo': at(new_lo), 'vx': at(vx), 'to': at(to_day), 'rs': rt,
                       'e50': at(C) > at(E[50]), 'e200': at(C) > at(E[200]), 'n200': at(count) >= 200})[traded]
    sd = sd[sd.d1.notna()]
    band = pd.Series(np.nan, index=sd.index)
    for bnd in (2, 5, 10, 20):
        band[(sd.d1.abs() - bnd).abs() <= 0.15] = bnd
    uc_m = band.notna() & (sd.d1 > 0) & (sd.p >= sd.h)
    lc_m = band.notna() & (sd.d1 < 0) & (sd.p <= sd.l)

    def pick(x, extra=None):
        out = []
        for r in x.itertuples(index=False):
            o = dict(s=r.s, sec=r.sec, p=r2(r.p), d1=r2(r.d1), vx=r2(r.vx, 1), to=r2(r.to), rs=None if r.rs != r.rs else int(r.rs))
            if extra is not None:
                o[extra[0]] = int(extra[1][r.s])
            out.append(o)
        return out

    sd = sd.set_index('s', drop=False)
    band.index = sd.index
    secs = []
    for name, g in sd.groupby('sec'):
        if len(g) >= 10:
            secs.append(dict(name=name, n=int(len(g)), med=round(float(g.d1.median()), 2), up=int((g.d1 > 0).sum()), dn=int((g.d1 < 0).sum())))
    secs.sort(key=lambda x: -x['med'])
    e = sd[sd.n200]
    sc = dict(asof=str(D.date()), tracked=int(len(sd)),
              adv=int((sd.d1 > 0).sum()), dec=int((sd.d1 < 0).sum()), unch=int((sd.d1 == 0).sum()),
              e50=round(float(e.e50.mean() * 100), 1), e200=round(float(e.e200.mean() * 100), 1),
              hi=pick(sd[sd.hi.astype(bool)].sort_values('d1', ascending=False)),
              lo=pick(sd[sd.lo.astype(bool)].sort_values('d1')),
              vs=pick(sd[(sd.vx >= 3) & (sd.to >= 1)].sort_values('vx', ascending=False)),
              uc=pick(sd[uc_m.to_numpy()].sort_values('d1', ascending=False), ('uc', band)),
              lc=pick(sd[lc_m.to_numpy()].sort_values('d1'), ('lc', band)),
              top=secs[:8], worst=secs[::-1][:8])
    path = os.path.join(HIST, f'{D.date()}.json')
    json.dump(dict(d=d, sc=sc), open(path, 'w'), separators=(',', ':'), allow_nan=False)
    written.append(str(D.date()))

index = dict(dates=written[::-1])
if DATA_END is not None:
    index['frozen'] = written[-1]   # tells the site that updates are paused
json.dump(index, open(os.path.join(HIST, 'index.json'), 'w'), separators=(',', ':'))
json.dump({s: [meta[s]['company'].replace(' Limited', '').replace(' LIMITED', '').replace(' Ltd.', '').replace(' Ltd', ''),
               meta[s]['sector'], meta[s]['basicIndustry']] for s in sorted(used)},
          open(os.path.join(HIST, 'meta.json'), 'w'), separators=(',', ':'))
total = sum(os.path.getsize(os.path.join(HIST, f)) for f in os.listdir(HIST))
print('wrote', len(written), 'snapshots,', round(total / 1e6, 1), 'MB')
