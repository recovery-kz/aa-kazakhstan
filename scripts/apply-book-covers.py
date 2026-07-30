from pathlib import Path
from html import escape
import json

cover_dir = Path('book-covers')
cover_dir.mkdir(exist_ok=True)

cover_specs = {
    ('Анонимные Алкоголики (с историями) твердый', 'рус'): ('aa-stories-ru.svg', ['АНОНИМНЫЕ', 'АЛКОГОЛИКИ'], 'БОЛЬШАЯ КНИГА С ИСТОРИЯМИ'),
    ('Анонимные Алкоголики (стандарт)', 'рус'): ('aa-standard-ru.svg', ['АНОНИМНЫЕ', 'АЛКОГОЛИКИ'], 'ЧЕТВЕРТОЕ ИЗДАНИЕ БОЛЬШОЙ КНИГИ'),
    ('Анонимные Алкоголики (стандарт) карманный', 'рус'): ('aa-pocket-ru.svg', ['АНОНИМНЫЕ', 'АЛКОГОЛИКИ'], 'КАРМАННЫЙ ВАРИАНТ'),
    ('Двенадцать шагов и двенадцать традиций', 'рус'): ('12x12-ru.svg', ['ДВЕНАДЦАТЬ ШАГОВ', 'ДВЕНАДЦАТЬ ТРАДИЦИЙ'], '12 × 12'),
    ('Двенадцать шагов и двенадцать традиций', 'каз'): ('12x12-kz.svg', ['ОН ЕКІ ҚАДАМ', 'ОН ЕКІ ДӘСТҮР'], '12 × 12'),
    ('Ежедневные размышления', 'рус'): ('daily-reflections-ru.svg', ['ЕЖЕДНЕВНЫЕ', 'РАЗМЫШЛЕНИЯ'], 'КНИГА РАЗМЫШЛЕНИЙ ЧЛЕНОВ АА'),
    ('Ежедневные размышления', 'каз'): ('daily-reflections-kz.svg', ['КҮНДЕЛІКТІ', 'ОЙ-ТОЛҒАУ'], 'АА МҮШЕЛЕРІНІҢ КҮНДЕЛІКТІ ОҚУЛАРЫ'),
    ('Жить трезвыми', 'рус'): ('living-sober-ru.svg', ['ЖИТЬ', 'ТРЕЗВЫМИ'], 'НЕКОТОРЫЕ МЕТОДЫ СОХРАНЕНИЯ ТРЕЗВОСТИ'),
    ('Жить трезвыми', 'каз'): ('living-sober-kz.svg', ['САЛАУАТТЫ', 'ӨМІР СҮРУ'], 'САУЫҒУ ЖОЛЫНДАҒЫ ПРАКТИКАЛЫҚ КЕҢЕСТЕР'),
    ('Сбросить камень', 'рус'): ('drop-the-rock-ru.svg', ['СБРОСИТЬ', 'КАМЕНЬ'], 'УСТРАНЕНИЕ НЕДОСТАТКОВ ХАРАКТЕРА'),
    ('Сбросить камень', 'каз'): ('drop-the-rock-kz.svg', ['ТАСТЫ', 'ТАСТАУ'], 'МІНЕЗ-ҚҰЛЫҚ КЕМШІЛІКТЕРІНЕН АРЫЛУ'),
    ('Доктор Боб и славные ветераны', 'рус'): ('dr-bob-ru.svg', ['ДОКТОР БОБ', 'И СЛАВНЫЕ', 'ВЕТЕРАНЫ'], 'ИСТОРИЯ ПЕРВЫХ ЧЛЕНОВ АА'),
    ('АА Взрослеет', 'рус'): ('aa-comes-of-age-ru.svg', ['АНОНИМНЫЕ', 'АЛКОГОЛИКИ', 'ВЗРОСЛЕЮТ'], 'КРАТКАЯ ИСТОРИЯ АА'),
    ('Рук-во по обслуживанию АА + 12 Принципов', 'рус'): ('service-manual-ru.svg', ['РУКОВОДСТВО', 'ПО ОБСЛУЖИВАНИЮ АА'], '12 КОНЦЕПЦИЙ ВСЕМИРНОГО ОБСЛУЖИВАНИЯ'),
    ('Группа АА там где все начинается', 'рус'): ('group-aa-ru.svg', ['ГРУППА АА'], 'ТАМ, ГДЕ ВСЁ НАЧИНАЕТСЯ'),
}

def make_svg(lines, subtitle):
    title_start = 170 if len(lines) == 2 else 135
    title_size = 42 if max(map(len, lines)) < 20 else 32
    title_nodes = ''.join(
        f'<text x="300" y="{title_start + i * 58}" text-anchor="middle" class="title" font-size="{title_size}">{escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="920" viewBox="0 0 600 920">
<rect width="600" height="920" fill="#07073f"/>
<g fill="none" stroke="#d4a62a" stroke-width="4">
<rect x="24" y="24" width="552" height="872"/>
<rect x="38" y="38" width="524" height="844"/>
<path d="M24 92h74L130 58h340l32 34h74M24 828h74l32 34h340l32-34h74"/>
</g>
<g fill="#d4a62a" font-family="Georgia,serif" font-size="116" font-weight="700">
<text x="205" y="540">A</text><text x="318" y="540">A</text>
</g>
<g fill="#fff" font-family="Arial,sans-serif">
{title_nodes}
<text x="300" y="650" text-anchor="middle" font-size="23">{escape(subtitle)}</text>
<text x="300" y="790" text-anchor="middle" font-size="25">ЛИТЕРАТУРНЫЙ КОМИТЕТ</text>
<text x="300" y="826" text-anchor="middle" font-size="22">АНОНИМНЫХ АЛКОГОЛИКОВ В КАЗАХСТАНЕ</text>
<text x="300" y="866" text-anchor="middle" font-size="22">АЛМАТЫ · 2025</text>
</g>
</svg>'''

cover_map = {}
for key, (filename, lines, subtitle) in cover_specs.items():
    path = cover_dir / filename
    path.write_text(make_svg(lines, subtitle), encoding='utf-8')
    cover_map[key] = str(path).replace('\\', '/')

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
    if not Path(relative).is_file() or Path(relative).stat().st_size < 500:
        raise SystemExit(f'Invalid cover file: {relative}')
json.loads(books_path.read_text(encoding='utf-8'))
print(f'Applied {len(matched)} covers; retained all {original_count} books')
