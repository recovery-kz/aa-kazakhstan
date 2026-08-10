import json
import re
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

errors = []
warnings = []


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f'{path}: invalid JSON: {exc}')
        return None


def local_path(value):
    value = str(value or '').split('?', 1)[0].split('#', 1)[0]
    if not value or value.startswith(('#', 'http://', 'https://', 'tel:', 'mailto:', 'javascript:')):
        return None
    return Path(value.lstrip('./'))


def require_file(path, source):
    target = local_path(path)
    if target is not None and not target.is_file():
        errors.append(f'{source}: missing file: {target.as_posix()}')
    return target


class HtmlRefs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        for key in ('src', 'href'):
            if attrs.get(key):
                self.refs.append((tag, key, attrs[key]))


groups = load_json('groups.json')
books = load_json('books.json')
news = load_json('news.json')
manifest = load_json('manifest.json')
version = load_json('version.json')

if not isinstance(groups,list) or not groups: errors.append('groups empty')
seen=set()
for i,g in enumerate(groups or []):
 name=str(g.get('n','')).strip(); city=str(g.get('c','')).strip()
 if not name: errors.append(f'group {i}: empty name')
 key=(city.lower(),name.lower())
 if key in seen: errors.append(f'duplicate group: {city}/{name}')
 seen.add(key)
 for p in g.get('p',[]) or []:
  digits=re.sub(r'\D','',str(p))
  if len(digits)<10 or len(digits)>12: errors.append(f'bad phone {name}: {p}')
 for slot in g.get('sc',[]) or []:
  if not (0<=slot.get('d',-1)<=6): errors.append(f'bad weekday {name}')
  for k in ('s','e'):
   v=slot.get(k,-1); hh=v//100; mm=v%100
   if not (0<=hh<=23 and 0<=mm<=59): errors.append(f'bad time {name}: {v}')
 for field in ('a','z'):
  v=str(g.get(field,'') or '')
  if v.startswith('http') and not re.match(r'^https?://',v): errors.append(f'bad url {name}: {v}')
if not isinstance(books,list): errors.append('books invalid')
if not isinstance(news,list): errors.append('news invalid')
seen_news_ids = set()
previous_news_date = None
for i, item in enumerate(news or []):
    if not isinstance(item, dict):
        errors.append(f'news item {i}: invalid object')
        continue

    news_id = str(item.get('id', '')).strip()
    if not news_id:
        errors.append(f'news item {i}: empty id')
    elif news_id in seen_news_ids:
        errors.append(f'duplicate news id: {news_id}')
    seen_news_ids.add(news_id)

    try:
        publication_date = date.fromisoformat(str(item.get('date', '')))
    except ValueError:
        errors.append(f'news item {i} ({news_id or "unnamed"}): invalid date')
        publication_date = None

    if publication_date is not None:
        if previous_news_date is not None and publication_date > previous_news_date:
            errors.append('news order invalid: newest items must be first')
        previous_news_date = publication_date

    for field in ('title', 'category', 'description', 'language'):
        if not isinstance(item.get(field, ''), str):
            errors.append(f'news item {i} ({news_id or "unnamed"}): {field} must be text')

    images = item.get('images')
    if not isinstance(images, list) or not images:
        errors.append(f'news item {i} ({news_id or "unnamed"}): no images')
    elif any(not isinstance(image, str) or not image.strip() for image in images):
        errors.append(f'news item {i} ({news_id or "unnamed"}): invalid image path')

if isinstance(groups, list) and len(groups) != 47:
    warnings.append(f'group count changed: expected 47, found {len(groups)}')
if isinstance(books, list) and len(books) != 27:
    warnings.append(f'book count changed: expected 27, found {len(books)}')

for i, book in enumerate(books or []):
    if not str(book.get('n', '')).strip():
        errors.append(f'book {i}: empty name')
    image = book.get('img')
    if image:
        require_file(image, f'book {i} ({book.get("n", "unnamed")})')

for i, item in enumerate(news or []):
    for image in item.get('images', []) or []:
        require_file(image, f'news item {i} ({item.get("id", "unnamed")})')

for required in ('index.html', 'manifest.json', 'app.js', 'i18n.js', 'principles.js',
                 'styles.css', 'groups.json', 'books.json', 'news.json', 'version.json'):
    if not Path(required).is_file():
        errors.append(f'missing required application file: {required}')

html_path = Path('index.html')
if html_path.is_file():
    parser = HtmlRefs()
    parser.feed(html_path.read_text(encoding='utf-8'))
    seen_ids = set()
    for element_id in parser.ids:
        if element_id in seen_ids:
            errors.append(f'duplicate HTML id: {element_id}')
        seen_ids.add(element_id)
    for tag, attribute, value in parser.refs:
        require_file(value, f'index.html {tag}[{attribute}]')

if isinstance(manifest, dict):
    for icon in manifest.get('icons', []) or []:
        require_file(icon.get('src'), 'manifest icon')

if isinstance(version, dict):
    declared = str(version.get('version', '')).strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', declared):
        errors.append(f'version.json: invalid semantic version: {declared!r}')
    if html_path.is_file():
        displayed = re.search(r'id="settings-version-value"[^>]*>([^<]+)', html_path.read_text(encoding='utf-8'))
        if displayed and displayed.group(1).strip() != declared:
            warnings.append(
                f'version mismatch: version.json={declared}, interface={displayed.group(1).strip()}'
            )

text=Path('app.js').read_text(encoding='utf-8')+Path('i18n.js').read_text(encoding='utf-8')
for bad in ('>undefined<','>null<','>NaN<'):
 if bad in text: errors.append('literal '+bad)
if warnings:
    print('\n'.join(f'WARNING: {warning}' for warning in warnings))
if errors:
    print('\n'.join(f'ERROR: {error}' for error in errors))
    sys.exit(1)
print(f'OK: {len(groups)} groups, {len(books)} books, {len(news)} news items')
