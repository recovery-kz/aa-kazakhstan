from pathlib import Path
from PIL import Image

path = Path('news/2026-07-31-almaty-forum-4/original-poster.jpg')
with Image.open(path) as image:
    image.convert('RGB').save(path, 'JPEG', quality=90, optimize=True, progressive=True)
print(f'Converted {path} to real JPEG')
