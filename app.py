"""Fallback for Vercel's Python preset when the project builds from the repo root.

The site lives in scripts/public/ and is served by scripts/app.py. This module
loads that server by file path, so both possible Vercel root folders work.
"""
import importlib.util
import os

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts', 'app.py')
_spec = importlib.util.spec_from_file_location('site_server', _path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

app = _mod.app
