"""Run browser checks against an isolated local server, with mandatory axe coverage."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.preview import preview


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--firefox', action='store_true')
    args = parser.parse_args()
    axe = Path(os.environ.get('AXE_SCRIPT', str(ROOT / 'qa/axe.min.js')))
    if not axe.is_file():
        raise SystemExit('AXE_REQUIRED: run python tools/fetch_axe.py before browser validation')
    checks = [(name, 'chromium') for name in ['browser_check.py', 'round2_check.py', 'round3_check.py', 'scientific_browser.py', 'privacy_browser.py']]
    if args.firefox:
        checks += [(name, 'firefox') for name in ['scientific_browser.py', 'privacy_browser.py']]
    results = []
    with preview(ROOT / 'public') as url:
        for name, browser in checks:
            env = os.environ.copy()
            env.update(TEST_BASE_URL=url, AXE_SCRIPT=str(axe), PLAYWRIGHT_BROWSER=browser)
            started = time.perf_counter()
            result = subprocess.run([sys.executable, str(ROOT / 'tests' / name)], cwd=ROOT, env=env)
            results.append({'script': name, 'browser': browser, 'returncode': result.returncode,
                            'seconds': round(time.perf_counter()-started, 3)})
            (ROOT / 'qa/browser-suite.json').write_text(json.dumps(results, indent=2)+'\n', encoding='utf8')
            if result.returncode:
                return result.returncode
    print('BROWSER_SUITE_VALID:', len(results), 'checks; loopback server closed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
