from pathlib import Path

app = Path('app.js')
text = app.read_text(encoding='utf-8')
old = "        if (!localStorage.getItem('aa_first_run_done_v1')) setTimeout(openFirstRun, 450);"
new = "        localStorage.setItem('aa_first_run_done_v1', '1');\n        const firstRunModal = document.getElementById('first-run');\n        if (firstRunModal) {\n            firstRunModal.classList.remove('open');\n            firstRunModal.setAttribute('aria-hidden', 'true');\n        }\n        document.body.classList.remove('first-run-open');"
if old not in text:
    raise SystemExit('first-run startup call not found')
app.write_text(text.replace(old, new, 1), encoding='utf-8')

styles = Path('styles.css')
css = styles.read_text(encoding='utf-8')
marker = "\n/* Emergency hotfix: disable unstable first-run overlay */\n#first-run { display: none !important; }\nbody.first-run-open { overflow: auto !important; }\n"
if marker.strip() not in css:
    styles.write_text(css + marker, encoding='utf-8')

sw = Path('sw.js')
sw_text = sw.read_text(encoding='utf-8').replace("aa-kaz-v10", "aa-kaz-v11")
sw.write_text(sw_text, encoding='utf-8')

version = Path('version.json')
version.write_text('{\n  "version": "1.9.1",\n  "build": "2026-07-30-first-run-hotfix"\n}\n', encoding='utf-8')
