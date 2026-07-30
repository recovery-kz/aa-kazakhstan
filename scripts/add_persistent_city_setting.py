from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Add persistent city setting to profile.
anchor = '''            <div class="ornament-divider"></div> <button class="acc-btn" type="button" data-acc-target="acc-notifications" id="btn-notifications-head">'''
block = '''            <div class="ornament-divider"></div> <button class="acc-btn" type="button" data-acc-target="acc-city" id="btn-city-head"><span class="acc-btn-left"><span class="acc-btn-title" id="city-head-text">МОЙ ГОРОД</span></span></button>
            <div class="acc-content" id="acc-city">
                <div class="notification-setting" style="border-bottom:none;">
                    <span class="notification-setting-main"><span class="notification-setting-title" id="city-setting-title">Выберите свой город</span><span class="notification-setting-note" id="city-setting-note">Он используется для ближайших собраний и уведомлений</span></span>
                    <button type="button" class="notification-small-btn" id="city-setting-open">Изменить</button>
                </div>
                <div id="city-setting-current" style="padding:0 0 14px;color:var(--primary);font-weight:850;"></div>
            </div>
'''
if 'id="acc-city"' not in text:
    if anchor not in text:
        raise SystemExit('profile anchor not found')
    text = text.replace(anchor, block + anchor, 1)

# Add translations.
text = text.replace("firstText: 'Собрания бесплатные. Записываться не нужно. Можно ничего не говорить и просто слушать. Фамилию называть необязательно.'", "firstText: 'Собрания бесплатные. Записываться не нужно. Можно ничего не говорить и просто слушать. Фамилию называть необязательно.', cityHead: 'МОЙ ГОРОД', citySettingTitle: 'Выберите свой город', citySettingNote: 'Он используется для ближайших собраний и уведомлений', cityChange: 'Изменить', cityNotSelected: 'Город не выбран'")
text = text.replace("firstText: 'Жиналыстар тегін. Алдын ала жазылудың қажеті жоқ. Ештеңе айтпай, жай ғана тыңдауға болады. Тегіңізді айту міндетті емес.'", "firstText: 'Жиналыстар тегін. Алдын ала жазылудың қажеті жоқ. Ештеңе айтпай, жай ғана тыңдауға болады. Тегіңізді айту міндетті емес.', cityHead: 'МЕНІҢ ҚАЛАМ', citySettingTitle: 'Қалаңызды таңдаңыз', citySettingNote: 'Ол ең жақын жиналыстар мен хабарламалар үшін қолданылады', cityChange: 'Өзгерту', cityNotSelected: 'Қала таңдалмаған'")

# Make my-city filter open selector when city is absent.
old = '''        if (mode === 'mycity') {
            const city = getSavedUserCity();
            document.getElementById('citySelect').value = city || 'all';
        } else if (mode === 'favorites') {'''
new = '''        if (mode === 'mycity') {
            const city = getSavedUserCity();
            if (!city) {
                openCityOnboarding();
                groupFilterMode = 'all';
                document.querySelectorAll('[data-group-mode]').forEach(button => button.classList.remove('active'));
                return;
            }
            document.getElementById('citySelect').value = city;
        } else if (mode === 'favorites') {'''
if old in text:
    text = text.replace(old, new, 1)

# Sync labels in setLang.
lang_anchor = "        document.getElementById('notification-button').setAttribute('aria-label', d.notificationCenter);"
lang_extra = '''        document.getElementById('city-head-text').innerText = d.cityHead;
        document.getElementById('city-setting-title').innerText = d.citySettingTitle;
        document.getElementById('city-setting-note').innerText = d.citySettingNote;
        document.getElementById('city-setting-open').innerText = d.cityChange;
        updateCitySettingDisplay();
'''
if 'updateCitySettingDisplay();' not in text.split(lang_anchor,1)[0][-500:]:
    text = text.replace(lang_anchor, lang_anchor + '\n' + lang_extra, 1)

# Add helper next to onboarding functions.
helper_anchor = "    function openCityOnboarding() {"
helper = '''    function updateCitySettingDisplay() {
        const el = document.getElementById('city-setting-current');
        if (!el) return;
        el.innerText = getSavedUserCity() || i18n[curLang].cityNotSelected;
    }

'''
if 'function updateCitySettingDisplay()' not in text:
    text = text.replace(helper_anchor, helper + helper_anchor, 1)

# Update display after save/all.
text = text.replace("        renderNearestMeeting();\n        closeCityOnboarding();", "        renderNearestMeeting();\n        updateCitySettingDisplay();\n        closeCityOnboarding();")

# Add event.
event_anchor = "        document.getElementById('city-onboarding-save').addEventListener('click', saveCityFromOnboarding);"
if "city-setting-open" not in text.split('function attachEvents()',1)[1]:
    text = text.replace(event_anchor, event_anchor + "\n        document.getElementById('city-setting-open').addEventListener('click', openCityOnboarding);", 1)

# Initial display.
init_anchor = "        syncNotificationSettingsUI();"
if "updateCitySettingDisplay();" not in text.split('function init()',1)[1].split("window.addEventListener('online'",1)[0]:
    text = text.replace(init_anchor, init_anchor + "\n        updateCitySettingDisplay();", 1)

# Bump SW version.
text = text.replace("navigator.serviceWorker.register('sw.js?v=4'", "navigator.serviceWorker.register('sw.js?v=5'")
text = text.replace("navigator.serviceWorker.register('sw.js?v=3'", "navigator.serviceWorker.register('sw.js?v=5'")

path.write_text(text, encoding='utf-8')
