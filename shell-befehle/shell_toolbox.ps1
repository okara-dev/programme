# PowerShell-Profil: Microsoft.PowerShell_profile.ps1
# A-Z Shell Toolbox

Remove-Item Alias:h -ErrorAction SilentlyContinue -Force
Remove-Item Alias:r -ErrorAction SilentlyContinue -Force

function hilfe {
    Write-Host "[HELP] Verfuegbare Funktionen (A-Z):" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "a  - Akkustatus anzeigen" -ForegroundColor Green
    Write-Host "b  - Browser oeffnen" -ForegroundColor Green
    Write-Host "c  - Taschenrechner" -ForegroundColor Green
    Write-Host "d  - Datum anzeigen + Kalender oeffnen" -ForegroundColor Green
    Write-Host "e  - Terminal-Farbe aendern" -ForegroundColor Green
    Write-Host "f  - Papierkorb leeren" -ForegroundColor Green
    Write-Host "g  - GitHub oeffnen" -ForegroundColor Green
    Write-Host "h  - Wechselt zum Home Verzeichnis" -ForegroundColor Green
    Write-Host "i  - Bildschirm-Reiniger" -ForegroundColor Green
    Write-Host "j  - Downloads-Ordner aufraeumen" -ForegroundColor Green
    Write-Host "k  - Muenzwurf" -ForegroundColor Green
    Write-Host "l  - Ordner-Groesse anzeigen" -ForegroundColor Green
    Write-Host "m  - Passwort-Generator" -ForegroundColor Green
    Write-Host "n  - Notenpunkte berechnen" -ForegroundColor Green
    Write-Host "o  - Zu Projekt-Ordner wechseln" -ForegroundColor Green
    Write-Host "p  - Autostart-Programme anzeigen" -ForegroundColor Green
    Write-Host "q  - PC neustarten" -ForegroundColor Green
    Write-Host "r  - Wikipedia-Artikel anzeigen" -ForegroundColor Green
    Write-Host "s  - Wetter anzeigen" -ForegroundColor Green
    Write-Host "t  - Speedtest" -ForegroundColor Green
    Write-Host "u  - Windows-Updates suchen" -ForegroundColor Green
    Write-Host "v  - Bilder/Screenshots loeschen" -ForegroundColor Green
    Write-Host "w  - Wuerfeln" -ForegroundColor Green
    Write-Host "x  - Office oeffnen" -ForegroundColor Green
    Write-Host "y  - Morsecode Generator" -ForegroundColor Green
    Write-Host "z  - Spiele-Menue (Schere-Stein-Papier, Blackjack, Zahlenraten, Tic-Tac-Toe, Vier gewinnt)" -ForegroundColor Green
    Write-Host ""
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
    Write-Host "[FARBE] Was moechtest du aendern?" -ForegroundColor Cyan
    Write-Host "1  Textfarbe" -ForegroundColor Green
    Write-Host "2  Hintergrundfarbe (ganzes Terminal)" -ForegroundColor Green
    Write-Host "3  Beides" -ForegroundColor Green
    Write-Host "0  Abbrechen" -ForegroundColor Red
    $modus = Read-Host "[FARBE] Wahl (0-3)"

    if ($modus -eq "0") { return }

    $farben = @(
        "Black","DarkBlue","DarkGreen","DarkCyan","DarkRed","DarkMagenta",
        "DarkYellow","Gray","DarkGray","Blue","Green","Cyan","Red",
        "Magenta","Yellow","White"
    )

    function WaehleFarbe($titel) {
        Write-Host ""
        Write-Host "[FARBE] $titel" -ForegroundColor Cyan
        for ($i = 0; $i -lt $farben.Count; $i++) {
            Write-Host ("{0,2}  {1}" -f $i, $farben[$i]) -ForegroundColor $farben[$i]
        }
        Write-Host ""
        $wahl = Read-Host "[FARBE] Nummer waehlen (0-$($farben.Count - 1)) oder 'q'"
        if ($wahl -eq "q") { return $null }
        if ($wahl -match "^\d+$" -and [int]$wahl -ge 0 -and [int]$wahl -lt $farben.Count) {
            return $farben[[int]$wahl]
        }
        Write-Host "[FEHLER] Ungueltige Eingabe!" -ForegroundColor Red
        return $null
    }

    switch ($modus) {
        "1" {
            $farbe = WaehleFarbe "Textfarbe waehlen"
            if ($farbe) {
                $host.UI.RawUI.ForegroundColor = $farbe
                Write-Host "[FARBE] Textfarbe geaendert zu: $farbe" -ForegroundColor $farbe
            }
        }
        "2" {
            $farbe = WaehleFarbe "Hintergrundfarbe waehlen"
            if ($farbe) {
                $host.UI.RawUI.BackgroundColor = $farbe
                Clear-Host
                Write-Host "[FARBE] Hintergrundfarbe geaendert zu: $farbe" -ForegroundColor Cyan
            }
        }
        "3" {
            $textFarbe = WaehleFarbe "Textfarbe waehlen"
            if (-not $textFarbe) { return }
            $bgFarbe = WaehleFarbe "Hintergrundfarbe waehlen"
            if (-not $bgFarbe) { return }
            $host.UI.RawUI.ForegroundColor = $textFarbe
            $host.UI.RawUI.BackgroundColor = $bgFarbe
            Clear-Host
            Write-Host "[FARBE] Text: $textFarbe | Hintergrund: $bgFarbe" -ForegroundColor $textFarbe
        }
        default {
            Write-Host "[FEHLER] Ungueltige Eingabe!" -ForegroundColor Red
        }
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
    Set-Location ~
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
    $downloads = "$env:USERPROFILE\Downloads"
    if (-not (Test-Path $downloads)) {
        Write-Host "[DOWNLOADS] Ordner nicht gefunden: $downloads" -ForegroundColor Red
        return
    }

    Write-Host "[DOWNLOADS] Analysiere: $downloads" -ForegroundColor Cyan
    $dateien = Get-ChildItem -Path $downloads -File -ErrorAction SilentlyContinue
    if (-not $dateien) {
        Write-Host "[DOWNLOADS] Keine Dateien vorhanden." -ForegroundColor Green
        return
    }

    $gesamt = ($dateien | Measure-Object -Property Length -Sum).Sum
    $gesamtMB = [math]::Round($gesamt / 1MB, 2)
    Write-Host "[DOWNLOADS] $($dateien.Count) Dateien, $gesamtMB MB" -ForegroundColor Yellow

    $alt = $dateien | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }
    if ($alt) {
        $altMB = [math]::Round((($alt | Measure-Object -Property Length -Sum).Sum) / 1MB, 2)
        Write-Host "[DOWNLOADS] $($alt.Count) Dateien aelter als 30 Tage ($altMB MB)" -ForegroundColor Magenta
    } else {
        Write-Host "[DOWNLOADS] Keine alten Dateien (>30 Tage)." -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "1  Alte Dateien (>30 Tage) loeschen" -ForegroundColor Yellow
    Write-Host "2  Alle Dateien loeschen" -ForegroundColor Red
    Write-Host "3  Nur anzeigen (nichts loeschen)" -ForegroundColor Green
    Write-Host "0  Abbrechen" -ForegroundColor Gray
    $wahl = Read-Host "[DOWNLOADS] Wahl"

    switch ($wahl) {
        "1" {
            if (-not $alt) { Write-Host "[DOWNLOADS] Nichts zu loeschen." -ForegroundColor Green; return }
            $alt | Remove-Item -Force -ErrorAction SilentlyContinue
            Write-Host "[DOWNLOADS] $($alt.Count) alte Dateien geloescht." -ForegroundColor Green
        }
        "2" {
            $bestaetigung = Read-Host "[DOWNLOADS] Wirklich ALLE Dateien loeschen? (j/n)"
            if ($bestaetigung -eq "j") {
                $dateien | Remove-Item -Force -ErrorAction SilentlyContinue
                Write-Host "[DOWNLOADS] Alle Dateien geloescht." -ForegroundColor Green
            } else {
                Write-Host "[ABBRUCH]" -ForegroundColor Yellow
            }
        }
        "3" {
            $dateien | Select-Object Name, @{N="MB";E={[math]::Round($_.Length/1MB,2)}}, LastWriteTime |
                Format-Table -AutoSize
        }
        default { Write-Host "[ABBRUCH]" -ForegroundColor Yellow }
    }
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
    Write-Host "[AUTOSTART] Programme im Autostart:" -ForegroundColor Cyan
    Write-Host ""

    $pfade = @(
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run",
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
        "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"
    )

    $gefunden = $false
    foreach ($pfad in $pfade) {
        if (Test-Path $pfad) {
            $eintraege = Get-ItemProperty -Path $pfad -ErrorAction SilentlyContinue
            $eintraege.PSObject.Properties | Where-Object { $_.Name -notlike "PS*" } | ForEach-Object {
                Write-Host "  [$($_.Name)]" -ForegroundColor Yellow
                Write-Host "    $($_.Value)" -ForegroundColor Gray
                $gefunden = $true
            }
        }
    }

    $startupOrdner = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
    if (Test-Path $startupOrdner) {
        $dateien = Get-ChildItem -Path $startupOrdner -ErrorAction SilentlyContinue
        if ($dateien) {
            Write-Host ""
            Write-Host "[AUTOSTART] Startup-Ordner:" -ForegroundColor Cyan
            $dateien | ForEach-Object {
                Write-Host "  $($_.Name)" -ForegroundColor Yellow
                $gefunden = $true
            }
        }
    }

    if (-not $gefunden) {
        Write-Host "[AUTOSTART] Keine Eintraege gefunden." -ForegroundColor Green
    }
    Write-Host ""
}

function q {
    Write-Host "[NEUSTART] PC wirklich neu starten? (j/n)" -ForegroundColor Red
    $antwort = Read-Host
    if ($antwort -eq "j") {
        Write-Host "[NEUSTART] PC wird in 10 Sekunden neu gestartet... (Abbrechen mit shutdown /a)" -ForegroundColor Yellow
        shutdown /r /t 10
    } else {
        Write-Host "[ABBRUCH] Vorgang abgebrochen" -ForegroundColor Yellow
    }
}

function r {
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

function s {
    param([string]$stadt = "Istanbul")

    Write-Host "========================================" -ForegroundColor Gray
    Write-Host "          WETTERVORHERSAGE" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Gray
    Write-Host ""

    try {
        # 1. Stadt -> Koordinaten
        $geoUrl = "https://geocoding-api.open-meteo.com/v1/search?name=$([uri]::EscapeDataString($stadt))&count=1&language=de&format=json"
        $geo = Invoke-RestMethod -Uri $geoUrl -ErrorAction Stop

        if (-not $geo.results -or $geo.results.Count -eq 0) {
            Write-Host "[FEHLER] Stadt nicht gefunden: $stadt" -ForegroundColor Red
            return
        }

        $ort = $geo.results[0]
        $lat = $ort.latitude
        $lon = $ort.longitude

        # 2. Wetter + Vorhersage
        $wetterUrl = "https://api.open-meteo.com/v1/forecast?latitude=$lat&longitude=$lon&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=4"
        $wetter = Invoke-RestMethod -Uri $wetterUrl -ErrorAction Stop

        $aktuell = $wetter.current
        $taeglich = $wetter.daily

        # Wetter-Code -> Beschreibung + Symbol
        function WetterCode($code) {
            switch ($code) {
                0 { return @("[SONNE]", "Klarer Himmel") }
                1 { return @("[SONNE]", "Ueberwiegend klar") }
                2 { return @("[WOLKEN]", "Teilweise bewoelkt") }
                3 { return @("[BEDECKT]", "Bedeckt") }
                45 { return @("[NEBEL]", "Nebel") }
                48 { return @("[NEBEL]", "Reifnebel") }
                51 { return @("[REGEN]", "Leichter Nieselregen") }
                53 { return @("[REGEN]", "Nieselregen") }
                55 { return @("[REGEN]", "Starker Nieselregen") }
                61 { return @("[REGEN]", "Leichter Regen") }
                63 { return @("[REGEN]", "Regen") }
                65 { return @("[REGEN]", "Starker Regen") }
                71 { return @("[SCHNEE]", "Leichter Schneefall") }
                73 { return @("[SCHNEE]", "Schneefall") }
                75 { return @("[SCHNEE]", "Starker Schneefall") }
                77 { return @("[SCHNEE]", "Schneegriesel") }
                80 { return @("[REGEN]", "Leichte Regenschauer") }
                81 { return @("[REGEN]", "Regenschauer") }
                82 { return @("[REGEN]", "Starke Regenschauer") }
                85 { return @("[SCHNEE]", "Leichte Schneeschauer") }
                86 { return @("[SCHNEE]", "Starke Schneeschauer") }
                95 { return @("[GEWITTER]", "Gewitter") }
                96 { return @("[GEWITTER]", "Gewitter mit Hagel") }
                99 { return @("[GEWITTER]", "Starkes Gewitter mit Hagel") }
                default { return @("[WETTER]", "Unbekannt") }
            }
        }

        $info = WetterCode $aktuell.weather_code

        Write-Host "Ort: $($ort.name), $($ort.country)" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Gray
        Write-Host "$($info[0]) Temperatur: $($aktuell.temperature_2m)°C (gefuehlt $($aktuell.apparent_temperature)°C)" -ForegroundColor Green
        Write-Host "Bedingung: $($info[1])" -ForegroundColor Yellow
        Write-Host "Luftfeuchtigkeit: $($aktuell.relative_humidity_2m)%" -ForegroundColor Blue
        Write-Host "Wind: $($aktuell.wind_speed_10m) km/h" -ForegroundColor Cyan
        Write-Host "Stand: $($aktuell.time)" -ForegroundColor DarkGray

        Write-Host ""
        Write-Host "VORHERSAGE (naechste 3 Tage):" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Gray

        for ($i = 1; $i -le 3; $i++) {
            $datum = [datetime]::ParseExact($taeglich.time[$i], "yyyy-MM-dd", $null).ToString("dd.MM.")
            $code = $taeglich.weather_code[$i]
            $info = WetterCode $code
            $max = $taeglich.temperature_2m_max[$i]
            $min = $taeglich.temperature_2m_min[$i]
            Write-Host "${datum}: $($info[1]), $min°C - $max°C" -ForegroundColor Yellow
        }

    } catch {
        Write-Host "FEHLER: Wetter konnte nicht abgerufen werden" -ForegroundColor Red
        Write-Host "Details: $($_.Exception.Message)" -ForegroundColor DarkRed
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
    $ordner = "$env:USERPROFILE\Pictures"
    $screenshotOrdner = "$env:USERPROFILE\Pictures\Screenshots"

    Write-Host "[BILDER] Ziel-Ordner: $ordner" -ForegroundColor Cyan

    if (-not (Test-Path $ordner)) {
        Write-Host "[BILDER] Bilder-Ordner nicht gefunden!" -ForegroundColor Red
        return
    }

    $bildEndungen = @("*.jpg","*.jpeg","*.png","*.gif","*.bmp","*.tiff","*.webp")
    $bilder = @()
    foreach ($endung in $bildEndungen) {
        $bilder += Get-ChildItem -Path $ordner -Filter $endung -File -ErrorAction SilentlyContinue
    }

    if ($screenshotOrdner -and (Test-Path $screenshotOrdner)) {
        foreach ($endung in $bildEndungen) {
            $bilder += Get-ChildItem -Path $screenshotOrdner -Filter $endung -File -ErrorAction SilentlyContinue
        }
    }

    $bilder = $bilder | Sort-Object FullName -Unique

    if (-not $bilder) {
        Write-Host "[BILDER] Keine Bilder gefunden." -ForegroundColor Green
        return
    }

    $gesamtMB = [math]::Round((($bilder | Measure-Object -Property Length -Sum).Sum) / 1MB, 2)
    Write-Host "[BILDER] $($bilder.Count) Bilder gefunden ($gesamtMB MB)" -ForegroundColor Yellow
    Write-Host ""

    Write-Host "1  Bilder aelter als 30 Tage loeschen" -ForegroundColor Yellow
    Write-Host "2  Screenshots loeschen" -ForegroundColor Red
    Write-Host "3  Alle Bilder loeschen" -ForegroundColor Red
    Write-Host "4  Nur anzeigen" -ForegroundColor Green
    Write-Host "0  Abbrechen" -ForegroundColor Gray
    $wahl = Read-Host "[BILDER] Wahl"

    switch ($wahl) {
        "1" {
            $alt = $bilder | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }
            if (-not $alt) { Write-Host "[BILDER] Keine alten Bilder." -ForegroundColor Green; return }
            $altMB = [math]::Round((($alt | Measure-Object -Property Length -Sum).Sum) / 1MB, 2)
            Write-Host "[BILDER] $($alt.Count) Bilder ($altMB MB) loeschen? (j/n)" -ForegroundColor Yellow
            if ((Read-Host) -eq "j") {
                $alt | Remove-Item -Force -ErrorAction SilentlyContinue
                Write-Host "[BILDER] $($alt.Count) Bilder geloescht." -ForegroundColor Green
            } else { Write-Host "[ABBRUCH]" -ForegroundColor Yellow }
        }
        "2" {
            if (-not (Test-Path $screenshotOrdner)) { Write-Host "[BILDER] Kein Screenshot-Ordner." -ForegroundColor Red; return }
            $shots = Get-ChildItem -Path $screenshotOrdner -File -ErrorAction SilentlyContinue
            if (-not $shots) { Write-Host "[BILDER] Keine Screenshots." -ForegroundColor Green; return }
            Write-Host "[BILDER] $($shots.Count) Screenshots loeschen? (j/n)" -ForegroundColor Yellow
            if ((Read-Host) -eq "j") {
                $shots | Remove-Item -Force -ErrorAction SilentlyContinue
                Write-Host "[BILDER] Screenshots geloescht." -ForegroundColor Green
            } else { Write-Host "[ABBRUCH]" -ForegroundColor Yellow }
        }
        "3" {
            Write-Host "[BILDER] Wirklich ALLE $($bilder.Count) Bilder loeschen? (j/n)" -ForegroundColor Red
            if ((Read-Host) -eq "j") {
                $bilder | Remove-Item -Force -ErrorAction SilentlyContinue
                Write-Host "[BILDER] Alle Bilder geloescht." -ForegroundColor Green
            } else { Write-Host "[ABBRUCH]" -ForegroundColor Yellow }
        }
        "4" {
            $bilder | Select-Object Name, @{N="MB";E={[math]::Round($_.Length/1MB,2)}}, LastWriteTime, DirectoryName |
                Format-Table -AutoSize
        }
        default { Write-Host "[ABBRUCH]" -ForegroundColor Yellow }
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
    while ($true) {
        Clear-Host
        Write-Host "========================================" -ForegroundColor Gray
        Write-Host "           SPIELE-MENUE" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Gray
        Write-Host "1  Schere-Stein-Papier (Best of 5)" -ForegroundColor Green
        Write-Host "2  Blackjack" -ForegroundColor Green
        Write-Host "3  Zahlenraten" -ForegroundColor Green
        Write-Host "4  Tic-Tac-Toe (gegen PC)" -ForegroundColor Green
        Write-Host "5  Vier gewinnt (gegen PC)" -ForegroundColor Green
        Write-Host "0  Zurueck" -ForegroundColor Red
        Write-Host "========================================" -ForegroundColor Gray
        $wahl = Read-Host "[SPIELE] Deine Wahl (0-5)"

        switch ($wahl) {
            "1" { Spiel_SchereSteinPapier }
            "2" { Spiel_Blackjack }
            "3" { Spiel_Zahlenraten }
            "4" { Spiel_TicTacToe }
            "5" { Spiel_VierGewinnt }
            "0" { return }
            default { Write-Host "[FEHLER] Ungueltige Eingabe!" -ForegroundColor Red; Start-Sleep -Seconds 1 }
        }
    }
}

function Spiel_SchereSteinPapier {
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
    Read-Host "Enter zum Fortfahren"
}

function Spiel_Blackjack {
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
    Read-Host "Enter zum Fortfahren"
}

function Spiel_Zahlenraten {
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
    Read-Host "Enter zum Fortfahren"
}

function Spiel_TicTacToe {
    # Feld: 3x3, Bezeichnung A1..C3
    $felder = @{}
    foreach ($zeile in @("A","B","C")) {
        foreach ($spalte in 1..3) {
            $felder["$zeile$spalte"] = " "
        }
    }

    function ZeigeFeld($f) {
        Write-Host ""
        Write-Host "    1   2   3" -ForegroundColor Gray
        foreach ($zeile in @("A","B","C")) {
            Write-Host "  +---+---+---+" -ForegroundColor Gray
            Write-Host -NoNewline " $zeile"
            foreach ($spalte in 1..3) {
                Write-Host -NoNewline "| $($f["$zeile$spalte"]) "
            }
            Write-Host "|" -ForegroundColor Gray
        }
        Write-Host "  +---+---+---+" -ForegroundColor Gray
        Write-Host ""
    }

    function PruefeSieg($f, $spieler) {
        $linien = @(
            @("A1","A2","A3"), @("B1","B2","B3"), @("C1","C2","C3"),
            @("A1","B1","C1"), @("A2","B2","C2"), @("A3","B3","C3"),
            @("A1","B2","C3"), @("A3","B2","C1")
        )
        foreach ($linie in $linien) {
            if ($f[$linie[0]] -eq $spieler -and $f[$linie[1]] -eq $spieler -and $f[$linie[2]] -eq $spieler) {
                return $true
            }
        }
        return $false
    }

    function FreieFelder($f) {
        return @($f.Keys | Where-Object { $f[$_] -eq " " })
    }

    function PcZug($f) {
        $frei = FreieFelder $f
        # Gewinnzug?
        foreach ($k in $frei) {
            $test = $f.Clone()
            $test[$k] = "O"
            if (PruefeSieg $test "O") { return $k }
        }
        # Blockieren?
        foreach ($k in $frei) {
            $test = $f.Clone()
            $test[$k] = "X"
            if (PruefeSieg $test "X") { return $k }
        }
        # Mitte
        if ($f["B2"] -eq " ") { return "B2" }
        # Zufall
        return $frei | Get-Random
    }

    Write-Host "[TICTACTOE] Du bist X, PC ist O" -ForegroundColor Cyan
    Write-Host "[TICTACTOE] Felder: A1-A3, B1-B3, C1-C3" -ForegroundColor Yellow

    $zug = 0
    while ($true) {
        ZeigeFeld $felder
        $eingabe = (Read-Host "[TICTACTOE] Dein Zug (z.B. A1) oder 'q'").ToUpper()
        if ($eingabe -eq "Q") { return }
        if (-not $felder.ContainsKey($eingabe) -or $felder[$eingabe] -ne " ") {
            Write-Host "[FEHLER] Ungueltiges oder belegtes Feld!" -ForegroundColor Red
            continue
        }
        $felder[$eingabe] = "X"
        $zug++

        if (PruefeSieg $felder "X") {
            ZeigeFeld $felder
            Write-Host "[TICTACTOE] Du hast gewonnen!" -ForegroundColor Green
            Read-Host "Enter zum Fortfahren"
            return
        }
        if ($zug -eq 9) {
            ZeigeFeld $felder
            Write-Host "[TICTACTOE] Unentschieden!" -ForegroundColor Yellow
            Read-Host "Enter zum Fortfahren"
            return
        }

        $pcZug = PcZug $felder
        $felder[$pcZug] = "O"
        $zug++
        Write-Host "[TICTACTOE] PC spielt: $pcZug" -ForegroundColor Magenta

        if (PruefeSieg $felder "O") {
            ZeigeFeld $felder
            Write-Host "[TICTACTOE] PC hat gewonnen!" -ForegroundColor Red
            Read-Host "Enter zum Fortfahren"
            return
        }
        if ($zug -eq 9) {
            ZeigeFeld $felder
            Write-Host "[TICTACTOE] Unentschieden!" -ForegroundColor Yellow
            Read-Host "Enter zum Fortfahren"
            return
        }
    }
}

function Spiel_VierGewinnt {
    # Feld: 6 Zeilen (A-F) x 7 Spalten (1-7)
    $zeilen = @("A","B","C","D","E","F")
    $spalten = 1..7
    $felder = @{}
    foreach ($z in $zeilen) {
        foreach ($s in $spalten) {
            $felder["$z$s"] = " "
        }
    }

    function ZeigeFeldVG($f) {
        Write-Host ""
        Write-Host "    1   2   3   4   5   6   7" -ForegroundColor Gray
        foreach ($z in @("A","B","C","D","E","F")) {
            Write-Host "  +---+---+---+---+---+---+---+" -ForegroundColor Gray
            Write-Host -NoNewline " $z"
            foreach ($s in 1..7) {
                Write-Host -NoNewline "| $($f["$z$s"]) "
            }
            Write-Host "|" -ForegroundColor Gray
        }
        Write-Host "  +---+---+---+---+---+---+---+" -ForegroundColor Gray
        Write-Host ""
    }

    function PruefeSiegVG($f, $spieler) {
        # horizontal
        foreach ($z in @("A","B","C","D","E","F")) {
            for ($s = 1; $s -le 4; $s++) {
                if ($f["$z$s"] -eq $spieler -and $f["$z$($s+1)"] -eq $spieler -and $f["$z$($s+2)"] -eq $spieler -and $f["$z$($s+3)"] -eq $spieler) { return $true }
            }
        }
        # vertikal
        for ($s = 1; $s -le 7; $s++) {
            for ($i = 0; $i -le 2; $i++) {
                $z1 = $zeilen[$i]; $z2 = $zeilen[$i+1]; $z3 = $zeilen[$i+2]; $z4 = $zeilen[$i+3]
                if ($f["$z1$s"] -eq $spieler -and $f["$z2$s"] -eq $spieler -and $f["$z3$s"] -eq $spieler -and $f["$z4$s"] -eq $spieler) { return $true }
            }
        }
        # diagonal rechts
        for ($i = 0; $i -le 2; $i++) {
            for ($s = 1; $s -le 4; $s++) {
                $z1 = $zeilen[$i]; $z2 = $zeilen[$i+1]; $z3 = $zeilen[$i+2]; $z4 = $zeilen[$i+3]
                if ($f["$z1$s"] -eq $spieler -and $f["$z2$($s+1)"] -eq $spieler -and $f["$z3$($s+2)"] -eq $spieler -and $f["$z4$($s+3)"] -eq $spieler) { return $true }
            }
        }
        # diagonal links
        for ($i = 0; $i -le 2; $i++) {
            for ($s = 4; $s -le 7; $s++) {
                $z1 = $zeilen[$i]; $z2 = $zeilen[$i+1]; $z3 = $zeilen[$i+2]; $z4 = $zeilen[$i+3]
                if ($f["$z1$s"] -eq $spieler -and $f["$z2$($s-1)"] -eq $spieler -and $f["$z3$($s-2)"] -eq $spieler -and $f["$z4$($s-3)"] -eq $spieler) { return $true }
            }
        }
        return $false
    }

    function FindeEinwurf($f, $spalte) {
        # unterste freie Zeile in Spalte
        for ($i = 5; $i -ge 0; $i--) {
            $z = $zeilen[$i]
            if ($f["$z$spalte"] -eq " ") { return "$z$spalte" }
        }
        return $null
    }

    function PcZugVG($f) {
        $freieSpalten = @()
        foreach ($s in 1..7) {
            if (FindeEinwurf $f $s) { $freieSpalten += $s }
        }
        # Gewinnen?
        foreach ($s in $freieSpalten) {
            $test = $f.Clone()
            $pos = FindeEinwurf $test $s
            $test[$pos] = "O"
            if (PruefeSiegVG $test "O") { return $s }
        }
        # Blockieren?
        foreach ($s in $freieSpalten) {
            $test = $f.Clone()
            $pos = FindeEinwurf $test $s
            $test[$pos] = "X"
            if (PruefeSiegVG $test "X") { return $s }
        }
        # Mitte bevorzugen
        $mitte = @(4,3,5,2,6,1,7)
        foreach ($s in $mitte) {
            if ($s -in $freieSpalten) { return $s }
        }
        return $freieSpalten | Get-Random
    }

    Write-Host "[VIER GEWINNT] Du bist X, PC ist O" -ForegroundColor Cyan
    Write-Host "[VIER GEWINNT] Waehle eine Spalte 1-7, Stein faellt nach unten" -ForegroundColor Yellow

    $zug = 0
    while ($true) {
        ZeigeFeldVG $felder
        $eingabe = Read-Host "[VIER GEWINNT] Deine Spalte (1-7) oder 'q'"
        if ($eingabe -eq "q") { return }
        if ($eingabe -notmatch "^[1-7]$") {
            Write-Host "[FEHLER] Bitte 1-7 eingeben!" -ForegroundColor Red
            continue
        }
        $pos = FindeEinwurf $felder ([int]$eingabe)
        if (-not $pos) {
            Write-Host "[FEHLER] Spalte ist voll!" -ForegroundColor Red
            continue
        }
        $felder[$pos] = "X"
        $zug++

        if (PruefeSiegVG $felder "X") {
            ZeigeFeldVG $felder
            Write-Host "[VIER GEWINNT] Du hast gewonnen!" -ForegroundColor Green
            Read-Host "Enter zum Fortfahren"
            return
        }
        if ($zug -eq 42) {
            ZeigeFeldVG $felder
            Write-Host "[VIER GEWINNT] Unentschieden!" -ForegroundColor Yellow
            Read-Host "Enter zum Fortfahren"
            return
        }

        $pcSpalte = PcZugVG $felder
        $pcPos = FindeEinwurf $felder $pcSpalte
        $felder[$pcPos] = "O"
        $zug++
        Write-Host "[VIER GEWINNT] PC wirft in Spalte $pcSpalte" -ForegroundColor Magenta

        if (PruefeSiegVG $felder "O") {
            ZeigeFeldVG $felder
            Write-Host "[VIER GEWINNT] PC hat gewonnen!" -ForegroundColor Red
            Read-Host "Enter zum Fortfahren"
            return
        }
        if ($zug -eq 42) {
            ZeigeFeldVG $felder
            Write-Host "[VIER GEWINNT] Unentschieden!" -ForegroundColor Yellow
            Read-Host "Enter zum Fortfahren"
            return
        }
    }
}