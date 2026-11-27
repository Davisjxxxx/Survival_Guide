"""Read-only negative probe: rotate visible geometry but preserve bearing metadata.

This mutates an SVG in memory only. It exercises the unit geometry validator,
not the artifact-equality check or the release process. No delivered SVG changes.
"""
import argparse
import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    sys.path.insert(0, str(args.repo/'scripts'))
    import build_w2c_navigation as nav
    svg = nav.z11_r05_svg()
    root = ET.fromstring(svg)
    needle = root.find(".//*[@id='compass-after-needle']")
    if needle is None:
        raise SystemExit('Expected needle not present; reassess probe for this revision.')
    needle.set('transform', 'rotate(90 513.7 244.0)')
    mutant = ET.tostring(root, encoding='unicode')
    payload = {
        'scope': 'unit geometry validator only; no production edit or artifact-equality bypass',
        'mutation': '90-degree visible needle rotation with unchanged data-bearing',
        'baseline': nav.z11_r05_checks(svg),
        'mutant': nav.z11_r05_checks(mutant),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2)+'\n')
    print('Baseline accepted:', payload['baseline']['accepted'])
    print('Mutant accepted:', payload['mutant']['accepted'])


if __name__ == '__main__':
    main()
