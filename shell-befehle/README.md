# 🐚 A-Z Shell Toolbox

Eine Sammlung praktischer PowerShell-Funktionen – von **`a`** bis **`z`**.
Jeder Buchstabe ist ein Befehl. Einfach eintippen und loslegen.

![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📦 Installation

1. Öffne PowerShell und finde dein Profil:
   ```powershell
   $PROFILE
2. Öffne die Datei (oder erstelle sie):
powershell
notepad $PROFILE
Kopiere den Inhalt von Microsoft.PowerShell_profile.ps1 hinein.
3. Profil neu laden:
powershell
. $PROFILE

Tippe hilfe – fertig! 🎉

## Hinweis
Beim ersten Start kann es sein, dass die Ausführung von Skripten blockiert wird.
Dann einmalig ausführen:

powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned


🕹️ Befehlsübersicht (A–Z)
Befehl	Beschreibung
a	Akkustatus anzeigen (Prozent, Restzeit, Status)
b	Browser öffnen (Standard: DeepSeek)
c	Taschenrechner öffnen
d	Datum anzeigen + Google Kalender öffnen
e	Terminal-Textfarbe ändern
f	Papierkorb leeren (mit Nachfrage)
g	GitHub öffnen
h	Zum Home-Verzeichnis wechseln
i	Bildschirm-Reiniger (Endlos-Animation)
j	Downloads-Ordner aufräumen
k	Münzwurf (Kopf / Zahl)
l	Ordner-Größe anzeigen
m	Passwort-Generator (20 Zeichen, Clipboard)
n	Notenpunkte berechnen
o	Zum Projekt-Ordner wechseln/erstellen
p	Autostart-Programme anzeigen
q	PC neustarten (10 Sek. Verzögerung)
r	Wikipedia-Artikel anzeigen (zufällig oder Suche)
s	Wetter anzeigen (Open-Meteo)
t	Speedtest (Ping, Download, Upload)
u	Windows-Updates suchen
v	Bilder/Screenshots löschen
w	Würfeln (1–6)
x	Office-Programm öffnen (Word, Excel, …)
y	Morsecode-Generator (hin & zurück)
z	Spiele-Menü 🎮
hilfe	Diese Übersicht anzeigen


🎮 Spiele-Menü (z)
Das Spiele-Menü vereint 5 Spiele in einem:
Nr.	Spiel	Beschreibung
1	Schere-Stein-Papier	Best of 5 gegen den PC
2	Blackjack	Klassisches 21 – Karte ziehen oder passen
3	Zahlenraten	1–100 erraten in max. 10 Versuchen
4	Tic-Tac-Toe	3×3 gegen PC (Felder A1–C3)
5	Vier gewinnt	6×7 gegen PC (Spalten 1–7)


📜 Lizenz
MIT – mach damit, was du willst. 