import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, UnidentifiedImageError


errors = []
assets = set()


def add(path, source):
    if not path or str(path).startswith(('http://', 'https://')):
        return
    target = Path(str(path).split('?', 1)[0].split('#', 1)[0])
    if not target.is_file():
        errors.append(f'{source}: missing image: {target.as_posix()}')
        return
    assets.add(target)


for source in ('news.json', 'books.json'):
    data = json.loads(Path(source).read_text(encoding='utf-8'))
    for index, item in enumerate(data):
        for path in item.get('images', []) or []:
            add(path, f'{source} item {index}')
        add(item.get('img'), f'{source} item {index}')

for post_path in Path('news').glob('*/post.json'):
    post = json.loads(post_path.read_text(encoding='utf-8'))
    for path in post.get('images', []) or []:
        add(path, post_path.as_posix())

for path in sorted(assets):
    try:
        if path.suffix.lower() == '.svg':
            ET.parse(path)
        else:
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                image.load()
                if image.width < 1 or image.height < 1:
                    raise ValueError('image has invalid dimensions')
    except (OSError, ValueError, ET.ParseError, UnidentifiedImageError) as exc:
        errors.append(f'{path.as_posix()}: image cannot be decoded: {exc}')

if errors:
    print('\n'.join(f'ERROR: {error}' for error in errors))
    sys.exit(1)

print(f'OK: {len(assets)} referenced images decoded successfully')
