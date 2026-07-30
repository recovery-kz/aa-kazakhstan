from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

css_anchor = "        .bottom-nav {"
css = r'''        .notification-button { position: relative; width: 40px; height: 40px; border: none; border-radius: 12px; background: rgba(255,255,255,0.18); color: white; font-size: 20px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        .notification-badge { position: absolute; right: -4px; top: -5px; min-width: 18px; height: 18px; padding: 0 5px; border-radius: 10px; background: #d64545; color: white; font-size: 10px; font-weight: 900; display: none; align-items: center; justify-content: center; border: 2px solid var(--primary); }
        .notification-badge.show { display: flex; }
        .notification-panel { position: fixed; inset: 0; z-index: 4500; background: rgba(0,0,0,0.52); display: none; align-items: flex-end; justify-content: center; padding: 12px 12px max(12px, env(safe-area-inset-bottom)); }
        .notification-panel.open { display: flex; }
        .notification-sheet { width: 100%; max-width: 520px; max-height: 86vh; overflow: hidden; background: var(--card-bg); border-radius: 24px; box-shadow: 0 20px 55px rgba(0,0,0,0.32); display: flex; flex-direction: column; }
        .notification-head { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 18px; border-bottom: 1px solid var(--border); }
        .notification-title { font-size: 19px; font-weight: 850; color: var(--text-main); }
        .notification-head-actions { display: flex; gap: 8px; }
        .notification-small-btn { border: 1px solid var(--border); border-radius: 10px; background: var(--card-bg); color: var(--primary); min-height: 34px; padding: 0 10px; font-size: 11px; font-weight: 800; cursor: pointer; }
        .notification-close { width: 34px; padding: 0; font-size: 20px; color: var(--text-main); }
        .notification-list { overflow-y: auto; padding: 10px 14px 18px; }
        .notification-empty { padding: 34px 20px; text-align: center; color: var(--text-sub); font-size: 14px; line-height: 1.55; }
        .notification-item { width: 100%; border: none; border-bottom: 1px solid var(--border); background: transparent; color: inherit; text-align: left; padding: 14px 4px; cursor: pointer; display: grid; grid-template-columns: 38px minmax(0,1fr); gap: 11px; }
        .notification-item.unread { background: color-mix(in srgb, var(--accent) 8%, transparent); }
        .notification-icon { width: 38px; height: 38px; border-radius: 12px; background: var(--bg); display: flex; align-items: center; justify-content: center; font-size: 18px; }
        .notification-item-title { color: var(--text-main); font-size: 14px; line-height: 1.35; font-weight: 850; }
        .notification-item-text { color: var(--text-sub); font-size: 12px; line-height: 1.45; margin-top: 3px; }
        .notification-time { color: var(--nav-inactive); font-size: 10px; margin-top: 6px; }
        .notification-dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #d64545; margin-right: 5px; }
        .notification-settings { display: flex; flex-direction: column; gap: 0; }
        .notification-setting { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 13px 0; border-bottom: 1px solid var(--border); }
        .notification-setting:last-child { border-bottom: none; }
        .notification-setting-main { min-width: 0; }
        .notification-setting-title { color: var(--text-main); font-size: 14px; font-weight: 800; }
        .notification-setting-note { color: var(--text-sub); font-size: 11px; line-height: 1.4; margin-top: 3px; }
        .notification-switch { appearance: none; width: 46px; height: 26px; border-radius: 15px; background: var(--border); position: relative; cursor: pointer; flex-shrink: 0; transition: .2s; }
        .notification-switch::after { content: ''; position: absolute; width: 20px; height: 20px; left: 3px; top: 3px; border-radius: 50%; background: white; box-shadow: 0 1px 4px rgba(0,0,0,.25); transition: .2s; }
        .notification-switch:checked { background: var(--primary); }
        .notification-switch:checked::after { transform: translateX(20px); }
        .notification-select { min-height: 38px; border: 1px solid var(--border); border-radius: 10px; background: var(--card-bg); color: var(--text-main); padding: 0 9px; font-weight: 700; }
        body.notifications-open { overflow: hidden; }

'''
if '.notification-panel {' not in text:
    text = text.replace(css_anchor, css + css_anchor)

header_old = '''        <button class="theme-toggle" id="theme-icon" type="button">🌙</button>
        <div class="lang-switch">'''
header_new = '''        <button class="theme-toggle" id="theme-icon" type="button">🌙</button>
        <button class="notification-button" id="notification-button" type="button" aria-label="Уведомления">🔔<span class="notification-badge" id="notification-badge">0</span></button>
        <div class="lang-switch">'''
if 'id="notification-button"' not in text:
    if header_old not in text: raise SystemExit('Header anchor not found')
    text = text.replace(header_old, header_new, 1)

profile_anchor = '''            <div class="ornament-divider"></div> <button class="acc-btn" type="button" data-acc-target="acc-prayer"'''
settings_html = '''            <div class="ornament-divider"></div> <button class="acc-btn" type="button" data-acc-target="acc-notifications" id="btn-notifications-head"><span class="acc-btn-left"><span class="acc-btn-title" id="notifications-head-text">УВЕДОМЛЕНИЯ</span></span></button>
            <div class="acc-content" id="acc-notifications">
                <div class="notification-settings">
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-master-title">Внутренние уведомления</span><span class="notification-setting-note" id="notif-master-note">Показывать новые события в центре уведомлений</span></span><input class="notification-switch" id="notif-master" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-reflection-title">Ежедневные размышления</span><span class="notification-setting-note" id="notif-reflection-note">Сообщать о новом размышлении при открытии приложения</span></span><input class="notification-switch" id="notif-reflection" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-news-title">Новости</span><span class="notification-setting-note" id="notif-news-note">Сообщать о новых публикациях</span></span><input class="notification-switch" id="notif-news" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-today-title">Группы сегодня</span><span class="notification-setting-note" id="notif-today-note">Показывать сводку собраний на текущий день</span></span><input class="notification-switch" id="notif-today" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-favorites-title">Избранные группы</span><span class="notification-setting-note" id="notif-favorites-note">Напоминать перед началом собрания, пока приложение открыто</span></span><input class="notification-switch" id="notif-favorites" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-browser-title">Системное окно при открытом приложении</span><span class="notification-setting-note" id="notif-browser-note">Не работает после полного закрытия приложения</span></span><input class="notification-switch" id="notif-browser" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-before-title">Напоминать заранее</span></span><select class="notification-select" id="notif-before"><option value="15">15 мин</option><option value="30">30 мин</option><option value="60">1 час</option><option value="120">2 часа</option></select></label>
                </div>
            </div>
'''
if 'id="acc-notifications"' not in text:
    if profile_anchor not in text: raise SystemExit('Profile anchor not found')
    text = text.replace(profile_anchor, settings_html + profile_anchor, 1)

panel_anchor = '</main>\n\n<nav class="bottom-nav">'
panel_html = '''</main>

<div class="notification-panel" id="notification-panel" aria-hidden="true">
    <div class="notification-sheet" role="dialog" aria-modal="true" aria-labelledby="notification-center-title">
        <div class="notification-head"><div class="notification-title" id="notification-center-title">Уведомления</div><div class="notification-head-actions"><button class="notification-small-btn" id="notification-read-all" type="button">Прочитать все</button><button class="notification-small-btn notification-close" id="notification-close" type="button">×</button></div></div>
        <div class="notification-list" id="notification-list"></div>
    </div>
</div>

<nav class="bottom-nav">'''
if 'id="notification-panel"' not in text:
    if panel_anchor not in text: raise SystemExit('Panel anchor not found')
    text = text.replace(panel_anchor, panel_html, 1)

# Extend translation dictionaries.
text = text.replace("bookShared: 'Текст о книге скопирован',", "bookShared: 'Текст о книге скопирован', notificationsHead: 'УВЕДОМЛЕНИЯ', notificationCenter: 'Уведомления', notificationReadAll: 'Прочитать все', notificationEmpty: 'Здесь появятся новые размышления, новости и напоминания о собраниях.', notifMasterTitle: 'Внутренние уведомления', notifMasterNote: 'Показывать новые события в центре уведомлений', notifReflectionTitle: 'Ежедневные размышления', notifReflectionNote: 'Сообщать о новом размышлении при открытии приложения', notifNewsTitle: 'Новости', notifNewsNote: 'Сообщать о новых публикациях', notifTodayTitle: 'Группы сегодня', notifTodayNote: 'Показывать сводку собраний на текущий день', notifFavoritesTitle: 'Избранные группы', notifFavoritesNote: 'Напоминать перед началом собрания, пока приложение открыто', notifBrowserTitle: 'Системное окно при открытом приложении', notifBrowserNote: 'Не работает после полного закрытия приложения', notifBeforeTitle: 'Напоминать заранее', notifReflectionNew: 'Новое ежедневное размышление', notifNewsNew: 'Новая публикация', notifTodayNew: 'Собрания сегодня', notifFavoriteNew: 'Скоро начнётся собрание',")
text = text.replace("bookShared: 'Кітап туралы мәтін көшірілді',", "bookShared: 'Кітап туралы мәтін көшірілді', notificationsHead: 'ХАБАРЛАМАЛАР', notificationCenter: 'Хабарламалар', notificationReadAll: 'Барлығын оқу', notificationEmpty: 'Мұнда жаңа ойлар, жаңалықтар және жиналыстар туралы еске салулар пайда болады.', notifMasterTitle: 'Ішкі хабарламалар', notifMasterNote: 'Жаңа оқиғаларды хабарламалар орталығында көрсету', notifReflectionTitle: 'Күнделікті ойлар', notifReflectionNote: 'Қосымша ашылғанда жаңа ой туралы хабарлау', notifNewsTitle: 'Жаңалықтар', notifNewsNote: 'Жаңа жарияланымдар туралы хабарлау', notifTodayTitle: 'Бүгінгі топтар', notifTodayNote: 'Бүгінгі жиналыстардың қорытындысын көрсету', notifFavoritesTitle: 'Таңдаулы топтар', notifFavoritesNote: 'Қосымша ашық кезде жиналыс алдында еске салу', notifBrowserTitle: 'Қосымша ашық кездегі жүйелік терезе', notifBrowserNote: 'Қосымша толық жабылғаннан кейін жұмыс істемейді', notifBeforeTitle: 'Алдын ала еске салу', notifReflectionNew: 'Жаңа күнделікті ой', notifNewsNew: 'Жаңа жарияланым', notifTodayNew: 'Бүгінгі жиналыстар', notifFavoriteNew: 'Жиналыс жақында басталады',")

state_anchor = "    const FAVORITES_STORAGE_KEY = 'aa_group_favorites_v1';"
state = """    const NOTIFICATIONS_STORAGE_KEY = 'aa_internal_notifications_v1';
    const NOTIFICATION_SETTINGS_KEY = 'aa_internal_notification_settings_v1';
    const NOTIFICATION_SEEN_KEY = 'aa_internal_notification_seen_v1';
    let notificationTimer = null;
"""
if 'NOTIFICATIONS_STORAGE_KEY' not in text:
    if state_anchor not in text: raise SystemExit('State anchor not found')
    text = text.replace(state_anchor, state_anchor + '\n' + state, 1)

func_anchor = '    function cleanPhone(phone) {'
functions = r'''    function defaultNotificationSettings() {
        return { master: true, reflection: true, news: true, today: true, favorites: true, browser: false, before: 60 };
    }

    function getNotificationSettings() {
        try { return { ...defaultNotificationSettings(), ...JSON.parse(localStorage.getItem(NOTIFICATION_SETTINGS_KEY) || '{}') }; }
        catch (error) { return defaultNotificationSettings(); }
    }

    function saveNotificationSettings(settings) {
        localStorage.setItem(NOTIFICATION_SETTINGS_KEY, JSON.stringify(settings));
    }

    function getInternalNotifications() {
        try { const value = JSON.parse(localStorage.getItem(NOTIFICATIONS_STORAGE_KEY) || '[]'); return Array.isArray(value) ? value : []; }
        catch (error) { return []; }
    }

    function saveInternalNotifications(items) {
        localStorage.setItem(NOTIFICATIONS_STORAGE_KEY, JSON.stringify(items.slice(0, 80)));
    }

    function notificationSeen(key) {
        try { return JSON.parse(localStorage.getItem(NOTIFICATION_SEEN_KEY) || '{}')[key] === true; }
        catch (error) { return false; }
    }

    function markNotificationSeen(key) {
        let seen = {};
        try { seen = JSON.parse(localStorage.getItem(NOTIFICATION_SEEN_KEY) || '{}'); } catch (error) {}
        seen[key] = true;
        const keys = Object.keys(seen);
        if (keys.length > 250) keys.slice(0, keys.length - 200).forEach(item => delete seen[item]);
        localStorage.setItem(NOTIFICATION_SEEN_KEY, JSON.stringify(seen));
    }

    function addInternalNotification(item, showBrowser = true) {
        const settings = getNotificationSettings();
        if (!settings.master || notificationSeen(item.key)) return false;
        const items = getInternalNotifications();
        items.unshift({ ...item, id: item.key, createdAt: Date.now(), read: false });
        saveInternalNotifications(items);
        markNotificationSeen(item.key);
        updateNotificationBadge();
        if (showBrowser && settings.browser && document.visibilityState === 'visible' && 'Notification' in window && Notification.permission === 'granted') {
            try { new Notification(item.title, { body: item.text, icon: 'icon-192.png', tag: item.key }); } catch (error) {}
        }
        return true;
    }

    function updateNotificationBadge() {
        const unread = getInternalNotifications().filter(item => !item.read).length;
        const badge = document.getElementById('notification-badge');
        if (!badge) return;
        badge.textContent = unread > 99 ? '99+' : String(unread);
        badge.classList.toggle('show', unread > 0);
    }

    function formatNotificationTime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString(curLang === 'kz' ? 'kk-KZ' : 'ru-RU', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
    }

    function renderNotificationCenter() {
        const list = document.getElementById('notification-list');
        if (!list) return;
        const items = getInternalNotifications();
        if (!items.length) { list.innerHTML = `<div class="notification-empty">${i18n[curLang].notificationEmpty}</div>`; return; }
        list.innerHTML = items.map(item => `<button class="notification-item${item.read ? '' : ' unread'}" type="button" data-notification-id="${escapeHtml(item.id)}"><span class="notification-icon">${escapeHtml(item.icon || '🔔')}</span><span><span class="notification-item-title">${item.read ? '' : '<span class="notification-dot"></span>'}${escapeHtml(item.title)}</span><span class="notification-item-text">${escapeHtml(item.text)}</span><span class="notification-time">${formatNotificationTime(item.createdAt)}</span></span></button>`).join('');
    }

    function openNotificationCenter() {
        renderNotificationCenter();
        document.getElementById('notification-panel').classList.add('open');
        document.getElementById('notification-panel').setAttribute('aria-hidden', 'false');
        document.body.classList.add('notifications-open');
    }

    function closeNotificationCenter() {
        document.getElementById('notification-panel').classList.remove('open');
        document.getElementById('notification-panel').setAttribute('aria-hidden', 'true');
        document.body.classList.remove('notifications-open');
    }

    function markAllNotificationsRead() {
        const items = getInternalNotifications().map(item => ({ ...item, read: true }));
        saveInternalNotifications(items);
        renderNotificationCenter();
        updateNotificationBadge();
    }

    function openInternalNotification(id) {
        const items = getInternalNotifications();
        const current = items.find(item => item.id === id);
        saveInternalNotifications(items.map(item => item.id === id ? { ...item, read: true } : item));
        updateNotificationBadge();
        closeNotificationCenter();
        if (!current) return;
        if (current.tab) goTo(current.tab);
        if (current.action === 'today') {
            onlyToday = true;
            document.getElementById('todayFilter').classList.add('active');
            renderGroups();
        }
        if (current.action === 'favorites') {
            document.getElementById('citySelect').value = 'favorites';
            renderGroups();
        }
    }

    function syncNotificationSettingsUI() {
        const settings = getNotificationSettings();
        ['master','reflection','news','today','favorites','browser'].forEach(key => {
            const input = document.getElementById(`notif-${key}`);
            if (input) input.checked = Boolean(settings[key]);
        });
        const before = document.getElementById('notif-before');
        if (before) before.value = String(settings.before || 60);
    }

    async function updateNotificationSetting(key, value) {
        const settings = getNotificationSettings();
        settings[key] = value;
        if (key === 'browser' && value && 'Notification' in window && Notification.permission !== 'granted') {
            const permission = await Notification.requestPermission();
            settings.browser = permission === 'granted';
            const input = document.getElementById('notif-browser');
            if (input) input.checked = settings.browser;
        }
        saveNotificationSettings(settings);
    }

    function checkReflectionNotification() {
        const settings = getNotificationSettings();
        if (!settings.master || !settings.reflection) return;
        const title = document.getElementById('mot-title')?.innerText?.trim();
        if (!title || title === 'Загрузка...' || title === 'Жүктелуде...') return;
        const dateKey = new Date().toISOString().slice(0, 10);
        addInternalNotification({ key: `reflection:${dateKey}`, type: 'reflection', icon: '📖', title: i18n[curLang].notifReflectionNew, text: title, tab: 'counter' });
    }

    function getNewsIdentity(item) {
        return String(item?.id || item?.date || item?.title || item?.n || JSON.stringify(item || '')).slice(0, 180);
    }

    function checkNewsNotification() {
        const settings = getNotificationSettings();
        if (!settings.master || !settings.news || !currentNewsData) return;
        const list = Array.isArray(currentNewsData) ? currentNewsData : (currentNewsData.news || currentNewsData.items || []);
        if (!Array.isArray(list) || !list.length) return;
        const latest = list[0];
        const identity = getNewsIdentity(latest);
        const previous = localStorage.getItem('aa_last_news_identity');
        localStorage.setItem('aa_last_news_identity', identity);
        if (!previous || previous === identity) return;
        const title = latest.title || latest.n || latest.name || i18n[curLang].notifNewsNew;
        addInternalNotification({ key: `news:${identity}`, type: 'news', icon: '📰', title: i18n[curLang].notifNewsNew, text: String(title), tab: 'news' });
    }

    function checkTodayGroupsNotification() {
        const settings = getNotificationSettings();
        if (!settings.master || !settings.today) return;
        const now = new Date();
        const day = now.getDay();
        const dateKey = now.toISOString().slice(0, 10);
        const groups = data.filter(group => Array.isArray(group.sc) && group.sc.some(slot => slot.d === day));
        if (!groups.length) return;
        const cities = [...new Set(groups.map(group => group.c))];
        const text = curLang === 'kz' ? `${groups.length} жиналыс · ${cities.slice(0, 3).join(', ')}` : `${groups.length} собраний · ${cities.slice(0, 3).join(', ')}`;
        addInternalNotification({ key: `today:${dateKey}`, type: 'today', icon: '📅', title: i18n[curLang].notifTodayNew, text, tab: 'groups', action: 'today' }, false);
    }

    function minutesFromSlot(value) { return Math.floor(value / 100) * 60 + (value % 100); }

    function checkFavoriteGroupReminders() {
        const settings = getNotificationSettings();
        if (!settings.master || !settings.favorites) return;
        const favorites = getFavoriteGroups();
        if (!favorites.size) return;
        const now = new Date();
        const day = now.getDay();
        const currentMinutes = now.getHours() * 60 + now.getMinutes();
        const before = Number(settings.before || 60);
        const dateKey = now.toISOString().slice(0, 10);
        data.forEach(group => {
            if (!favorites.has(getGroupId(group)) || !Array.isArray(group.sc)) return;
            group.sc.filter(slot => slot.d === day).forEach(slot => {
                const start = minutesFromSlot(slot.s);
                const remaining = start - currentMinutes;
                if (remaining < 0 || remaining > before) return;
                const time = `${String(Math.floor(slot.s / 100)).padStart(2,'0')}:${String(slot.s % 100).padStart(2,'0')}`;
                const text = `${group.n} · ${time}${group.online ? ' · онлайн' : group.a ? ` · ${group.a}` : ''}`;
                addInternalNotification({ key: `favorite:${dateKey}:${getGroupId(group)}:${slot.s}:${before}`, type: 'favorite', icon: '⭐', title: i18n[curLang].notifFavoriteNew, text, tab: 'groups', action: 'favorites' });
            });
        });
    }

    function runInternalNotificationChecks() {
        checkReflectionNotification();
        checkNewsNotification();
        checkTodayGroupsNotification();
        checkFavoriteGroupReminders();
    }

'''
if 'function defaultNotificationSettings()' not in text:
    if func_anchor not in text: raise SystemExit('Function anchor not found')
    text = text.replace(func_anchor, functions + func_anchor, 1)

# Language UI updates.
lang_anchor = "        document.getElementById('notes-head-text').innerText = d.notesHead;"
lang_lines = """        document.getElementById('notifications-head-text').innerText = d.notificationsHead;
        document.getElementById('notification-center-title').innerText = d.notificationCenter;
        document.getElementById('notification-read-all').innerText = d.notificationReadAll;
        document.getElementById('notif-master-title').innerText = d.notifMasterTitle;
        document.getElementById('notif-master-note').innerText = d.notifMasterNote;
        document.getElementById('notif-reflection-title').innerText = d.notifReflectionTitle;
        document.getElementById('notif-reflection-note').innerText = d.notifReflectionNote;
        document.getElementById('notif-news-title').innerText = d.notifNewsTitle;
        document.getElementById('notif-news-note').innerText = d.notifNewsNote;
        document.getElementById('notif-today-title').innerText = d.notifTodayTitle;
        document.getElementById('notif-today-note').innerText = d.notifTodayNote;
        document.getElementById('notif-favorites-title').innerText = d.notifFavoritesTitle;
        document.getElementById('notif-favorites-note').innerText = d.notifFavoritesNote;
        document.getElementById('notif-browser-title').innerText = d.notifBrowserTitle;
        document.getElementById('notif-browser-note').innerText = d.notifBrowserNote;
        document.getElementById('notif-before-title').innerText = d.notifBeforeTitle;
        document.getElementById('notification-button').setAttribute('aria-label', d.notificationCenter);
"""
if "document.getElementById('notifications-head-text')" not in text:
    if lang_anchor not in text: raise SystemExit('Language anchor not found')
    text = text.replace(lang_anchor, lang_anchor + '\n' + lang_lines, 1)

# Event listeners.
event_anchor = "        document.getElementById('todayFilter').addEventListener('click', toggleToday);"
events = r'''        document.getElementById('notification-button').addEventListener('click', openNotificationCenter);
        document.getElementById('notification-close').addEventListener('click', closeNotificationCenter);
        document.getElementById('notification-read-all').addEventListener('click', markAllNotificationsRead);
        document.getElementById('notification-panel').addEventListener('click', event => { if (event.target.id === 'notification-panel') closeNotificationCenter(); });
        document.getElementById('notification-list').addEventListener('click', event => { const item = event.target.closest('[data-notification-id]'); if (item) openInternalNotification(item.dataset.notificationId); });
        ['master','reflection','news','today','favorites','browser'].forEach(key => document.getElementById(`notif-${key}`).addEventListener('change', event => updateNotificationSetting(key, event.target.checked)));
        document.getElementById('notif-before').addEventListener('change', event => updateNotificationSetting('before', Number(event.target.value)));
        document.addEventListener('keydown', event => { if (event.key === 'Escape') closeNotificationCenter(); });
'''
if "notification-button').addEventListener" not in text:
    if event_anchor not in text: raise SystemExit('Events anchor not found')
    text = text.replace(event_anchor, event_anchor + '\n' + events, 1)

# Init hooks.
init_anchor = "        loadTrust();\n        setLang(curLang);"
init_new = "        loadTrust();\n        syncNotificationSettingsUI();\n        updateNotificationBadge();\n        setLang(curLang);"
if 'syncNotificationSettingsUI();' not in text.split('function init()',1)[-1]:
    if init_anchor not in text: raise SystemExit('Init anchor not found')
    text = text.replace(init_anchor, init_new, 1)

init_tail = "        renderGroups();\n        renderLit();"
init_tail_new = "        renderGroups();\n        renderLit();\n        setTimeout(runInternalNotificationChecks, 1800);\n        notificationTimer = setInterval(runInternalNotificationChecks, 60000);"
if 'notificationTimer = setInterval' not in text:
    if init_tail not in text: raise SystemExit('Init tail not found')
    text = text.replace(init_tail, init_tail_new, 1)

# Recheck after online/news refresh and when favorites change.
text = text.replace("        renderGroups();\n    }\n\n    function cleanPhone", "        renderGroups();\n        setTimeout(checkFavoriteGroupReminders, 0);\n    }\n\n    function cleanPhone", 1)
text = text.replace("        loadNews(true);\n    });", "        loadNews(true);\n        setTimeout(runInternalNotificationChecks, 1800);\n    });", 1)

path.write_text(text, encoding='utf-8')

# Basic integrity checks.
final = path.read_text(encoding='utf-8')
required = ['notification-button', 'notification-panel', 'acc-notifications', 'runInternalNotificationChecks', 'checkFavoriteGroupReminders', 'notificationTimer = setInterval']
missing = [item for item in required if item not in final]
if missing: raise SystemExit('Missing notification features: ' + ', '.join(missing))
print('Internal notifications migration applied')
