from pathlib import Path

app = Path('app.js')
text = app.read_text(encoding='utf-8')

old_controller = """        let serviceWorkerRefreshing = false;

        navigator.serviceWorker.addEventListener('controllerchange', () => {
            if (serviceWorkerRefreshing) return;
            serviceWorkerRefreshing = true;
            window.location.reload();
        });
"""
new_controller = """        navigator.serviceWorker.addEventListener('controllerchange', () => {
            console.log('Service Worker updated without automatic reload');
        });
"""
if old_controller not in text:
    raise SystemExit('controllerchange reload block not found')
text = text.replace(old_controller, new_controller, 1)

text = text.replace("navigator.serviceWorker.register('sw.js?v=8'", "navigator.serviceWorker.register('sw.js?v=12'", 1)

old_force = """    async function forceUpdate(){
        if(!('serviceWorker' in navigator))return;
        try{
            const registration=await navigator.serviceWorker.register('sw.js?v=10',{updateViaCache:'none'});
            await registration.update();
            if(registration.waiting) registration.waiting.postMessage({type:'SKIP_WAITING'});
            const response=await fetch('version.json?ts='+Date.now(),{cache:'no-store'});
            if(response.ok){const info=await response.json();const previous=localStorage.getItem('aa_app_build');if(previous&&previous!==info.build&&!sessionStorage.getItem('aa_update_reloaded')){localStorage.setItem('aa_app_build',info.build);sessionStorage.setItem('aa_update_reloaded','1');location.reload();return;}localStorage.setItem('aa_app_build',info.build);}
        }catch(e){console.warn('Update check failed',e);}
    }
"""
new_force = """    async function forceUpdate(){
        if(!('serviceWorker' in navigator))return;
        try{
            const registration=await navigator.serviceWorker.register('sw.js?v=12',{updateViaCache:'none'});
            await registration.update();
            if(registration.waiting) registration.waiting.postMessage({type:'SKIP_WAITING'});
            const response=await fetch('version.json?ts='+Date.now(),{cache:'no-store'});
            if(response.ok){const info=await response.json();localStorage.setItem('aa_app_build',info.build);}
        }catch(e){console.warn('Update check failed',e);}
    }
"""
if old_force not in text:
    raise SystemExit('forceUpdate reload block not found')
text = text.replace(old_force, new_force, 1)

if 'location.reload();' in text[text.find("async function forceUpdate"):]:
    raise SystemExit('automatic reload remains in update code')

app.write_text(text, encoding='utf-8')

sw = Path('sw.js')
sw_text = sw.read_text(encoding='utf-8').replace("const CACHE_NAME = 'aa-kaz-v11';", "const CACHE_NAME = 'aa-kaz-v12';", 1)
if "aa-kaz-v12" not in sw_text:
    raise SystemExit('cache version was not updated')
sw.write_text(sw_text, encoding='utf-8')

version = Path('version.json')
version.write_text('{\n  "version": "1.9.2",\n  "build": "2026-07-30-update-loop-hotfix"\n}\n', encoding='utf-8')
