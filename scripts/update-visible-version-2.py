from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = '<strong id="settings-version-value">1.9</strong>'
new = '<strong id="settings-version-value">2.0</strong>'
if old not in text:
    raise SystemExit('Visible version 1.9 not found')
path.write_text(text.replace(old, new, 1), encoding='utf-8')
