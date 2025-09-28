/**
 * Service Worker for CodeSampler Crowd Controller PWA
 * Offline cache for /crowd/* pages and assets
 */

const CACHE_NAME = 'codesampler-crowd-v1';
const CACHE_URLS = [
  '/crowd/',
  '/crowd/index.html',
  '/manifest.webmanifest',
  '/icons/icon-192.png',
  '/icons/icon-512.png'
];

// Install event - cache resources
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching app shell');
        return cache.addAll(CACHE_URLS);
      })
      .then(() => {
        console.log('[SW] Skip waiting');
        return self.skipWaiting();
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('[SW] Claiming clients');
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;
  
  // Skip non-crowd requests
  if (!event.request.url.includes('/crowd/')) return;
  
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      })
      .catch(() => {
        // Fallback for offline
        if (event.request.destination === 'document') {
          return caches.match('/crowd/index.html');
        }
      })
  );
});

// Background sync for crowd messages (optional)
self.addEventListener('sync', (event) => {
  if (event.tag === 'crowd-sync') {
    console.log('[SW] Background sync for crowd messages');
    // Could queue crowd messages for when connection is restored
  }
});

console.log('[SW] Service Worker loaded');
