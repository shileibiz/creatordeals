#!/usr/bin/env python3
"""Validate source-linked deals, deduplicate, and archive expired entries."""
from datetime import datetime, timezone
from pathlib import Path
import json
import re
from jsonschema import Draft202012Validator, FormatChecker
from adapters.file_provider import load

ROOT = Path(__file__).resolve().parents[1]
MERCHANTS = ROOT / 'data' / 'merchants'
SCHEMA = json.loads((ROOT / 'data' / 'merchant.schema.json').read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
NOW = datetime.now(timezone.utc)

def parse_time(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)

def validate(data, path):
    errors = sorted(VALIDATOR.iter_errors(data), key=lambda e: str(e.path))
    if errors:
        raise ValueError(f'{path}: ' + '; '.join(e.message for e in errors))
    if len(re.findall(r"\b[\w'-]+\b", data['editorial'])) < 150:
        raise ValueError(f'{path}: fewer than 150 editorial words')
    ids = [o['id'] for o in data['offers'] + data['expired']]
    if len(ids) != len(set(ids)):
        raise ValueError(f'{path}: duplicate offer id')
    for offer in data['offers'] + data['expired']:
        if not offer['source_url'].startswith('https://'):
            raise ValueError(f'{path}: offer source must use HTTPS')

def main():
    files = {p.stem: p for p in MERCHANTS.glob('*.json')}
    if len(files) != 20:
        raise ValueError(f'Expected 20 merchants, found {len(files)}')
    for raw in load(ROOT / 'data' / 'raw'):
        slug = raw.get('merchant_slug')
        if slug not in files:
            raise ValueError(f'Unknown merchant: {slug}')
        path = files[slug]
        data = json.loads(path.read_text())
        old = {o['id']: o for o in data['offers'] + data['expired']}
        for offer in raw['offers']:
            old[offer['id']] = offer
        data['offers'] = list(old.values())
        data['expired'] = []
        validate(data, path)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    for slug, path in files.items():
        data = json.loads(path.read_text())
        active, expired = [], list(data['expired'])
        for offer in data['offers']:
            (expired if parse_time(offer['expires_at']) <= NOW else active).append(offer)
        data['offers'], data['expired'] = active, expired
        validate(data, path)
        rendered = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
        if rendered != path.read_text():
            path.write_text(rendered)
    print(f'Validated {len(files)} merchants at {NOW.isoformat()}')

if __name__ == '__main__':
    main()
