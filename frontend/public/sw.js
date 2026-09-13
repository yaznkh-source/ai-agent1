// Service Worker for AI Agency OS PWA
const CACHE_NAME = 'ai-agency-os-v8';
const urlsToCache = [
  '/',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached or fetch
        return response || fetch(event.request);
      })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Push notifications (for task updates, client messages)
self.addEventListener('push', event => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || 'AI Agency OS';
  const options = {
    body: data.body || 'New update',
    icon: '/icon-192.png',
    badge: '/icon-192.png',
    data: data
  };
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});
