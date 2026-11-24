"""Bundle the complete versioned source and reader with a deterministic member manifest."""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

root = Path(__file__).resolve().parents[1]
target = root / 'production/Survival-Field-Encyclopedia-Owner-Review.zip'
manifest = 'PACKAGE-SHA256.txt'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def add(archive, name, data):
    member = ZipInfo(name,(2026,11,24,0,0,0))
    member.compress_type = ZIP_DEFLATED
    member.external_attr = (0o100755 if os.access(root/name,os.X_OK) else 0o100644) << 16
    archive.writestr(member,data)


def verify(path, names):
    with ZipFile(path) as archive:
        assert archive.testzip() is None, 'ZIP CRC failed'
        assert sorted(archive.namelist())==sorted([*names,manifest]), 'Package membership drift'
        expected = ''.join(f'{digest((root/name).read_bytes())}  {name}\n' for name in names)
        assert archive.read(manifest)==expected.encode(), 'Manifest drift'
        for name in names:
            assert digest(archive.read(name))==digest((root/name).read_bytes()),name


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    tracked = subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
    names = sorted(n for n in tracked if n and root/n!=target)
    assert 'reader/index.html' in names and 'production/OUTSTANDING_ISSUES.md' in names
    if args.check:
        verify(target,names)
    else:
        with tempfile.TemporaryDirectory(dir=target.parent) as tmp:
            candidate = Path(tmp)/target.name
            entries = []
            with ZipFile(candidate,'w') as archive:
                for name in names:
                    data = (root/name).read_bytes()
                    add(archive,name,data)
                    entries.append(f'{digest(data)}  {name}\n')
                add(archive,manifest,''.join(entries).encode())
            verify(candidate,names)
            os.replace(candidate,target)
    print(f'{len(names)} files + SHA-256 manifest; {target.stat().st_size} bytes; SHA-256 {digest(target.read_bytes())}')
