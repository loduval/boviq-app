// BOVIQ Service Worker — stratégie Network-First
// Toujours tente le réseau ; cache uniquement si offline
const CACHE = 'boviq-v20260321';
const ASSETS = [
  './boviq-v6-latest.html',
  './boviq-milklic.html',
  './boviq-cours-marche.html',
  './index.html'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Network-first : réseau en priorité, cache en fallback offline uniquement
self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request)
      .then(response => {
        // Mettre à jour le cache avec la nouvelle version
        const clone = response.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return response;
      })
      .catch(() => caches.match(e.request)) // Offline → sert le cache
  );
});
