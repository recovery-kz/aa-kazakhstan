from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

css='''
        /* Приоритет 4: доверие и первый запуск */
        .data-freshness { margin-top: 14px; padding-top: 13px; border-top: 1px solid var(--border); color: var(--text-sub); font-size: 12px; line-height: 1.7; }
        .data-freshness strong { color: var(--text-main); }
        .report-error { grid-column: 1 / -1; min-height: 40px; border: 0; background: transparent; color: var(--text-sub); font: inherit; font-size: 12px; font-weight: 750; text-decoration: underline; text-underline-offset: 3px; cursor: pointer; }
        .first-run { position: fixed; inset: 0; z-index: 7000; display: none; align-items: flex-end; justify-content: center; background: rgba(0,0,0,.58); padding: 14px 12px max(14px,env(safe-area-inset-bottom)); }
        .first-run.open { display: flex; }
        .first-run-sheet { width: 100%; max-width: 500px; background: var(--card-bg); border-radius: 24px; padding: 22px; box-shadow: 0 20px 55px rgba(0,0,0,.34); }
        .first-run-progress { color: var(--accent); font-size: 11px; font-weight: 900; letter-spacing: .05em; text-transform: uppercase; margin-bottom: 8px; }
        .first-run-title { color: var(--text-main); font-size: 23px; line-height: 1.25; font-weight: 900; }
        .first-run-note { color: var(--text-sub); font-size: 13px; line-height: 1.5; margin: 7px 0 17px; }
        .first-run-step { display: none; }
        .first-run-step.active { display: block; }
        .first-run-options { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; }
        .first-run-option { min-height: 50px; border: 1px solid var(--border); border-radius: 13px; background: var(--card-bg); color: var(--primary); font: inherit; font-weight: 850; cursor: pointer; }
        .first-run-option.active { background: var(--primary); border-color: var(--primary); color: white; }
        .first-run-select { width: 100%; min-height: 52px; border: 1px solid var(--border); border-radius: 13px; background: var(--card-bg); color: var(--text-main); padding: 0 12px; font: inherit; font-weight: 800; }
        .first-run-actions { display: grid; grid-template-columns: 1fr 1.4fr; gap: 9px; margin-top: 17px; }
        .first-run-btn { min-height: 48px; border: 1px solid var(--border); border-radius: 13px; background: var(--card-bg); color: var(--primary); font: inherit; font-weight: 850; cursor: pointer; }
        .first-run-btn.primary { background: var(--primary); border-color: var(--primary); color: white; }
        body.first-run-open { overflow: hidden; }
'''
s=s.replace('        /* Разделитель только между крупными смысловыми блоками */',css+'\n        /* Разделитель только между крупными смысловыми блоками */',1)

old='<div class="settings-version"><span id="settings-version-label">Версия приложения</span>: <strong id="settings-version-value">1.7</strong><br><span id="settings-update-label">Обновление применяется автоматически при запуске</span></div>'
new='''<div class="settings-version"><span id="settings-version-label">Версия приложения</span>: <strong id="settings-version-value">1.8</strong><br><span id="settings-update-label">Обновление применяется автоматически при запуске</span></div>
                <div class="data-freshness">
                    <div><span id="schedule-updated-label">Расписание обновлено</span>: <strong id="schedule-updated-value">30 июля 2026</strong></div>
                    <div><span id="news-checked-label">Новости проверены</span>: <strong id="news-checked-value">—</strong></div>
                </div>'''
s=s.replace(old,new,1)

first_run='''
<div class="first-run" id="first-run" aria-hidden="true">
  <div class="first-run-sheet" role="dialog" aria-modal="true" aria-labelledby="first-run-title">
    <div class="first-run-progress" id="first-run-progress">Шаг 1 из 3</div>
    <div class="first-run-step active" data-first-step="1">
      <div class="first-run-title" id="first-run-title">Выберите язык</div>
      <div class="first-run-note" id="first-run-note-1">Язык можно изменить позже в верхней части экрана.</div>
      <div class="first-run-options"><button class="first-run-option active" type="button" data-first-lang="ru">Русский</button><button class="first-run-option" type="button" data-first-lang="kz">Қазақша</button></div>
    </div>
    <div class="first-run-step" data-first-step="2">
      <div class="first-run-title" id="first-run-city-title">Выберите город</div>
      <div class="first-run-note" id="first-run-note-2">Покажем ближайшие собрания.</div>
      <select class="first-run-select" id="first-run-city"></select>
    </div>
    <div class="first-run-step" data-first-step="3">
      <div class="first-run-title" id="first-run-group-title">Добавьте группу в избранное</div>
      <div class="first-run-note" id="first-run-note-3">Этот шаг можно пропустить.</div>
      <select class="first-run-select" id="first-run-group"><option value="">Не выбирать сейчас</option></select>
    </div>
    <div class="first-run-actions"><button class="first-run-btn" type="button" id="first-run-back">Назад</button><button class="first-run-btn primary" type="button" id="first-run-next">Далее</button></div>
  </div>
</div>
'''
s=s.replace('<div class="city-onboarding" id="city-onboarding"',first_run+'\n<div class="city-onboarding" id="city-onboarding"',1)

# report link beneath group actions
s=s.replace('                    <div class="group-actions">${buildGroupActions(g)}</div>\n                </div>`;', '                    <div class="group-actions">${buildGroupActions(g)}<a class="report-error" href="${buildReportLink(g)}" target="_blank" rel="noopener noreferrer" data-track="report_error" data-group="${escapeHtml(g.n)}">${i18n[curLang].reportError}</a></div>\n                </div>`;',1)

# i18n additions
s=s.replace("understood: 'Понятно'", "understood: 'Понятно', reportError: 'Сообщить об ошибке', scheduleUpdated: 'Расписание обновлено', newsChecked: 'Новости проверены'")
s=s.replace("understood: 'Түсінікті'", "understood: 'Түсінікті', reportError: 'Қате туралы хабарлау', scheduleUpdated: 'Кесте жаңартылды', newsChecked: 'Жаңалықтар тексерілді'")

# helper functions before getSavedUserCity
marker="    function getSavedUserCity() { return localStorage.getItem(USER_CITY_STORAGE_KEY) || ''; }"
helpers=r'''    function buildReportLink(g) {
        const text = curLang === 'kz'
            ? `Сәлеметсіз бе. Қазақстан АА қосымшасында «${g.n}» тобы туралы деректерден қате таптым.\n\nНақты емес ақпарат: `
            : `Здравствуйте. В приложении АА Казахстана обнаружена неточность в данных группы «${g.n}».\n\nЧто именно неверно: `;
        return `https://wa.me/77072080553?text=${encodeURIComponent(text)}`;
    }

    function formatCheckedTime(value) {
        if (!value) return '—';
        const d = new Date(value);
        if (Number.isNaN(d.getTime())) return '—';
        const today = new Date();
        const sameDay = d.toDateString() === today.toDateString();
        const time = d.toLocaleTimeString(curLang === 'kz' ? 'kk-KZ' : 'ru-RU', {hour:'2-digit', minute:'2-digit'});
        return sameDay ? `${curLang === 'kz' ? 'бүгін' : 'сегодня'}, ${time}` : d.toLocaleString(curLang === 'kz' ? 'kk-KZ' : 'ru-RU', {day:'numeric', month:'long', hour:'2-digit', minute:'2-digit'});
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
        const empty=curLang==='kz'?'Қазір таңдамау':'Не выбирать сейчас';
        select.innerHTML=`<option value="">${empty}</option>`+data.filter(g=>!g.online&&g.c===city).map(g=>`<option value="${escapeHtml(getGroupId(g))}">${escapeHtml(g.n)}</option>`).join('');
    }
    function renderFirstRun() {
        document.querySelectorAll('[data-first-step]').forEach(el=>el.classList.toggle('active',Number(el.dataset.firstStep)===firstRunStep));
        document.getElementById('first-run-progress').innerText=curLang==='kz'?`${firstRunStep}/3 қадам`:`Шаг ${firstRunStep} из 3`;
        document.getElementById('first-run-back').style.visibility=firstRunStep===1?'hidden':'visible';
        document.getElementById('first-run-next').innerText=firstRunStep===3?(curLang==='kz'?'Дайын':'Готово'):(curLang==='kz'?'Әрі қарай':'Далее');
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

'''
s=s.replace(marker,helpers+marker,1)

# setLang freshness
s=s.replace("        document.getElementById('t-kaspi-note').innerText = d.kaspiNote;", "        document.getElementById('t-kaspi-note').innerText = d.kaspiNote;\n        updateFreshnessDisplay();")

# successful news timestamp
s=s.replace("            saveCachedNews(posts);\n            showAppStatus(i18n[curLang].statusUpdated);", "            saveCachedNews(posts);\n            localStorage.setItem('aa_news_checked_at', new Date().toISOString());\n            updateFreshnessDisplay();\n            showAppStatus(i18n[curLang].statusUpdated);")

# events onboarding and report analytics
insert_events=r'''        document.querySelectorAll('[data-first-lang]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-first-lang]').forEach(b=>b.classList.remove('active'));button.classList.add('active');setLang(button.dataset.firstLang);renderFirstRun();}));
        document.getElementById('first-run-city').addEventListener('change',fillFirstRunGroups);
        document.getElementById('first-run-back').addEventListener('click',()=>{if(firstRunStep>1){firstRunStep--;renderFirstRun();}});
        document.getElementById('first-run-next').addEventListener('click',()=>{if(firstRunStep<3){firstRunStep++;if(firstRunStep===3)fillFirstRunGroups();renderFirstRun();}else finishFirstRun();});
'''
s=s.replace("        document.getElementById('theme-icon').addEventListener('click', () => {",insert_events+"        document.getElementById('theme-icon').addEventListener('click', () => {",1)
s=s.replace("            const onlineLink = e.target.closest('[data-track=\"open_online\"]');", "            const reportLink = e.target.closest('[data-track=\"report_error\"]');\n            if (reportLink) { trackEvent('report_group_error', reportLink.getAttribute('data-group') || 'group'); return; }\n\n            const onlineLink = e.target.closest('[data-track=\"open_online\"]');",1)

# init first run replacing city-only intro
s=s.replace("        if (!localStorage.getItem('aa_city_onboarding_done_v1')) {\n            localStorage.setItem('aa_city_onboarding_done_v1', '1');\n            setTimeout(openCityOnboarding, 450);\n        }", "        updateFreshnessDisplay();\n        if (!localStorage.getItem('aa_first_run_done_v1')) setTimeout(openFirstRun, 450);")

s=s.replace("navigator.serviceWorker.register('sw.js?v=5'", "navigator.serviceWorker.register('sw.js?v=8'")

p.write_text(s,encoding='utf-8')

sw=Path('sw.js')
w=sw.read_text(encoding='utf-8').replace("aa-kaz-v7","aa-kaz-v8")
sw.write_text(w,encoding='utf-8')
