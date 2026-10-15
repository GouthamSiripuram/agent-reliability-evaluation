"""Resolve pinned checkpoint assets without changing the frozen research inputs.

Added after protocol freeze as a distribution helper, not experimental logic.
Defaults to an alternate output so it cannot replace a running study's settings.
"""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-dir', type=Path, required=True)
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--output', type=Path, default=Path('local_assets.replication.json'))
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    output = args.output.resolve()
    if output.exists():
        parser.error('Output already exists; choose a new output path.')
    if output == (root / 'local_assets.json').resolve() and (root / 'runs/RUNNING.lock').exists():
        parser.error('Cannot create live configuration while a study lock exists.')
    from huggingface_hub import snapshot_download
    manifest = json.loads((root / 'MODEL_MANIFEST.json').read_text(encoding='utf-8'))
    models = []
    for entry in manifest['models']:
        location = Path(snapshot_download(
            repo_id=entry['id'], revision=entry['revision'],
            cache_dir=str(args.cache_dir.resolve()),
            allow_patterns=list(entry['files']), local_files_only=args.offline,
        )).resolve()
        for name, expected in entry['files'].items():
            digest = hashlib.sha256()
            with (location / name).open('rb') as stream:
                for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                    digest.update(chunk)
            if digest.hexdigest() != expected:
                raise RuntimeError(f'Pinned file hash mismatch: {entry["id"]}/{name}')
        models.append({**entry, 'local_path': str(location)})
        print('Verified', entry['id'], entry['revision'])
    with output.open('x', encoding='utf-8') as stream:
        json.dump({'models': models}, stream, indent=2)
        stream.write('\n')
    print('Wrote machine-local configuration:', output)


if __name__ == '__main__':
    main()
