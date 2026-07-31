from pathlib import Path
import base64

source = Path('tmp/release-poster/chunk1.txt')
target = Path('news/2026-07-31-aa-kazakhstan-2-0/poster.jpg')
encoded = ''.join(source.read_text(encoding='utf-8').split())
data = base64.b64decode(encoded, validate=True)
if not data.startswith(b'\xff\xd8\xff') or not data.endswith(b'\xff\xd9'):
    raise SystemExit('Invalid JPEG data')
target.parent.mkdir(parents=True, exist_ok=True)
target.write_bytes(data)
print(f'Installed {target}: {len(data)} bytes')
