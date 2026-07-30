from pathlib import Path
import re, json

root=Path('.')
idx=root/'index.html'
s=idx.read_text(encoding='utf-8')

# Extract CSS
m=re.search(r'<style>(.*?)</style>',s,re.S)
if not m: raise SystemExit('style block not found')
css=m.group(1).strip()+r'''

/* Priority 5: install and backup */
.install-banner{position:fixed;left:12px;right:12px;bottom:92px;max-width:500px;margin:auto;z-index:6500;display:none;align-items:center;gap:12px;padding:13px 14px;border:1px solid var(--accent);border-radius:16px;background:var(--card-bg);box-shadow:0 12px 35px rgba(0,0,0,.2)}
.install-banner.show{display:flex}.install-banner-text{flex:1;min-width:0;font-size:13px;line-height:1.4;color:var(--text-main);font-weight:750}.install-banner button{min-height:42px;border:0;border-radius:11px;padding:0 14px;background:var(--primary);color:#fff;font:inherit;font-weight:850;cursor:pointer}.install-banner .install-close{width:36px;min-width:36px;padding:0;background:transparent;color:var(--text-sub);font-size:20px}
.backup-tools{padding:14px 0 2px;border-top:1px solid var(--border);margin-top:14px}.backup-title{font-size:14px;font-weight:850;margin-bottom:9px}.backup-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px}.backup-btn{min-height:46px;border:1px solid var(--border);border-radius:12px;background:var(--card-bg);color:var(--primary);font:inherit;font-size:12px;font-weight:850;cursor:pointer}.backup-file{display:none}
body.large-text .backup-btn{min-height:52px;font-size:14px}
'''
(root/'styles.css').write_text(css,encoding='utf-8')
s=s[:m.start()]+'<link rel="stylesheet" href="styles.css?v=1.9">'+s[m.end():]

# Select largest inline script (application script)
scripts=list(re.finditer(r'<script>(.*?)</script>',s,re.S))
app_match=max(scripts,key=lambda x: len(x.group(1)))
js=app_match.group(1).strip()

def extract_const_array(text,name):
    marker=f'const {name} = '
    start=text.find(marker)
    if start<0: raise SystemExit(f'{name} not found')
    val_start=start+len(marker)
    while val_start<len(text) and text[val_start].isspace(): val_start+=1
    opener=text[val_start]
    pairs={'[':']','{':'}'}
    if opener not in pairs: raise SystemExit(f'{name} unsupported opener')
    closer=pairs[opener]; depth=0; quote=None; esc=False
    i=val_start
    while i<len(text):
        ch=text[i]
        if quote:
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch==quote: quote=None
        else:
            if ch in "'\"`": quote=ch
            elif ch==opener: depth+=1
            elif ch==closer:
                depth-=1
                if depth==0:
                    end=i+1
                    j=end
                    while j<len(text) and text[j].isspace(): j+=1
                    if j<len(text) and text[j]==';': j+=1
                    return text[val_start:end], start, j
        i+=1
    raise SystemExit(f'{name} end not found')

items={}
for name in ('data','books','i18n'):
    value,a,b=extract_const_array(js,name)
    items[name]=(value,a,b)
for name,(value,a,b) in sorted(items.items(),key=lambda kv:kv[1][1],reverse=True):
    replacement={'data':'let data = [];','books':'let books = [];','i18n':'const i18n = window.AA_I18N;'}[name]
    js=js[:a]+replacement+js[b:]

(root/'groups.json').write_text(items['data'][0],encoding='utf-8')
(root/'books.json').write_text(items['books'][0],encoding='utf-8')
(root/'i18n.js').write_text('window.AA_I18N = '+items['i18n'][0]+';\n',encoding='utf-8')

js=js.replace("    function init() {\n        trackEvent('app_loaded', 'initial_load');", "    async function init() {\n        try {\n            const [groupsResponse, booksResponse] = await Promise.all([fetch('groups.json', {cache:'no-store'}), fetch('books.json', {cache:'no-store'})]);\n            if (!groupsResponse.ok || !booksResponse.ok) throw new Error('data_load_failed');\n            data = await groupsResponse.json();\n            books = await booksResponse.json();\n        } catch (error) {\n            console.error('Не удалось загрузить данные приложения:', error);\n            showAppStatus(curLang === 'kz' ? 'Қолданба деректерін жүктеу мүмкін болмады' : 'Не удалось загрузить данные приложения', 4000);\n        }\n        trackEvent('app_loaded', 'initial_load');")
js=js.replace("        if (!localStorage.getItem('aa_city_onboarding_done_v1')) {\n            localStorage.setItem('aa_city_onboarding_done_v1', '1');\n            setTimeout(openCityOnboarding, 450);\n        }\n","")
extra=r'''

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
        try{const payload=JSON.parse(await file.text()); if(payload?.format!=='aa-kazakhstan-backup'||!payload.data) throw new Error('invalid'); Object.entries(payload.data).forEach(([k,v])=>{if(k.startsWith('aa_')) localStorage.setItem(k,String(v));}); alert(document.documentElement.lang==='kk'?'Деректер қалпына келтірілді. Қолданба қайта жүктеледі.':'Данные восстановлены. Приложение будет перезапущено.'); location.reload();}catch(e){alert(document.documentElement.lang==='kk'?'Файлды қалпына келтіру мүмкін болмады.':'Не удалось восстановить данные из файла.');}
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
    async function forceUpdate(){
        if(!('serviceWorker' in navigator))return;
        try{
            const registration=await navigator.serviceWorker.register('sw.js?v=10',{updateViaCache:'none'});
            await registration.update();
            if(registration.waiting) registration.waiting.postMessage({type:'SKIP_WAITING'});
            const response=await fetch('version.json?ts='+Date.now(),{cache:'no-store'});
            if(response.ok){const info=await response.json();const previous=localStorage.getItem('aa_app_build');if(previous&&previous!==info.build&&!sessionStorage.getItem('aa_update_reloaded')){localStorage.setItem('aa_app_build',info.build);sessionStorage.setItem('aa_update_reloaded','1');location.reload();return;}localStorage.setItem('aa_app_build',info.build);}
        }catch(e){console.warn('Update check failed',e);}
    }
    window.addEventListener('load',forceUpdate);
})();
'''
js += extra
(root/'app.js').write_text(js+'\n',encoding='utf-8')
s=s[:app_match.start()]+'<script src="i18n.js?v=1.9"></script>\n<script src="app.js?v=1.9" defer></script>'+s[app_match.end():]
needle='<div class="settings-version">'
backup='''<div class="backup-tools"><div class="backup-title" id="backup-title">Резервная копия</div><div class="backup-actions"><button class="backup-btn" id="export-data" type="button">Экспортировать мои данные</button><button class="backup-btn" id="restore-data" type="button">Восстановить данные</button></div><input class="backup-file" id="restore-file" type="file" accept="application/json"></div>\n                '''
if needle not in s: raise SystemExit('settings marker missing')
s=s.replace(needle,backup+needle,1)
nav='<nav class="bottom-nav"'
banner='''<div class="install-banner" id="install-banner" role="status"><div class="install-banner-text">Установите приложение АА Казахстана на телефон</div><button id="install-app" type="button">Установить</button><button class="install-close" id="install-close" type="button" aria-label="Закрыть">×</button></div>\n'''
s=s.replace(nav,banner+nav,1)
s=s.replace('id="settings-version-value">1.8<','id="settings-version-value">1.9<')
idx.write_text(s,encoding='utf-8')
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
manifest.update({'id':'./','start_url':'./?source=pwa','scope':'./','display':'standalone','display_override':['window-controls-overlay','standalone','minimal-ui'],'orientation':'portrait-primary','categories':['health','lifestyle'],'lang':'ru'})
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(root/'version.json').write_text(json.dumps({'version':'1.9','build':'2026-07-30-priority5'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sw=r'''const CACHE_NAME = 'aa-kaz-v10';
const CORE_ASSETS = ['./','index.html','styles.css','app.js','i18n.js','groups.json','books.json','news.json','daily_reflections_full.json','manifest.json','version.json'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(CORE_ASSETS)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE_NAME).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('message',event=>{if(event.data&&event.data.type==='SKIP_WAITING')self.skipWaiting();});
self.addEventListener('fetch',event=>{
 if(event.request.method!=='GET')return;
 const url=new URL(event.request.url);
 if(event.request.mode==='navigate'){
   event.respondWith(fetch(event.request,{cache:'no-store'}).then(r=>{const c=r.clone();caches.open(CACHE_NAME).then(cache=>cache.put('index.html',c));return r;}).catch(()=>caches.match('index.html')));return;
 }
 if(url.origin===location.origin){
   event.respondWith(fetch(event.request,{cache:'no-store'}).then(r=>{if(r.ok){const c=r.clone();caches.open(CACHE_NAME).then(cache=>cache.put(event.request,c));}return r;}).catch(()=>caches.match(event.request)));return;
 }
 event.respondWith(caches.match(event.request).then(c=>c||fetch(event.request)));
});
'''
(root/'sw.js').write_text(sw,encoding='utf-8')
validator=r'''import json,re,sys
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
'''
(root/'scripts/validate-data.py').write_text(validator,encoding='utf-8')
# workflow trigger refresh
