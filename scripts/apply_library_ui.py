from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_css_start = "        .book-item { background: var(--card-bg);"
old_css_end = "        .lang-kz { background: #FFF3E0; color: #E65100; }"
start = text.index(old_css_start)
end = text.index(old_css_end, start) + len(old_css_end)
new_css = '''        .library-contact { padding: 17px; text-align: left; }
        .library-contact-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }
        .library-contact-title { font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.07em; color: var(--accent); margin-bottom: 5px; }
        .library-contact-name { font-size: 18px; font-weight: 800; color: var(--text-main); }
        .library-contact-note { font-size: 12px; color: var(--text-sub); line-height: 1.45; margin-top: 4px; }
        .library-call { width: 44px; height: 44px; border-radius: 13px; background: var(--primary); color: white; text-decoration: none; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
        .library-phone { display: inline-block; margin-top: 10px; color: var(--link); text-decoration: none; font-size: 14px; font-weight: 800; }
        .book-filters { display: flex; gap: 8px; width: 100%; margin-bottom: 16px; }
        .book-filter { flex: 1; min-height: 42px; border: 1px solid var(--border); border-radius: 12px; background: var(--card-bg); color: var(--text-sub); font: inherit; font-size: 12px; font-weight: 800; cursor: pointer; }
        .book-filter.active { border-color: var(--primary); background: var(--primary); color: white; }
        .book-grid { width: 100%; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px 12px; align-items: start; }
        .book-item { min-width: 0; border: none; background: transparent; padding: 0; text-align: left; cursor: pointer; font: inherit; color: inherit; }
        .book-cover { aspect-ratio: 0.68; width: 100%; border-radius: 8px 13px 13px 8px; position: relative; overflow: hidden; padding: 16px 12px 14px 16px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 9px 20px rgba(0,0,0,0.16), inset 4px 0 0 rgba(255,255,255,0.18); transition: transform 0.2s ease, box-shadow 0.2s ease; }
        .book-item:active .book-cover { transform: translateY(2px) scale(0.985); box-shadow: 0 5px 12px rgba(0,0,0,0.14); }
        .book-cover::before { content: ''; position: absolute; inset: 0; background: linear-gradient(135deg, rgba(255,255,255,0.17), transparent 38%, rgba(0,0,0,0.12)); pointer-events: none; }
        .book-cover::after { content: ''; position: absolute; left: 7px; top: 0; bottom: 0; width: 1px; background: rgba(255,255,255,0.32); box-shadow: 2px 0 4px rgba(0,0,0,0.16); }
        .book-cover-0, .book-cover-5, .book-cover-10, .book-cover-15, .book-cover-20 { background: linear-gradient(155deg, #123d67, #00284d); color: white; }
        .book-cover-1, .book-cover-6, .book-cover-11, .book-cover-16, .book-cover-21 { background: linear-gradient(155deg, #b99b4b, #826817); color: white; }
        .book-cover-2, .book-cover-7, .book-cover-12, .book-cover-17, .book-cover-22 { background: linear-gradient(155deg, #f1e7d4, #d7c5a3); color: #183650; }
        .book-cover-3, .book-cover-8, .book-cover-13, .book-cover-18, .book-cover-23 { background: linear-gradient(155deg, #477269, #274b45); color: white; }
        .book-cover-4, .book-cover-9, .book-cover-14, .book-cover-19, .book-cover-24 { background: linear-gradient(155deg, #873f43, #542124); color: white; }
        .book-cover-mark { position: relative; z-index: 1; width: 38px; height: 38px; border: 1px solid currentColor; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 900; opacity: 0.9; }
        .book-cover-title { position: relative; z-index: 1; font-size: 13px; line-height: 1.22; font-weight: 850; overflow-wrap: anywhere; }
        .book-meta { padding: 9px 3px 0; }
        .book-title { font-size: 12px; font-weight: 800; color: var(--text-main); line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; min-height: 31px; }
        .lang-tag { display: inline-block; margin-top: 6px; font-size: 8px; padding: 3px 7px; border-radius: 6px; font-weight: 800; text-transform: uppercase; }
        .lang-ru { background: #E0F2F1; color: #00796B; }
        .lang-kz { background: #FFF3E0; color: #E65100; }
        .book-modal { position: fixed; inset: 0; z-index: 4000; display: none; align-items: flex-end; justify-content: center; background: rgba(0,0,0,0.52); padding: 18px 12px max(18px, env(safe-area-inset-bottom)); }
        .book-modal.open { display: flex; animation: fadeIn 0.18s ease; }
        .book-modal-panel { width: 100%; max-width: 500px; max-height: 88vh; overflow-y: auto; background: var(--card-bg); border-radius: 24px; padding: 18px; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }
        .book-modal-head { display: flex; gap: 16px; align-items: flex-start; }
        .book-modal-cover { width: 112px; flex-shrink: 0; }
        .book-modal-cover .book-cover { padding: 14px 10px 12px 14px; }
        .book-modal-cover .book-cover-title { font-size: 11px; }
        .book-modal-main { min-width: 0; flex: 1; }
        .book-modal-title { font-size: 20px; line-height: 1.25; font-weight: 850; color: var(--text-main); padding-right: 30px; }
        .book-modal-close { position: absolute; right: 18px; top: 16px; width: 34px; height: 34px; border: none; border-radius: 50%; background: var(--bg); color: var(--text-main); font-size: 20px; cursor: pointer; }
        .book-modal-panel { position: relative; }
        .book-modal-desc { margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--border); font-size: 14px; line-height: 1.6; color: var(--text-main); }
        .book-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; margin-top: 18px; }
        .book-action { min-height: 46px; border: 1px solid var(--border); border-radius: 13px; background: var(--card-bg); color: var(--primary); text-decoration: none; font: inherit; font-size: 12px; font-weight: 850; display: flex; align-items: center; justify-content: center; gap: 7px; cursor: pointer; text-align: center; }
        .book-action.primary { background: var(--primary); border-color: var(--primary); color: white; }
        .book-action.share { grid-column: 1 / -1; }
        body.modal-open { overflow: hidden; }'''
text = text[:start] + new_css + text[end:]

old_html_start = '    <div id="tab-lit" class="content-section">'
old_html_end = '    <div id="tab-groups" class="content-section">'
start = text.index(old_html_start)
end = text.index(old_html_end, start)
new_html = '''    <div id="tab-lit" class="content-section">
        <div class="card library-contact">
            <div class="library-contact-top">
                <div>
                    <div class="library-contact-title" id="t-lit-com">Литературный комитет</div>
                    <div class="library-contact-name">Вячеслав</div>
                    <div class="library-contact-note" id="t-lit-price">Наличие, цены и заказ литературы</div>
                </div>
                <a href="tel:+77775567141" class="library-call" aria-label="Позвонить Вячеславу">📞</a>
            </div>
            <a href="tel:+77775567141" class="library-phone">+7 (777) 556-71-41</a>
        </div>
        <div class="ornament-divider"></div>
        <div class="book-filters" id="book-filters">
            <button type="button" class="book-filter active" data-book-filter="all">Все</button>
            <button type="button" class="book-filter" data-book-filter="рус">Рус</button>
            <button type="button" class="book-filter" data-book-filter="каз">Қаз</button>
        </div>
        <div id="book-list" class="book-grid"></div>
    </div>

    <div id="book-modal" class="book-modal" aria-hidden="true">
        <div class="book-modal-panel" role="dialog" aria-modal="true" aria-labelledby="book-modal-title">
            <button type="button" class="book-modal-close" id="book-modal-close" aria-label="Закрыть">×</button>
            <div id="book-modal-content"></div>
        </div>
    </div>

'''
text = text[:start] + new_html + text[end:]

text = text.replace(
    "placeholder: 'Ваши мысли, благодарности или инсайты...', litCom: 'ЛИТЕРАТУРНЫЙ КОМИТЕТ', litPrice: 'Наличие и цены:',",
    "placeholder: 'Ваши мысли, благодарности или инсайты...', litCom: 'Литературный комитет', litPrice: 'Наличие, цены и заказ литературы', bookAll: 'Все', bookRu: 'Рус', bookKz: 'Қаз', bookBuy: 'Купить', bookCall: 'Позвонить', bookShare: 'Поделиться',"
)
text = text.replace(
    "placeholder: 'Ойларыңыз, ризашылықтарыңыз немесе инсайттарыңыз...', litCom: 'ӘДЕБИЕТ КОМИТЕТІ', litPrice: 'Қолжетімділігі мен бағасы:',",
    "placeholder: 'Ойларыңыз, ризашылықтарыңыз немесе инсайттарыңыз...', litCom: 'Әдебиет комитеті', litPrice: 'Әдебиеттің бар-жоғы, бағасы және тапсырыс', bookAll: 'Барлығы', bookRu: 'Рус', bookKz: 'Қаз', bookBuy: 'Сатып алу', bookCall: 'Қоңырау шалу', bookShare: 'Бөлісу',"
)

text = text.replace("    let onlyToday = false;\n    let saveTimeout = null;", "    let onlyToday = false;\n    let currentBookFilter = 'all';\n    let activeBookIndex = null;\n    let saveTimeout = null;")

old_block_start = '    function toggleBook(id) {'
old_block_end = '    function getGroupStatus(g) {'
start = text.index(old_block_start)
end = text.index(old_block_end, start)
new_block = '''    function getBookCover(index, book, compact = false) {
        const language = book.l === 'рус' ? 'RU' : 'ҚАЗ';
        return `
            <div class="book-cover book-cover-${index % 25}">
                <div class="book-cover-mark">АА</div>
                <div class="book-cover-title">${escapeHtml(book.n)}</div>
                <div class="book-cover-mark" style="width:auto;height:auto;border:none;border-radius:0;justify-content:flex-start;font-size:9px;">${language}</div>
            </div>
        `;
    }

    function renderLit() {
        const c = document.getElementById('book-list');
        const filteredBooks = books
            .map((book, index) => ({ book, index }))
            .filter(item => currentBookFilter === 'all' || item.book.l === currentBookFilter);

        c.innerHTML = filteredBooks.map(({ book, index }) => `
            <button type="button" class="book-item" data-book-index="${index}" aria-label="${escapeHtml(book.n)}">
                ${getBookCover(index, book)}
                <div class="book-meta">
                    <div class="book-title">${escapeHtml(book.n)}</div>
                    <span class="lang-tag lang-${book.l === 'рус' ? 'ru' : 'kz'}">${escapeHtml(book.l)}</span>
                </div>
            </button>
        `).join('');
    }

    function setBookFilter(filter) {
        currentBookFilter = filter;
        document.querySelectorAll('.book-filter').forEach(button => {
            button.classList.toggle('active', button.dataset.bookFilter === filter);
        });
        trackEvent('book_filter', filter);
        renderLit();
    }

    function openBook(index) {
        const book = books[Number(index)];
        if (!book) return;
        activeBookIndex = Number(index);
        const d = i18n[curLang];
        const content = document.getElementById('book-modal-content');
        content.innerHTML = `
            <div class="book-modal-head">
                <div class="book-modal-cover">${getBookCover(activeBookIndex, book, true)}</div>
                <div class="book-modal-main">
                    <div class="book-modal-title" id="book-modal-title">${escapeHtml(book.n)}</div>
                    <span class="lang-tag lang-${book.l === 'рус' ? 'ru' : 'kz'}">${escapeHtml(book.l)}</span>
                </div>
            </div>
            <div class="book-modal-desc">${escapeHtml(book.d)}</div>
            <div class="book-actions">
                <a href="tel:+77775567141" class="book-action primary" data-book-action="buy">🛒 ${d.bookBuy}</a>
                <a href="tel:+77775567141" class="book-action" data-book-action="call">📞 ${d.bookCall}</a>
                <button type="button" class="book-action share" data-book-action="share">↗ ${d.bookShare}</button>
            </div>
        `;
        const modal = document.getElementById('book-modal');
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('modal-open');
        trackEvent('book_open', book.n);
    }

    function closeBook() {
        const modal = document.getElementById('book-modal');
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('modal-open');
        activeBookIndex = null;
    }

    async function shareBook() {
        const book = books[activeBookIndex];
        if (!book) return;
        const shareText = `${book.n}\n\n${book.d}\n\nЛитературный комитет АА Казахстана: +7 (777) 556-71-41`;
        try {
            if (navigator.share) {
                await navigator.share({ title: book.n, text: shareText });
            } else if (navigator.clipboard) {
                await navigator.clipboard.writeText(shareText);
                alert(curLang === 'kz' ? 'Кітап туралы ақпарат көшірілді' : 'Информация о книге скопирована');
            }
            trackEvent('book_share', book.n);
        } catch (error) {
            if (error && error.name !== 'AbortError') console.error('Ошибка отправки:', error);
        }
    }

'''
text = text[:start] + new_block + text[end:]

text = text.replace(
    "        document.getElementById('t-lit-price').innerText = d.litPrice;",
    "        document.getElementById('t-lit-price').innerText = d.litPrice;\n        const bookFilterButtons = document.querySelectorAll('.book-filter');\n        if (bookFilterButtons.length === 3) {\n            bookFilterButtons[0].innerText = d.bookAll;\n            bookFilterButtons[1].innerText = d.bookRu;\n            bookFilterButtons[2].innerText = d.bookKz;\n        }"
)

old_event = '''        document.getElementById('book-list').addEventListener('click', e => {
            const item = e.target.closest('.book-item');
            if (!item) return;
            toggleBook(item.getAttribute('data-book-index'));
        });'''
new_event = '''        document.getElementById('book-filters').addEventListener('click', e => {
            const button = e.target.closest('[data-book-filter]');
            if (button) setBookFilter(button.dataset.bookFilter);
        });
        document.getElementById('book-list').addEventListener('click', e => {
            const item = e.target.closest('.book-item');
            if (item) openBook(item.getAttribute('data-book-index'));
        });
        document.getElementById('book-modal-close').addEventListener('click', closeBook);
        document.getElementById('book-modal').addEventListener('click', e => {
            if (e.target.id === 'book-modal') closeBook();
            const action = e.target.closest('[data-book-action]');
            if (!action) return;
            const book = books[activeBookIndex];
            if (action.dataset.bookAction === 'share') shareBook();
            if (book && action.dataset.bookAction === 'buy') trackEvent('book_buy', book.n);
            if (book && action.dataset.bookAction === 'call') trackEvent('call', 'literature_committee', { book: book.n });
        });
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && document.getElementById('book-modal').classList.contains('open')) closeBook();
        });'''
if old_event not in text:
    raise SystemExit('Old book event block not found')
text = text.replace(old_event, new_event)

path.write_text(text, encoding='utf-8')
print('Library UI updated')
