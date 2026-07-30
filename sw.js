const CACHE_NAME = 'aa-kaz-v12';
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
