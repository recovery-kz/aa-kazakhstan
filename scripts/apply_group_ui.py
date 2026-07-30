from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

names = {
    'АА «ШАГ ЗА ШАГОМ»': 'АА «Шаг за шагом»',
    'АА «8 марта»': 'АА «8 Марта»',
    'АА «АлмА» (женская)': 'АА «Алма» (женская)',
    'АА «НОВЫЕ ОЧКИ»': 'АА «Новые очки»',
    'АА «боралдай»': 'АА «Боралдай»',
    'АА «большая перемена»': 'АА «Большая перемена»',
    'АА «ПУТЬ»': 'АА «Путь»',
    'АА «ВОЗРОЖДЕНИЕ»': 'АА «Возрождение»',
    'АА «гармония»': 'АА «Гармония»',
    'АА «үміт» (каз)': 'АА «Үміт» (каз)',
    'АА «ОАЗИС»': 'АА «Оазис»',
    'АА «НАЧАЛО»': 'АА «Начало»',
    'АА «решение есть»': 'АА «Решение есть»',
    'АА «НАДЕЖДА»': 'АА «Надежда»',
    'АА «ДОСТАР»': 'АА «Достар»',
    'АА «СЕМЁРОЧКА»': 'АА «Семёрочка»',
    'АА «жетысу»': 'АА «Жетысу»',
    'АА «УСТЬЕ»': 'АА «Устье»',
    'АА «сырдарья»': 'АА «Сырдарья»',
    'АА «СВОБОДА»': 'АА «Свобода»',
    'АА «ПАНА» (каз)': 'АА «Пана» (каз)',
    'АА «куат»': 'АА «Куат»',
}
for old, new in names.items():
    text = text.replace(old, new)

css_start = text.index('        .group-card {')
css_end = text.index('        /* Тонкие орнаментальные разделители */', css_start)
new_css = '''        .group-card { border-left: 5px solid var(--primary); padding: 16px; text-align: left; position: relative; }
        .group-card.favorite { border-left-color: var(--accent); }
        .group-card-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
        .group-card-main { min-width: 0; flex: 1; }
        .favorite-btn { width: 38px; height: 38px; flex-shrink: 0; border: 1px solid var(--border); border-radius: 12px; background: var(--card-bg); color: var(--nav-inactive); font-size: 20px; line-height: 1; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        .favorite-btn.active { color: var(--accent); border-color: var(--accent); background: var(--card-bg); }
        .status-badge { font-size: 9px; line-height: 1.2; font-weight: 800; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 8px; display: flex; align-items: center; }
        .status-dot { width: 7px; height: 7px; border-radius: 50%; margin-right: 6px; }
        .s-open { color: var(--open); } .s-open .status-dot { background: var(--open); }
        .s-soon { color: var(--soon); } .s-soon .status-dot { background: var(--soon); }
        .s-closed { color: var(--closed); } .s-closed .status-dot { background: var(--closed); }
        .group-name { font-size: 18px; font-weight: 800; color: var(--text-main); margin-bottom: 5px; line-height: 1.28; letter-spacing: -0.01em; }
        .city-tag { font-size: 10px; color: var(--text-sub); font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 5px; }
        .group-icons { font-size: 13px; margin-left: 5px; letter-spacing: 0; }
        .group-info { margin-top: 12px; border-top: 1px solid var(--border); }
        .info-row { display: flex; gap: 10px; align-items: flex-start; padding: 11px 0; margin: 0; font-size: 13px; line-height: 1.5; color: var(--text-main); border-bottom: 1px solid var(--border); }
        .info-row:last-child { border-bottom: none; padding-bottom: 0; }
        .info-row-icon { width: 20px; flex-shrink: 0; text-align: center; color: var(--accent); padding-top: 1px; }
        .info-row > div { min-width: 0; flex: 1; }
        .group-phones { display: flex; flex-direction: column; gap: 7px; margin-top: 3px; }
        .phone-link, .inline-link { color: var(--link); text-decoration: none; font-weight: 700; }
        .phone-link { font-size: 14px; }
        .inline-link { display: inline-block; margin-top: 4px; }
        .muted { color: var(--text-sub); font-size: 9px; line-height: 1.2; font-weight: 800; letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 3px; }
        .groups-empty { padding: 24px 18px; text-align: center; color: var(--text-sub); font-size: 14px; line-height: 1.5; }

'''
text = text[:css_start] + new_css + text[css_end:]

text = text.replace("allCities: 'Все города',", "allCities: 'Все города', favorites: '★ Избранное', noFavorites: 'Добавьте нужные группы в избранное, нажав на звезду в карточке.', addFavorite: 'Добавить в избранное', removeFavorite: 'Убрать из избранного',")
text = text.replace("allCities: 'Барлық қалалар',", "allCities: 'Барлық қалалар', favorites: '★ Таңдаулылар', noFavorites: 'Қажетті топтарды карточкадағы жұлдызшаны басып таңдаулыларға қосыңыз.', addFavorite: 'Таңдаулыларға қосу', removeFavorite: 'Таңдаулылардан алып тастау',")
text = text.replace("    const NEWS_STORAGE_KEY = 'aa_news_cache_v1';", "    const NEWS_STORAGE_KEY = 'aa_news_cache_v1';\n    const FAVORITES_STORAGE_KEY = 'aa_group_favorites_v1';")

anchor = "    function cleanPhone(phone) { return String(phone || '').replace(/[^\\d+]/g, ''); }"
helpers = '''    function getGroupId(g) {
        return [g.c, g.n, g.a || '', g.t || ''].join('|');
    }

    function getFavoriteGroups() {
        try {
            const saved = JSON.parse(localStorage.getItem(FAVORITES_STORAGE_KEY) || '[]');
            return new Set(Array.isArray(saved) ? saved : []);
        } catch (error) {
            return new Set();
        }
    }

    function saveFavoriteGroups(favorites) {
        localStorage.setItem(FAVORITES_STORAGE_KEY, JSON.stringify([...favorites]));
    }

    function toggleFavorite(groupId) {
        const favorites = getFavoriteGroups();
        const isAdding = !favorites.has(groupId);
        if (isAdding) favorites.add(groupId);
        else favorites.delete(groupId);
        saveFavoriteGroups(favorites);
        trackEvent(isAdding ? 'group_favorite_add' : 'group_favorite_remove', groupId);
        renderGroups();
    }

'''
text = text.replace(anchor, helpers + anchor)

render_start = text.index('    function renderGroups() {')
render_end = text.index('    function rebuildCityOptions() {', render_start)
new_render = '''    function renderGroups() {
        const selected = document.getElementById('citySelect').value;
        const c = document.getElementById('list-container');
        const currentDay = new Date().getDay();
        const favorites = getFavoriteGroups();
        const filtered = data.filter(g => {
            const matchesLocation = selected === 'all' || g.c === selected || (selected === 'favorites' && favorites.has(getGroupId(g)));
            const matchesToday = !onlyToday || g.sc.some(s => s.d === currentDay);
            return matchesLocation && matchesToday;
        });
        if (selected === 'favorites' && filtered.length === 0) {
            c.innerHTML = `<div class="card groups-empty">${i18n[curLang].noFavorites}</div>`;
            return;
        }
        c.innerHTML = filtered.map(g => {
            const icons = `${g.online ? '🌍' : '👤'} ${g.f ? '👩' : ''} ${g.k ? '🇰🇿' : ''}`.trim();
            const groupId = getGroupId(g);
            const isFavorite = favorites.has(groupId);
            const favoriteLabel = isFavorite ? i18n[curLang].removeFavorite : i18n[curLang].addFavorite;
            return `
                <div class="card group-card${isFavorite ? ' favorite' : ''}">
                    <div class="group-card-head">
                        <div class="group-card-main">
                            ${getGroupStatus(g)}
                            <div class="city-tag">${escapeHtml(g.c)}</div>
                            <div class="group-name">${escapeHtml(g.n)} ${icons ? `<span class="group-icons">${icons}</span>` : ''}</div>
                        </div>
                        <button type="button" class="favorite-btn${isFavorite ? ' active' : ''}" data-favorite-id="${escapeHtml(groupId)}" aria-label="${escapeHtml(favoriteLabel)}" title="${escapeHtml(favoriteLabel)}">${isFavorite ? '★' : '☆'}</button>
                    </div>
                    <div class="group-info">
                        ${renderAddress(g)}
                        ${renderOnlineLinks(g)}
                        <div class="info-row"><span class="info-row-icon">⏰</span><div><div class="muted">${i18n[curLang].scheduleLabel}</div><div>${escapeHtml(g.t || i18n[curLang].noSchedule)}</div></div></div>
                        ${g.p && g.p.length ? renderPhones(g.p) : ''}
                    </div>
                </div>`;
        }).join('');
    }

'''
text = text[:render_start] + new_render + text[render_end:]

city_start = text.index('    function rebuildCityOptions() {')
city_end = text.index('    function applySavedTheme() {', city_start)
new_city = '''    function rebuildCityOptions() {
        const s = document.getElementById('citySelect');
        const current = s.value || 'all';
        const cities = [...new Set(data.map(x => x.c))].sort((a,b) => a.localeCompare(b, 'ru'));
        const ct = ['all', 'favorites', ...cities];
        s.innerHTML = '';
        ct.forEach(city => {
            const o = document.createElement('option');
            o.value = city;
            o.innerText = city === 'all' ? i18n[curLang].allCities : city === 'favorites' ? i18n[curLang].favorites : city;
            s.appendChild(o);
        });
        s.value = [...s.options].some(opt => opt.value === current) ? current : 'all';
    }

'''
text = text[:city_start] + new_city + text[city_end:]

listener = "    document.getElementById('todayFilter').addEventListener('click', toggleToday);"
text = text.replace(listener, listener + "\n    document.getElementById('list-container').addEventListener('click', event => {\n        const button = event.target.closest('[data-favorite-id]');\n        if (!button) return;\n        toggleFavorite(button.dataset.favoriteId);\n    });")

if text.count("{c:") != 43:
    raise SystemExit(f'Unexpected group count: {text.count("{c:")}')
if "value = 'favorites'" not in text and "['all', 'favorites'" not in text:
    raise SystemExit('Favorites filter was not added')

path.write_text(text, encoding='utf-8')

sw = Path('service-worker.js')
sw_text = sw.read_text(encoding='utf-8').replace("const CACHE_NAME = 'aa-kaz-v2';", "const CACHE_NAME = 'aa-kaz-v3';")
sw.write_text(sw_text, encoding='utf-8')
