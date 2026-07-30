from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# CSS
css_anchor = "        .bottom-nav {"
css = r'''        .today-actions { width:100%; display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; margin:0 0 15px; }
        .today-action { min-height:72px; border:1px solid var(--border); border-radius:16px; background:var(--card-bg); color:var(--text-main); font:inherit; font-size:13px; font-weight:850; line-height:1.25; padding:12px; display:flex; flex-direction:column; align-items:flex-start; justify-content:space-between; text-align:left; cursor:pointer; box-shadow:0 3px 10px rgba(0,0,0,.04); }
        .today-action-icon { font-size:22px; line-height:1; }
        .nearest-card { padding:17px; text-align:left; }
        .nearest-label { color:var(--accent); font-size:10px; font-weight:900; letter-spacing:.07em; text-transform:uppercase; margin-bottom:7px; }
        .nearest-name { color:var(--text-main); font-size:19px; line-height:1.25; font-weight:900; }
        .nearest-time { color:var(--primary); font-size:15px; font-weight:850; margin-top:7px; }
        .nearest-remaining { color:var(--text-sub); font-size:12px; margin-top:3px; }
        .nearest-actions { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; margin-top:15px; }
        .nearest-action { min-height:43px; border:1px solid var(--border); border-radius:12px; background:var(--card-bg); color:var(--primary); font:inherit; font-size:12px; font-weight:850; text-decoration:none; display:flex; align-items:center; justify-content:center; text-align:center; cursor:pointer; }
        .nearest-action.primary { background:var(--primary); border-color:var(--primary); color:white; }
        .nearest-empty { color:var(--text-sub); font-size:13px; line-height:1.5; }
        .group-quick-filters { width:100%; display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; margin-bottom:10px; }
        .group-quick-filter { min-height:43px; border:1px solid var(--border); border-radius:12px; background:var(--card-bg); color:var(--text-main); font:inherit; font-size:12px; font-weight:850; cursor:pointer; }
        .group-quick-filter.active { background:var(--primary); border-color:var(--primary); color:white; }
        .group-city-row { width:100%; display:flex; gap:8px; margin-bottom:6px; }
        .group-city-row #citySelect { width:100%; flex:1; }
        .city-onboarding { position:fixed; inset:0; z-index:5000; background:rgba(0,0,0,.58); display:none; align-items:flex-end; justify-content:center; padding:14px 12px max(14px,env(safe-area-inset-bottom)); }
        .city-onboarding.open { display:flex; }
        .city-onboarding-sheet { width:100%; max-width:500px; background:var(--card-bg); border-radius:24px; padding:20px; box-shadow:0 20px 55px rgba(0,0,0,.32); }
        .city-onboarding-title { font-size:22px; line-height:1.25; font-weight:900; color:var(--text-main); }
        .city-onboarding-note { font-size:13px; line-height:1.5; color:var(--text-sub); margin:7px 0 16px; }
        .city-onboarding-select { width:100%; min-height:50px; border:1px solid var(--border); border-radius:13px; background:var(--card-bg); color:var(--text-main); padding:0 12px; font:inherit; font-weight:800; }
        .city-onboarding-actions { display:grid; gap:9px; margin-top:13px; }
        .city-onboarding-btn { min-height:48px; border:1px solid var(--primary); border-radius:13px; background:var(--primary); color:white; font:inherit; font-weight:850; cursor:pointer; }
        .city-onboarding-btn.secondary { background:var(--card-bg); color:var(--primary); }
        body.city-onboarding-open { overflow:hidden; }

'''
if '.today-actions {' not in text:
    text = text.replace(css_anchor, css + css_anchor, 1)

# Main quick actions and nearest card.
main_anchor = '        <div class="ornament-divider"></div> <div class="card counter-card">'
main_insert = '''        <div class="today-actions" id="today-actions">
            <button class="today-action" type="button" data-today-action="today"><span class="today-action-icon">📅</span><span id="quick-today-text">Найти собрание сегодня</span></button>
            <a class="today-action" href="tel:+77072080553" data-today-action="call" style="text-decoration:none;"><span class="today-action-icon">☎</span><span id="quick-call-text">Позвонить в АА</span></a>
            <button class="today-action" type="button" data-today-action="favorites"><span class="today-action-icon">★</span><span id="quick-favorites-text">Мои группы</span></button>
            <button class="today-action" type="button" data-today-action="first"><span class="today-action-icon">?</span><span id="quick-first-text">Я впервые в АА</span></button>
        </div>
        <div class="card nearest-card" id="nearest-meeting-card"></div>
        <div class="ornament-divider"></div> <div class="card counter-card">'''
if 'id="today-actions"' not in text:
    if main_anchor not in text: raise SystemExit('main anchor missing')
    text = text.replace(main_anchor, main_insert, 1)

# Group filters.
old_filters = '''        <div class="group-filters">
            <select id="citySelect"></select>
            <button id="todayFilter" type="button" class="filter-btn">📅 Сегодня</button>
        </div>'''
new_filters = '''        <div class="group-quick-filters" id="group-quick-filters">
            <button type="button" class="group-quick-filter" data-group-mode="mycity" id="group-filter-mycity">Мой город</button>
            <button type="button" class="group-quick-filter" data-group-mode="today" id="todayFilter">Сегодня</button>
            <button type="button" class="group-quick-filter" data-group-mode="favorites" id="group-filter-favorites">Избранные</button>
            <button type="button" class="group-quick-filter" data-group-mode="online" id="group-filter-online">Онлайн</button>
        </div>
        <div class="group-city-row"><select id="citySelect"></select></div>'''
if 'id="group-quick-filters"' not in text:
    if old_filters not in text: raise SystemExit('group filters anchor missing')
    text = text.replace(old_filters, new_filters, 1)

# City onboarding modal.
panel_anchor = '<div class="notification-panel" id="notification-panel"'
city_modal = '''<div class="city-onboarding" id="city-onboarding" aria-hidden="true">
    <div class="city-onboarding-sheet" role="dialog" aria-modal="true" aria-labelledby="city-onboarding-title">
        <div class="city-onboarding-title" id="city-onboarding-title">В каком городе вы находитесь?</div>
        <div class="city-onboarding-note" id="city-onboarding-note">Мы покажем ваши группы и ближайшее собрание.</div>
        <select class="city-onboarding-select" id="city-onboarding-select"></select>
        <div class="city-onboarding-actions">
            <button class="city-onboarding-btn" type="button" id="city-onboarding-save">Сохранить город</button>
            <button class="city-onboarding-btn secondary" type="button" id="city-onboarding-all">Показать все города</button>
        </div>
    </div>
</div>

'''
if 'id="city-onboarding"' not in text:
    text = text.replace(panel_anchor, city_modal + panel_anchor, 1)

# Rename nav and translations, append priority-one translations after existing notification fields.
text = text.replace("nav: ['Счетчик','Новости','Книги','Группы']", "nav: ['Сегодня','Новости','Книги','Группы']")
text = text.replace("nav: ['Есептегіш','Жаңалықтар','Кітаптар','Топтар']", "nav: ['Бүгін','Жаңалықтар','Кітаптар','Топтар']")
text = text.replace('<span class="nav-txt">Счетчик</span>', '<span class="nav-txt">Сегодня</span>', 1)

ru_marker = "soberUnitsShort: ['лет', 'мес.', 'дней']"
kz_marker = "soberUnitsShort: ['жыл', 'ай', 'күн']"
ru_extra = ", quickToday: 'Найти собрание сегодня', quickCall: 'Позвонить в АА', quickFavorites: 'Мои группы', quickFirst: 'Я впервые в АА', nearestMeeting: 'Ближайшее собрание', nearestEmpty: 'Сегодня подходящих предстоящих собраний не найдено.', todayAt: 'Сегодня в', tomorrowAt: 'Завтра в', route: 'Маршрут', callAction: 'Позвонить', details: 'Подробнее', myCity: 'Мой город', onlineFilter: 'Онлайн', chooseCityTitle: 'В каком городе вы находитесь?', chooseCityNote: 'Мы покажем ваши группы и ближайшее собрание.', saveCity: 'Сохранить город', showAllCities: 'Показать все города', firstTitle: 'Первый раз в АА', firstText: 'Собрания бесплатные. Записываться не нужно. Можно ничего не говорить и просто слушать. Фамилию называть необязательно.'"
kz_extra = ", quickToday: 'Бүгінгі жиналысты табу', quickCall: 'АА-ға қоңырау шалу', quickFavorites: 'Менің топтарым', quickFirst: 'Мен АА-ға алғаш рет келдім', nearestMeeting: 'Ең жақын жиналыс', nearestEmpty: 'Жақын уақытта қолайлы жиналыс табылмады.', todayAt: 'Бүгін', tomorrowAt: 'Ертең', route: 'Бағыт', callAction: 'Қоңырау шалу', details: 'Толығырақ', myCity: 'Менің қалам', onlineFilter: 'Онлайн', chooseCityTitle: 'Сіз қай қаладасыз?', chooseCityNote: 'Сіздің топтарыңыз бен ең жақын жиналысты көрсетеміз.', saveCity: 'Қаланы сақтау', showAllCities: 'Барлық қалаларды көрсету', firstTitle: 'АА-ға алғаш рет', firstText: 'Жиналыстар тегін. Алдын ала жазылудың қажеті жоқ. Ештеңе айтпай, жай ғана тыңдауға болады. Тегіңізді айту міндетті емес.'"
if 'quickToday:' not in text:
    text = text.replace(ru_marker, ru_marker + ru_extra, 1)
    text = text.replace(kz_marker, kz_marker + kz_extra, 1)

# State.
state_anchor = "    const NOTIFICATION_SEEN_KEY = 'aa_internal_notification_seen_v1';"
state_extra = "\n    const USER_CITY_STORAGE_KEY = 'aa_user_city_v1';\n    let groupFilterMode = 'all';"
if 'USER_CITY_STORAGE_KEY' not in text:
    text = text.replace(state_anchor, state_anchor + state_extra, 1)

# Online groups should never render URL as address.
text = text.replace("    function renderAddress(g) {\n        if (!g.a) return '';", "    function renderAddress(g) {\n        if (!g.a || g.online) return '';", 1)

# Replace renderGroups and rebuildCityOptions.
pattern = re.compile(r"    function renderGroups\(\) \{.*?\n    \}\n\n    function rebuildCityOptions\(\) \{.*?\n    \}", re.S)
replacement = r'''    function getSavedUserCity() { return localStorage.getItem(USER_CITY_STORAGE_KEY) || ''; }

    function setGroupFilterMode(mode) {
        groupFilterMode = mode;
        onlyToday = mode === 'today';
        document.querySelectorAll('[data-group-mode]').forEach(button => button.classList.toggle('active', button.dataset.groupMode === mode));
        if (mode === 'mycity') {
            const city = getSavedUserCity();
            document.getElementById('citySelect').value = city || 'all';
        } else if (mode === 'favorites') {
            document.getElementById('citySelect').value = 'all';
        } else if (mode === 'online') {
            document.getElementById('citySelect').value = 'Онлайн';
        }
        renderGroups();
    }

    function renderGroups() {
        const selected = document.getElementById('citySelect').value;
        const c = document.getElementById('list-container');
        const currentDay = new Date().getDay();
        const favorites = getFavoriteGroups();
        const userCity = getSavedUserCity();
        const filtered = data.filter(g => {
            let matchesLocation = selected === 'all' || g.c === selected;
            if (groupFilterMode === 'mycity') matchesLocation = userCity ? g.c === userCity : true;
            if (groupFilterMode === 'favorites') matchesLocation = favorites.has(getGroupId(g));
            if (groupFilterMode === 'online') matchesLocation = Boolean(g.online);
            const matchesToday = groupFilterMode !== 'today' || (Array.isArray(g.sc) && g.sc.some(s => s.d === currentDay));
            return matchesLocation && matchesToday;
        });
        if (groupFilterMode === 'favorites' && filtered.length === 0) {
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

    function rebuildCityOptions() {
        const s = document.getElementById('citySelect');
        const current = s.value || getSavedUserCity() || 'all';
        const cities = [...new Set(data.map(x => x.c).filter(city => city !== 'Онлайн'))].sort((a,b) => a.localeCompare(b, 'ru'));
        const ct = ['all', 'Онлайн', ...cities];
        s.innerHTML = '';
        ct.forEach(city => {
            const o = document.createElement('option');
            o.value = city;
            o.innerText = city === 'all' ? i18n[curLang].allCities : city;
            s.appendChild(o);
        });
        s.value = [...s.options].some(opt => opt.value === current) ? current : 'all';
        buildCityOnboardingOptions();
    }'''
text, count = pattern.subn(replacement, text, count=1)
if count != 1 and 'function setGroupFilterMode' not in text:
    raise SystemExit('renderGroups replacement failed')

# Add home/city/nearest functions before applySavedTheme.
func_anchor = "    function applySavedTheme() {"
functions = r'''    function buildCityOnboardingOptions() {
        const select = document.getElementById('city-onboarding-select');
        if (!select) return;
        const current = getSavedUserCity();
        const cities = [...new Set(data.filter(group => !group.online).map(group => group.c))].sort((a,b) => a.localeCompare(b, 'ru'));
        select.innerHTML = cities.map(city => `<option value="${escapeHtml(city)}">${escapeHtml(city)}</option>`).join('');
        if (current && cities.includes(current)) select.value = current;
    }

    function openCityOnboarding() {
        buildCityOnboardingOptions();
        const modal = document.getElementById('city-onboarding');
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('city-onboarding-open');
    }

    function closeCityOnboarding() {
        const modal = document.getElementById('city-onboarding');
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('city-onboarding-open');
    }

    function saveUserCity(city) {
        if (city) localStorage.setItem(USER_CITY_STORAGE_KEY, city);
        else localStorage.removeItem(USER_CITY_STORAGE_KEY);
        rebuildCityOptions();
        setGroupFilterMode(city ? 'mycity' : 'all');
        renderNearestMeeting();
        closeCityOnboarding();
    }

    function getUpcomingMeetings() {
        const now = new Date();
        const currentMinutes = now.getHours() * 60 + now.getMinutes();
        const favorites = getFavoriteGroups();
        const userCity = getSavedUserCity();
        const candidates = [];
        for (let offset = 0; offset <= 1; offset++) {
            const day = (now.getDay() + offset) % 7;
            data.forEach(group => {
                if (!Array.isArray(group.sc)) return;
                group.sc.filter(slot => slot.d === day).forEach(slot => {
                    const start = minutesFromSlot(slot.s);
                    if (offset === 0 && start <= currentMinutes) return;
                    const rank = favorites.has(getGroupId(group)) ? 0 : (userCity && group.c === userCity ? 1 : (group.online ? 2 : 3));
                    candidates.push({ group, slot, offset, rank, minutesAway: offset * 1440 + start - currentMinutes });
                });
            });
            if (candidates.length) break;
        }
        return candidates.sort((a,b) => a.rank - b.rank || a.minutesAway - b.minutesAway);
    }

    function renderNearestMeeting() {
        const card = document.getElementById('nearest-meeting-card');
        if (!card) return;
        const d = i18n[curLang];
        const meeting = getUpcomingMeetings()[0];
        if (!meeting) {
            card.innerHTML = `<div class="nearest-label">${d.nearestMeeting}</div><div class="nearest-empty">${d.nearestEmpty}</div>`;
            return;
        }
        const g = meeting.group;
        const time = `${String(Math.floor(meeting.slot.s / 100)).padStart(2,'0')}:${String(meeting.slot.s % 100).padStart(2,'0')}`;
        const when = meeting.offset === 0 ? `${d.todayAt} ${time}` : `${d.tomorrowAt} ${time}`;
        const map = build2GISLink(g);
        const phone = g.p && g.p.length ? cleanPhone(g.p[0]) : '';
        const onlineUrl = g.online ? g.a : g.z;
        const remaining = formatRemainingMinutes(Math.max(0, meeting.minutesAway));
        card.innerHTML = `<div class="nearest-label">${d.nearestMeeting}</div><div class="nearest-name">${escapeHtml(g.n)}</div><div class="nearest-time">${escapeHtml(when)}</div><div class="nearest-remaining">${d.sSoon} ${remaining}</div><div class="nearest-actions">${map ? `<a class="nearest-action" href="${map}" target="_blank" rel="noopener noreferrer">${d.route}</a>` : ''}${phone ? `<a class="nearest-action" href="tel:${phone}">${d.callAction}</a>` : ''}${onlineUrl ? `<a class="nearest-action primary" href="${onlineUrl}" target="_blank" rel="noopener noreferrer">${g.chat ? d.openChat : d.openZoom}</a>` : ''}<button class="nearest-action" type="button" data-nearest-details="${escapeHtml(getGroupId(g))}">${d.details}</button></div>`;
    }

    function openFirstTimeInfo() {
        const d = i18n[curLang];
        alert(`${d.firstTitle}\n\n${d.firstText}`);
    }

'''
if 'function renderNearestMeeting()' not in text:
    text = text.replace(func_anchor, functions + func_anchor, 1)

# Update today notifications by selected city.
old_today = "        const groups = data.filter(group => Array.isArray(group.sc) && group.sc.some(slot => slot.d === day));"
new_today = "        const userCity = getSavedUserCity();\n        const groups = data.filter(group => Array.isArray(group.sc) && group.sc.some(slot => slot.d === day) && (!userCity || group.c === userCity || group.online));"
text = text.replace(old_today, new_today, 1)

# setLang updates.
lang_anchor = "        document.getElementById('notification-button').setAttribute('aria-label', d.notificationCenter);"
lang_extra = """
        document.getElementById('quick-today-text').innerText = d.quickToday;
        document.getElementById('quick-call-text').innerText = d.quickCall;
        document.getElementById('quick-favorites-text').innerText = d.quickFavorites;
        document.getElementById('quick-first-text').innerText = d.quickFirst;
        document.getElementById('group-filter-mycity').innerText = d.myCity;
        document.getElementById('todayFilter').innerText = d.todayBtn.replace('📅 ', '');
        document.getElementById('group-filter-favorites').innerText = d.favorites.replace('★ ', '');
        document.getElementById('group-filter-online').innerText = d.onlineFilter;
        document.getElementById('city-onboarding-title').innerText = d.chooseCityTitle;
        document.getElementById('city-onboarding-note').innerText = d.chooseCityNote;
        document.getElementById('city-onboarding-save').innerText = d.saveCity;
        document.getElementById('city-onboarding-all').innerText = d.showAllCities;
        renderNearestMeeting();"""
if "quick-today-text').innerText" not in text:
    text = text.replace(lang_anchor, lang_anchor + lang_extra, 1)

# Existing toggleToday should use filter mode.
text = re.sub(r"    function toggleToday\(\) \{.*?\n    \}", "    function toggleToday() { setGroupFilterMode(groupFilterMode === 'today' ? 'all' : 'today'); }", text, count=1, flags=re.S)

# Event listeners.
event_anchor = "        document.getElementById('mot-toggle').addEventListener('click', toggleMotivation);"
events = r'''
        document.getElementById('today-actions').addEventListener('click', event => {
            const action = event.target.closest('[data-today-action]');
            if (!action) return;
            if (action.dataset.todayAction === 'today') { goTo('groups'); setGroupFilterMode('today'); }
            if (action.dataset.todayAction === 'favorites') { goTo('groups'); setGroupFilterMode('favorites'); }
            if (action.dataset.todayAction === 'first') openFirstTimeInfo();
            if (action.dataset.todayAction === 'call') trackEvent('call', 'quick_aa_phone');
        });
        document.getElementById('nearest-meeting-card').addEventListener('click', event => {
            const details = event.target.closest('[data-nearest-details]');
            if (!details) return;
            goTo('groups');
            const group = data.find(item => getGroupId(item) === details.dataset.nearestDetails);
            if (group) { document.getElementById('citySelect').value = group.c; groupFilterMode = 'all'; renderGroups(); }
        });
        document.getElementById('group-quick-filters').addEventListener('click', event => {
            const button = event.target.closest('[data-group-mode]');
            if (button) setGroupFilterMode(button.dataset.groupMode);
        });
        document.getElementById('city-onboarding-save').addEventListener('click', () => saveUserCity(document.getElementById('city-onboarding-select').value));
        document.getElementById('city-onboarding-all').addEventListener('click', () => saveUserCity(''));
'''
if "quick_aa_phone" not in text:
    text = text.replace(event_anchor, event_anchor + events, 1)

# city select manual selection resets quick mode.
text = text.replace("            trackEvent('city_filter', e.target.value);\n            renderGroups();", "            trackEvent('city_filter', e.target.value);\n            groupFilterMode = 'all';\n            document.querySelectorAll('[data-group-mode]').forEach(button => button.classList.remove('active'));\n            renderGroups();", 1)

# Favorite changes refresh nearest.
text = text.replace("        renderGroups();\n    }\n\n    function defaultNotificationSettings", "        renderGroups();\n        renderNearestMeeting();\n    }\n\n    function defaultNotificationSettings", 1)

# Init: render nearest and first-run city prompt.
init_anchor = "        renderLit();\n        setTimeout(runInternalNotificationChecks, 1800);"
init_new = "        renderLit();\n        renderNearestMeeting();\n        if (!localStorage.getItem('aa_city_onboarding_done_v1')) {\n            localStorage.setItem('aa_city_onboarding_done_v1', '1');\n            setTimeout(openCityOnboarding, 450);\n        }\n        setTimeout(runInternalNotificationChecks, 1800);"
text = text.replace(init_anchor, init_new, 1)

# Saving a city should mark onboarding done even if reopened later.
text = text.replace("    function saveUserCity(city) {\n        if (city)", "    function saveUserCity(city) {\n        localStorage.setItem('aa_city_onboarding_done_v1', '1');\n        if (city)", 1)

# Service worker version bump.
text = text.replace("register('sw.js?v=3'", "register('sw.js?v=4'", 1)

# Basic validation.
required = ['today-actions', 'nearest-meeting-card', 'city-onboarding', 'group-quick-filters', 'function renderNearestMeeting()', "if (!g.a || g.online) return '';"]
missing = [item for item in required if item not in text]
if missing: raise SystemExit(f'missing: {missing}')

path.write_text(text, encoding='utf-8')
