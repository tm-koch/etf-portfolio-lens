[[ETF Portfolio Lens]]

Adapting a Progressive Web App (PWA) to support multiple languages—such as English and German—involves decoupling your content from the codebase, managing locale-specific assets, and handling offline caching.

### 1. Extract and Centralize UI Strings

- Move all hardcoded user-facing text out of your code and into external resource files, typically organized as JSON structures (e.g., `en.json` and `de.json`).
- Avoid string concatenation or breaking sentences into small UI fragments. German often changes word order or uses compound words, so sentences must be translated as cohesive units.

### 2. Implement an i18n Library

- Integrate a reliable internationalization framework like **i18next** (which works across vanilla JavaScript, React, Vue, and Angular) or framework-specific libraries like **Vue I18n**.
- Leverage detection plugins (e.g., `i18next-browser-languagedetector`) to automatically identify the user's preferred language from their browser settings, falling back gracefully between English and German.

### 3. Handle PWA Manifest and Service Workers

- **Localized Manifests**: Browsers read metadata from your web app manifest. While you can maintain separate manifest files per locale (e.g., `manifest.en.webmanifest` and `manifest.de.webmanifest`) to customize app names on the home screen, you can also dynamically swap the `<link rel="manifest">` tag based on user selection.
- **Offline Caching**: Update your service worker's caching strategy to explicitly cache translation files for both languages. This ensures your PWA remains multilingual and fully functional even when offline.

### 4. Apply Locale-Aware Formatting

- Utilize built-in browser APIs like `Intl.DateTimeFormat` and `Intl.NumberFormat`. This ensures that dates, times, and numbers render in the correct local format (e.g., using periods for decimals in German vs. commas in English).

Are you using a specific front-end framework (like React, Vue, or Angular) for your PWA so we can look at a code implementation?

===

Building a multilingual vanilla JavaScript PWA is straightforward when you use a lightweight localization approach with `data-attributes` and modular language files.

Here is a step-by-step implementation guide tailored for vanilla JavaScript.

### Step 1: Create Translation Files

Create a folder named `i18n` and set up your language dictionary files as JavaScript modules (or JSON files if you prefer using `fetch`).

`**i18n/en.js**`

export const en = {
  title: "Welcome to My App",
  greeting: "Hello, traveler!",
  offlineMessage: "You are currently offline."
};

`**i18n/de.js**`

export const de = {
  title: "Willkommen in meiner App",
  greeting: "Hallo, Reisender!",
  offlineMessage: "Du bist derzeit offline."
};

### Step 2: Update your HTML with Data Attributes

Use a custom `data-i18n` attribute on HTML elements to link them to keys in your translation dictionaries.

`**index.html**`

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title data-i18n="title">Welcome to My App</title>
</head>
<body>
  <!-- Language Selector -->
  <select id="lang-select">
    <option value="en">English</option>
    <option value="de">Deutsch</option>
  </select>

  <h1 data-i18n="greeting">Hello, traveler!</h1>

  <script type="module" src="app.js"></script>
</body>
</html>

### Step 3: Implement the Translation Engine

Write a small translation manager that loads the selected language, updates the DOM, and saves the preference to `localStorage`.

`**app.js**`

import { en } from './i18n/en.js';
import { de } from './i18n/de.js';

const translations = { en, de };

// Get saved language or fallback to browser language (defaulting to 'en')
function getInitialLang() {
  const saved = localStorage.getItem('pwa-lang');
  if (saved && translations[saved]) return saved;
  
  const browserLang = navigator.language.slice(0, 2);
  return translations[browserLang] ? browserLang : 'en';
}

let currentLang = getInitialLang();

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('pwa-lang', lang);
  
  // Update HTML lang attribute for accessibility/screen readers
  document.documentElement.lang = lang;
  
  // Update all elements with data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (translations[lang][key]) {
      el.textContent = translations[lang][key];
    }
  });
}

// Event listener for language switcher dropdown
document.getElementById('lang-select').addEventListener('change', (e) => {
  setLanguage(e.target.value);
});

// Initialize on load
document.getElementById('lang-select').value = currentLang;
setLanguage(currentLang);

### Step 4: Update Your Service Worker for Offline Use

Because your PWA needs to work offline, make sure your service worker explicitly caches your localization modules (`en.js`, `de.js`, etc.) during the `install` phase:

const CACHE_NAME = 'pwa-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/app.js',
  '/i18n/en.js',
  '/i18n/de.js'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

Would you like help handling dynamic text (like inserting a user's name into a translated sentence) using this setup?