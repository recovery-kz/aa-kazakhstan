from pathlib import Path
from PIL import Image

# Convert the existing original forum poster bytes to an actual JPEG file.
path = Path('news/2026-07-31-almaty-forum-4/original-poster.jpg')
with Image.open(path) as image:
    image.convert('RGB').save(path, 'JPEG', quality=90, optimize=True, progressive=True)
print(f'Converted {path} to real JPEG')
