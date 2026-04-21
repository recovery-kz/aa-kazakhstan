const CACHE_NAME = 'aa-kazakhstan-cache-v3';
const APP_SHELL = [
  './',
  './index.html',
  './manifest.json',
  'https://aaorg.kz/wp-content/uploads/2020/02/%D0%BB%D0%BE%D0%B3%D0%BE.png',
  'https://cdn.jsdelivr.net/gh/recovery-kz/aa-kazakhstan@main/forum26.jpeg',
  'https://cdn.jsdelivr.net/gh/recovery-kz/aa-kazakhstan@main/ChatGPT%20Image%2020%20%D0%B0%D0%BF%D1%80.%202026%20%D0%B3.,%2009_15_29.png',
  'https://cdn.jsdelivr.net/gh/recovery-kz/aa-kazakhstan@main/daily_reflections_short.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)).catch(() => Promise.resolve())
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const request = event.request;

  if (request.method !== 'GET') return;
  if (request.url.includes('googletagmanager.com') || request.url.includes('google-analytics.com')) return;

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then(response => {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put('./index.html', responseClone));
          return response;
        })
        .catch(() => caches.match('./index.html'))
    );
    return;
  }

  event.respondWith(
    caches.match(request).then(cachedResponse => {
      const networkFetch = fetch(request)
        .then(response => {
          if (!response || response.status !== 200) return response;
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, responseClone));
          return response;
        })
        .catch(() => cachedResponse);

      return cachedResponse || networkFetch;
    })
  );
});