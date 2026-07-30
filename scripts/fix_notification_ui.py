from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

s=s.replace("""        .header-controls {
            position: absolute;
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 15px;
            top: 50%;
            transform: translateY(-50%);
        }
""","""        .header-controls {
            position: absolute;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 15px;
            top: 50%;
            transform: translateY(-50%);
            pointer-events: none;
        }
        .header-left-controls { display:flex; align-items:center; gap:8px; pointer-events:auto; }
        .lang-switch { pointer-events:auto; }
""")
s=s.replace("""        <button class="theme-toggle" id="theme-icon" type="button">🌙</button>
        <button class="notification-button" id="notification-button" type="button" aria-label="Уведомления">🔔<span class="notification-badge" id="notification-badge">0</span></button>
        <div class="lang-switch">""","""        <div class="header-left-controls">
            <button class="theme-toggle" id="theme-icon" type="button">🌙</button>
            <button class="notification-button" id="notification-button" type="button" aria-label="Уведомления">🔔<span class="notification-badge" id="notification-badge">0</span></button>
        </div>
        <div class="lang-switch">""")

ru_anchor="            soberUnitsShort: ['лет', 'мес.', 'дней']"
ru_keys="""            notificationsHead: 'УВЕДОМЛЕНИЯ', notificationCenter: 'Уведомления', notificationReadAll: 'Прочитать все', notificationEmpty: 'Здесь появятся новые размышления, новости и напоминания о собраниях.',
            notifMasterTitle: 'Внутренние уведомления', notifMasterNote: 'Показывать новые события в центре уведомлений', notifReflectionTitle: 'Ежедневные размышления', notifReflectionNote: 'Сообщать о новом размышлении при открытии приложения', notifNewsTitle: 'Новости', notifNewsNote: 'Сообщать о новых публикациях', notifTodayTitle: 'Группы сегодня', notifTodayNote: 'Показывать сводку собраний на текущий день', notifFavoritesTitle: 'Избранные группы', notifFavoritesNote: 'Напоминать перед началом собрания, пока приложение открыто', notifBrowserTitle: 'Системное окно при открытом приложении', notifBrowserNote: 'Не работает после полного закрытия приложения', notifBeforeTitle: 'Напоминать заранее',
            notifReflectionNew: 'Новое ежедневное размышление', notifNewsNew: 'Новая публикация', notifTodayNew: 'Собрания сегодня', notifFavoriteNew: 'Скоро начнётся собрание',
"""
if "notificationCenter: 'Уведомления'" not in s:
    s=s.replace(ru_anchor,ru_keys+ru_anchor)

kz_anchor="            soberUnitsShort: ['жыл', 'ай', 'күн']"
kz_keys="""            notificationsHead: 'ХАБАРЛАМАЛАР', notificationCenter: 'Хабарламалар', notificationReadAll: 'Барлығын оқу', notificationEmpty: 'Мұнда жаңа ойлар, жаңалықтар және жиналыстар туралы еске салулар пайда болады.',
            notifMasterTitle: 'Ішкі хабарламалар', notifMasterNote: 'Жаңа оқиғаларды хабарламалар орталығында көрсету', notifReflectionTitle: 'Күнделікті ойлар', notifReflectionNote: 'Қосымша ашылғанда жаңа ой туралы хабарлау', notifNewsTitle: 'Жаңалықтар', notifNewsNote: 'Жаңа жарияланымдар туралы хабарлау', notifTodayTitle: 'Бүгінгі топтар', notifTodayNote: 'Бүгінгі жиналыстардың қорытындысын көрсету', notifFavoritesTitle: 'Таңдаулы топтар', notifFavoritesNote: 'Қосымша ашық кезде жиналыс алдында еске салу', notifBrowserTitle: 'Қосымша ашық кездегі жүйелік терезе', notifBrowserNote: 'Қосымша толық жабылғаннан кейін жұмыс істемейді', notifBeforeTitle: 'Алдын ала еске салу',
            notifReflectionNew: 'Жаңа күнделікті ой', notifNewsNew: 'Жаңа жарияланым', notifTodayNew: 'Бүгінгі жиналыстар', notifFavoriteNew: 'Жиналыс жақында басталады',
"""
if "notificationCenter: 'Хабарламалар'" not in s:
    s=s.replace(kz_anchor,kz_keys+kz_anchor)

old="""        list.innerHTML = items.map(item => `<button class="notification-item${item.read ? '' : ' unread'}" type="button" data-notification-id="${escapeHtml(item.id)}"><span class="notification-icon">${escapeHtml(item.icon || '🔔')}</span><span><span class="notification-item-title">${item.read ? '' : '<span class="notification-dot"></span>'}${escapeHtml(item.title)}</span><span class="notification-item-text">${escapeHtml(item.text)}</span><span class="notification-time">${formatNotificationTime(item.createdAt)}</span></span></button>`).join('');"""
new="""        const fallbackTitles = { reflection: i18n[curLang].notifReflectionNew, news: i18n[curLang].notifNewsNew, today: i18n[curLang].notifTodayNew, favorite: i18n[curLang].notifFavoriteNew };
        list.innerHTML = items.map(item => {
            const safeTitle = !item.title || item.title === 'undefined' ? (fallbackTitles[item.type] || i18n[curLang].notificationCenter) : item.title;
            const safeText = !item.text || item.text === 'undefined' ? '' : item.text;
            return `<button class="notification-item${item.read ? '' : ' unread'}" type="button" data-notification-id="${escapeHtml(item.id)}"><span class="notification-icon">${escapeHtml(item.icon || '🔔')}</span><span><span class="notification-item-title">${item.read ? '' : '<span class="notification-dot"></span>'}${escapeHtml(safeTitle)}</span><span class="notification-item-text">${escapeHtml(safeText)}</span><span class="notification-time">${formatNotificationTime(item.createdAt)}</span></span></button>`;
        }).join('');"""
if old in s: s=s.replace(old,new)

p.write_text(s,encoding='utf-8')
