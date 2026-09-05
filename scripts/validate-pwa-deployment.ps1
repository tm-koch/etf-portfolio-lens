param(
  [string]$BaseUrl = 'https://tm-koch.github.io/etf-portfolio-lens/'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

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
Test-PwaAsset -Path 'sw.js' -ExpectedContentType 'application/javascript' | Out-Null
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

Write-Host 'PWA deployment validation passed.'
