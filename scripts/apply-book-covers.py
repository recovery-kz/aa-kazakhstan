from pathlib import Path
import base64
import json
import zipfile

zip_path = Path('assets/book-covers.zip')
if not zip_path.is_file():
    raise SystemExit('Book cover archive not found')
archive_path = zip_path
if not zipfile.is_zipfile(zip_path):
    archive_path = Path('/tmp/book-covers-decoded.zip')
    archive_path.write_bytes(base64.b64decode(zip_path.read_text(encoding='utf-8').strip()))
if not zipfile.is_zipfile(archive_path):
    raise SystemExit('Prepared book cover archive is invalid')
cover_dir = Path('book-covers')
cover_dir.mkdir(exist_ok=True)
with zipfile.ZipFile(archive_path) as archive:
    archive.extractall(cover_dir)

cover_map = {
    ('Анонимные Алкоголики (с историями) твердый', 'рус'): 'book-covers/aa-stories-ru.webp',
    ('Анонимные Алкоголики (стандарт)', 'рус'): 'book-covers/aa-standard-ru.webp',
    ('Анонимные Алкоголики (стандарт) карманный', 'рус'): 'book-covers/aa-pocket-ru.webp',
    ('Двенадцать шагов и двенадцать традиций', 'рус'): 'book-covers/12x12-ru.webp',
    ('Двенадцать шагов и двенадцать традиций', 'каз'): 'book-covers/12x12-kz.webp',
    ('Ежедневные размышления', 'рус'): 'book-covers/daily-reflections-ru.webp',
    ('Ежедневные размышления', 'каз'): 'book-covers/daily-reflections-kz.webp',
    ('Жить трезвыми', 'рус'): 'book-covers/living-sober-ru.webp',
    ('Жить трезвыми', 'каз'): 'book-covers/living-sober-kz.webp',
    ('Сбросить камень', 'рус'): 'book-covers/drop-the-rock-ru.webp',
    ('Сбросить камень', 'каз'): 'book-covers/drop-the-rock-kz.webp',
    ('Доктор Боб и славные ветераны', 'рус'): 'book-covers/dr-bob-ru.webp',
    ('АА Взрослеет', 'рус'): 'book-covers/aa-comes-of-age-ru.webp',
    ('Рук-во по обслуживанию АА + 12 Принципов', 'рус'): 'book-covers/service-manual-ru.webp',
    ('Группа АА там где все начинается', 'рус'): 'book-covers/group-aa-ru.webp',
}
books_path = Path('books.json')
books = json.loads(books_path.read_text(encoding='utf-8'))
original_count = len(books)
matched = []
for book in books:
    key = (book.get('n'), book.get('l'))
    if key in cover_map:
        book['img'] = cover_map[key]
        matched.append(key)
if len(books) != original_count:
    raise SystemExit('Book list size changed unexpectedly')
if len(matched) != len(cover_map):
    missing = sorted(set(cover_map) - set(matched))
    raise SystemExit(f'Not all covers matched: {missing}')
books_path.write_text(json.dumps(books, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

app_path = Path('app.js')
app = app_path.read_text(encoding='utf-8')
old = '''    function getBookCover(index, book, compact = false) {
        const language = book.l === 'рус' ? 'RU' : 'ҚАЗ';
        return `
            <div class="book-cover book-cover-${index % 25}">
                <div class="book-cover-mark">АА</div>
                <div class="book-cover-title">${escapeHtml(book.n)}</div>
                <div class="book-cover-mark" style="width:auto;height:auto;border:none;border-radius:0;justify-content:flex-start;font-size:9px;">${language}</div>
            </div>
        `;
    }
'''
new = '''    function getBookCover(index, book, compact = false) {
        if (book.img) {
            return `
                <div class="book-cover book-cover-real">
                    <img class="book-cover-image" src="${escapeHtml(book.img)}" alt="${escapeHtml(book.n)}" loading="lazy" decoding="async">
                </div>
            `;
        }
        const language = book.l === 'рус' ? 'RU' : 'ҚАЗ';
        return `
            <div class="book-cover book-cover-${index % 25}">
                <div class="book-cover-mark">АА</div>
                <div class="book-cover-title">${escapeHtml(book.n)}</div>
                <div class="book-cover-mark" style="width:auto;height:auto;border:none;border-radius:0;justify-content:flex-start;font-size:9px;">${language}</div>
            </div>
        `;
    }
'''
if old not in app:
    raise SystemExit('getBookCover block not found')
app_path.write_text(app.replace(old, new, 1), encoding='utf-8')

styles_path = Path('styles.css')
styles = styles_path.read_text(encoding='utf-8')
css = '''
        .book-cover.book-cover-real { padding: 0; background: #08083f; }
        .book-cover.book-cover-real::before,
        .book-cover.book-cover-real::after { display: none; }
        .book-cover-image { width: 100%; height: 100%; display: block; object-fit: cover; object-position: center; }
'''
if '.book-cover.book-cover-real' not in styles:
    styles_path.write_text(styles + css, encoding='utf-8')

index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')
index = index.replace('styles.css?v=2.0.2', 'styles.css?v=2.0.3')
index = index.replace('app.js?v=2.0.2', 'app.js?v=2.0.3')
index_path.write_text(index, encoding='utf-8')

for relative in cover_map.values():
    if not Path(relative).is_file() or Path(relative).stat().st_size < 10000:
        raise SystemExit(f'Invalid cover file: {relative}')
json.loads(books_path.read_text(encoding='utf-8'))
print(f'Applied {len(matched)} book covers; retained all {original_count} books')
