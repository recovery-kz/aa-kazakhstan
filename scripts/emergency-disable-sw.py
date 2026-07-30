from pathlib import Path
import re

root = Path('.')
app_path = root / 'app.js'
index_path = root / 'index.html'
sw_path = root / 'sw.js'

app = app_path.read_text(encoding='utf-8')

# Remove the primary service worker registration block.
app = re.sub(
    r"\n\s*if \('serviceWorker' in navigator\) \{.*?\n\s*\}\n\}\)\(\);",
    "\n})();",
    app,
    count=1,
    flags=re.S,
)

# Remove the background forceUpdate function and its load listener.
app = re.sub(
    r"\n\s*async function forceUpdate\(\)\{.*?window\.addEventListener\('load',forceUpdate\);",
    "",
    app,
    count=1,
    flags=re.S,
)

if "window.location.reload();" in app:
    # Keep the explicit reload used only after manual data restore.
    occurrences = app.count("window.location.reload();")
    if occurrences > 1:
        raise SystemExit(f'Unexpected automatic reloads remain: {occurrences}')

app_path.write_text(app, encoding='utf-8')

index = index_path.read_text(encoding='utf-8')
index = re.sub(r'app\.js\?v=[^"\']+', 'app.js?v=2.0.1', index)
index = re.sub(r'i18n\.js\?v=[^"\']+', 'i18n.js?v=2.0.1', index)
index = re.sub(r'styles\.css\?v=[^"\']+', 'styles.css?v=2.0.1', index)

kill_script = """<script>
    // Emergency recovery from a stale service-worker reload loop.
    window.__AA_DISABLE_SERVICE_WORKER__ = true;
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations().then(registrations =>
            Promise.all(registrations.map(registration => registration.unregister()))
        ).catch(() => {});
    }
    if ('caches' in window) {
        caches.keys().then(keys => Promise.all(keys.map(key => caches.delete(key)))).catch(() => {});
    }
</script>
"""
if 'window.__AA_DISABLE_SERVICE_WORKER__' not in index:
    index = index.replace('</head>', kill_script + '</head>')
index_path.write_text(index, encoding='utf-8')

# Replace the service worker with a self-destructing kill switch for users still controlled by an old worker.
sw_path.write_text("""const CACHE_NAME = 'aa-kaz-disabled-v13';
self.addEventListener('install', event => event.waitUntil(self.skipWaiting()));
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.map(key => caches.delete(key)));
    await self.registration.unregister();
    const clientsList = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    clientsList.forEach(client => client.postMessage({ type: 'AA_SW_DISABLED' }));
  })());
});
self.addEventListener('fetch', () => {});
""", encoding='utf-8')

print('Emergency service worker shutdown applied')
