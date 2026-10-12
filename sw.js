// BOVIQ — Service Worker
// Strategie : reseau d'abord, cache de secours uniquement hors ligne.
// Le numero de version doit changer a chaque mise en ligne : il purge
// automatiquement les anciens caches (c'etait la cause des "vide ton cache").
const VERSION = '2026-10-12-01';
const CACHE   = 'boviq-' + VERSION;

const ASSETS = [
  './index.html',
  './boviq-v6-latest.html',
  './boviq-milklic.html',
  './boviq-cours-marche.html'
];

// Jamais mis en cache : donnees vivantes et appels authentifies.
// Servir une version perimee de ces reponses pourrait conduire a
// reecrire d'anciennes donnees par-dessus les donnees reelles.
const JAMAIS_EN_CACHE = [
  'api.github.com',
  'raw.githubusercontent.com'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(ASSETS))
      .catch(() => null)
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(cles => Promise.all(cles.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function cacheInterdit(req) {
  if (req.method !== 'GET') return true;
  let u;
  try { u = new URL(req.url); } catch (e) { return true; }
  if (u.protocol !== 'http:' && u.protocol !== 'https:') return true;
  return JAMAIS_EN_CACHE.some(h => u.hostname === h || u.hostname.endsWith('.' + h));
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (cacheInterdit(req)) return;   // donnees vivantes : jamais interceptees
  e.respondWith(
    fetch(req)
      .then(rep => {
        if (rep && rep.ok && rep.type === 'basic') {
          const copie = rep.clone();
          caches.open(CACHE).then(c => c.put(req, copie)).catch(() => {});
        }
        return rep;
      })
      .catch(() => caches.match(req).then(r => r || Response.error()))
  );
});

self.addEventListener('message', e => {
  if (e.data === 'MAJ_IMMEDIATE') self.skipWaiting();
});
