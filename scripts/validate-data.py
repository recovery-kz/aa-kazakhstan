import json,re,sys
from pathlib import Path
errors=[]
groups=json.loads(Path('groups.json').read_text(encoding='utf-8'))
books=json.loads(Path('books.json').read_text(encoding='utf-8'))
if not isinstance(groups,list) or not groups: errors.append('groups empty')
seen=set()
for i,g in enumerate(groups):
 name=str(g.get('n','')).strip(); city=str(g.get('c','')).strip()
 if not name: errors.append(f'group {i}: empty name')
 key=(city.lower(),name.lower())
 if key in seen: errors.append(f'duplicate group: {city}/{name}')
 seen.add(key)
 for p in g.get('p',[]) or []:
  digits=re.sub(r'\D','',str(p))
  if len(digits)<10 or len(digits)>12: errors.append(f'bad phone {name}: {p}')
 for slot in g.get('sc',[]) or []:
  if not (0<=slot.get('d',-1)<=6): errors.append(f'bad weekday {name}')
  for k in ('s','e'):
   v=slot.get(k,-1); hh=v//100; mm=v%100
   if not (0<=hh<=23 and 0<=mm<=59): errors.append(f'bad time {name}: {v}')
 for field in ('a','z'):
  v=str(g.get(field,'') or '')
  if v.startswith('http') and not re.match(r'^https?://',v): errors.append(f'bad url {name}: {v}')
if not isinstance(books,list): errors.append('books invalid')
text=Path('app.js').read_text(encoding='utf-8')+Path('i18n.js').read_text(encoding='utf-8')
for bad in ('>undefined<','>null<','>NaN<'):
 if bad in text: errors.append('literal '+bad)
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'OK: {len(groups)} groups, {len(books)} books')
