from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old = """    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('sw.js')
                .then(() => console.log('Service Worker registered'))
                .catch(error => console.error('Service Worker registration failed:', error));
        });
    }
"""

new = """    if ('serviceWorker' in navigator) {
        let serviceWorkerRefreshing = false;

        navigator.serviceWorker.addEventListener('controllerchange', () => {
            if (serviceWorkerRefreshing) return;
            serviceWorkerRefreshing = true;
            window.location.reload();
        });

        window.addEventListener('load', async () => {
            try {
                const registration = await navigator.serviceWorker.register('sw.js?v=3', { updateViaCache: 'none' });
                await registration.update();
                if (registration.waiting) registration.waiting.postMessage({ type: 'SKIP_WAITING' });
                console.log('Service Worker registered and checked for updates');
            } catch (error) {
                console.error('Service Worker registration failed:', error);
            }
        });
    }
"""

if old not in text:
    raise SystemExit('Service worker registration block not found')

text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
