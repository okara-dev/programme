# PowerShell-Profil: Microsoft.PowerShell_profile.ps1
# A-Z Shell Toolbox

Remove-Item Alias:h -ErrorAction SilentlyContinue -Force
Remove-Item Alias:r -ErrorAction SilentlyContinue -Force

function hilfe {
    Write-Host "[HELP] Verfuegbare Funktionen:" -ForegroundColor Cyan
    Write-Host "a - Akkustatus anzeigen" -ForegroundColor Green
    Write-Host "b - Browser oeffnen" -ForegroundColor Green
    Write-Host "c - Taschenrechner" -ForegroundColor Green
    Write-Host "d - Datum anzeigen" -ForegroundColor Green
    Write-Host "e - Schere-Stein-Papier spielen" -ForegroundColor Green
    Write-Host "f - Papierkorb leeren" -ForegroundColor Green
    Write-Host "g - GitHub oeffnen" -ForegroundColor Green
    Write-Host "h - Wikipedia-Artikel anzeigen" -ForegroundColor Green
    Write-Host "i - Bildschirm-Reiniger" -ForegroundColor Green
    Write-Host "j - Regenbogen-Text" -ForegroundColor Green
    Write-Host "k - Muenzwurf" -ForegroundColor Green
    Write-Host "l - Ordner-Groesse anzeigen" -ForegroundColor Green
    Write-Host "m - Password Generator" -ForegroundColor Green
    Write-Host "n - Notenpunkte berechnen" -ForegroundColor Green
    Write-Host "o - Zu Projekt-Ordner wechseln" -ForegroundColor Green
    Write-Host "p - Netzwerk-Scan" -ForegroundColor Green
    Write-Host "q - IP-Info" -ForegroundColor Green
    Write-Host "r - Wechselt zum Home Verzeichnis" -ForegroundColor Green
    Write-Host "s - Wetter Anzeige" -ForegroundColor Green
    Write-Host "t - Speedtest" -ForegroundColor Green
    Write-Host "u - Windows-Updates suchen" -ForegroundColor Green
    Write-Host "v - Blackjack spielen" -ForegroundColor Green
    Write-Host "w - Wuerfeln" -ForegroundColor Green
    Write-Host "x - Office oeffnen" -ForegroundColor Green
    Write-Host "y - MorseCode Generator" -ForegroundColor Green
    Write-Host "z - Zahlenraten" -ForegroundColor Green
}

function a {
    $akku = Get-CimInstance -ClassName Win32_Battery
    if ($akku) {
        $prozent = $akku.EstimatedChargeRemaining
        $ladezeit = $akku.EstimatedRunTime

        if ($ladezeit -gt 1000) {
            $zeit = "unendlich (Netzbetrieb)"
        } elseif ($ladezeit -gt 0 -and $prozent -gt 5) {
            $zeitBis5Prozent = $ladezeit * (($prozent - 5) / $prozent)
            $stunden = [math]::Floor($zeitBis5Prozent / 60)
            $minuten = [math]::Round($zeitBis5Prozent % 60)
            if ($stunden -gt 0) {
                if ($minuten -gt 0) {
                    $zeit = "$stunden Std $minuten Min"
                } else {
                    $zeit = "$stunden Std"
                }
            } else {
                $zeit = "$minuten Min"
            }
        } elseif ($prozent -le 5) {
            $zeit = "Weniger als 5 Prozent - PC geht gleich aus!"
        } else {
            $zeit = "Wird geladen..."
        }

        if ($prozent -ge 50) {
            $farbe = "Green"
        } elseif ($prozent -ge 20) {
            $farbe = "Yellow"
        } elseif ($prozent -ge 10) {
            $farbe = "DarkYellow"
        } else {
            $farbe = "Red"
        }

        Write-Host "[AKKU] $prozent%" -ForegroundColor $farbe
        Write-Host "[RESTZEIT] $zeit" -ForegroundColor Yellow

        $status = $akku.BatteryStatus
        switch ($status) {
            1 { $statusText = "Entladen" }
            2 { $statusText = "Wird geladen" }
            3 { $statusText = "Voll geladen" }
            4 { $statusText = "Standby" }
            5 { $statusText = "Unbekannt" }
            default { $statusText = "Unbekannt" }
        }
        Write-Host "[STATUS] $statusText" -ForegroundColor Cyan

    } else {
        Write-Host "[PC] Kein Akku gefunden (Desktop-PC?)" -ForegroundColor Red
    }
}

function b {
    param([string]$url = "https://chat.deepseek.com/")
    Start-Process $url
    Write-Host "[BROWSER] Geoeffnet mit: $url" -ForegroundColor Cyan
}

function c {
    Start-Process calc.exe
    Write-Host "[CALC] Taschenrechner geoeffnet" -ForegroundColor Cyan
}

function d {
    $d = Get-Date -Format "dddd dd.MM.yyyy"
    $url = "https://calendar.google.com/calendar/u/0/r?pli=1"
    Write-Host "[DATUM] $d" -ForegroundColor Blue
    Start-Process $url
}

function e {
    $optionen = @("schere", "stein", "papier")
    $spielerPunkte = 0
    $pcPunkte = 0
    $runden = 0

    Write-Host "[SPIEL] Best of 5 - Schere, Stein, Papier" -ForegroundColor Cyan
    Write-Host "[SPIEL] Wer zuerst 3 Runden gewinnt, siegt!" -ForegroundColor Yellow
    Write-Host ""

    while ($spielerPunkte -lt 3 -and $pcPunkte -lt 3) {
        $runden++
        Write-Host "[RUNDE $runden] Punktestand: Du $spielerPunkte : $pcPunkte PC" -ForegroundColor Cyan

        $pc = $optionen[(Get-Random -Max 3)]
        $spieler = Read-Host "[SPIEL] schere, stein oder papier? (oder 'q' zum Abbrechen)"

        if ($spieler -eq "q") {
            Write-Host "[SPIEL] Spiel abgebrochen!" -ForegroundColor Yellow
            return
        }

        if ($spieler -notin $optionen) {
            Write-Host "[FEHLER] Ungueltige Eingabe! Bitte 'schere', 'stein' oder 'papier' eingeben." -ForegroundColor Red
            $runden--
            continue
        }

        Write-Host "[SPIEL] Du: $spieler | PC: $pc" -ForegroundColor White

        if ($spieler -eq $pc) {
            Write-Host "[UNENTSCHIEDEN] Diese Runde geht an niemanden!" -ForegroundColor Yellow
        } elseif (
            ($spieler -eq "schere" -and $pc -eq "papier") -or
            ($spieler -eq "stein" -and $pc -eq "schere") -or
            ($spieler -eq "papier" -and $pc -eq "stein")
        ) {
            Write-Host "[GEWONNEN] Du gewinnst diese Runde!" -ForegroundColor Green
            $spielerPunkte++
        } else {
            Write-Host "[VERLOREN] PC gewinnt diese Runde!" -ForegroundColor Red
            $pcPunkte++
        }
        Write-Host ""
    }

    Write-Host "[SPIEL] ENDE! Endergebnis: Du $spielerPunkte : $pcPunkte PC" -ForegroundColor Cyan
    if ($spielerPunkte -gt $pcPunkte) {
        Write-Host "[SPIEL] HERZLICHEN GLUECKWUNSCH! Du hast das Best-of-5 gewonnen!" -ForegroundColor Green
    } else {
        Write-Host "[SPIEL] Schade! Der PC hat das Best-of-5 gewonnen!" -ForegroundColor Red
    }
}

function f {
    Write-Host "[PAPIERKORB] Willst du den Papierkorb wirklich leeren? (j/n)" -ForegroundColor Red
    $antwort = Read-Host
    if ($antwort -eq "j") {
        Clear-RecycleBin -Force -ErrorAction SilentlyContinue
        Write-Host "[PAPIERKORB] wurde geleert!" -ForegroundColor Green
    } else {
        Write-Host "[ABBRUCH] Vorgang abgebrochen" -ForegroundColor Yellow
    }
}

function g {
    $url = "https://www.github.com"
    Start-Process $url
    Write-Host "[GITHUB] Geoeffnet mit: $url" -ForegroundColor Cyan
}

function h {
    param([string]$begriff = "")

    if ($begriff -eq "") {
        Write-Host "[WIKIPEDIA] Lade zufaelligen Artikel..." -ForegroundColor Cyan
        $url = "https://de.wikipedia.org/api/rest_v1/page/random/summary"
    } else {
        Write-Host "[WIKIPEDIA] Suche nach: $begriff" -ForegroundColor Cyan
        $url = "https://de.wikipedia.org/api/rest_v1/page/summary/$([System.Web.HttpUtility]::UrlEncode($begriff))"
    }

    try {
        $article = Invoke-RestMethod -Uri $url -ErrorAction Stop

        Write-Host "========================================" -ForegroundColor Gray
        Write-Host "$($article.title)" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Gray
        Write-Host ""

        $extract = $article.extract
        if ($extract.Length -gt 500) {
            $extract = $extract.Substring(0, 500) + "..."
        }
        Write-Host $extract -ForegroundColor Yellow
        Write-Host ""

        if ($article.content_urls) {
            Write-Host "Weiterlesen: $($article.content_urls.desktop.page)" -ForegroundColor Cyan
        }

        Write-Host "========================================" -ForegroundColor Gray

        $open = Read-Host "Im Browser oeffnen? (j/n)"
        if ($open -eq "j" -or $open -eq "J") {
            Start-Process $article.content_urls.desktop.page
        }
    } catch {
        Write-Host "Artikel nicht gefunden!" -ForegroundColor Red
        Write-Host "Versuche: h 'PowerShell'" -ForegroundColor Yellow
        Write-Host "Oder: h (fuer zufaelligen Artikel)" -ForegroundColor Yellow
    }
}

function i {
    Clear-Host
    Write-Host "[SCREENSAVER] Startet... (Strg+C zum Beenden)" -ForegroundColor Cyan
    Start-Sleep -Seconds 2
    $farben = @('Red','Green','Yellow','Blue','Magenta','Cyan','White')
    $zeichen = @('#','*','+','.','o','O','@','%')
    while ($true) {
        $x = Get-Random -Minimum 0 -Maximum 80
        $y = Get-Random -Minimum 0 -Maximum 20
        $farbe = $farben | Get-Random
        $z = $zeichen | Get-Random
        [Console]::SetCursorPosition($x, $y)
        Write-Host $z -ForegroundColor $farbe -NoNewline
        Start-Sleep -Milliseconds (Get-Random -Minimum 10 -Maximum 100)
    }
}

function j {
    param([string]$text = "Hallo Onur!")

    if ([string]::IsNullOrEmpty($text)) {
        $text = "Hallo Onur!"
    }

    $farben = @('Red','Yellow','Green','Cyan','Blue','Magenta','DarkYellow','DarkCyan')
    $i = 0
    $text.ToCharArray() | ForEach-Object {
        Write-Host $_ -ForegroundColor $farben[$i % $farben.Count] -NoNewline
        $i++
    }
    Write-Host ""
}

function k {
    if ((Get-Random -Min 1 -Max 3) -eq 1) {
        "[MUENZE] Kopf"
    } else {
        "[MUENZE] Zahl"
    }
}

function l {
    param([string]$pfad = ".")
    if ($pfad -eq ".") { $pfad = (Get-Location).Path }
    $groesse = Get-ChildItem -Path $pfad -Recurse -ErrorAction SilentlyContinue |
               Measure-Object -Property Length -Sum
    $gesamtMB = [math]::Round($groesse.Sum / 1MB, 2)
    $gesamtGB = [math]::Round($groesse.Sum / 1GB, 2)
    Write-Host "[ORDNER] $pfad" -ForegroundColor Cyan
    Write-Host "[GROESSE] $gesamtMB MB ($gesamtGB GB)" -ForegroundColor Green
}

function m {
    param([int]$laenge = 20)

    $gross = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    $klein = "abcdefghijklmnopqrstuvwxyz"
    $zahlen = "0123456789"
    $sonder = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
    $alle = $gross + $klein + $zahlen + $sonder

    $passwort = ""
    $passwort += $gross[(Get-Random -Max $gross.Length)]
    $passwort += $klein[(Get-Random -Max $klein.Length)]
    $passwort += $zahlen[(Get-Random -Max $zahlen.Length)]
    $passwort += $sonder[(Get-Random -Max $sonder.Length)]

    for ($i = 4; $i -lt $laenge; $i++) {
        $passwort += $alle[(Get-Random -Max $alle.Length)]
    }

    $passwort = -join ($passwort.ToCharArray() | Sort-Object { Get-Random })
    Write-Host $passwort -ForegroundColor Green
    $passwort | Set-Clipboard
}

function n {
    param($max, $erreicht)
    $p = ($erreicht / $max) * 100

    if ($p -ge 95) { $note = 15 }
    elseif ($p -ge 90) { $note = 14 }
    elseif ($p -ge 85) { $note = 13 }
    elseif ($p -ge 80) { $note = 12 }
    elseif ($p -ge 75) { $note = 11 }
    elseif ($p -ge 70) { $note = 10 }
    elseif ($p -ge 65) { $note = 9 }
    elseif ($p -ge 60) { $note = 8 }
    elseif ($p -ge 55) { $note = 7 }
    elseif ($p -ge 50) { $note = 6 }
    elseif ($p -ge 45) { $note = 5 }
    elseif ($p -ge 40) { $note = 4 }
    elseif ($p -ge 33) { $note = 3 }
    elseif ($p -ge 27) { $note = 2 }
    elseif ($p -ge 20) { $note = 1 }
    else { $note = 0 }

    Write-Host "Erreicht: $erreicht von $max Punkten" -ForegroundColor Cyan
    Write-Host "Prozent: $([math]::Round($p, 1))%" -ForegroundColor Yellow
    Write-Host "Note: $note Notenpunkte" -ForegroundColor Green
}

function o {
    param([string]$ordner = "")
    $basis = "$env:USERPROFILE\Desktop\Projekte"
    if (-not (Test-Path $basis)) {
        New-Item -Path $basis -ItemType Directory -Force | Out-Null
        Write-Host "[ORDNER] Projekt-Ordner erstellt: $basis" -ForegroundColor Yellow
    }

    if ($ordner -eq "") {
        Set-Location $basis
    } else {
        $zielPfad = "$basis\$ordner"
        if (-not (Test-Path $zielPfad)) {
            New-Item -Path $zielPfad -ItemType Directory -Force | Out-Null
            Write-Host "[ORDNER] Neuen Projekt-Ordner erstellt: $ordner" -ForegroundColor Green
        }
        Set-Location $zielPfad
    }
    Write-Host "[PROJEKT] Wechsel zu: $(Get-Location)" -ForegroundColor Cyan
}

function p {
    $netz = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
        $_.InterfaceAlias -ne "Loopback" -and
        $_.PrefixOrigin -ne "WellKnown"
    })[0].IPAddress

    if (-not $netz) {
        Write-Host "[FEHLER] Keine gueltige Netzwerk-IP gefunden!" -ForegroundColor Red
        return
    }

    $netz = $netz.Substring(0, $netz.LastIndexOf('.')) + "."
    Write-Host "[SCAN] Scanne Netzwerk: $netz" -ForegroundColor Cyan
    Write-Host "[INFO] Das kann 10-30 Sekunden dauern..." -ForegroundColor Yellow

    $aktiveIPs = @()
    $jobs = @()
    1..254 | ForEach-Object {
        $ip = "$netz$_"
        $jobs += Start-Job -ScriptBlock {
            param($ip)
            if (Test-Connection -ComputerName $ip -Count 1 -Quiet -ErrorAction SilentlyContinue) {
                return $ip
            }
            return $null
        } -ArgumentList $ip
    }

    $jobs | ForEach-Object {
        $result = Receive-Job -Job $_ -Wait -ErrorAction SilentlyContinue
        if ($result) {
            $aktiveIPs += $result
            Write-Host "[FOUND] $result" -ForegroundColor Green
        }
        Remove-Job -Job $_ -Force
    }

    Write-Host ""
    Write-Host "[ERGEBNIS] $($aktiveIPs.Count) aktive Geräte gefunden:" -ForegroundColor Cyan
    if ($aktiveIPs.Count -gt 0) {
        $aktiveIPs | Sort-Object { [version]$_ } | ForEach-Object {
            Write-Host "  $($_)" -ForegroundColor Green
        }
    } else {
        Write-Host "  Keine Geräte gefunden" -ForegroundColor Red
    }

    return $aktiveIPs
}

function q {
    param([string]$ip = (Invoke-RestMethod -Uri "https://api.ipify.org").Content)
    try {
        $daten = Invoke-RestMethod -Uri "http://ip-api.com/json/$ip"
        if ($daten.status -eq "success") {
            if ([string]::IsNullOrEmpty($ip)) {
                $ip = $daten.query
            }
            Write-Host "[IP] $ip" -ForegroundColor Cyan
            Write-Host "[LAND] $($daten.country)" -ForegroundColor Green
            Write-Host "[STADT] $($daten.city)" -ForegroundColor Yellow
            Write-Host "[ISP] $($daten.isp)" -ForegroundColor Magenta
            Write-Host "[KOORDINATEN] $($daten.lat), $($daten.lon)" -ForegroundColor Gray
            Write-Host "[ZEITZONE] $($daten.timezone)" -ForegroundColor DarkCyan
            Write-Host "[ORG] $($daten.org)" -ForegroundColor DarkMagenta
        } else {
            Write-Host "[FEHLER] Keine Daten fuer diese IP gefunden" -ForegroundColor Red
        }
    } catch {
        Write-Host "[FEHLER] beim Abrufen der Daten: $_" -ForegroundColor Red
    }
}

function r {
    Set-Location ~
}

function s {
    param([string]$stadt = "Istanbul")

    Write-Host "========================================" -ForegroundColor Gray
    Write-Host "          WETTERVORHERSAGE" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Gray
    Write-Host ""

    try {
        $wetter = Invoke-RestMethod -Uri "https://wttr.in/$stadt?format=j1" -ErrorAction Stop
        $aktuell = $wetter.current_condition[0]
        $ort = $wetter.nearest_area[0]

        $wetterIcon = switch -Wildcard ($aktuell.weatherDesc[0].value) {
            "*Sunny*" { "[SONNE]" }
            "*Clear*" { "[NACHT]" }
            "*Partly*" { "[WOLKEN]" }
            "*Cloud*" { "[BEDECKT]" }
            "*Rain*" { "[REGEN]" }
            "*Thunder*" { "[GEWITTER]" }
            "*Snow*" { "[SCHNEE]" }
            "*Mist*" { "[NEBEL]" }
            "*Fog*" { "[NEBEL]" }
            default { "[WETTER]" }
        }

        Write-Host "Ort: $($ort.areaName[0].value), $($ort.country[0].value)" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Gray
        Write-Host "$wetterIcon Temperatur: $($aktuell.temp_C)°C (gefuehlt $($aktuell.FeelsLikeC)°C)" -ForegroundColor Green
        Write-Host "Bedingung: $($aktuell.weatherDesc[0].value)" -ForegroundColor Yellow
        Write-Host "Luftfeuchtigkeit: $($aktuell.humidity)%" -ForegroundColor Blue
        Write-Host "Wind: $($aktuell.windSpeed) km/h" -ForegroundColor Cyan
        Write-Host "Sichtweite: $($aktuell.visibility) km" -ForegroundColor Gray
        Write-Host "Stand: $($aktuell.observation_time) UTC" -ForegroundColor DarkGray

        Write-Host ""
        Write-Host "VORHERSAGE (naechste 3 Tage):" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Gray

        $vorhersage = $wetter.weather[1..3]
        foreach ($tag in $vorhersage) {
            $datum = [datetime]::ParseExact($tag.date, "yyyy-MM-dd", $null).ToString("dd.MM.")
            $maxTemp = $tag.maxtempC
            $minTemp = $tag.mintempC
            $bedingung = $tag.hourly[0].weatherDesc[0].value
            Write-Host "${datum}: $bedingung, $minTemp°C - $maxTemp°C" -ForegroundColor Yellow
        }

    } catch {
        Write-Host "FEHLER: Wetter konnte nicht abgerufen werden" -ForegroundColor Red
        Write-Host "Tipp: Pruefen Sie Ihre Internetverbindung" -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Gray
}

function t {
    Write-Host "[INTERNET] Teste Verbindung..." -ForegroundColor Cyan
    $ping = Test-Connection -ComputerName google.de -Count 4 -ErrorAction SilentlyContinue
    if ($ping) {
        $durchschnitt = [math]::Round(($ping | Measure-Object -Property ResponseTime -Average).Average, 0)
        Write-Host "[PING] $durchschnitt ms" -ForegroundColor Green
    } else {
        Write-Host "[FEHLER] Keine Internetverbindung!" -ForegroundColor Red
        return
    }
    Write-Host "[SPEEDTEST] Messe Geschwindigkeit (Download)..." -ForegroundColor Yellow
    $url = "https://speedtest.tele2.net/10MB.zip"
    $start = Get-Date
    try {
        Invoke-WebRequest -Uri $url -OutFile "$env:TEMP\speedtest.zip" -ErrorAction Stop
        $ende = Get-Date
        $dauer = ($ende - $start).TotalSeconds
        $groesse = 10
        $speed = [math]::Round($groesse / $dauer, 2)
        Write-Host "[DOWNLOAD] $speed MB/s" -ForegroundColor Green
        Remove-Item "$env:TEMP\speedtest.zip" -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Host "[WARNUNG] Speedtest fehlgeschlagen (ggf. Firewall/Proxy)" -ForegroundColor Yellow
    }
    Write-Host "[SPEEDTEST] Messe Geschwindigkeit (Upload)..." -ForegroundColor Yellow
    try {
        $uploadStart = Get-Date
        $dummy = [byte[]]::new(1MB)
        Invoke-WebRequest -Uri "https://httpbin.org/post" -Method Post -Body $dummy -ErrorAction Stop | Out-Null
        $uploadEnde = Get-Date
        $uploadDauer = ($uploadEnde - $uploadStart).TotalSeconds
        $uploadSpeed = [math]::Round(1 / $uploadDauer, 2)
        Write-Host "[UPLOAD] $uploadSpeed MB/s" -ForegroundColor Green
    } catch {
        Write-Host "[WARNUNG] Upload-Test fehlgeschlagen (ggf. Firewall/Proxy)" -ForegroundColor Yellow
    }
}

function u {
    Write-Host "[WINDOWS-UPDATE] Suche nach Updates..." -ForegroundColor Cyan
    try {
        $updates = Get-WindowsUpdate -ErrorAction SilentlyContinue
        if ($updates) {
            Write-Host "[UPDATES] $($updates.Count) Updates verfuegbar:" -ForegroundColor Yellow
            $updates | Select-Object Title, Size, KB | Format-Table -AutoSize
        } else {
            Write-Host "[UPDATES] Keine Updates verfuegbar (oder Modul fehlt)" -ForegroundColor Green
        }
    } catch {
        Write-Host "[UPDATES] Modul 'PSWindowsUpdate' nicht installiert" -ForegroundColor Yellow
    }
}

function v {
    $karten = 2..11
    $spieler = @()
    $pc = @()
    $spieler += $karten | Get-Random
    $pc += $karten | Get-Random
    $spieler += $karten | Get-Random
    $pc += $karten | Get-Random
    function summe($hand) { ($hand | Measure-Object -Sum).Sum }
    Write-Host "[BLACKJACK] Deine Karten: $($spieler -join ', ') (Summe: $(summe $spieler))" -ForegroundColor Cyan
    Write-Host "[BLACKJACK] PC zeigt: $($pc[0]) + ?" -ForegroundColor Yellow
    while ((summe $spieler) -lt 21) {
        $antwort = Read-Host "[BLACKJACK] Noch eine Karte? (j/n)"
        if ($antwort -eq "j") {
            $spieler += $karten | Get-Random
            Write-Host "[BLACKJACK] Deine Karten: $($spieler -join ', ') (Summe: $(summe $spieler))" -ForegroundColor Cyan
        } else {
            break
        }
    }
    while ((summe $pc) -lt 17) { $pc += $karten | Get-Random }
    $summeSpieler = summe $spieler
    $summePC = summe $pc
    Write-Host "[BLACKJACK] PC hat: $($pc -join ', ') (Summe: $summePC)" -ForegroundColor Yellow
    if ($summeSpieler -gt 21) {
        Write-Host "[BLACKJACK] Ueber 21! Du hast verloren." -ForegroundColor Red
    } elseif ($summePC -gt 21 -or $summeSpieler -gt $summePC) {
        Write-Host "[BLACKJACK] Du gewinnst!" -ForegroundColor Green
    } elseif ($summeSpieler -eq $summePC) {
        Write-Host "[BLACKJACK] Unentschieden!" -ForegroundColor Yellow
    } else {
        Write-Host "[BLACKJACK] PC gewinnt!" -ForegroundColor Red
    }
}

function w {
    $z = Get-Random -Min 1 -Max 7
    [Console]::Beep(500 + $z * 80, 150)
    Write-Host "[WUERFEL] $z" -ForegroundColor Magenta
}

function x {
    Write-Host "[OFFICE] Welches Programm?" -ForegroundColor Cyan
    Write-Host "1  Word" -ForegroundColor Yellow
    Write-Host "2  Excel" -ForegroundColor Green
    Write-Host "3  PowerPoint" -ForegroundColor Magenta
    Write-Host "4  Outlook" -ForegroundColor Blue
    Write-Host "5  OneNote" -ForegroundColor DarkCyan
    Write-Host "0  Abbrechen" -ForegroundColor Red
    $wahl = Read-Host "[OFFICE] Deine Wahl (0-5)"
    switch ($wahl) {
        "1" { Start-Process winword.exe; Write-Host "[WORD] geoeffnet" -ForegroundColor Yellow }
        "2" { Start-Process excel.exe; Write-Host "[EXCEL] geoeffnet" -ForegroundColor Green }
        "3" { Start-Process powerpnt.exe; Write-Host "[POWERPOINT] geoeffnet" -ForegroundColor Magenta }
        "4" { Start-Process outlook.exe; Write-Host "[OUTLOOK] geoeffnet" -ForegroundColor Blue }
        "5" { Start-Process onenote.exe; Write-Host "[ONENOTE] geoeffnet" -ForegroundColor DarkCyan }
        "0" { Write-Host "[ABBRUCH]" -ForegroundColor Red }
        default { Write-Host "[FEHLER] Ungueltige Eingabe!" -ForegroundColor Red }
    }
}

function y {
    param(
        [string]$text,
        [switch]$rueck
    )

    if ([string]::IsNullOrEmpty($text) -and -not $rueck) {
        Write-Host "Beispiel: y HALLO" -ForegroundColor Yellow
        Write-Host "Morse zu Text: y '.... .- .-.. .-.. ---' -rueck" -ForegroundColor Yellow
        return
    }

    if ($rueck) {
        $text = $text -replace "/", " / "
        $words = $text -split " / "
        $result = ""
        foreach ($word in $words) {
            $letters = $word.Trim() -split " "
            foreach ($letter in $letters) {
                switch ($letter) {
                    ".-" { $result += "A" }
                    "-..." { $result += "B" }
                    "-.-." { $result += "C" }
                    "-.." { $result += "D" }
                    "." { $result += "E" }
                    "..-." { $result += "F" }
                    "--." { $result += "G" }
                    "...." { $result += "H" }
                    ".." { $result += "I" }
                    ".---" { $result += "J" }
                    "-.-" { $result += "K" }
                    ".-.." { $result += "L" }
                    "--" { $result += "M" }
                    "-." { $result += "N" }
                    "---" { $result += "O" }
                    ".--." { $result += "P" }
                    "--.-" { $result += "Q" }
                    ".-." { $result += "R" }
                    "..." { $result += "S" }
                    "-" { $result += "T" }
                    "..-" { $result += "U" }
                    "...-" { $result += "V" }
                    ".--" { $result += "W" }
                    "-..-" { $result += "X" }
                    "-.--" { $result += "Y" }
                    "--.." { $result += "Z" }
                    default { $result += "?" }
                }
            }
            $result += " "
        }
        Write-Host $result.Trim() -ForegroundColor Yellow
    } else {
        $result = ""
        foreach ($char in $text.ToUpper().ToCharArray()) {
            switch ($char) {
                "A" { $result += ".- " }
                "B" { $result += "-... " }
                "C" { $result += "-.-. " }
                "D" { $result += "-.. " }
                "E" { $result += ". " }
                "F" { $result += "..-. " }
                "G" { $result += "--. " }
                "H" { $result += ".... " }
                "I" { $result += ".. " }
                "J" { $result += ".--- " }
                "K" { $result += "-.- " }
                "L" { $result += ".-.. " }
                "M" { $result += "-- " }
                "N" { $result += "-. " }
                "O" { $result += "--- " }
                "P" { $result += ".--. " }
                "Q" { $result += "--.- " }
                "R" { $result += ".-. " }
                "S" { $result += "... " }
                "T" { $result += "- " }
                "U" { $result += "..- " }
                "V" { $result += "...- " }
                "W" { $result += ".-- " }
                "X" { $result += "-..- " }
                "Y" { $result += "-.-- " }
                "Z" { $result += "--.. " }
                " " { $result += "/ " }
                default { $result += "? " }
            }
        }
        Write-Host $result.Trim() -ForegroundColor Green
    }
}

function z {
    $ziel = Get-Random -Min 1 -Max 101
    $versuche = 0
    $maxVersuche = 10
    Write-Host "[ZAHLENRATEN] Ich denke an eine Zahl zwischen 1 und 100!" -ForegroundColor Cyan
    Write-Host "[ZAHLENRATEN] Du hast $maxVersuche Versuche." -ForegroundColor Yellow
    do {
        $versuche++
        $eingabe = Read-Host "[ZAHLENRATEN] Versuch $versuche von $maxVersuche"
        if ($eingabe -gt $ziel) {
            Write-Host "[ZAHLENRATEN] Zu hoch!" -ForegroundColor Red
        } elseif ($eingabe -lt $ziel) {
            Write-Host "[ZAHLENRATEN] Zu niedrig!" -ForegroundColor Red
        }
        if ($versuche -eq $maxVersuche -and $eingabe -ne $ziel) {
            Write-Host "[ZAHLENRATEN] Leider verloren! Die Zahl war $ziel." -ForegroundColor Magenta
            break
        }
    } while ($eingabe -ne $ziel)
    if ($eingabe -eq $ziel) {
        Write-Host "[ZAHLENRATEN] Richtig! Du hast $versuche Versuche gebraucht." -ForegroundColor Green
    }
}