from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# CSS: priority 3
marker = "        /* Разделитель только между крупными смысловыми блоками */"
css = r'''        /* Приоритет 3: доступность и понятные действия */
        .text-size-setting { padding: 4px 0 14px; }
        .text-size-title { font-size: 14px; font-weight: 800; color: var(--text-main); margin-bottom: 9px; }
        .text-size-options { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
        .text-size-btn { min-height: 44px; border: 1px solid var(--border); border-radius: 12px; background: var(--card-bg); color: var(--primary); font: inherit; font-size: 13px; font-weight: 800; cursor: pointer; }
        .text-size-btn.active { background: var(--primary); border-color: var(--primary); color: white; }

        .group-actions { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 9px; margin-top: 14px; }
        .group-action { min-height: 46px; border: 1px solid var(--border); border-radius: 12px; background: var(--card-bg); color: var(--primary); font: inherit; font-size: 13px; font-weight: 850; text-decoration: none; display: flex; align-items: center; justify-content: center; text-align: center; cursor: pointer; }
        .group-action.primary { background: var(--primary); border-color: var(--primary); color: white; }
        .group-action.full { grid-column: 1 / -1; }

        .app-status { position: fixed; left: 50%; bottom: calc(88px + env(safe-area-inset-bottom)); transform: translate(-50%, 18px); width: calc(100% - 30px); max-width: 470px; z-index: 6000; padding: 11px 14px; border-radius: 13px; background: var(--text-main); color: var(--card-bg); font-size: 13px; font-weight: 750; line-height: 1.35; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,.2); opacity: 0; pointer-events: none; transition: opacity .2s ease, transform .2s ease; }
        .app-status.show { opacity: 1; transform: translate(-50%, 0); }

        body.large-text .group-name { font-size: 21px; }
        body.large-text .info-row { font-size: 16px; line-height: 1.55; }
        body.large-text .phone-link { font-size: 17px; }
        body.large-text .group-action { min-height: 52px; font-size: 15px; }
        body.large-text .notification-item-title,
        body.large-text .notification-setting-title { font-size: 16px; }
        body.large-text .notification-item-text,
        body.large-text .notification-setting-note { font-size: 14px; }
        body.large-text .nav-txt { font-size: 11px; }
        body.large-text .nav-icon { width: 26px; height: 26px; }
        body.large-text .nav-item { min-height: 61px; }
        body.large-text .bottom-nav { min-height: 84px; }
        body.large-text .main-container { padding-bottom: 112px; }

'''
if css not in s:
    s = s.replace(marker, css + marker)

# Settings control
needle = '''                <div class="settings-version"><span id="settings-version-label">Версия приложения</span>: <strong id="settings-version-value">1.6</strong><br><span id="settings-update-label">Обновление применяется автоматически при запуске</span></div>'''
replacement = '''                <div class="text-size-setting">
                    <div class="text-size-title" id="text-size-title">Размер текста</div>
                    <div class="text-size-options">
                        <button type="button" class="text-size-btn active" id="text-size-normal" data-text-size="normal">Обычный</button>
                        <button type="button" class="text-size-btn" id="text-size-large" data-text-size="large">Крупный</button>
                    </div>
                </div>
                <div class="settings-version"><span id="settings-version-label">Версия приложения</span>: <strong id="settings-version-value">1.7</strong><br><span id="settings-update-label">Обновление применяется автоматически при запуске</span></div>'''
s = s.replace(needle, replacement)

# Global status element
s = s.replace('</nav>\n\n<script>', '</nav>\n<div class="app-status" id="app-status" role="status" aria-live="polite"></div>\n\n<script>')

# i18n additions
s = s.replace("versionLabel: 'Версия приложения', updateLabel: 'Обновление применяется автоматически при запуске', understood: 'Понятно'", "versionLabel: 'Версия приложения', updateLabel: 'Обновление применяется автоматически при запуске', textSizeTitle: 'Размер текста', textSizeNormal: 'Обычный', textSizeLarge: 'Крупный', statusUpdating: 'Обновляем данные…', statusUpdated: 'Данные обновлены', statusOffline: 'Нет интернета. Показана сохранённая версия', statusZoomFailed: 'Не удалось открыть Zoom', statusNoPhone: 'Номер телефона не указан', understood: 'Понятно'")
s = s.replace("versionLabel: 'Қосымша нұсқасы', updateLabel: 'Жаңарту қосымша іске қосылғанда автоматты түрде қолданылады', understood: 'Түсінікті'", "versionLabel: 'Қосымша нұсқасы', updateLabel: 'Жаңарту қосымша іске қосылғанда автоматты түрде қолданылады', textSizeTitle: 'Мәтін өлшемі', textSizeNormal: 'Қалыпты', textSizeLarge: 'Үлкен', statusUpdating: 'Деректер жаңартылуда…', statusUpdated: 'Деректер жаңартылды', statusOffline: 'Интернет жоқ. Сақталған нұсқа көрсетілді', statusZoomFailed: 'Zoom ашылмады', statusNoPhone: 'Телефон нөмірі көрсетілмеген', understood: 'Түсінікті'")

# setLang bindings
lang_anchor = "        document.getElementById('city-onboarding-all').innerText = d.showAllCities;"
lang_extra = """        document.getElementById('city-onboarding-all').innerText = d.showAllCities;
        document.getElementById('text-size-title').innerText = d.textSizeTitle;
        document.getElementById('text-size-normal').innerText = d.textSizeNormal;
        document.getElementById('text-size-large').innerText = d.textSizeLarge;"""
s = s.replace(lang_anchor, lang_extra)

# Add helpers before goTo
helper_anchor = "    function goTo(tab, direction = null) {"
helpers = r'''    let appStatusTimer = null;

    function showAppStatus(message, duration = 2600) {
        const el = document.getElementById('app-status');
        if (!el || !message) return;
        clearTimeout(appStatusTimer);
        el.textContent = message;
        el.classList.add('show');
        appStatusTimer = setTimeout(() => el.classList.remove('show'), duration);
    }

    function applyTextSize(size) {
        const large = size === 'large';
        document.body.classList.toggle('large-text', large);
        localStorage.setItem('aa_text_size', large ? 'large' : 'normal');
        document.querySelectorAll('[data-text-size]').forEach(button => {
            button.classList.toggle('active', button.dataset.textSize === (large ? 'large' : 'normal'));
            button.setAttribute('aria-pressed', button.classList.contains('active') ? 'true' : 'false');
        });
    }

    function getPrimaryPhone(g) {
        return g && Array.isArray(g.p) && g.p.length ? g.p[0] : '';
    }

    function buildGroupActions(g) {
        const d = i18n[curLang];
        const phone = getPrimaryPhone(g);
        const map = (!g.online && g.a) ? build2GISLink(g) : '';
        const online = g.online && g.a ? g.a : (g.z || '');
        const actions = [];
        if (phone) actions.push(`<a href="tel:${cleanPhone(phone)}" class="group-action primary" data-track="group_phone" data-phone="${escapeHtml(phone)}">${d.callAction}</a>`);
        if (map) actions.push(`<a href="${map}" target="_blank" rel="noopener noreferrer" class="group-action" data-track="map_open" data-group="${escapeHtml(g.n)}" data-city="${escapeHtml(g.c)}">${d.route}</a>`);
        if (online) actions.push(`<a href="${escapeHtml(online)}" target="_blank" rel="noopener noreferrer" class="group-action${actions.length % 2 === 0 ? ' full' : ''}" data-online-action="true" data-track="open_online" data-group="${escapeHtml(g.n)}" data-city="${escapeHtml(g.c)}">${g.chat ? d.openChat : d.openZoom}</a>`);
        if (!actions.length) return `<button type="button" class="group-action full" data-no-phone="true">${d.statusNoPhone}</button>`;
        return actions.join('');
    }

'''
if helpers not in s:
    s = s.replace(helper_anchor, helpers + helper_anchor)

# Replace card internals: keep informational rows, add actions
old = '''                        ${renderAddress(g)}
                        ${renderOnlineLinks(g)}
                        <div class="info-row"><span class="info-row-icon">⏰</span><div><div class="muted">${i18n[curLang].scheduleLabel}</div><div>${escapeHtml(g.t || i18n[curLang].noSchedule)}</div></div></div>
                        ${g.p && g.p.length ? renderPhones(g.p) : ''}
                    </div>
                </div>`;'''
new = '''                        ${renderAddress(g)}
                        <div class="info-row"><span class="info-row-icon">⏰</span><div><div class="muted">${i18n[curLang].scheduleLabel}</div><div>${escapeHtml(g.t || i18n[curLang].noSchedule)}</div></div></div>
                        ${g.p && g.p.length ? renderPhones(g.p) : ''}
                    </div>
                    <div class="group-actions">${buildGroupActions(g)}</div>
                </div>`;'''
s = s.replace(old, new)

# loadNews states
s = s.replace("        if (!currentNewsData) {\n            container.innerHTML = `", "        if (!currentNewsData) {\n            showAppStatus(i18n[curLang].statusUpdating);\n            container.innerHTML = `")
s = s.replace("        if (!navigator.onLine && cachedNews) {\n            newsLoaded = true;", "        if (!navigator.onLine && cachedNews) {\n            showAppStatus(i18n[curLang].statusOffline, 3200);\n            newsLoaded = true;")
s = s.replace("            saveCachedNews(posts);\n            newsLoaded = true;", "            saveCachedNews(posts);\n            showAppStatus(i18n[curLang].statusUpdated);\n            newsLoaded = true;")

# Event bindings before initialization marker
bind_anchor = "    applySavedTheme();"
bindings = r'''    document.querySelectorAll('[data-text-size]').forEach(button => {
        button.addEventListener('click', () => applyTextSize(button.dataset.textSize));
    });

    document.addEventListener('click', event => {
        const noPhone = event.target.closest('[data-no-phone="true"]');
        if (noPhone) {
            event.preventDefault();
            showAppStatus(i18n[curLang].statusNoPhone);
            return;
        }
        const onlineAction = event.target.closest('[data-online-action="true"]');
        if (onlineAction && !onlineAction.getAttribute('href')) {
            event.preventDefault();
            showAppStatus(i18n[curLang].statusZoomFailed);
        }
    });

    window.addEventListener('offline', () => showAppStatus(i18n[curLang].statusOffline, 3200));
    window.addEventListener('online', () => showAppStatus(i18n[curLang].statusUpdated));

    applyTextSize(localStorage.getItem('aa_text_size') || 'normal');
'''
if bindings not in s:
    s = s.replace(bind_anchor, bindings + bind_anchor)

p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
sw_text = sw.read_text(encoding='utf-8').replace("aa-kaz-v6", "aa-kaz-v7")
sw.write_text(sw_text, encoding='utf-8')
