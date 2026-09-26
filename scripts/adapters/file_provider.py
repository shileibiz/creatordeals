from pathlib import Path
import json

def load(raw_dir: Path):
    for path in sorted(raw_dir.glob('*.json')):
        payload = json.loads(path.read_text())
        if not isinstance(payload, dict) or not isinstance(payload.get('offers'), list):
            raise ValueError(f'{path}: expected object with offers array')
        yield payload
