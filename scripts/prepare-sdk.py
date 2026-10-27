"""Seed the test harness with a pinned, checksum-verified official GenVM bundle.

genlayer-test 0.29.2 still requests the pre-0.3 asset name. genvm-linter
0.11.0 understands the renamed runners bundle; share its verified download.
"""
from pathlib import Path
import hashlib
import shutil
from genvm_linter.validate.artifacts import download_artifacts

VERSION = 'v0.3.0-rc7'
SHA256 = 'e218a1854214681560351051f76fe2b878545cf3409455ef372d57014a88ca67'

def prepare():
    archive = download_artifacts(VERSION)
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == SHA256, 'GenVM bundle checksum mismatch'
    target = Path.home() / '.cache' / 'gltest-direct' / f'genvm-universal-{VERSION}.tar.xz'
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest() != SHA256:
        temporary = target.with_suffix('.preparing')
        shutil.copyfile(archive, temporary)
        temporary.replace(target)
    print(f'Official GenVM {VERSION} bundle verified and ready.')

if __name__ == '__main__':
    prepare()
