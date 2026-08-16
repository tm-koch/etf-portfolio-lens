param(
  [string]$Remote = 'origin',
  [string]$Branch = 'gh-pages',
  [string]$CommitMessage = 'Publish GitHub Pages site',
  [string]$RepositoryUrl = 'https://github.com/tm-koch/etf-portfolio-lens',
  [switch]$NoPush
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Invoke-Git {
  param(
    [Parameter(Mandatory = $true)]
    [string[]]$Args,
    [switch]$AllowFailure
  )

  $output = & git @Args 2>&1
  if (-not $AllowFailure -and $LASTEXITCODE -ne 0) {
    throw "git $($Args -join ' ') failed:`n$output"
  }
  return $output
}

$repoRoot = (Invoke-Git -Args @('rev-parse', '--show-toplevel')).Trim()
Set-Location $repoRoot
$sourceCommit = (Invoke-Git -Args @('rev-parse', 'HEAD')).Trim()
$sourceCommitTimestamp = (Invoke-Git -Args @('show', '-s', '--format=%cI', 'HEAD')).Trim()

if (-not (git remote).Contains($Remote)) {
  throw "Remote '$Remote' is not configured. Add the GitHub remote before publishing."
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) 'etf-lens-gh-pages-worktree'
if (Test-Path $tempRoot) {
  Remove-Item -Recurse -Force $tempRoot
}

Invoke-Git -Args @('worktree', 'add', '--detach', $tempRoot, 'HEAD') | Out-Null

try {
  Set-Location $tempRoot

  Get-ChildItem -Force |
    Where-Object { $_.Name -ne '.git' } |
    Remove-Item -Recurse -Force

  New-Item -ItemType File -Force -Path (Join-Path $tempRoot '.nojekyll') | Out-Null

  New-Item -ItemType Directory -Force -Path (Join-Path $tempRoot 'data') | Out-Null

  $webFiles = @(
    'index.html',
    'styles.css',
    'app.js',
    'charts.js',
    'data.js',
    'package.json'
  )

  foreach ($file in $webFiles) {
    Copy-Item -Force (Join-Path $repoRoot (Join-Path 'web' $file)) (Join-Path $tempRoot $file)
  }

  Copy-Item -Force (Join-Path $repoRoot 'README.md') (Join-Path $tempRoot 'README.md')

  Copy-Item -Force (Join-Path $repoRoot 'web\data\catalog.json') (Join-Path $tempRoot 'data\catalog.json')
  Copy-Item -Recurse -Force (Join-Path $repoRoot 'data\raw') (Join-Path $tempRoot 'data')

  $catalog = Get-Content (Join-Path $tempRoot 'data\catalog.json') -Raw | ConvertFrom-Json
  $buildInfo = [ordered]@{
    schemaVersion = 1
    repositoryUrl = $RepositoryUrl
    source = [ordered]@{
      commit = $sourceCommit
      commitTimestamp = $sourceCommitTimestamp
    }
    publishedAt = (Get-Date).ToUniversalTime().ToString('o')
    data = [ordered]@{
      timestamp = $catalog.generatedAt
    }
    details = [ordered]@{}
  }
  $buildInfo | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $tempRoot 'build-info.json') -Encoding utf8

  $changes = Invoke-Git -Args @('status', '--porcelain')
  if (-not $changes) {
    Write-Host 'No publish changes detected.'
  } else {
    Invoke-Git -Args @('add', '-A') | Out-Null
    Invoke-Git -Args @('commit', '-m', $CommitMessage) | Out-Null
    if (-not $NoPush) {
      Invoke-Git -Args @('push', '--force-with-lease', $Remote, "HEAD:$Branch") | Out-Null
    }
  }
}
finally {
  Set-Location $repoRoot
  if (Test-Path $tempRoot) {
    Invoke-Git -Args @('worktree', 'remove', '--force', $tempRoot) -AllowFailure | Out-Null
    if (Test-Path $tempRoot) {
      Remove-Item -Recurse -Force $tempRoot
    }
  }
}
