$PwaCacheSensitivePaths = @(
  'index.html',
  'styles.css',
  'fonts.css',
  'app.js',
  'report-data.js',
  'export-view.js',
  'report-renderer.js',
  'pdf-export.js',
  'localization.js',
  'taxonomy.js',
  'formatting.js',
  'redundancy.js',
  'explore-settings.js',
  'pairwise-overlap.js',
  'diversification.js',
  'locales/en-CH.json',
  'locales/de-CH.json',
  'locales/pl-PL.json',
  'portfolio-import.js',
  'charts.js',
  'data.js',
  'manifest.json',
  'icons/launchericon-192x192.png',
  'icons/launchericon-512x512.png',
  'fonts/space-grotesk-latin-400-normal.woff2',
  'fonts/space-grotesk-latin-500-normal.woff2',
  'fonts/space-grotesk-latin-700-normal.woff2',
  'fonts/space-grotesk-latin-ext-400-normal.woff2',
  'fonts/space-grotesk-latin-ext-500-normal.woff2',
  'fonts/space-grotesk-latin-ext-700-normal.woff2',
  'vendor/chart.umd.min.js',
  'vendor/i18next.min.js',
  'vendor/lucide.js',
  'vendor/pdf.min.js',
  'vendor/pdf.worker.min.js',
  'vendor/html2pdf.bundle.min.js'
)

function Get-PwaCacheSensitivePaths {
  return $PwaCacheSensitivePaths
}

function Get-PwaCacheGeneration {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Root
  )

  $hashInputs = foreach ($relativePath in $PwaCacheSensitivePaths) {
    $path = Join-Path $Root $relativePath
    if (-not (Test-Path $path -PathType Leaf)) {
      throw "Cache-sensitive PWA asset is missing: $path"
    }

    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLowerInvariant()
    "${relativePath}:$hash"
  }

  $payload = [System.Text.Encoding]::UTF8.GetBytes(($hashInputs -join "`n"))
  $digest = [System.Security.Cryptography.SHA256]::Create().ComputeHash($payload)
  return ([System.BitConverter]::ToString($digest) -replace '-', '').ToLowerInvariant().Substring(0, 16)
}

function Set-PwaServiceWorkerGeneration {
  param(
    [Parameter(Mandatory = $true)]
    [string]$ServiceWorkerPath,
    [Parameter(Mandatory = $true)]
    [string]$Generation
  )

  $content = Get-Content -Raw -LiteralPath $ServiceWorkerPath
  $updated = $content.Replace('__PWA_CACHE_GENERATION__', $Generation)
  if ($updated -eq $content) {
    throw "Service worker does not contain the __PWA_CACHE_GENERATION__ token: $ServiceWorkerPath"
  }
  Set-Content -LiteralPath $ServiceWorkerPath -Value $updated -Encoding utf8
}

function Get-PwaServiceWorkerGeneration {
  param(
    [Parameter(Mandatory = $true)]
    [string]$ServiceWorkerContent
  )

  $match = [regex]::Match($ServiceWorkerContent, "const CACHE_VERSION = '([^']+)';")
  if (-not $match.Success) {
    throw 'Published service worker does not define CACHE_VERSION.'
  }
  return $match.Groups[1].Value
}
