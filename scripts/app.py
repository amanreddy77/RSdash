"""Serves the static site in public/ (next to this file) under Vercel's Python preset.

With the "Other" preset Vercel serves public/ directly and this file is unused.
It has no dependencies: a plain WSGI app that returns files from public/.
"""
import mimetypes
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')


def serve(environ, start_response):
    path = environ.get('PATH_INFO') or '/'
    if path.endswith('/'):
        path += 'index.html'
    full = os.path.normpath(os.path.join(ROOT, path.lstrip('/')))
    # Stay inside public/; anything unknown falls back to the site itself
    if not full.startswith(ROOT + os.sep) or not os.path.isfile(full):
        full = os.path.join(ROOT, 'index.html')
    with open(full, 'rb') as f:
        body = f.read()
    ctype = mimetypes.guess_type(full)[0] or 'application/octet-stream'
    if ctype.startswith('text/') or ctype == 'application/json':
        ctype += '; charset=utf-8'
    # The page and the files that list what exists must never be served stale;
    # one day's snapshot can be cached for an hour.
    name = os.path.basename(full)
    if '/data/history/' in full and name[:4].isdigit():
        cache = 'public, max-age=3600'
    else:
        cache = 'no-cache'
    start_response('200 OK', [('Content-Type', ctype), ('Content-Length', str(len(body))), ('Cache-Control', cache)])
    return [body]


# Vercel looks for a module-level `app` (see [tool.vercel] in pyproject.toml)
app = serve
