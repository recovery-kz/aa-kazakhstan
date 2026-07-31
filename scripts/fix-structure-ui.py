from pathlib import Path

# Fix nested accordion behavior and add image zoom modal.
app_path = Path('app.js')
app = app_path.read_text(encoding='utf-8')
old_toggle = '''    function toggleAcc(id, btn) {
        const el = document.getElementById(id);
        const isOpen = el.style.display === 'block';
        document.querySelectorAll('.acc-content').forEach(c => c.style.display = 'none');
        document.querySelectorAll('.acc-btn').forEach(b => b.classList.remove('open'));
        if (!isOpen) {
            el.style.display = 'block';
            btn.classList.add('open');
        }
    }
'''
new_toggle = '''    function toggleAcc(id, btn) {
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
'''
if old_toggle not in app:
    raise SystemExit('toggleAcc block not found')
app = app.replace(old_toggle, new_toggle, 1)

anchor = "        document.getElementById('mot-toggle').addEventListener('click', toggleMotivation);\n"
zoom_events = '''        document.getElementById('structure-image-trigger')?.addEventListener('click', openStructureImage);
        document.getElementById('structure-image-close')?.addEventListener('click', closeStructureImage);
        document.getElementById('structure-image-modal')?.addEventListener('click', event => {
            if (event.target.id === 'structure-image-modal') closeStructureImage();
        });
'''
if zoom_events not in app:
    if anchor not in app:
        raise SystemExit('event anchor not found')
    app = app.replace(anchor, anchor + zoom_events, 1)

func_anchor = "    function toggleToday() { setGroupFilterMode(groupFilterMode === 'today' ? 'all' : 'today'); }\n"
zoom_funcs = '''    function openStructureImage() {
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

'''
if 'function openStructureImage()' not in app:
    if func_anchor not in app:
        raise SystemExit('function anchor not found')
    app = app.replace(func_anchor, zoom_funcs + func_anchor, 1)

# Extend existing Escape handler safely.
old_escape = "        document.addEventListener('keydown', event => { if (event.key === 'Escape') closeNotificationCenter(); });"
new_escape = "        document.addEventListener('keydown', event => { if (event.key === 'Escape') { closeNotificationCenter(); closeStructureImage(); } });"
if old_escape in app:
    app = app.replace(old_escape, new_escape, 1)

app_path.write_text(app, encoding='utf-8')

index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')
old_img = '<div class="structure-image-wrap"><img class="structure-image" src="assets/aa-kazakhstan-structure.svg" alt="Структура Сообщества АА в Республике Казахстан" loading="lazy"></div>'
new_img = '<button class="structure-image-wrap" id="structure-image-trigger" type="button" aria-label="Увеличить схему структуры АА Казахстана"><img class="structure-image" src="assets/aa-kazakhstan-structure.svg" alt="Структура Сообщества АА в Республике Казахстан" loading="lazy"><span class="structure-image-hint">Нажмите, чтобы увеличить</span></button>'
if old_img not in index:
    raise SystemExit('structure image block not found')
index = index.replace(old_img, new_img, 1)

modal_anchor = '<div class="notification-panel" id="notification-panel" aria-hidden="true">'
modal_html = '''<div class="structure-image-modal" id="structure-image-modal" aria-hidden="true">
    <div class="structure-image-modal-panel" role="dialog" aria-modal="true" aria-label="Структура АА Казахстана">
        <button class="structure-image-close" id="structure-image-close" type="button" aria-label="Закрыть">×</button>
        <img src="assets/aa-kazakhstan-structure.svg" alt="Структура Сообщества АА в Республике Казахстан">
    </div>
</div>

'''
if 'id="structure-image-modal"' not in index:
    if modal_anchor not in index:
        raise SystemExit('modal anchor not found')
    index = index.replace(modal_anchor, modal_html + modal_anchor, 1)

index = index.replace('styles.css?v=2.0.3', 'styles.css?v=2.0.4')
index = index.replace('app.js?v=2.0.3', 'app.js?v=2.0.4')
index_path.write_text(index, encoding='utf-8')

styles_path = Path('styles.css')
styles = styles_path.read_text(encoding='utf-8')
old_css = '''.structure-image-wrap { width: 100%; overflow-x: auto; border: 1px solid var(--border); border-radius: 14px; background: #f7f8fb; margin-bottom: 14px; -webkit-overflow-scrolling: touch; }
.structure-image { display: block; width: 100%; min-width: 760px; height: auto; }
'''
new_css = '''.structure-image-wrap { width: 100%; display: block; position: relative; overflow: hidden; padding: 0; border: 1px solid var(--border); border-radius: 14px; background: #f7f8fb; margin-bottom: 14px; cursor: zoom-in; font: inherit; }
.structure-image { display: block; width: 100%; min-width: 0; height: auto; object-fit: contain; }
.structure-image-hint { position: absolute; right: 8px; bottom: 8px; padding: 6px 9px; border-radius: 999px; background: rgba(0,0,0,.7); color: #fff; font-size: 10px; line-height: 1; font-weight: 800; }
.structure-image-modal { position: fixed; inset: 0; z-index: 9000; display: none; align-items: center; justify-content: center; padding: 18px; background: rgba(0,0,0,.88); }
.structure-image-modal.open { display: flex; }
.structure-image-modal-panel { position: relative; width: 100%; max-width: 1200px; max-height: 94vh; overflow: auto; border-radius: 14px; background: #fff; }
.structure-image-modal-panel img { display: block; width: 100%; height: auto; min-width: 760px; }
.structure-image-close { position: sticky; float: right; top: 10px; right: 10px; z-index: 2; width: 42px; height: 42px; margin: 10px 10px -52px 0; border: 0; border-radius: 50%; background: rgba(0,0,0,.75); color: #fff; font-size: 28px; line-height: 1; cursor: pointer; }
body.structure-image-open { overflow: hidden; }
'''
if old_css not in styles:
    raise SystemExit('structure image css not found')
styles = styles.replace(old_css, new_css, 1)
styles_path.write_text(styles, encoding='utf-8')

print('Structure UI fixed')
