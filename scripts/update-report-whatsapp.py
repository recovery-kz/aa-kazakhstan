from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = '77072080553'
new = '77051871335'
if old not in s:
    raise SystemExit('Old WhatsApp number not found')
s = s.replace(old, new)
p.write_text(s, encoding='utf-8')

sw = Path('sw.js')
t = sw.read_text(encoding='utf-8')
t = t.replace("aa-kaz-v8", "aa-kaz-v9")
sw.write_text(t, encoding='utf-8')
