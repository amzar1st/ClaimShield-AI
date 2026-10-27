"""Prepare the official pinned SDK before direct-mode fixtures import it."""
from pathlib import Path
import runpy

def pytest_sessionstart(session):
    runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts' / 'prepare-sdk.py'), run_name='__main__')
