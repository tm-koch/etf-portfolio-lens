param(
  [string]$BaseUrl = 'https://tm-koch.github.io/etf-portfolio-lens/'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repositoryRoot = (Get-Item $PSScriptRoot).Parent.FullName
$cacheGenerationScript = Join-Path $repositoryRoot 'scripts\pwa-cache-generation.ps1'
if (-not (Test-Path $cacheGenerationScript -PathType Leaf)) {
  throw "PWA cache-generation helper is missing: $cacheGenerationScript"
}
. $cacheGenerationScript

$normalizedBaseUrl = if ($BaseUrl.EndsWith('/')) { $BaseUrl } else { "$BaseUrl/" }
if (-not $normalizedBaseUrl.StartsWith('https://')) {
  throw "PWA deployment validation requires an HTTPS BaseUrl: $normalizedBaseUrl"
}

function Test-PwaAsset {
  param(
    [Parameter(Mandatory = $true)]
    [AllowEmptyString()]
    [string]$Path,
    [Parameter(Mandatory = $true)]
    [string]$ExpectedContentType
  )

  $url = [Uri]::new([Uri]$normalizedBaseUrl, $Path).AbsoluteUri
  $response = Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing
  if ($response.StatusCode -ne 200) {
    throw "$url returned HTTP $($response.StatusCode)"
  }
  if (-not $response.Headers['Content-Type'].StartsWith($ExpectedContentType)) {
    throw "$url returned Content-Type '$($response.Headers['Content-Type'])', expected '$ExpectedContentType'"
  }
  Write-Host "OK $url [$($response.Headers['Content-Type'])]"
  return $response
}

$index = Test-PwaAsset -Path '' -ExpectedContentType 'text/html'
$manifestResponse = Test-PwaAsset -Path 'manifest.json' -ExpectedContentType 'application/json'
$serviceWorkerResponse = Test-PwaAsset -Path 'sw.js' -ExpectedContentType 'application/javascript'
Test-PwaAsset -Path 'icons/launchericon-192x192.png' -ExpectedContentType 'image/png' | Out-Null
Test-PwaAsset -Path 'icons/launchericon-512x512.png' -ExpectedContentType 'image/png' | Out-Null

$manifest = $manifestResponse.Content | ConvertFrom-Json
$manifestUri = [Uri]::new([Uri]$normalizedBaseUrl, 'manifest.json')
if (-not $manifest.id) {
  throw 'Published manifest does not define a stable id.'
}
$manifestId = [Uri]::new($manifestUri, $manifest.id).AbsoluteUri
if (-not $manifestId.StartsWith($normalizedBaseUrl)) {
  throw "Manifest id '$($manifest.id)' resolves outside the published application: $manifestId"
}
if ($manifest.name -ne 'ETF Portfolio Lens' -or $manifest.short_name -ne 'ETF Portfolio Lens') {
  throw 'Manifest application name is not ETF Portfolio Lens.'
}
if ($manifest.display -ne 'standalone') {
  throw 'Manifest display mode is not standalone.'
}

$manifestLink = [regex]::Match($index.Content, '<link\s+rel="manifest"\s+href="([^"]+)"').Groups[1].Value
if (-not $manifestLink) {
  throw 'Published index.html does not contain a manifest link.'
}
$resolvedManifestLink = [Uri]::new([Uri]$normalizedBaseUrl, $manifestLink).AbsoluteUri
if ($resolvedManifestLink -ne $manifestUri.AbsoluteUri) {
  throw "Manifest link resolves to $resolvedManifestLink instead of $manifestUri"
}

$validationRoot = Join-Path ([System.IO.Path]::GetTempPath()) "etf-lens-pwa-validation-$PID"
New-Item -ItemType Directory -Force -Path $validationRoot | Out-Null
try {
  foreach ($relativePath in Get-PwaCacheSensitivePaths) {
    $url = [Uri]::new([Uri]$normalizedBaseUrl, $relativePath).AbsoluteUri
    $response = Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing
    if ($response.StatusCode -ne 200) {
      throw "$url returned HTTP $($response.StatusCode)"
    }
    $localPath = Join-Path $validationRoot $relativePath
    New-Item -ItemType Directory -Force -Path (Split-Path $localPath -Parent) | Out-Null
    [System.IO.File]::WriteAllBytes($localPath, $response.RawContentStream.ToArray())
  }

  $expectedGeneration = Get-PwaCacheGeneration -Root $validationRoot
  $actualGeneration = Get-PwaServiceWorkerGeneration -ServiceWorkerContent $serviceWorkerResponse.Content
  if ($actualGeneration -ne $expectedGeneration) {
    throw "Published service worker cache generation '$actualGeneration' does not match the published shell generation '$expectedGeneration'."
  }
  Write-Host "OK published shell cache generation [$actualGeneration]"
}
finally {
  if (Test-Path $validationRoot) {
    Remove-Item -Recurse -Force $validationRoot
  }
}

Write-Host 'PWA deployment validation passed.'
