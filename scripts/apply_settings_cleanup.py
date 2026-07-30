from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Add generic internal information modal styles.
css_anchor = "        .city-onboarding {"
css = """        .info-modal { position:fixed; inset:0; z-index:5100; background:rgba(0,0,0,.58); display:none; align-items:flex-end; justify-content:center; padding:14px 12px max(14px,env(safe-area-inset-bottom)); }
        .info-modal.open { display:flex; }
        .info-modal-sheet { width:100%; max-width:500px; background:var(--card-bg); border-radius:24px; padding:22px; box-shadow:0 20px 55px rgba(0,0,0,.32); }
        .info-modal-title { font-size:21px; line-height:1.25; font-weight:900; color:var(--text-main); margin-bottom:12px; }
        .info-modal-text { font-size:15px; line-height:1.65; color:var(--text-main); white-space:pre-line; }
        .info-modal-close { width:100%; min-height:48px; margin-top:18px; border:0; border-radius:13px; background:var(--primary); color:white; font:inherit; font-weight:850; cursor:pointer; }
        .settings-version { padding:14px 0 2px; color:var(--text-sub); font-size:12px; line-height:1.6; }

"""
if '.info-modal {' not in text:
    text = text.replace(css_anchor, css + css_anchor, 1)

# Extract city and notifications blocks from their current position.
city_pattern = re.compile(r'\s*<div class="ornament-divider"></div> <button class="acc-btn" type="button" data-acc-target="acc-city".*?</div>\s*</div>', re.S)
notif_pattern = re.compile(r'\s*<div class="ornament-divider"></div> <button class="acc-btn" type="button" data-acc-target="acc-notifications".*?</div>\s*</div>', re.S)
city_match = city_pattern.search(text)
notif_match = notif_pattern.search(text)
if not city_match or not notif_match:
    raise SystemExit('city or notification block not found')
city_block = city_match.group(0).strip()
notif_block = notif_match.group(0).strip()
text = text[:city_match.start()] + text[city_match.end():]
# Re-find notifications after first removal.
notif_match = notif_pattern.search(text)
if not notif_match:
    raise SystemExit('notification block missing after city removal')
notif_block = notif_match.group(0).strip()
text = text[:notif_match.start()] + text[notif_match.end():]

# Insert one Settings accordion at the very bottom of profile card.
notes_anchor = '<div class="acc-content" id="acc-notes"><textarea class="notes-area" id="user-notes"></textarea></div>'
settings_block = f'''{notes_anchor}
            <div class="ornament-divider"></div> <button class="acc-btn" type="button" data-acc-target="acc-settings" id="btn-settings-head"><span class="acc-btn-left"><span class="acc-btn-title" id="settings-head-text">НАСТРОЙКИ</span></span></button>
            <div class="acc-content" id="acc-settings">
                <div style="padding:2px 0 10px;">
                    <div class="notification-setting" style="border-bottom:none;">
                        <span class="notification-setting-main"><span class="notification-setting-title" id="city-setting-title">Выберите свой город</span><span class="notification-setting-note" id="city-setting-note">Он используется для ближайших собраний и уведомлений</span></span>
                        <button type="button" class="notification-small-btn" id="city-setting-open">Изменить</button>
                    </div>
                    <div id="city-setting-current" style="padding:0 0 14px;color:var(--primary);font-weight:850;"></div>
                </div>
                <div class="ornament-divider"></div>
                <div class="notification-settings" style="padding-top:4px;">
                    <div class="notification-setting-title" id="notifications-head-text" style="padding:0 0 10px;">УВЕДОМЛЕНИЯ</div>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-master-title">Внутренние уведомления</span><span class="notification-setting-note" id="notif-master-note">Показывать новые события в центре уведомлений</span></span><input class="notification-switch" id="notif-master" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-reflection-title">Ежедневные размышления</span><span class="notification-setting-note" id="notif-reflection-note">Сообщать о новом размышлении при открытии приложения</span></span><input class="notification-switch" id="notif-reflection" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-news-title">Новости</span><span class="notification-setting-note" id="notif-news-note">Сообщать о новых публикациях</span></span><input class="notification-switch" id="notif-news" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-today-title">Группы сегодня</span><span class="notification-setting-note" id="notif-today-note">Показывать сводку собраний на текущий день</span></span><input class="notification-switch" id="notif-today" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-favorites-title">Избранные группы</span><span class="notification-setting-note" id="notif-favorites-note">Напоминать перед началом собрания, пока приложение открыто</span></span><input class="notification-switch" id="notif-favorites" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-browser-title">Системное окно при открытом приложении</span><span class="notification-setting-note" id="notif-browser-note">Не работает после полного закрытия приложения</span></span><input class="notification-switch" id="notif-browser" type="checkbox"></label>
                    <label class="notification-setting"><span class="notification-setting-main"><span class="notification-setting-title" id="notif-before-title">Напоминать заранее</span></span><select class="notification-select" id="notif-before"><option value="15">15 мин</option><option value="30">30 мин</option><option value="60">1 час</option><option value="120">2 часа</option></select></label>
                </div>
                <div class="settings-version"><span id="settings-version-label">Версия приложения</span>: <strong id="settings-version-value">1.6</strong><br><span id="settings-update-label">Обновление применяется автоматически при запуске</span></div>
            </div>'''
if 'id="acc-settings"' not in text:
    text = text.replace(notes_anchor, settings_block, 1)

# Add custom first-time modal before city modal.
modal_anchor = '<div class="city-onboarding" id="city-onboarding"'
first_modal = '''<div class="info-modal" id="first-time-modal" aria-hidden="true">
    <div class="info-modal-sheet" role="dialog" aria-modal="true" aria-labelledby="first-time-modal-title">
        <div class="info-modal-title" id="first-time-modal-title">Первый раз в АА</div>
        <div class="info-modal-text" id="first-time-modal-text"></div>
        <button class="info-modal-close" type="button" id="first-time-modal-close">Понятно</button>
    </div>
</div>

'''
if 'id="first-time-modal"' not in text:
    text = text.replace(modal_anchor, first_modal + modal_anchor, 1)

# Translations.
text = text.replace("cityNotSelected: 'Город не выбран'", "cityNotSelected: 'Город не выбран', settingsHead: 'НАСТРОЙКИ', versionLabel: 'Версия приложения', updateLabel: 'Обновление применяется автоматически при запуске', understood: 'Понятно'")
text = text.replace("cityNotSelected: 'Қала таңдалмаған'", "cityNotSelected: 'Қала таңдалмаған', settingsHead: 'БАПТАУЛАР', versionLabel: 'Қосымша нұсқасы', updateLabel: 'Жаңарту қосымша іске қосылғанда автоматты түрде қолданылады', understood: 'Түсінікті'")

# Adjust setLang to no longer expect removed city heading and to update settings/modal.
text = text.replace("        document.getElementById('city-head-text').innerText = d.cityHead;\n", '')
text = text.replace("        document.getElementById('city-setting-open').innerText = d.cityChange;\n", "        document.getElementById('city-setting-open').innerText = d.cityChange;\n        document.getElementById('settings-head-text').innerText = d.settingsHead;\n        document.getElementById('settings-version-label').innerText = d.versionLabel;\n        document.getElementById('settings-update-label').innerText = d.updateLabel;\n        document.getElementById('first-time-modal-close').innerText = d.understood;\n")

# Replace system alert with internal modal.
old = """    function openFirstTimeInfo() {
        const d = i18n[curLang];
        alert(`${d.firstTitle}\n\n${d.firstText}`);
    }
"""
new = """    function openFirstTimeInfo() {
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
"""
if old not in text:
    raise SystemExit('first time alert function not found')
text = text.replace(old, new, 1)

# Fix missing city change listener and modal listeners.
event_anchor = "        document.getElementById('city-onboarding-all').addEventListener('click', () => saveUserCity(''));"
event_extra = """
        document.getElementById('city-setting-open').addEventListener('click', event => { event.stopPropagation(); openCityOnboarding(); });
        document.getElementById('first-time-modal-close').addEventListener('click', closeFirstTimeInfo);
        document.getElementById('first-time-modal').addEventListener('click', event => { if (event.target.id === 'first-time-modal') closeFirstTimeInfo(); });"""
if "city-setting-open').addEventListener" not in text:
    text = text.replace(event_anchor, event_anchor + event_extra, 1)

# Close first-time modal on Escape too.
text = text.replace("document.addEventListener('keydown', event => { if (event.key === 'Escape') closeNotificationCenter(); });", "document.addEventListener('keydown', event => { if (event.key === 'Escape') { closeNotificationCenter(); closeFirstTimeInfo(); } });", 1)

# Update SW query to force pickup.
text = text.replace("register('sw.js?v=3'", "register('sw.js?v=4'", 1)

path.write_text(text, encoding='utf-8')
