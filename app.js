(() => {
    'use strict';

    const i18n = window.AA_I18N;
    const principles = window.AA_PRINCIPLES;
    const englishProfile = window.AA_PROFILE_EN;

    let curLang = localStorage.getItem('aa_lang') || 'ru';
    if (!i18n[curLang]) curLang = 'ru';
    let onlyToday = false;
    let currentBookFilter = 'all';
    let activeBookIndex = null;
    let saveTimeout = null;

    const TAB_ORDER = ['counter', 'news', 'lit', 'groups', 'profile'];
    const SWIPE_MIN_DISTANCE = 60;
    const SWIPE_MAX_VERTICAL_DRIFT = 80;
    let touchStartX = 0;
    let touchStartY = 0;
    let touchStartTime = 0;
    let swipeBlocked = false;

    const REFLECTIONS_STORAGE_KEY = 'aa_daily_reflections_full_cache_v1';
    const NEWS_STORAGE_KEY = 'aa_news_cache_v1';
    const FAVORITES_STORAGE_KEY = 'aa_group_favorites_v1';
    const NOTIFICATIONS_STORAGE_KEY = 'aa_internal_notifications_v1';
    const NOTIFICATION_SETTINGS_KEY = 'aa_internal_notification_settings_v1';
    const NOTIFICATION_SEEN_KEY = 'aa_internal_notification_seen_v1';
    const USER_CITY_STORAGE_KEY = 'aa_user_city_v1';
    let groupFilterMode = 'all';
    let notificationTimer = null;

    let currentReflectionsData = null;
    let currentNewsData = null;
    let newsLoaded = false;

    let books = [];

    let data = [];

    function getLocale() {
        if (curLang === 'kz') return 'kk-KZ';
        if (curLang === 'en') return 'en-US';
        return 'ru-RU';
    }

    function setEnglishOnlyText(id, englishText) {
        const element = document.getElementById(id);
        if (!element) return;
        if (!element.dataset.defaultText) element.dataset.defaultText = element.textContent;
        element.textContent = curLang === 'en' ? englishText : element.dataset.defaultText;
    }

    function renderEnglishProfile() {
        const profile = document.getElementById('tab-profile');
        if (!profile) return;

        const structureTitle = document.querySelector('#btn-aa-structure .acc-btn-title');
        const structureHint = document.querySelector('#structure-image-trigger .structure-image-hint');
        const structureTrigger = document.getElementById('structure-image-trigger');
        const structureImages = document.querySelectorAll('.structure-image, #structure-image-modal img');
        const structureModalPanel = document.querySelector('#structure-image-modal [role="dialog"]');
        const useEnglish = curLang === 'en';

        [structureTitle, structureHint].forEach(element => {
            if (element && !element.dataset.defaultText) element.dataset.defaultText = element.textContent;
        });
        if (structureTitle) structureTitle.textContent = useEnglish ? i18n.en.structureTitle : structureTitle.dataset.defaultText;
        if (structureHint) structureHint.textContent = useEnglish ? i18n.en.structureHint : structureHint.dataset.defaultText;
        if (structureTrigger) structureTrigger.setAttribute('aria-label', useEnglish ? i18n.en.structureImageLabel : 'Увеличить схему структуры АА Казахстана');
        if (structureModalPanel) structureModalPanel.setAttribute('aria-label', useEnglish ? i18n.en.structureImageLabel : 'Структура АА Казахстана');
        structureImages.forEach(image => {
            image.src = useEnglish ? 'assets/aa-kazakhstan-structure-en.svg' : 'assets/aa-kazakhstan-structure.svg';
            image.alt = useEnglish ? i18n.en.structureImageLabel : 'Структура Сообщества АА в Республике Казахстан';
        });

        document.querySelectorAll('#acc-aa-structure .committee-item').forEach((item, index) => {
            const title = item.querySelector('.committee-btn .acc-btn-title');
            const description = item.querySelector('.committee-content p');
            const contact = item.querySelector('.committee-contact strong');
            const message = item.querySelector('.committee-whatsapp');
            [title, description, contact, message].forEach(element => {
                if (element && !element.dataset.defaultText) element.dataset.defaultText = element.textContent;
            });
            const translation = englishProfile?.committees?.[index];
            if (title) title.textContent = useEnglish && translation ? translation.title : title.dataset.defaultText;
            if (description) description.textContent = useEnglish && translation ? translation.description : description.dataset.defaultText;
            if (contact) contact.textContent = useEnglish && translation ? translation.contact : contact.dataset.defaultText;
            if (message) {
                message.textContent = useEnglish ? i18n.en.writeAction : message.dataset.defaultText;
                message.setAttribute('aria-label', useEnglish ? 'Message on WhatsApp' : 'Написать в WhatsApp');
                if (!message.dataset.defaultHref) message.dataset.defaultHref = message.href;
                if (useEnglish && translation) {
                    const phoneMatch = message.href.match(/wa\.me\/(\d+)/);
                    const englishMessage = `Hello. I am writing from the AA Kazakhstan app about: ${translation.title}.`;
                    if (phoneMatch) message.href = `https://wa.me/${phoneMatch[1]}?text=${encodeURIComponent(englishMessage)}`;
                } else {
                    message.href = message.dataset.defaultHref;
                }
            }
        });
    }

    function getGroupId(g) {
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

    function defaultNotificationSettings() {
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
        return date.toLocaleString(getLocale(), { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
    }

    function renderNotificationCenter() {
        const list = document.getElementById('notification-list');
        if (!list) return;
        const items = getInternalNotifications();
        if (!items.length) { list.innerHTML = `<div class="notification-empty">${i18n[curLang].notificationEmpty}</div>`; return; }
        const fallbackTitles = { reflection: i18n[curLang].notifReflectionNew, news: i18n[curLang].notifNewsNew, today: i18n[curLang].notifTodayNew, favorite: i18n[curLang].notifFavoriteNew };
        list.innerHTML = items.map(item => {
            const safeTitle = !item.title || item.title === 'undefined' ? (fallbackTitles[item.type] || i18n[curLang].notificationCenter) : item.title;
            const safeText = !item.text || item.text === 'undefined' ? '' : item.text;
            return `<button class="notification-item${item.read ? '' : ' unread'}" type="button" data-notification-id="${escapeHtml(item.id)}"><span class="notification-icon">${escapeHtml(item.icon || '🔔')}</span><span><span class="notification-item-title">${item.read ? '' : '<span class="notification-dot"></span>'}${escapeHtml(safeTitle)}</span><span class="notification-item-text">${escapeHtml(safeText)}</span><span class="notification-time">${formatNotificationTime(item.createdAt)}</span></span></button>`;
        }).join('');
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
        if (!title || title === 'Загрузка...' || title === 'Жүктелуде...' || title === i18n.en.reflectionLoading) return;
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
        const userCity = getSavedUserCity();
        const groups = data.filter(group => Array.isArray(group.sc) && group.sc.some(slot => slot.d === day) && (!userCity || group.c === userCity || group.online));
        if (!groups.length) return;
        const cities = [...new Set(groups.map(group => group.c))];
        const text = curLang === 'kz'
            ? `${groups.length} жиналыс · ${cities.slice(0, 3).join(', ')}`
            : curLang === 'en'
                ? `${i18n.en.meetingCount(groups.length)} · ${cities.slice(0, 3).join(', ')}`
                : `${groups.length} собраний · ${cities.slice(0, 3).join(', ')}`;
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
                const text = `${group.n} · ${time}${group.online ? ` · ${i18n[curLang].onlineWord || 'онлайн'}` : group.a ? ` · ${group.a}` : ''}`;
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

    function cleanPhone(phone) { return String(phone || '').replace(/[^\d+]/g, ''); }
    function escapeHtml(value) { return String(value).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#039;'); }
    function plural(n, t) { return t[(n%10===1 && n%100!==11)?0:n%10>=2 && n%10<=4 && (n%100<10||n%100>=20)?1:2]; }

    function trackEvent(action, label, params = {}) {
        if (typeof window.gtag !== 'function') return;
        window.gtag('event', action, Object.assign({
            event_category: 'engagement',
            event_label: label
        }, params));
    }

    function getCachedReflections() {
        try {
            const raw = localStorage.getItem(REFLECTIONS_STORAGE_KEY);
            return raw ? JSON.parse(raw) : null;
        } catch (error) {
            console.error('Ошибка чтения кэша размышлений:', error);
            return null;
        }
    }

    function saveCachedReflections(reflections) {
        try {
            localStorage.setItem(REFLECTIONS_STORAGE_KEY, JSON.stringify(reflections));
        } catch (error) {
            console.error('Ошибка сохранения кэша размышлений:', error);
        }
    }

    function formatReflectionTitle(value) {
        const raw = String(value || '').trim().replace(/\s+-\s+/g, ' — ');
        if (!raw) return '';

        const lower = raw.toLocaleLowerCase('ru-RU');
        const sentenceCase = lower.replace(/[а-яёa-z]/i, letter => letter.toLocaleUpperCase('ru-RU'));

        return sentenceCase
            .replace(/\bаа\b/gi, 'АА')
            .replace(/\bа\.\s*а\.\b/gi, 'А.А.');
    }

    function getReflectionLine(today, item) {
        const monthNames = {
            ru: ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'],
            kz: ['қаңтар','ақпан','наурыз','сәуір','мамыр','маусым','шілде','тамыз','қыркүйек','қазан','қараша','желтоқсан'],
            en: ['January','February','March','April','May','June','July','August','September','October','November','December']
        };

        const fallbackMonth = monthNames[curLang]?.[today.getMonth()] || monthNames.ru[today.getMonth()];
        const fallbackDate = `${today.getDate()} ${fallbackMonth}`;
        const dateText = curLang === 'ru' && item.date_ru ? item.date_ru : fallbackDate;
        const titleText = formatReflectionTitle(item.title);

        return titleText ? `${dateText}. ${titleText}` : dateText;
    }

    function renderMotivationFromData(reflections) {
        const titleEl = document.getElementById('mot-title');
        const quoteEl = document.getElementById('mot-quote');
        const sourceEl = document.getElementById('mot-source');
        const fullTextEl = document.getElementById('mot-full-text');

        if (!titleEl || !quoteEl || !sourceEl || !fullTextEl || !reflections) return false;

        currentReflectionsData = reflections;

        const today = new Date();
        const key = `${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
        const item = reflections[key];

        if (!item) {
            titleEl.innerText = curLang === 'kz'
                ? 'Бүгінге мәтін табылмады'
                : curLang === 'en' ? i18n.en.reflectionMissing : 'Размышление на сегодня не найдено';
            quoteEl.innerText = '';
            sourceEl.innerText = '';
            fullTextEl.innerText = '';
            return false;
        }

        titleEl.innerText = getReflectionLine(today, item);
        quoteEl.innerText = item.quote || '';
        sourceEl.innerText = item.source || '';
        fullTextEl.innerText = item.text || '';
        return true;
    }

    function toggleMotivation() {
        const toggle = document.getElementById('mot-toggle');
        const content = document.getElementById('mot-content');
        if (!toggle || !content) return;

        const isOpening = !content.classList.contains('open');
        content.classList.toggle('open', isOpening);
        toggle.classList.toggle('open', isOpening);
        toggle.setAttribute('aria-expanded', String(isOpening));

        trackEvent(
            isOpening ? 'reflection_open' : 'reflection_close',
            document.getElementById('mot-title')?.innerText || 'daily_reflection'
        );
    }

    function formatRemainingMinutes(minutes) {
        const d = i18n[curLang];
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        if (hours > 0) return `${hours} ${d.hoursShort} ${mins} ${d.minutesShort}`;
        return `${mins} ${d.minutesShort}`;
    }

    function build2GISLink(g) {
        if (!g || !g.a || g.online) return '';
        const rawAddress = String(g.a).trim();
        if (!rawAddress) return '';
        if (/^(инфо по тел\.?|уточнять по номеру)$/i.test(rawAddress)) return '';
        if (g.map) return g.map;
        return `https://2gis.kz/search/${encodeURIComponent(g.c + ', ' + rawAddress)}`;
    }

    function toggleSos() {
        const box = document.getElementById('sos-box');
        const isOpening = !box.classList.contains('open');
        box.classList.toggle('open');
        trackEvent(isOpening ? 'sos_open' : 'sos_close', 'main_button');
    }

    function toggleTheme() {
        const isDark = document.body.classList.toggle('dark-mode');
        localStorage.setItem('aa_theme', isDark ? 'dark' : 'light');
        document.getElementById('theme-icon').innerText = isDark ? '☀️' : '🌙';
        const themeColor = isDark ? '#080A0D' : '#FAF0E6';
        document.querySelector('meta[name="theme-color"]').setAttribute('content', themeColor);
    }

    function toggleAcc(id, btn) {
        const el = document.getElementById(id);
        if (!el || !btn) return;
        const isOpen = el.style.display === 'block';

        // Вложенные комитеты раскрываются независимо и не закрывают общий раздел.
        if (btn.classList.contains('committee-btn')) {
            el.style.display = isOpen ? 'none' : 'block';
            btn.classList.toggle('open', !isOpen);
            btn.setAttribute('aria-expanded', String(!isOpen));
            return;
        }

        // Для верхнего уровня сохраняем поведение обычного аккордеона.
        document.querySelectorAll('.acc-content:not(.committee-content)').forEach(c => c.style.display = 'none');
        document.querySelectorAll('.acc-btn:not(.committee-btn)').forEach(b => {
            b.classList.remove('open');
            b.setAttribute('aria-expanded', 'false');
        });
        if (!isOpen) {
            el.style.display = 'block';
            btn.classList.add('open');
            btn.setAttribute('aria-expanded', 'true');
        }
    }

    function openStructureImage() {
        const modal = document.getElementById('structure-image-modal');
        if (!modal) return;
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('structure-image-open');
    }

    function closeStructureImage() {
        const modal = document.getElementById('structure-image-modal');
        if (!modal) return;
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('structure-image-open');
    }

    function toggleToday() { setGroupFilterMode(groupFilterMode === 'today' ? 'all' : 'today'); }

    function setTrustCallState(id, phone) {
        const link = document.getElementById(`call-${id}`);
        const clean = cleanPhone(phone || '');
        if (clean) {
            link.href = `tel:${clean}`;
            link.classList.remove('disabled');
        } else {
            link.href = '#';
            link.classList.add('disabled');
        }
    }

    function saveTrust(id) {
        const n = document.getElementById(`tr-n-${id}`).value;
        const p = document.getElementById(`tr-p-${id}`).value;
        localStorage.setItem(`aa_trust_n_${id}`, n);
        localStorage.setItem(`aa_trust_p_${id}`, p);
        setTrustCallState(id, p);
    }

    function saveNotes(val) {
        const status = document.getElementById('save-status');
        if (status) {
            status.innerText = i18n[curLang].savePending;
            status.classList.add('show');
        }
        if (saveTimeout) clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            localStorage.setItem('aa_user_notes', val);
            if (status) {
                status.innerText = i18n[curLang].saveDone;
                setTimeout(() => status.classList.remove('show'), 2000);
            }
        }, 800);
    }

    function updateMedalProgress(totalDays, startDateVal) {
        const start = new Date(startDateVal);
        const now = new Date();
        let targetDate = new Date(start);
        let lastMilestoneDate = new Date(start);
        if (totalDays < 365) {
            let monthCount = 0;
            while (targetDate <= now) {
                lastMilestoneDate = new Date(targetDate);
                monthCount += 1;
                targetDate = new Date(start.getFullYear(), start.getMonth() + monthCount, start.getDate());
            }
        } else {
            let yearCount = 0;
            while (targetDate <= now) {
                lastMilestoneDate = new Date(targetDate);
                yearCount += 1;
                targetDate = new Date(start.getFullYear() + yearCount, start.getMonth(), start.getDate());
            }
        }
        const totalInterval = targetDate - lastMilestoneDate;
        const timePassed = now - lastMilestoneDate;
        const progress = totalInterval > 0 ? Math.min(100, Math.max(0, (timePassed / totalInterval) * 100)) : 100;
        document.getElementById('medal-fill-main').style.width = `${progress}%`;
        const daysLeft = Math.max(0, Math.ceil((targetDate - now) / 86400000));
        document.getElementById('medal-info-text').innerText = `${i18n[curLang].nextMedal}: ${i18n[curLang].left} ${daysLeft} ${plural(daysLeft, i18n[curLang].units[2])}`;
    }

    function saveSoberDate(v) {
        localStorage.setItem('aa_sober_v3', v);
        // Clean up old keys if they exist, to rely on a single source of truth
        localStorage.removeItem('aa_sober');
        localStorage.removeItem('sobriety_date');
        localStorage.removeItem('soberDate');
    }

    function getSavedSoberDate() {
        return localStorage.getItem('aa_sober_v3')
            || localStorage.getItem('aa_sober')
            || localStorage.getItem('sobriety_date')
            || localStorage.getItem('soberDate')
            || '';
    }

    function updateDate(v) {
        if (!v) return;
        saveSoberDate(v);
        const s = new Date(v);
        const n = new Date();
        let y = n.getFullYear() - s.getFullYear();
        let m = n.getMonth() - s.getMonth();
        let d = n.getDate() - s.getDate();
        if (d < 0) {
            m--;
            d += new Date(n.getFullYear(), n.getMonth(), 0).getDate();
        }
        if (m < 0) {
            y--;
            m += 12;
        }
        const tD = Math.max(0, Math.floor((n - s) / 86400000));

        // Update complex display with separate ornamental units
        const units = [y, m, d];
        const baseLabels = i18n[curLang].soberUnitsShort;
        let yearLabel = baseLabels[0];
        if (curLang === 'ru') {
            yearLabel = (y >= 1 && y <= 4) ? 'года' : 'лет';
        }
        const labels = curLang === 'en'
            ? [y === 1 ? 'year' : 'years', 'mo.', d === 1 ? 'day' : 'days']
            : [yearLabel, baseLabels[1], baseLabels[2]];
        const complexDisplay = document.getElementById('complex-sober-display');
        complexDisplay.innerHTML = units.map((val, i) => `
            <div class="sober-unit">
                <div class="sober-num">${val}</div>
                <div class="sober-label">${labels[i]}</div>
            </div>
        `).join('');

        document.getElementById('total-days-display').innerText = `${i18n[curLang].total} ${tD} ${plural(tD, i18n[curLang].units[2])}`;
        updateMedalProgress(tD, v);
        trackEvent('sobriety_date_set', 'counter', { value: tD });
    }

    function setLang(lang) {
        if (!i18n[lang]) lang = 'ru';
        curLang = lang;
        document.documentElement.lang = lang === 'kz' ? 'kk' : lang;
        trackEvent('language_switch', lang);
        localStorage.setItem('aa_lang', lang);
        document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(`l-${lang}`).classList.add('active');
        document.querySelectorAll('[data-first-lang]').forEach(button => button.classList.toggle('active', button.dataset.firstLang === lang));
        const d = i18n[lang];
        document.getElementById('t-head').innerText = d.head;
        document.getElementById('t-mot-lab').innerText = d.motLab;
        document.getElementById('t-kaspi').innerText = d.kaspi;
        document.getElementById('t-kaspi-note').innerText = d.kaspiNote;
        updateFreshnessDisplay();
        document.getElementById('todayFilter').innerText = d.todayBtn;
        document.getElementById('btn-sos-main').innerText = d.sosMain;
        document.getElementById('sos-ru-text').innerText = d.sosRu;
        document.getElementById('sos-kz-text').innerText = d.sosKz;
        document.getElementById('n-prof').innerText = d.nProf;
        document.getElementById('trust-head-text').innerText = d.trustHead;
        document.getElementById('prayer-head-text').innerText = d.prayerHead;
        document.getElementById('notes-head-text').innerText = d.notesHead;
        document.getElementById('notifications-head-text').innerText = d.notificationsHead;
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
        document.getElementById('city-setting-title').innerText = d.citySettingTitle;
        document.getElementById('city-setting-note').innerText = d.citySettingNote;
        document.getElementById('city-setting-open').innerText = d.cityChange;
        document.getElementById('settings-head-text').innerText = d.settingsHead;
        document.getElementById('settings-version-label').innerText = d.versionLabel;
        document.getElementById('settings-update-label').innerText = d.updateLabel;
        renderEnglishProfile();
        renderPrinciples(lang);
        updateCitySettingDisplay();

        document.getElementById('quick-today-text').innerText = d.quickToday;
        document.getElementById('quick-favorites-text').innerText = d.quickFavorites;
        document.getElementById('group-filter-mycity').innerText = d.myCity;
        document.getElementById('todayFilter').innerText = d.todayBtn.replace('📅 ', '');
        document.getElementById('group-filter-favorites').innerText = d.favorites.replace('★ ', '');
        document.getElementById('group-filter-online').innerText = d.onlineFilter;
        document.getElementById('city-onboarding-title').innerText = d.chooseCityTitle;
        document.getElementById('city-onboarding-note').innerText = d.chooseCityNote;
        document.getElementById('city-onboarding-save').innerText = d.saveCity;
        document.getElementById('city-onboarding-all').innerText = d.showAllCities;
        document.getElementById('text-size-title').innerText = d.textSizeTitle;
        document.getElementById('text-size-normal').innerText = d.textSizeNormal;
        document.getElementById('text-size-large').innerText = d.textSizeLarge;

        const newsLanguageNote = document.getElementById('news-language-note');
        if (newsLanguageNote) {
            newsLanguageNote.hidden = lang !== 'en';
            newsLanguageNote.innerText = i18n.en.newsOriginalNote;
        }
        setEnglishOnlyText('backup-title', i18n.en.backupTitle);
        setEnglishOnlyText('export-data', i18n.en.exportData);
        setEnglishOnlyText('restore-data', i18n.en.restoreData);
        setEnglishOnlyText('install-banner-text', i18n.en.installText);
        setEnglishOnlyText('install-app', i18n.en.installAction);
        setEnglishOnlyText('first-run-title', i18n.en.firstRunLanguage);
        setEnglishOnlyText('first-run-note-1', i18n.en.firstRunLanguageNote);
        setEnglishOnlyText('first-run-city-title', i18n.en.firstRunCity);
        setEnglishOnlyText('first-run-note-2', i18n.en.firstRunCityNote);
        setEnglishOnlyText('first-run-group-title', i18n.en.firstRunGroup);
        setEnglishOnlyText('first-run-note-3', i18n.en.firstRunGroupNote);
        setEnglishOnlyText('first-run-back', i18n.en.firstRunBack);
        setEnglishOnlyText('schedule-updated-value', i18n.en.scheduleDate);
        document.getElementById('install-close')?.setAttribute('aria-label', lang === 'en' ? i18n.en.closeAction : 'Закрыть');
        document.getElementById('book-modal-close')?.setAttribute('aria-label', lang === 'en' ? i18n.en.closeAction : 'Закрыть');
        document.getElementById('structure-image-close')?.setAttribute('aria-label', lang === 'en' ? i18n.en.closeAction : 'Закрыть');
        const minuteOptions = document.querySelectorAll('#notif-before option');
        minuteOptions.forEach((option, index) => {
            if (!option.dataset.defaultText) option.dataset.defaultText = option.textContent;
            option.textContent = lang === 'en' ? i18n.en.minuteOptions[index] : option.dataset.defaultText;
        });
        document.querySelectorAll('.nav-item').forEach((button, index) => {
            const label = index < 4 ? d.nav[index] : d.nProf;
            button.setAttribute('aria-label', label);
        });
        const splash = document.getElementById('app-splash');
        if (splash) splash.setAttribute('aria-label', lang === 'en' ? 'App loading' : 'Приложение загружается');
        const splashTitle = document.querySelector('.app-splash-title');
        const splashTagline = document.querySelector('.app-splash-tagline');
        [splashTitle, splashTagline].forEach(element => {
            if (element && !element.dataset.defaultText) element.dataset.defaultText = element.textContent;
        });
        if (splashTitle) splashTitle.textContent = lang === 'en' ? 'AA Kazakhstan' : splashTitle.dataset.defaultText;
        if (splashTagline) splashTagline.textContent = lang === 'en' ? 'There is a way out' : splashTagline.dataset.defaultText;
        document.title = lang === 'en' ? 'AA Kazakhstan' : 'АА Казахстана';

        document.getElementById('prayer-content').innerText = d.prayer;
        document.getElementById('user-notes').placeholder = d.placeholder;
        document.getElementById('save-status').innerText = d.saveDone;
        document.getElementById('t-lit-com').innerText = d.litCom;
        document.getElementById('t-lit-price').innerText = d.litPrice;
        const bookFilterButtons = document.querySelectorAll('.book-filter');
        if (bookFilterButtons.length === 3) {
            bookFilterButtons[0].innerText = d.bookAll;
            bookFilterButtons[1].innerText = d.bookRu;
            bookFilterButtons[2].innerText = d.bookKz;
        }
        document.querySelectorAll('.nav-txt').forEach((el, i) => { if (d.nav[i]) el.innerText = d.nav[i]; });
        for (let i = 0; i < 5; i++) {
            document.getElementById(`tr-n-${i}`).placeholder = d.trustName;
            document.getElementById(`tr-p-${i}`).placeholder = d.trustPhone;
        }
        rebuildCityOptions();
        updateDate(document.getElementById('date-input').value);
        if (currentReflectionsData) renderMotivationFromData(currentReflectionsData);
        if (currentNewsData) renderNews(currentNewsData);
        renderFirstRun();
        if (document.getElementById('tab-lit').classList.contains('active')) renderLit();
        if (document.getElementById('tab-groups').classList.contains('active')) renderGroups();
    }

    function renderPrinciples(lang) {
        const content = principles && principles[lang];
        if (!content) return;

        ['steps', 'traditions', 'concepts'].forEach(sectionName => {
            const section = content[sectionName];
            const title = document.getElementById(`${sectionName}-title`);
            const container = document.getElementById(`${sectionName}-content`);
            if (!section || !title || !container) return;

            title.innerText = section.title;
            container.innerHTML = `
                <p class="principles-intro">${escapeHtml(section.intro)}</p>
                <ol class="principles-list">
                    ${section.items.map(item => `<li class="principles-item"><span class="principles-text">${escapeHtml(item)}</span></li>`).join('')}
                </ol>
            `;
        });
    }

    let appStatusTimer = null;

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

    function goTo(tab, direction = null) {
        if (!TAB_ORDER.includes(tab)) return;

        trackEvent('open_tab', tab, direction ? { navigation_method: 'swipe', swipe_direction: direction } : {});
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active', 'swipe-from-right', 'swipe-from-left');
        });
        document.querySelectorAll('.nav-item').forEach(button => button.classList.remove('active-nav'));

        const targetSection = document.getElementById(`tab-${tab}`);
        targetSection.classList.add('active');

        if (direction === 'left') targetSection.classList.add('swipe-from-right');
        if (direction === 'right') targetSection.classList.add('swipe-from-left');

        document.getElementById(`btn-${tab === 'profile' ? 'p' : tab[0]}`).classList.add('active-nav');

        if (tab === 'news') loadNews();
        if (tab === 'lit') renderLit();
        if (tab === 'groups') renderGroups();
        window.scrollTo(0, 0);
    }

    function getActiveTab() {
        const activeSection = document.querySelector('.content-section.active');
        return activeSection ? activeSection.id.replace('tab-', '') : 'counter';
    }

    function isSwipeBlockedTarget(target) {
        return Boolean(target.closest(
            'input, textarea, select, option, button, a, [contenteditable="true"], .book-item, .news-carousel'
        ));
    }

    function handleTouchStart(event) {
        if (event.touches.length !== 1) {
            swipeBlocked = true;
            return;
        }

        const touch = event.touches[0];
        touchStartX = touch.clientX;
        touchStartY = touch.clientY;
        touchStartTime = Date.now();
        swipeBlocked = isSwipeBlockedTarget(event.target);
    }

    function handleTouchEnd(event) {
        if (swipeBlocked || !event.changedTouches.length) return;

        const touch = event.changedTouches[0];
        const deltaX = touch.clientX - touchStartX;
        const deltaY = touch.clientY - touchStartY;
        const elapsed = Date.now() - touchStartTime;

        const isHorizontalSwipe =
            Math.abs(deltaX) >= SWIPE_MIN_DISTANCE &&
            Math.abs(deltaX) > Math.abs(deltaY) * 1.25 &&
            Math.abs(deltaY) <= SWIPE_MAX_VERTICAL_DRIFT &&
            elapsed <= 800;

        if (!isHorizontalSwipe) return;

        const currentTab = getActiveTab();
        const currentIndex = TAB_ORDER.indexOf(currentTab);

        if (deltaX < 0 && currentIndex < TAB_ORDER.length - 1) {
            goTo(TAB_ORDER[currentIndex + 1], 'left');
        } else if (deltaX > 0 && currentIndex > 0) {
            goTo(TAB_ORDER[currentIndex - 1], 'right');
        }
    }

    function loadTrust() {
        for (let i = 0; i < 5; i++) {
            const n = localStorage.getItem(`aa_trust_n_${i}`) || '';
            const p = localStorage.getItem(`aa_trust_p_${i}`) || '';
            document.getElementById(`tr-n-${i}`).value = n;
            document.getElementById(`tr-p-${i}`).value = p;
            setTrustCallState(i, p);
        }
        document.getElementById('user-notes').value = localStorage.getItem('aa_user_notes') || '';
    }

    function getBookCover(index, book, compact = false) {
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
        const shareText = `${book.n}

${book.d}

${curLang === 'en' ? i18n.en.literatureShare : 'Литературный комитет АА Казахстана'}: +7 (777) 556-71-41`;
        try {
            if (navigator.share) {
                await navigator.share({ title: book.n, text: shareText });
            } else if (navigator.clipboard) {
                await navigator.clipboard.writeText(shareText);
                alert(curLang === 'kz' ? 'Кітап туралы ақпарат көшірілді' : curLang === 'en' ? i18n.en.bookCopied : 'Информация о книге скопирована');
            }
            trackEvent('book_share', book.n);
        } catch (error) {
            if (error && error.name !== 'AbortError') console.error('Ошибка отправки:', error);
        }
    }

    function getGroupStatus(g) {
        if (!g.sc || g.sc.length === 0) return `<div class="status-badge s-closed"><div class="status-dot"></div>${i18n[curLang].sClosed}</div>`;
        const now = new Date();
        const d = now.getDay();
        const curM = now.getHours() * 60 + now.getMinutes();
        const todaySlots = g.sc.filter(s => s.d === d).sort((a,b) => a.s - b.s);
        for (const slot of todaySlots) {
            const startM = Math.floor(slot.s / 100) * 60 + (slot.s % 100);
            const endM = Math.floor(slot.e / 100) * 60 + (slot.e % 100);
            if (curM >= startM && curM < endM) return `<div class="status-badge s-open"><div class="status-dot"></div>${i18n[curLang].sOpen} ${formatRemainingMinutes(endM - curM)}</div>`;
            if (curM < startM) return `<div class="status-badge s-soon"><div class="status-dot"></div>${i18n[curLang].sSoon} ${formatRemainingMinutes(startM - curM)}</div>`;
        }
        return `<div class="status-badge s-closed"><div class="status-dot"></div>${i18n[curLang].sClosed}</div>`;
    }

    function renderPhones(arr) {
        const title = arr.length > 1 ? i18n[curLang].phonesLabel : i18n[curLang].phoneLabel;
        return `
            <div class="info-row">
                <span class="info-row-icon">📞</span>
                <div>
                    <div class="muted">${title}</div>
                    <div class="group-phones">${arr.map(phone => `<a href="tel:${cleanPhone(phone)}" class="phone-link" data-track="group_phone" data-phone="${escapeHtml(phone)}">${escapeHtml(phone)}</a>`).join('')}</div>
                </div>
            </div>
        `;
    }

    function renderAddress(g) {
        if (!g.a || g.online) return '';
        const mapLink = build2GISLink(g);
        const linkHtml = mapLink ? `<br><a href="${mapLink}" target="_blank" rel="noopener noreferrer" class="inline-link" data-track="map_open" data-group="${escapeHtml(g.n)}" data-city="${escapeHtml(g.c)}">${i18n[curLang].openMap}</a>` : '';
        return `
            <div class="info-row">
                <span class="info-row-icon">📍</span>
                <div>
                    <div class="muted">${i18n[curLang].addressLabel}</div>
                    <div>${escapeHtml(g.a)}${linkHtml}</div>
                </div>
            </div>
        `;
    }

    function renderOnlineLinks(g) {
        let html = '';
        if (g.online && g.a) {
            const label = g.chat ? i18n[curLang].chatLabel : i18n[curLang].zoomLabel;
            const text = g.chat ? i18n[curLang].openChat : i18n[curLang].openZoom;
            html += `
                <div class="info-row">
                    <span class="info-row-icon">🌐</span>
                    <div>
                        <div class="muted">${label}</div>
                        <a href="${g.a}" target="_blank" rel="noopener noreferrer" class="inline-link" data-track="open_online" data-group="${escapeHtml(g.n)}" data-city="${escapeHtml(g.c)}" data-type="${g.chat ? 'chat' : 'zoom'}">${text}</a>
                    </div>
                </div>
            `;
        }
        if (g.z) {
            html += `
                <div class="info-row">
                    <span class="info-row-icon">💬</span>
                    <div>
                        <div class="muted">${i18n[curLang].zoomLabel}</div>
                        <a href="${g.z}" target="_blank" rel="noopener noreferrer" class="inline-link" data-track="open_online" data-group="${escapeHtml(g.n)}" data-city="${escapeHtml(g.c)}" data-type="zoom_extra">${i18n[curLang].openZoom}</a>
                    </div>
                </div>
            `;
        }
        return html;
    }

    function buildReportLink(g) {
        const text = curLang === 'kz'
            ? `Сәлеметсіз бе. Қазақстан АА қосымшасында «${g.n}» тобы туралы деректерден қате таптым.\n\nНақты емес ақпарат: `
            : curLang === 'en'
                ? i18n.en.reportGroupMessage(g.n)
                : `Здравствуйте. В приложении АА Казахстана обнаружена неточность в данных группы «${g.n}».\n\nЧто именно неверно: `;
        return `https://wa.me/77051871335?text=${encodeURIComponent(text)}`;
    }

    function formatCheckedTime(value) {
        if (!value) return '—';
        const d = new Date(value);
        if (Number.isNaN(d.getTime())) return '—';
        const today = new Date();
        const sameDay = d.toDateString() === today.toDateString();
        const time = d.toLocaleTimeString(getLocale(), {hour:'2-digit', minute:'2-digit'});
        const todayWord = curLang === 'kz' ? 'бүгін' : curLang === 'en' ? i18n.en.checkedToday : 'сегодня';
        return sameDay ? `${todayWord}, ${time}` : d.toLocaleString(getLocale(), {day:'numeric', month:'long', hour:'2-digit', minute:'2-digit'});
    }

    function updateFreshnessDisplay() {
        const d=i18n[curLang];
        document.getElementById('schedule-updated-label').innerText=d.scheduleUpdated;
        document.getElementById('news-checked-label').innerText=d.newsChecked;
        document.getElementById('news-checked-value').innerText=formatCheckedTime(localStorage.getItem('aa_news_checked_at'));
    }

    let firstRunStep=1;
    function fillFirstRunGroups() {
        const city=document.getElementById('first-run-city').value;
        const select=document.getElementById('first-run-group');
        const empty=curLang==='kz'?'Қазір таңдамау':curLang==='en'?i18n.en.chooseLater:'Не выбирать сейчас';
        select.innerHTML=`<option value="">${empty}</option>`+data.filter(g=>!g.online&&g.c===city).map(g=>`<option value="${escapeHtml(getGroupId(g))}">${escapeHtml(g.n)}</option>`).join('');
    }
    function renderFirstRun() {
        document.querySelectorAll('[data-first-step]').forEach(el=>el.classList.toggle('active',Number(el.dataset.firstStep)===firstRunStep));
        document.getElementById('first-run-progress').innerText=curLang==='kz'?`${firstRunStep}/3 қадам`:curLang==='en'?i18n.en.firstRunProgress(firstRunStep):`Шаг ${firstRunStep} из 3`;
        document.getElementById('first-run-back').style.visibility=firstRunStep===1?'hidden':'visible';
        document.getElementById('first-run-next').innerText=firstRunStep===3?(curLang==='kz'?'Дайын':curLang==='en'?i18n.en.firstRunDone:'Готово'):(curLang==='kz'?'Әрі қарай':curLang==='en'?i18n.en.firstRunNext:'Далее');
    }
    function openFirstRun() {
        const cities=[...new Set(data.filter(g=>!g.online).map(g=>g.c))].sort((a,b)=>a.localeCompare(b,'ru'));
        const city=document.getElementById('first-run-city');
        city.innerHTML=cities.map(v=>`<option value="${escapeHtml(v)}">${escapeHtml(v)}</option>`).join('');
        const saved=getSavedUserCity(); if(saved&&cities.includes(saved)) city.value=saved;
        fillFirstRunGroups(); firstRunStep=1; renderFirstRun();
        document.getElementById('first-run').classList.add('open'); document.getElementById('first-run').setAttribute('aria-hidden','false'); document.body.classList.add('first-run-open');
    }
    function finishFirstRun() {
        const city=document.getElementById('first-run-city').value;
        if(city) localStorage.setItem(USER_CITY_STORAGE_KEY,city);
        const groupId=document.getElementById('first-run-group').value;
        if(groupId){const fav=getFavoriteGroups();fav.add(groupId);saveFavoriteGroups(fav);}
        localStorage.setItem('aa_first_run_done_v1','1'); localStorage.setItem('aa_city_onboarding_done_v1','1');
        document.getElementById('first-run').classList.remove('open'); document.getElementById('first-run').setAttribute('aria-hidden','true'); document.body.classList.remove('first-run-open');
        rebuildCityOptions(); updateCitySettingDisplay(); renderGroups();
    }

    function getSavedUserCity() { return localStorage.getItem(USER_CITY_STORAGE_KEY) || ''; }

    function setGroupFilterMode(mode) {
        groupFilterMode = mode;
        onlyToday = mode === 'today';
        document.querySelectorAll('[data-group-mode]').forEach(button => button.classList.toggle('active', button.dataset.groupMode === mode));
        if (mode === 'mycity') {
            const city = getSavedUserCity();
            if (!city) {
                openCityOnboarding();
                groupFilterMode = 'all';
                document.querySelectorAll('[data-group-mode]').forEach(button => button.classList.remove('active'));
                return;
            }
            document.getElementById('citySelect').value = city;
        } else if (mode === 'favorites') {
            document.getElementById('citySelect').value = 'all';
        } else if (mode === 'online') {
            document.getElementById('citySelect').value = 'Онлайн';
        }
        renderGroups();
    }

    function localizeSchedule(schedule) {
        if (curLang !== 'en' || !schedule) return schedule;
        const replacements = [
            [/По запросу/gi, 'On request'],
            [/Ежедневно/gi, 'Daily'],
            [/Суббота/gi, 'Saturday'],
            [/Пн/g, 'Mon'], [/Вт/g, 'Tue'], [/Ср/g, 'Wed'], [/Чт/g, 'Thu'], [/Пт/g, 'Fri'], [/Сб/g, 'Sat'], [/Вс/g, 'Sun'],
            [/все группы открытые/gi, 'all meetings open'],
            [/откр/gi, 'open'],
            [/Интервью с алкоголиком/gi, 'Interview with an alcoholic']
        ];
        return replacements.reduce((value, [pattern, replacement]) => value.replace(pattern, replacement), String(schedule));
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
                            <div class="city-tag">${escapeHtml(curLang === 'en' && g.c === 'Онлайн' ? i18n.en.onlineFilter : g.c)}</div>
                            <div class="group-name">${escapeHtml(g.n)} ${icons ? `<span class="group-icons">${icons}</span>` : ''}</div>
                        </div>
                        <button type="button" class="favorite-btn${isFavorite ? ' active' : ''}" data-favorite-id="${escapeHtml(groupId)}" aria-label="${escapeHtml(favoriteLabel)}" title="${escapeHtml(favoriteLabel)}">${isFavorite ? '★' : '☆'}</button>
                    </div>
                    <div class="group-info">
                        ${renderAddress(g)}
                        <div class="info-row"><span class="info-row-icon">⏰</span><div><div class="muted">${i18n[curLang].scheduleLabel}</div><div>${escapeHtml(localizeSchedule(g.t || i18n[curLang].noSchedule))}</div></div></div>
                        ${g.p && g.p.length ? renderPhones(g.p) : ''}
                    </div>
                    <div class="group-actions">${buildGroupActions(g)}<a class="report-error" href="${buildReportLink(g)}" target="_blank" rel="noopener noreferrer" data-track="report_error" data-group="${escapeHtml(g.n)}">${i18n[curLang].reportError}</a></div>
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
            o.innerText = city === 'all' ? i18n[curLang].allCities : (curLang === 'en' && city === 'Онлайн' ? i18n.en.onlineFilter : city);
            s.appendChild(o);
        });
        s.value = [...s.options].some(opt => opt.value === current) ? current : 'all';
        buildCityOnboardingOptions();
    }

    function buildCityOnboardingOptions() {
        const select = document.getElementById('city-onboarding-select');
        if (!select) return;
        const current = getSavedUserCity();
        const cities = [...new Set(data.filter(group => !group.online).map(group => group.c))].sort((a,b) => a.localeCompare(b, 'ru'));
        select.innerHTML = cities.map(city => `<option value="${escapeHtml(city)}">${escapeHtml(city)}</option>`).join('');
        if (current && cities.includes(current)) select.value = current;
    }

    function updateCitySettingDisplay() {
        const el = document.getElementById('city-setting-current');
        if (!el) return;
        el.innerText = getSavedUserCity() || i18n[curLang].cityNotSelected;
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
        localStorage.setItem('aa_city_onboarding_done_v1', '1');
        if (city) localStorage.setItem(USER_CITY_STORAGE_KEY, city);
        else localStorage.removeItem(USER_CITY_STORAGE_KEY);
        rebuildCityOptions();
        setGroupFilterMode(city ? 'mycity' : 'all');
        updateCitySettingDisplay();
        closeCityOnboarding();
    }


    function openFirstTimeInfo() {
    const d = i18n[curLang];
    document.getElementById('first-time-modal-title').innerText = d.firstTitle;
    document.getElementById('first-time-modal-text').innerText = d.firstText;
    const modal = document.getElementById('first-time-modal');
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
}

function closeFirstTimeInfo() {
    const modal = document.getElementById('first-time-modal');
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-open');
}

    function applySavedTheme() {
        const savedTheme = localStorage.getItem('aa_theme');
        const shouldDark = savedTheme !== 'light';
        if (shouldDark) {
            document.body.classList.add('dark-mode');
            document.getElementById('theme-icon').innerText = '☀️';
            document.querySelector('meta[name="theme-color"]').setAttribute('content', '#080A0D');
        } else {
            document.body.classList.remove('dark-mode');
            document.getElementById('theme-icon').innerText = '🌙';
            document.querySelector('meta[name="theme-color"]').setAttribute('content', '#FAF0E6');
        }
    }

    function formatNewsDate(dateString) {
        const parsed = new Date(`${dateString}T12:00:00`);
        if (Number.isNaN(parsed.getTime())) return dateString || '';

        return new Intl.DateTimeFormat(getLocale(), {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        }).format(parsed);
    }

    function getCachedNews() {
        try {
            const cached = localStorage.getItem(NEWS_STORAGE_KEY);
            return cached ? JSON.parse(cached) : null;
        } catch (error) {
            console.warn('Не удалось прочитать кэш новостей:', error);
            return null;
        }
    }

    function saveCachedNews(posts) {
        try {
            localStorage.setItem(NEWS_STORAGE_KEY, JSON.stringify(posts));
        } catch (error) {
            console.warn('Не удалось сохранить кэш новостей:', error);
        }
    }

    function updateNewsCarousel(card, index) {
        const carousel = card.querySelector('.news-carousel');
        const counter = card.querySelector('.news-counter');
        const dots = card.querySelectorAll('.news-dot');
        if (!carousel) return;

        const total = dots.length || 1;
        const safeIndex = Math.max(0, Math.min(index, total - 1));

        if (counter) counter.textContent = curLang === 'en' ? i18n.en.newsCounter(safeIndex + 1, total) : `${safeIndex + 1} из ${total}`;
        dots.forEach((dot, dotIndex) => {
            dot.classList.toggle('active', dotIndex === safeIndex);
            dot.setAttribute('aria-current', dotIndex === safeIndex ? 'true' : 'false');
        });
    }

    function attachNewsCarouselEvents() {
        document.querySelectorAll('.news-card').forEach(card => {
            const carousel = card.querySelector('.news-carousel');
            const dots = card.querySelectorAll('.news-dot');
            if (!carousel || carousel.dataset.ready === 'true') return;

            carousel.dataset.ready = 'true';
            let scrollTimer = null;

            carousel.addEventListener('scroll', () => {
                clearTimeout(scrollTimer);
                scrollTimer = setTimeout(() => {
                    const width = carousel.clientWidth || 1;
                    const index = Math.round(carousel.scrollLeft / width);
                    updateNewsCarousel(card, index);
                }, 60);
            }, { passive: true });

            dots.forEach((dot, index) => {
                dot.addEventListener('click', () => {
                    carousel.scrollTo({
                        left: carousel.clientWidth * index,
                        behavior: 'smooth'
                    });
                    updateNewsCarousel(card, index);
                });
            });

            updateNewsCarousel(card, 0);
        });
    }

    function renderNews(posts) {
        const container = document.getElementById('news-list');
        if (!container) return false;

        if (!Array.isArray(posts) || posts.length === 0) {
            container.innerHTML = `
                <div class="card news-empty">
                    ${curLang === 'kz' ? 'Әзірге жаңалықтар жоқ.' : curLang === 'en' ? i18n.en.newsEmpty : 'Пока новостей нет.'}
                </div>
            `;
            return false;
        }

        currentNewsData = posts;

        container.innerHTML = posts.map((post, postIndex) => {
            const images = Array.isArray(post.images) ? post.images.filter(Boolean) : [];
            const total = images.length;

            const slides = images.map((image, imageIndex) => `
                <div class="news-slide">
                    <img
                        src="${escapeHtml(image)}"
                        alt="${escapeHtml(post.title || (curLang === 'en' ? i18n.en.newsImageAlt : 'Новость АА Казахстана'))} — ${imageIndex + 1}"
                        loading="${postIndex === 0 && imageIndex === 0 ? 'eager' : 'lazy'}"
                        draggable="false"
                    >
                </div>
            `).join('');

            const dots = total > 1
                ? `<div class="news-dots" aria-label="${curLang === 'en' ? i18n.en.newsCarouselLabel : 'Навигация по карточкам'}">
                    ${images.map((_, imageIndex) => `
                        <button
                            type="button"
                            class="news-dot${imageIndex === 0 ? ' active' : ''}"
                            aria-label="${curLang === 'en' ? i18n.en.newsOpenCard(imageIndex + 1) : `Открыть карточку ${imageIndex + 1}`}"
                        ></button>
                    `).join('')}
                   </div>`
                : '';

            return `
                <article class="card news-card" data-news-id="${escapeHtml(post.id || '')}">
                    ${total ? `
                        <div class="news-carousel-wrap">
                            <div class="news-carousel">${slides}</div>
                            ${total > 1 ? `<div class="news-counter">${curLang === 'en' ? i18n.en.newsCounter(1, total) : `1 из ${total}`}</div>` : ''}
                        </div>
                        ${dots}
                    ` : ''}
                    <div class="news-meta">
                        <div class="news-category">${escapeHtml(post.category || '')}</div>
                        <div class="news-date">${escapeHtml(formatNewsDate(post.date))}</div>
                        <div class="news-title">${escapeHtml(post.title || '')}</div>
                        ${post.description
                            ? `<div class="news-description">${escapeHtml(post.description)}</div>`
                            : ''}
                    </div>
                </article>
                ${postIndex < posts.length - 1 ? '<div class="ornament-divider"></div>' : ''}
            `;
        }).join('');

        attachNewsCarouselEvents();
        return true;
    }

    async function loadNews(force = false) {
        if (newsLoaded && !force && currentNewsData) {
            renderNews(currentNewsData);
            return;
        }

        const container = document.getElementById('news-list');
        if (!container) return;

        if (!currentNewsData) {
            showAppStatus(i18n[curLang].statusUpdating);
            container.innerHTML = `
                <div class="card news-loading">
                    ${curLang === 'kz' ? 'Жаңалықтар жүктелуде...' : curLang === 'en' ? i18n.en.newsLoading : 'Загрузка новостей...'}
                </div>
            `;
        }

        const cachedNews = getCachedNews();

        if (!navigator.onLine && cachedNews) {
            showAppStatus(i18n[curLang].statusOffline, 3200);
            newsLoaded = true;
            renderNews(cachedNews);
            return;
        }

        try {
            const response = await fetch('news.json', { cache: 'no-cache' });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const posts = await response.json();
            saveCachedNews(posts);
            localStorage.setItem('aa_news_checked_at', new Date().toISOString());
            updateFreshnessDisplay();
            showAppStatus(i18n[curLang].statusUpdated);
            newsLoaded = true;
            renderNews(posts);
        } catch (error) {
            console.error('Не удалось загрузить новости:', error);

            if (cachedNews && renderNews(cachedNews)) {
                newsLoaded = true;
                return;
            }

            container.innerHTML = `
                <div class="card news-error">
                    ${curLang === 'kz'
                        ? 'Жаңалықтарды жүктеу мүмкін болмады.'
                        : curLang === 'en' ? i18n.en.newsError : 'Не удалось загрузить новости.'}
                </div>
            `;
        }
    }

    async function setMotivation() {
        const titleEl = document.getElementById('mot-title');
        if (!titleEl) return;
        titleEl.innerText = curLang === 'kz' ? 'Жүктелуде...' : curLang === 'en' ? i18n.en.reflectionLoading : 'Загрузка...';

        const cachedReflections = getCachedReflections();

        if (!navigator.onLine && cachedReflections) {
            if (renderMotivationFromData(cachedReflections)) return;
        }

        try {
            const response = await fetch('daily_reflections_full.json', { cache: 'no-cache' });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const reflections = await response.json();
            saveCachedReflections(reflections);
            renderMotivationFromData(reflections);
        } catch (error) {
            console.error('Не удалось загрузить полные ежедневные размышления:', error);

            if (cachedReflections && renderMotivationFromData(cachedReflections)) return;

            titleEl.innerText = curLang === 'kz'
                ? 'Күнделікті ойларды жүктеу мүмкін болмады'
                : curLang === 'en' ? i18n.en.reflectionError : 'Не удалось загрузить ежедневные размышления';
        }
    }

    function attachEvents() {
        document.querySelectorAll('[data-first-lang]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-first-lang]').forEach(b=>b.classList.remove('active'));button.classList.add('active');setLang(button.dataset.firstLang);renderFirstRun();}));
        document.getElementById('first-run-city').addEventListener('change',fillFirstRunGroups);
        document.getElementById('first-run-back').addEventListener('click',()=>{if(firstRunStep>1){firstRunStep--;renderFirstRun();}});
        document.getElementById('first-run-next').addEventListener('click',()=>{if(firstRunStep<3){firstRunStep++;if(firstRunStep===3)fillFirstRunGroups();renderFirstRun();}else finishFirstRun();});
        document.getElementById('theme-icon').addEventListener('click', () => {
            toggleTheme();
            trackEvent('theme_toggle', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        });
        document.getElementById('l-ru').addEventListener('click', () => setLang('ru'));
        document.getElementById('l-kz').addEventListener('click', () => setLang('kz'));
        document.getElementById('l-en').addEventListener('click', () => setLang('en'));
        document.getElementById('btn-sos-main').addEventListener('click', toggleSos);
        document.getElementById('mot-toggle').addEventListener('click', toggleMotivation);
        document.getElementById('structure-image-trigger')?.addEventListener('click', openStructureImage);
        document.getElementById('structure-image-close')?.addEventListener('click', closeStructureImage);
        document.getElementById('structure-image-modal')?.addEventListener('click', event => {
            if (event.target.id === 'structure-image-modal') closeStructureImage();
        });
        document.getElementById('today-actions').addEventListener('click', event => {
            const action = event.target.closest('[data-today-action]');
            if (!action) return;
            if (action.dataset.todayAction === 'today') { goTo('groups'); setGroupFilterMode('today'); }
            if (action.dataset.todayAction === 'favorites') { goTo('groups'); setGroupFilterMode('favorites'); }
        });
        document.getElementById('group-quick-filters').addEventListener('click', event => {
            const button = event.target.closest('[data-group-mode]');
            if (button) setGroupFilterMode(button.dataset.groupMode);
        });
        document.getElementById('city-onboarding-save').addEventListener('click', () => saveUserCity(document.getElementById('city-onboarding-select').value));
        document.getElementById('city-onboarding-all').addEventListener('click', () => saveUserCity(''));
        document.getElementById('city-setting-open').addEventListener('click', event => { event.stopPropagation(); openCityOnboarding(); });

        document.getElementById('todayFilter').addEventListener('click', toggleToday);
        document.getElementById('notification-button').addEventListener('click', openNotificationCenter);
        document.getElementById('notification-close').addEventListener('click', closeNotificationCenter);
        document.getElementById('notification-read-all').addEventListener('click', markAllNotificationsRead);
        document.getElementById('notification-panel').addEventListener('click', event => { if (event.target.id === 'notification-panel') closeNotificationCenter(); });
        document.getElementById('notification-list').addEventListener('click', event => { const item = event.target.closest('[data-notification-id]'); if (item) openInternalNotification(item.dataset.notificationId); });
        ['master','reflection','news','today','favorites','browser'].forEach(key => document.getElementById(`notif-${key}`).addEventListener('change', event => updateNotificationSetting(key, event.target.checked)));
        document.getElementById('notif-before').addEventListener('change', event => updateNotificationSetting('before', Number(event.target.value)));
        document.addEventListener('keydown', event => { if (event.key === 'Escape') { closeNotificationCenter(); closeStructureImage(); } });

    document.getElementById('list-container').addEventListener('click', event => {
        const button = event.target.closest('[data-favorite-id]');
        if (!button) return;
        toggleFavorite(button.dataset.favoriteId);
    });
        document.getElementById('citySelect').addEventListener('change', e => {
            trackEvent('city_filter', e.target.value);
            groupFilterMode = 'all';
            document.querySelectorAll('[data-group-mode]').forEach(button => button.classList.remove('active'));
            renderGroups();
        });
        document.getElementById('date-input').addEventListener('change', e => updateDate(e.target.value));
        document.getElementById('user-notes').addEventListener('input', e => saveNotes(e.target.value));
        document.querySelectorAll('.acc-btn').forEach(button => {
            button.addEventListener('click', () => {
                const target = button.getAttribute('data-acc-target');
                if (target) {
                    const isOpening = document.getElementById(target).style.display !== 'block';
                    toggleAcc(target, button);
                    trackEvent(isOpening ? 'accordion_open' : 'accordion_close', target);
                }
            });
        });
        document.querySelectorAll('.nav-item').forEach(button => {
            button.addEventListener('click', () => {
                const tab = button.getAttribute('data-tab');
                if (tab) goTo(tab);
            });
        });
        for (let i = 0; i < 5; i++) {
            document.getElementById(`tr-n-${i}`).addEventListener('input', () => saveTrust(i));
            document.getElementById(`tr-p-${i}`).addEventListener('input', () => saveTrust(i));
            document.getElementById(`call-${i}`).addEventListener('click', () => {
                const phone = document.getElementById(`tr-p-${i}`).value;
                if (cleanPhone(phone)) trackEvent('call', `trusted_contact_${i + 1}`, { phone_number: cleanPhone(phone) });
            });
        }
        document.getElementById('book-filters').addEventListener('click', e => {
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
        });

        document.getElementById('tab-counter').addEventListener('click', e => {
            const sosLink = e.target.closest('.sos-opt-link');
            if (sosLink) {
                const label = sosLink.querySelector('span') ? sosLink.querySelector('span').innerText.trim() : 'sos_call';
                trackEvent('call', label === i18n[curLang].sosKz ? 'sos_kz' : 'sos_ru');
                return;
            }

            const donationLink = e.target.closest('a[href*="kaspi.kz/pay/FOAAK"]');
            if (donationLink) trackEvent('donation_click', 'kaspi');
        });

        document.getElementById('tab-lit').addEventListener('click', e => {
            const litCall = e.target.closest('a[href^="tel:+77775567141"]');
            if (litCall) trackEvent('call', 'literature_committee');
        });

        const swipeArea = document.querySelector('.main-container');
        swipeArea.addEventListener('touchstart', handleTouchStart, { passive: true });
        swipeArea.addEventListener('touchend', handleTouchEnd, { passive: true });
        swipeArea.addEventListener('touchcancel', () => {
            swipeBlocked = true;
        }, { passive: true });

        document.getElementById('tab-groups').addEventListener('click', e => {
            const phoneLink = e.target.closest('[data-track="group_phone"]');
            if (phoneLink) {
                const card = phoneLink.closest('.group-card');
                const groupName = card && card.querySelector('.group-name') ? card.querySelector('.group-name').innerText.trim() : 'group_phone';
                trackEvent('call', groupName, { phone_number: cleanPhone(phoneLink.getAttribute('data-phone') || '') });
                return;
            }

            const mapLink = e.target.closest('[data-track="map_open"]');
            if (mapLink) {
                trackEvent('map_open', mapLink.getAttribute('data-group') || 'group_map', { city: mapLink.getAttribute('data-city') || '' });
                return;
            }

            const reportLink = e.target.closest('[data-track="report_error"]');
            if (reportLink) { trackEvent('report_group_error', reportLink.getAttribute('data-group') || 'group'); return; }

            const onlineLink = e.target.closest('[data-track="open_online"]');
            if (onlineLink) {
                trackEvent('open_online', onlineLink.getAttribute('data-group') || 'online_group', {
                    city: onlineLink.getAttribute('data-city') || '',
                    meeting_type: onlineLink.getAttribute('data-type') || ''
                });
            }
        });
    }

    async function init() {
        try {
            const [groupsResponse, booksResponse] = await Promise.all([fetch('groups.json', {cache:'no-store'}), fetch('books.json', {cache:'no-store'})]);
            if (!groupsResponse.ok || !booksResponse.ok) throw new Error('data_load_failed');
            data = await groupsResponse.json();
            books = await booksResponse.json();
        } catch (error) {
            console.error('Не удалось загрузить данные приложения:', error);
            showAppStatus(curLang === 'kz' ? 'Қолданба деректерін жүктеу мүмкін болмады' : curLang === 'en' ? 'Could not load app data' : 'Не удалось загрузить данные приложения', 4000);
        }
        trackEvent('app_loaded', 'initial_load');
        document.querySelectorAll('[data-text-size]').forEach(button => {
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
    applySavedTheme();
        attachEvents();
        rebuildCityOptions();
        const storedDate = getSavedSoberDate() || new Date().toISOString().split('T')[0];
        document.getElementById('date-input').value = storedDate;
        loadTrust();
        syncNotificationSettingsUI();
        updateCitySettingDisplay();
        updateNotificationBadge();
        setLang(curLang);
        setMotivation();
        loadNews();
        renderGroups();
        renderLit();
        updateFreshnessDisplay();
        const releaseNotificationKey = 'release:2.0';
        if (!notificationSeen(releaseNotificationKey)) {
            const releaseTitle = curLang === 'kz'
                ? 'Қазақстан АА қолданбасының 2.0 нұсқасы шықты'
                : curLang === 'en' ? i18n.en.releaseTitle : 'Вышла версия приложения АА Казахстана 2.0';
            const releaseText = curLang === 'kz'
                ? 'Жаңа навигация, ірі мәтін, топтардың жаңа түймелері, хабарламалар, сақтық көшірме және басқа өзгерістер.'
                : curLang === 'en' ? i18n.en.releaseText : 'Новая навигация, крупный текст, новые кнопки групп, уведомления, резервная копия и другие изменения.';
            const releaseItems = getInternalNotifications();
            releaseItems.unshift({
                key: releaseNotificationKey,
                id: releaseNotificationKey,
                type: 'news',
                icon: '🎉',
                title: releaseTitle,
                text: releaseText,
                tab: 'news',
                createdAt: Date.now(),
                read: false
            });
            saveInternalNotifications(releaseItems);
            markNotificationSeen(releaseNotificationKey);
            localStorage.setItem('aa_last_news_identity', 'release-2-0-ru');
            updateNotificationBadge();
        }

        localStorage.setItem('aa_first_run_done_v1', '1');
        const firstRunModal = document.getElementById('first-run');
        if (firstRunModal) {
            firstRunModal.classList.remove('open');
            firstRunModal.setAttribute('aria-hidden', 'true');
        }
        document.body.classList.remove('first-run-open');
        setTimeout(runInternalNotificationChecks, 1800);
        notificationTimer = setInterval(runInternalNotificationChecks, 60000);
        window.dispatchEvent(new Event('aa-app-ready'));
    }

    window.addEventListener('online', () => {
        trackEvent('network_status', 'online');
        setMotivation();
        loadNews(true);
        setTimeout(runInternalNotificationChecks, 1800);
    });

    window.addEventListener('offline', () => {
        trackEvent('network_status', 'offline');
    });

    window.addEventListener('load', init);
})();

(() => {
    'use strict';
    const BACKUP_PREFIXES = ['aa_'];
    const backupKeys = () => Object.keys(localStorage).filter(k => BACKUP_PREFIXES.some(p => k.startsWith(p)));
    function exportData(){
        const payload={format:'aa-kazakhstan-backup',version:1,createdAt:new Date().toISOString(),data:{}};
        backupKeys().forEach(k=>payload.data[k]=localStorage.getItem(k));
        const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
        const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=`aa-kazakhstan-backup-${new Date().toISOString().slice(0,10)}.json`; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),1000);
    }
    async function restoreData(file){
        const language = localStorage.getItem('aa_lang') || 'ru';
        try{const payload=JSON.parse(await file.text()); if(payload?.format!=='aa-kazakhstan-backup'||!payload.data) throw new Error('invalid'); Object.entries(payload.data).forEach(([k,v])=>{if(k.startsWith('aa_')) localStorage.setItem(k,String(v));}); alert(language==='kz'?'Деректер қалпына келтірілді. Қолданба қайта жүктеледі.':language==='en'?window.AA_I18N.en.backupRestored:'Данные восстановлены. Приложение будет перезапущено.'); location.reload();}catch(e){alert(language==='kz'?'Файлды қалпына келтіру мүмкін болмады.':language==='en'?window.AA_I18N.en.backupRestoreFailed:'Не удалось восстановить данные из файла.');}
    }
    let installEvent=null;
    window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installEvent=e;document.getElementById('install-banner')?.classList.add('show');});
    window.addEventListener('appinstalled',()=>{installEvent=null;document.getElementById('install-banner')?.classList.remove('show');localStorage.setItem('aa_pwa_installed','1');});
    window.addEventListener('load',()=>{
        document.getElementById('export-data')?.addEventListener('click',exportData);
        document.getElementById('restore-data')?.addEventListener('click',()=>document.getElementById('restore-file')?.click());
        document.getElementById('restore-file')?.addEventListener('change',e=>{const f=e.target.files?.[0];if(f)restoreData(f);});
        document.getElementById('install-app')?.addEventListener('click',async()=>{if(!installEvent)return;installEvent.prompt();await installEvent.userChoice;installEvent=null;document.getElementById('install-banner')?.classList.remove('show');});
        document.getElementById('install-close')?.addEventListener('click',()=>document.getElementById('install-banner')?.classList.remove('show'));
    });
})();
