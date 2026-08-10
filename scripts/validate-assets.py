import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, UnidentifiedImageError


errors = []
assets = set()
expected_dimensions = {}


def add(path, source):
    if not path or str(path).startswith(('http://', 'https://')):
        return None
    target = Path(str(path).split('?', 1)[0].split('#', 1)[0])
    if not target.is_file():
        errors.append(f'{source}: missing image: {target.as_posix()}')
        return None
    assets.add(target)
    return target


for source in ('news.json', 'books.json'):
    data = json.loads(Path(source).read_text(encoding='utf-8'))
    for index, item in enumerate(data):
        for path in item.get('images', []) or []:
            add(path, f'{source} item {index}')
        add(item.get('img'), f'{source} item {index}')

manifest = json.loads(Path('manifest.json').read_text(encoding='utf-8'))
for index, icon in enumerate(manifest.get('icons', []) or []):
    source = f'manifest icon {index}'
    target = add(icon.get('src'), source)
    sizes = str(icon.get('sizes', '')).strip()
    match = re.fullmatch(r'(\d+)x(\d+)', sizes)
    if not match:
        errors.append(f'{source}: invalid sizes declaration: {sizes!r}')
    elif target is not None:
        expected_dimensions[target] = (int(match.group(1)), int(match.group(2)), source)

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
                if path in expected_dimensions:
                    width, height, source = expected_dimensions[path]
                    if image.size != (width, height):
                        raise ValueError(
                            f'{source}: declared {width}x{height}, actual {image.width}x{image.height}'
                        )
    except (OSError, ValueError, ET.ParseError, UnidentifiedImageError) as exc:
        errors.append(f'{path.as_posix()}: image cannot be decoded: {exc}')

if errors:
    print('\n'.join(f'ERROR: {error}' for error in errors))
    sys.exit(1)

print(f'OK: {len(assets)} referenced images decoded successfully')
