from pathlib import Path

index_path = Path('index.html')
text = index_path.read_text(encoding='utf-8')

old_nav_css = '''        .bottom-nav {
            position: fixed;
            bottom: 0;
            width: 100%;
            background: var(--nav-bg);
            display: flex;
            height: 75px;
            box-shadow: 0 -4px 15px rgba(0,0,0,0.05);
            z-index: 2000;
            padding-bottom: env(safe-area-inset-bottom);
            border-top: 2px solid var(--accent); /* Песочно-золотая плашка */
        }

        .nav-item { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--nav-inactive); cursor: pointer; border: none; background: none; padding: 2px; min-width: 0; }
        .nav-item.active-nav { color: var(--primary); font-weight: 800; }
        .nav-txt { font-size: 8px; text-transform: uppercase; letter-spacing: 0.1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%; text-align: center; }
'''

new_nav_css = '''        .bottom-nav {
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            width: 100%;
            min-height: 78px;
            background: color-mix(in srgb, var(--nav-bg) 96%, transparent);
            display: flex;
            align-items: stretch;
            box-shadow: 0 -8px 28px rgba(0,0,0,0.08);
            z-index: 2000;
            padding: 5px 6px max(5px, env(safe-area-inset-bottom));
            border-top: 1px solid var(--border);
            backdrop-filter: blur(14px);
        }

        .nav-item {
            flex: 1;
            min-width: 0;
            min-height: 56px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 3px;
            color: var(--nav-inactive);
            cursor: pointer;
            border: none;
            border-radius: 16px;
            background: transparent;
            padding: 5px 2px;
            transition: color .2s ease, background .2s ease, transform .2s ease;
        }
        .nav-item:active { transform: scale(.97); }
        .nav-icon-wrap {
            width: 38px;
            height: 30px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: width .2s ease, background .2s ease;
        }
        .nav-icon { width: 23px; height: 23px; display: block; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
        .nav-item.active-nav { color: var(--primary); font-weight: 800; }
        .nav-item.active-nav .nav-icon-wrap { width: 48px; background: color-mix(in srgb, var(--accent) 18%, transparent); }
        .nav-item.active-nav .nav-icon { width: 25px; height: 25px; }
        .nav-txt { font-size: 10px; line-height: 1.1; letter-spacing: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%; text-align: center; }
'''

if old_nav_css not in text:
    raise SystemExit('Navigation CSS block not found')
text = text.replace(old_nav_css, new_nav_css, 1)

old_ornament_css = '''        /* Тонкие орнаментальные разделители */
        .ornament-divider {
            width: 100%;
            height: 20px;
            background-image: url('data:image/svg+xml;charset=UTF-8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="20" viewBox="0 0 100 20"><path d="M0 10 Q 25 0, 50 10 T 100 10" stroke="%23D4AF37" stroke-width="1" fill="none"/></svg>'); /* Линейный орнамент */
            background-repeat: repeat-x;
            opacity: 0.5;
            margin: 10px 0;
        }
'''
new_ornament_css = '''        /* Разделитель только между крупными смысловыми блоками */
        .ornament-divider {
            width: 100%;
            height: 1px;
            background: color-mix(in srgb, var(--accent) 28%, var(--border));
            opacity: .65;
            margin: 16px 0;
        }
'''
if old_ornament_css not in text:
    raise SystemExit('Ornament CSS block not found')
text = text.replace(old_ornament_css, new_ornament_css, 1)

button_system = '''
        /* Единая система действий */
        .btn-primary,
        .city-onboarding-btn,
        .book-action.primary,
        .sos-main-btn {
            min-height: 48px;
            border: 1px solid var(--primary);
            border-radius: 13px;
            background: var(--primary);
            color: white;
            font: inherit;
            font-weight: 800;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        .btn-secondary,
        .city-onboarding-btn.secondary,
        .book-action:not(.primary),
        .group-quick-filter,
        .notification-small-btn {
            min-height: 44px;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: var(--card-bg);
            color: var(--primary);
            font: inherit;
            font-weight: 800;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        .btn-icon,
        .favorite-btn,
        .book-modal-close,
        .notification-close,
        .library-call {
            width: 44px;
            height: 44px;
            min-width: 44px;
            min-height: 44px;
            padding: 0;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: var(--card-bg);
            color: var(--primary);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
'''
text = text.replace('        /* Разделитель только между крупными смысловыми блоками */', button_system + '\n        /* Разделитель только между крупными смысловыми блоками */', 1)

old_nav_html = '''<nav class="bottom-nav">
    <button class="nav-item active-nav" id="btn-c" type="button" data-tab="counter"><span>⏱</span><span class="nav-txt">Сегодня</span></button>
    <button class="nav-item" id="btn-n" type="button" data-tab="news"><span>📰</span><span class="nav-txt">Новости</span></button>
    <button class="nav-item" id="btn-l" type="button" data-tab="lit"><span>📚</span><span class="nav-txt">Книги</span></button>
    <button class="nav-item" id="btn-g" type="button" data-tab="groups"><span>📍</span><span class="nav-txt">Группы</span></button>
    <button class="nav-item" id="btn-p" type="button" data-tab="profile"><span>👤</span><span class="nav-txt" id="n-prof">Мой путь</span></button>
</nav>'''

new_nav_html = '''<nav class="bottom-nav" aria-label="Основная навигация">
    <button class="nav-item active-nav" id="btn-c" type="button" data-tab="counter" aria-label="Сегодня">
        <span class="nav-icon-wrap"><svg class="nav-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4M16 3v4M3 10h18"/><circle cx="12" cy="15" r="2"/></svg></span><span class="nav-txt">Сегодня</span>
    </button>
    <button class="nav-item" id="btn-n" type="button" data-tab="news" aria-label="Новости">
        <span class="nav-icon-wrap"><svg class="nav-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h13a2 2 0 0 1 2 2v12H6a2 2 0 0 1-2-2V5Z"/><path d="M19 9h1a1 1 0 0 1 1 1v7a2 2 0 0 1-2 2M8 9h7M8 13h7M8 17h4"/></svg></span><span class="nav-txt">Новости</span>
    </button>
    <button class="nav-item" id="btn-l" type="button" data-tab="lit" aria-label="Книги">
        <span class="nav-icon-wrap"><svg class="nav-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5.5A2.5 2.5 0 0 1 5.5 3H11v16H5.5A2.5 2.5 0 0 0 3 21.5v-16Z"/><path d="M21 5.5A2.5 2.5 0 0 0 18.5 3H13v16h5.5a2.5 2.5 0 0 1 2.5 2.5v-16Z"/></svg></span><span class="nav-txt">Книги</span>
    </button>
    <button class="nav-item" id="btn-g" type="button" data-tab="groups" aria-label="Группы">
        <span class="nav-icon-wrap"><svg class="nav-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3"/><circle cx="5.5" cy="10" r="2"/><circle cx="18.5" cy="10" r="2"/><path d="M6.5 19c.4-3 2.2-5 5.5-5s5.1 2 5.5 5M2.5 18c.3-2.1 1.5-3.5 3.7-3.8M21.5 18c-.3-2.1-1.5-3.5-3.7-3.8"/></svg></span><span class="nav-txt">Группы</span>
    </button>
    <button class="nav-item" id="btn-p" type="button" data-tab="profile" aria-label="Мой путь">
        <span class="nav-icon-wrap"><svg class="nav-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="9" r="3"/><path d="M6.8 18.2c1.1-2.5 2.8-3.7 5.2-3.7s4.1 1.2 5.2 3.7"/></svg></span><span class="nav-txt" id="n-prof">Мой путь</span>
    </button>
</nav>'''

if old_nav_html not in text:
    raise SystemExit('Navigation HTML block not found')
text = text.replace(old_nav_html, new_nav_html, 1)

# Remove decorative dividers from minor internal transitions.
for fragment in [
    '            <div class="ornament-divider"></div> <button class="acc-btn" type="button" data-acc-target="acc-prayer"',
    '            <div class="ornament-divider"></div> <button class="acc-btn" type="button" data-acc-target="acc-notes"',
    '            <div class="ornament-divider"></div> <button class="acc-btn" type="button" data-acc-target="acc-settings"',
    '                <div class="ornament-divider"></div>\n                <div class="notification-settings"',
    '        <div class="ornament-divider"></div>\n        <div class="book-filters"',
    '        <div class="ornament-divider"></div> <div id="list-container" style="width:100%;"></div>'
]:
    text = text.replace(fragment, fragment.replace('<div class="ornament-divider"></div> ', '').replace('<div class="ornament-divider"></div>\n                ', '').replace('<div class="ornament-divider"></div>\n        ', ''))

# Remove emoji from Seventh Tradition title; meaning remains explicit in the note.
text = text.replace("kaspi: '❤️ Седьмая Традиция'", "kaspi: 'Седьмая Традиция'")
text = text.replace("kaspi: '❤️ Жетінші Дәстүр'", "kaspi: 'Жетінші Дәстүр'")
text = text.replace('id="t-kaspi">❤️ Седьмая Традиция</span>', 'id="t-kaspi">Седьмая Традиция</span>')

index_path.write_text(text, encoding='utf-8')

sw_path = Path('sw.js')
sw = sw_path.read_text(encoding='utf-8')
sw = sw.replace("const CACHE_NAME = 'aa-kaz-v5';", "const CACHE_NAME = 'aa-kaz-v6';")
sw_path.write_text(sw, encoding='utf-8')

print('Visual phase 2 applied')
