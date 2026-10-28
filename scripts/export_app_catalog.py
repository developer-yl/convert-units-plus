#!/usr/bin/env python3
"""Refresh the committed website snapshot from the first-party package sources."""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def export(conversion, currency):
    paths = {
        'units': conversion / 'Tools/translations/catalog-en.json',
        'registry': conversion / 'Sources/ConversionKit/UnitCategory.swift',
        'currencyCases': conversion / 'Sources/ConversionKit/Units/CurrencyUnits.swift',
        'currencyPolicy': conversion / 'Sources/ConversionKit/Units/CurrencyUnits+extension.swift',
        'currencies': currency / 'Sources/CurrencyKit/CurrencyCatalog.swift',
    }
    categories = json.loads(paths['units'].read_text())['categories']
    registry = re.findall(r'^    case (\w+)$', paths['registry'].read_text().split('public var id:')[0], re.M)
    assert set(registry) == {c['rawValue'] for c in categories} | {'currency'}
    policy = paths['currencyPolicy'].read_text()
    retired = re.findall(r'"([^\"]+)"', re.search(r'retiredCodes: Set<String> = \[([^]]*)\]', policy)[1])
    pattern = r'CurrencyInfo\(code: "([^\"]+)", kind: \.(\w+), englishName: "((?:\\.|[^"\\])*)", flagCountryCode: "[^\"]*"\)'
    currencies = [dict(code=code, kind=kind, englishName=json.loads('"'+name+'"'))
                  for code, kind, name in re.findall(pattern, paths['currencies'].read_text())]
    case_body = paths['currencyCases'].read_text().split('public enum CurrencyUnits:')[1].split('\n}')[0]
    cases = re.findall(r'^    case (\w+)(?: = "([^\"]+)")?\s*$', case_body, re.M)
    assert {raw or name for name, raw in cases} == {c['code'] for c in currencies}
    currencies = sorted([c for c in currencies if c['code'] not in retired], key=lambda c: c['code'])
    counts = dict(Counter(c['kind'] for c in currencies))
    return {
        'schemaVersion': 1, 'checkedOn': '2026-10-28',
        'sources': {key: {'package': 'CurrencyKit' if key == 'currencies' else 'ConversionKit',
                          'path': str(path.relative_to(currency if key == 'currencies' else conversion)),
                          'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for key, path in paths.items()},
        'categoryCount': len(registry), 'measurementCategoryCount': len(categories),
        'measurementUnitCount': sum(len(c['units']) for c in categories),
        'currencyCount': len(currencies), 'currencyCountsByKind': counts,
        'excludedRetiredCodes': retired,
        'coverageNote': 'Catalog entries describe selectable units and recognized codes, not guaranteed fresh quotes, market activity or trading availability. Fiat grouping includes regional and currency-like units. Asset names and classifications follow the package catalog.',
        'categories': categories, 'currencies': currencies,
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--conversion-kit', type=Path, required=True)
    parser.add_argument('--currency-kit', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = export(args.conversion_kit, args.currency_kit)
    target = ROOT / 'content/app-catalog.json'
    if args.check:
        assert json.loads(target.read_text()) == data, 'Refresh the website snapshot; package sources have changed'
    else:
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in data.items() if k.endswith('Count') or k == 'currencyCountsByKind'}))
