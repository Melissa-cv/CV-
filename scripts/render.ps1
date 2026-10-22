# Genera los PDF del CV: powershell -File scripts/render.ps1 [-Langs es,en] [-Versions corta,larga]
# Cada PDF se imprime con un perfil de Edge aislado (si no, Edge falla con "Multiple targets").
param([string[]]$Langs = @('es', 'en'), [string[]]$Versions = @('corta', 'larga'))
$root = Split-Path -Parent $PSScriptRoot
$tmp = Join-Path $env:TEMP 'cv-render'
New-Item -ItemType Directory -Force $tmp | Out-Null
$edge = @('C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', 'C:\Program Files\Microsoft\Edge\Application\msedge.exe') |
    Where-Object { Test-Path $_ } | Select-Object -First 1
foreach ($lang in $Langs) { foreach ($v in $Versions) {
    $html = "$tmp\cv-$v-$lang.html"
    $pdf = "$root\output\CV-Melissa-Cadavid-$v-$lang.pdf"
    python -I "$root\scripts\build_cv.py" $lang $v $html
    if (Test-Path $pdf) { Remove-Item $pdf }
    $u = 'file:///' + $html.Replace('\', '/')
    $a = "--headless --disable-gpu --no-pdf-header-footer --user-data-dir=$tmp\prof-$v-$lang --print-to-pdf=$pdf $u"
    Start-Process -FilePath $edge -ArgumentList $a -Wait -NoNewWindow -RedirectStandardError "$tmp\edge.log" | Out-Null
    Get-Process msedge -ErrorAction SilentlyContinue | Stop-Process -Force
    if (Test-Path $pdf) {
        $txt = [Text.Encoding]::ASCII.GetString([IO.File]::ReadAllBytes($pdf))
        "$v-$lang : " + ([regex]::Matches($txt, '/Type\s*/Page[^s]')).Count + ' página(s)'
    } else { "$v-$lang : NO generado" }
} }
