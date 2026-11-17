"""Fetch the pinned development-only axe engine and verify the npm tarball integrity."""
from pathlib import Path
from io import BytesIO
import base64
import hashlib
import tarfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
VERSION = '4.14.1'
URL = 'https://registry.npmjs.org/axe-core/-/axe-core-' + VERSION + '.tgz'
SHA512 = 'FHfa+lmNjQZfJz1q8wKqIDwC6DExcHt/pkjNQb09a3NPjCKg2rhu5qb2S4r76ASyFNNtuFooJpZe37OgudVGtQ=='


def main():
    with urlopen(URL, timeout=45) as response:
        payload = response.read()
    if base64.b64encode(hashlib.sha512(payload).digest()).decode() != SHA512:
        raise SystemExit('AXE_INTEGRITY: pinned dependency bytes do not match')
    output = ROOT / 'qa'
    output.mkdir(exist_ok=True)
    with tarfile.open(fileobj=BytesIO(payload), mode='r:gz') as archive:
        for source, target in [('package/axe.min.js', 'axe.min.js'), ('package/LICENSE', 'axe-LICENSE.txt')]:
            entry = archive.getmember(source)
            if not entry.isfile():
                raise SystemExit('AXE_ARCHIVE: expected a regular dependency file')
            data = archive.extractfile(entry).read()
            (output / target).write_bytes(data)
    print('Pinned axe-core', VERSION, 'verified; development files saved under qa/')


if __name__ == '__main__':
    main()
