const CACHE_VERSION = '20260901-1';
const SHELL_CACHE = `etf-lens-shell-${CACHE_VERSION}`;
const RUNTIME_CACHE = `etf-lens-runtime-${CACHE_VERSION}`;
const MAX_RUNTIME_ENTRIES = 24;
const SHELL_PATHS = [
  'index.html',
  'styles.css',
  'app.js',
  'portfolio-import.js',
  'charts.js',
  'data.js',
  'manifest.json',
  'icons/launchericon-192x192.png',
  'icons/launchericon-512x512.png',
  'vendor/chart.umd.min.js',
  'vendor/lucide.js',
  'vendor/pdf.min.js',
  'vendor/pdf.worker.min.js',
];

const baseUrl = new URL('./', self.registration.scope);

function shellUrl(path) {
  return new URL(path, baseUrl).href;
}

function isSameOrigin(request) {
  return new URL(request.url).origin === baseUrl.origin;
}

function isRuntimeDataRequest(request) {
  const url = new URL(request.url);
  return isSameOrigin(request) && url.pathname.endsWith('.json') && url.pathname.includes('/data/');
}

function isNavigationRequest(request) {
  return request.mode === 'navigate';
}

async function trimRuntimeCache() {
  const cache = await caches.open(RUNTIME_CACHE);
  const requests = await cache.keys();
  if (requests.length <= MAX_RUNTIME_ENTRIES) return;
  await Promise.all(requests.slice(0, requests.length - MAX_RUNTIME_ENTRIES).map((request) => cache.delete(request)));
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE)
      .then((cache) => cache.addAll(SHELL_PATHS.map(shellUrl)))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys
          .filter((key) => key.startsWith('etf-lens-') && ![SHELL_CACHE, RUNTIME_CACHE].includes(key))
          .map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET' || !isSameOrigin(request)) return;

  if (isRuntimeDataRequest(request)) {
    event.respondWith((async () => {
      const cache = await caches.open(RUNTIME_CACHE);
      try {
        const response = await fetch(request);
        if (response.ok) {
          await cache.put(request, response.clone());
          await trimRuntimeCache();
        }
        return response;
      } catch {
        const cached = await cache.match(request, { ignoreSearch: true });
        if (cached) return cached;
        throw new Error(`Offline data unavailable: ${request.url}`);
      }
    })());
    return;
  }

  if (isNavigationRequest(request)) {
    event.respondWith((async () => {
      try {
        return await fetch(request);
      } catch {
        const cache = await caches.open(SHELL_CACHE);
        return cache.match(shellUrl('index.html'), { ignoreSearch: true });
      }
    })());
    return;
  }

  event.respondWith((async () => {
    const cache = await caches.open(SHELL_CACHE);
    const cached = await cache.match(request, { ignoreSearch: true });
    if (cached) return cached;
    return fetch(request);
  })());
});
