// BOVIQ — service worker de désinstallation (14/10/2026)
//
// Remplace le service worker figé au 21/03/2026, qui mettait en cache
// l'application entière — y compris les réponses de l'API GitHub — et
// pouvait resservir indéfiniment une version périmée.
//
// Celui-ci ne met rien en cache : il purge ce que l'ancien avait gardé,
// se désinscrit, et recharge les pages ouvertes pour qu'elles repartent
// du réseau. Il ne touche pas au localStorage, qui est un stockage
// distinct et peut contenir des données jamais envoyées au serveur.

self.addEventListener('install', function(e){
  self.skipWaiting();
});

self.addEventListener('activate', function(e){
  e.waitUntil((async function(){
    try {
      const noms = await caches.keys();
      await Promise.all(noms.map(function(n){ return caches.delete(n); }));
    } catch (err) { /* rien à purger */ }

    try { await self.registration.unregister(); } catch (err) {}

    try {
      const clients = await self.clients.matchAll({type:'window'});
      clients.forEach(function(c){ c.navigate(c.url); });
    } catch (err) {}
  })());
});

// Aucune interception : tout passe directement au réseau.
