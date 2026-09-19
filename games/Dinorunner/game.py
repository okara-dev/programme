"""
Chrome Dino Runner - Pygame Nachbau
Verhält sich nahezu identisch zum Chrome-Original.
"""
import pygame
import random
import sys

# ─── Initialisierung ─────────────────────────────────────
pygame.init()
pygame.mixer.init()

# Bildschirm (ähnlich dem Original-Canvas, etwas größer)
SCREEN_W, SCREEN_H = 900, 300
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Chrome Dino Runner 🦖")
clock = pygame.time.Clock()
FPS = 60

# ─── Farben (Original-Schwarz-Weiß-Stil) ─────────────────
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
GRAU = (120, 120, 120)
HINTERGRUND = (247, 247, 247)  # heller Original-Hintergrund

# ─── Physik-Konstanten (aus Chromium-Quellcode) ──────────
GRAVITATION = 0.6                    # Pixel/Frame²
SPRUNGGESCHWINDIGKEIT = -10          # Pixel/Frame
FALLGESCHWINDIGKEIT = 2              # Schneller Fall nach Tastenloslassen
MIN_SPRUNGHOEHE = 35                 # Ab dieser Höhe greift der schnelle Fall
MAX_GESCHWINDIGKEIT = 13             # Höchstgeschwindigkeit (Pixel/Frame)
START_GESCHWINDIGKEIT = 6            # Startgeschwindigkeit
BESCHLEUNIGUNG = 0.001               # Pro Frame
SCHONZEIT = 3000                     # Startphase ohne Hindernisse (ms)

# Boden-Y-Koordinate
BODEN_Y = SCREEN_H - 60

# ─── Soundeffekte (mit Pygame synthetisiert) ─────────────
def erzeuge_sprung_sound():
    """Aufsteigender Ton für den Sprung."""
    import numpy as np
    rate = 22050
    dauer = 0.08
    n = int(rate * dauer)
    freqs = np.linspace(400, 900, n)
    phase = np.cumsum(2 * np.pi * freqs / rate)
    buf = (np.sin(phase) * 0.4 * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack((buf, buf)))

def erzeuge_tod_sound():
    """Absteigender Ton beim Tod."""
    import numpy as np
    rate = 22050
    dauer = 0.3
    n = int(rate * dauer)
    freqs = np.linspace(600, 100, n)
    phase = np.cumsum(2 * np.pi * freqs / rate)
    buf = (np.sin(phase) * 0.4 * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack((buf, buf)))

def erzeuge_punkt_sound():
    """Kurzer hoher Piepton bei Punkte-Meilensteinen."""
    import numpy as np
    rate = 22050
    n = int(rate * 0.1)
    buf = (np.sin(2 * np.pi * 1200 * np.arange(n) / rate) * 0.3 * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack((buf, buf)))

try:
    SND_SPRUNG = erzeuge_sprung_sound()
    SND_TOD = erzeuge_tod_sound()
    SND_PUNKT = erzeuge_punkt_sound()
except Exception:
    SND_SPRUNG = SND_TOD = SND_PUNKT = None
    print("Hinweis: Für Soundeffekte 'numpy' installieren (pip install numpy)")

# ─── Schriften ───────────────────────────────────────────
schrift_pfad = pygame.font.match_font("couriernew,dejavusansmono,monospace")
try:
    SCHRIFT = pygame.font.Font(schrift_pfad, 20)
    SCHRIFT_KLEIN = pygame.font.Font(schrift_pfad, 16)
    SCHRIFT_GROSS = pygame.font.Font(schrift_pfad, 40)
except Exception:
    SCHRIFT = pygame.font.SysFont("monospace", 20)
    SCHRIFT_KLEIN = pygame.font.SysFont("monospace", 16)
    SCHRIFT_GROSS = pygame.font.SysFont("monospace", 40)

# ═══════════════════════════════════════════════════════════
#  Zeichenfunktionen (rein per Code, keine Bilddateien nötig)
# ═══════════════════════════════════════════════════════════
def zeichne_dino(flaeche, x, y, duckend=False, tot=False):
    """Zeichnet den Dino im Pixel-Stil."""
    c = (200, 60, 60) if tot else (80, 80, 80)

    if duckend:
        # Duckende Form: lang und flach
        pygame.draw.rect(flaeche, c, (x + 8, y + 14, 36, 16))   # Körper
        pygame.draw.rect(flaeche, c, (x + 38, y + 10, 22, 18))  # Kopf
        pygame.draw.rect(flaeche, c, (x - 2, y + 16, 14, 10))   # Schwanz
        # Auge
        pygame.draw.rect(flaeche, WEISS, (x + 50, y + 14, 4, 4))
        pygame.draw.rect(flaeche, c, (x + 51, y + 15, 2, 2))
        # Beine
        pygame.draw.rect(flaeche, c, (x + 14, y + 30, 4, 8))
        pygame.draw.rect(flaeche, c, (x + 26, y + 30, 4, 8))
    else:
        # Stehende / laufende Form
        pygame.draw.rect(flaeche, c, (x + 8, y + 10, 20, 22))   # Körper
        pygame.draw.rect(flaeche, c, (x + 22, y + 2, 22, 20))   # Kopf
        pygame.draw.rect(flaeche, c, (x - 4, y + 14, 14, 10))   # Schwanz
        pygame.draw.rect(flaeche, c, (x + 24, y + 18, 10, 4))   # Arm

        # Beinanimation (abwechselnd)
        if not tot:
            t = pygame.time.get_ticks() // 100
            if t % 2 == 0:
                pygame.draw.rect(flaeche, c, (x + 12, y + 32, 5, 12))
                pygame.draw.rect(flaeche, c, (x + 22, y + 30, 5, 10))
            else:
                pygame.draw.rect(flaeche, c, (x + 12, y + 30, 5, 10))
                pygame.draw.rect(flaeche, c, (x + 22, y + 32, 5, 12))
        else:
            pygame.draw.rect(flaeche, c, (x + 12, y + 32, 5, 12))
            pygame.draw.rect(flaeche, c, (x + 22, y + 32, 5, 12))

        # Auge
        pygame.draw.rect(flaeche, WEISS, (x + 34, y + 6, 5, 5))
        pygame.draw.rect(flaeche, c, (x + 36, y + 7, 3, 3))

def zeichne_kaktus(flaeche, x, y, breite, hoehe):
    """Zeichnet einen Kaktus aus einfachen Rechtecken."""
    c = (80, 80, 80)
    stamm_b = max(8, breite // 3)
    pygame.draw.rect(flaeche, c, (x + breite // 2 - stamm_b // 2, y, stamm_b, hoehe))

    if breite > 20:
        # Linker Arm
        pygame.draw.rect(flaeche, c, (x, y + hoehe // 3, breite // 3, 6))
        pygame.draw.rect(flaeche, c, (x, y + hoehe // 4, 6, hoehe // 3))
        # Rechter Arm
        pygame.draw.rect(flaeche, c, (x + breite - breite // 3, y + hoehe // 2, breite // 3, 6))
        pygame.draw.rect(flaeche, c, (x + breite - 6, y + hoehe // 3, 6, hoehe // 3))

def zeichne_vogel(flaeche, x, y, frame):
    """Zeichnet einen Flugsaurier (einfache Vogelform)."""
    c = (80, 80, 80)
    pygame.draw.rect(flaeche, c, (x, y + 8, 24, 8))        # Körper
    pygame.draw.rect(flaeche, c, (x + 20, y + 4, 10, 10))  # Kopf
    pygame.draw.rect(flaeche, c, (x + 28, y + 8, 8, 3))    # Schnabel

    if frame == 0:  # Flügel oben
        pygame.draw.polygon(flaeche, c, [
            (x + 6, y + 8), (x + 16, y - 8), (x + 22, y + 8)
        ])
    else:           # Flügel unten
        pygame.draw.polygon(flaeche, c, [
            (x + 6, y + 8), (x + 16, y + 24), (x + 22, y + 8)
        ])

# ═══════════════════════════════════════════════════════════
#  Spielfiguren
# ═══════════════════════════════════════════════════════════
class Dino:
    """Der spielbare Dinosaurier."""
    BREITE, HOEHE = 44, 48
    DUCK_BREITE, DUCK_HOEHE = 60, 32

    def __init__(self):
        self.zuruecksetzen()

    def zuruecksetzen(self):
        self.x = 50
        self.y = BODEN_Y - self.HOEHE
        self.geschw_y = 0
        self.auf_boden = True
        self.duckend = False
        self.lebt = True
        self.sprung_gehalten = False
        self.min_hoehe_erreicht = False
        self.max_hoehe = 0
        self.start_y = BODEN_Y - self.HOEHE

    @property
    def rechteck(self):
        if self.duckend and self.auf_boden:
            return pygame.Rect(self.x, self.y, self.DUCK_BREITE, self.DUCK_HOEHE)
        return pygame.Rect(self.x, self.y, self.BREITE, self.HOEHE)

    def springen(self):
        if self.auf_boden and self.lebt:
            self.geschw_y = SPRUNGGESCHWINDIGKEIT
            self.auf_boden = False
            self.sprung_gehalten = True
            self.min_hoehe_erreicht = False
            self.max_hoehe = 0
            if SND_SPRUNG:
                SND_SPRUNG.play()

    def sprung_loslassen(self):
        """Loslassen: falls Mindesthöhe erreicht → schneller Fall (kurzer Sprung)."""
        self.sprung_gehalten = False
        if (not self.auf_boden
                and self.min_hoehe_erreicht
                and self.geschw_y < FALLGESCHWINDIGKEIT):
            self.geschw_y = FALLGESCHWINDIGKEIT

    def ducken(self, aktiv):
        if self.lebt:
            self.duckend = aktiv and self.auf_boden

    def aktualisieren(self, geschwindigkeit):
        """Physik-Update pro Frame."""
        if not self.lebt:
            return

        if not self.auf_boden:
            self.geschw_y += GRAVITATION
            self.y += self.geschw_y

            aktuelle_hoehe = self.start_y - self.y
            if aktuelle_hoehe > self.max_hoehe:
                self.max_hoehe = aktuelle_hoehe
            if aktuelle_hoehe >= MIN_SPRUNGHOEHE:
                self.min_hoehe_erreicht = True

            # Landung
            if self.y >= BODEN_Y - self.HOEHE:
                self.y = BODEN_Y - self.HOEHE
                self.geschw_y = 0
                self.auf_boden = True
                self.sprung_gehalten = False
                self.min_hoehe_erreicht = False

        # In der Luft nicht ducken
        if not self.auf_boden:
            self.duckend = False

    def sterben(self):
        if self.lebt:
            self.lebt = False
            self.duckend = False
            if SND_TOD:
                SND_TOD.play()

class Hindernis:
    """Hindernis (Kaktus oder Vogel)."""
    KAKTUS_KLEIN = "kaktus_klein"
    KAKTUS_GROSS = "kaktus_gross"
    VOGEL = "vogel"

    def __init__(self, art, x, geschwindigkeit):
        self.art = art
        self.x = x
        self.ueberholt = False
        self.frame = 0
        self.frame_timer = 0

        if art == self.KAKTUS_KLEIN:
            self.breite = random.choice([17, 34])
            self.hoehe = 35
            self.y = BODEN_Y - self.hoehe
        elif art == self.KAKTUS_GROSS:
            self.breite = random.choice([25, 50])
            self.hoehe = 50
            self.y = BODEN_Y - self.hoehe
        else:  # VOGEL
            self.breite = 46
            self.hoehe = 30
            self.y = BODEN_Y - random.choice([50, 80, 110])

    @property
    def rechteck(self):
        return pygame.Rect(self.x, self.y, self.breite, self.hoehe)

    def aktualisieren(self, geschwindigkeit, dt):
        self.x -= geschwindigkeit * 60 * dt

        if self.art == self.VOGEL:
            self.frame_timer += dt
            if self.frame_timer >= 0.15:
                self.frame_timer = 0
                self.frame = 1 - self.frame

    def zeichnen(self, flaeche):
        if self.art in (self.KAKTUS_KLEIN, self.KAKTUS_GROSS):
            zeichne_kaktus(flaeche, int(self.x), int(self.y), self.breite, self.hoehe)
        else:
            zeichne_vogel(flaeche, int(self.x), int(self.y), self.frame)

class Wolke:
    """Hintergrund-Wolke."""
    def __init__(self):
        self.x = SCREEN_W + random.randint(0, 200)
        self.y = random.randint(30, BODEN_Y - 120)
        self.tempo_faktor = random.uniform(0.3, 0.6)
        self.breite = random.randint(40, 70)

    def aktualisieren(self, geschwindigkeit, dt):
        self.x -= geschwindigkeit * 60 * dt * self.tempo_faktor

    @property
    def ausserhalb(self):
        return self.x + self.breite < 0

    def zeichnen(self, flaeche):
        c = (200, 200, 200)
        pygame.draw.ellipse(flaeche, c, (self.x, self.y, self.breite, 16))
        pygame.draw.ellipse(flaeche, c, (self.x + 12, self.y - 8, self.breite - 20, 18))

# ═══════════════════════════════════════════════════════════
#  Haupt-Spielklasse
# ═══════════════════════════════════════════════════════════
class Spiel:
    def __init__(self):
        self.dino = Dino()
        self.hindernisse = []
        self.wolken = []
        self.geschwindigkeit = START_GESCHWINDIGKEIT
        self.punkte = 0
        self.highscore = 0
        self.laeuft = False
        self.spiel_vorbei = False
        self.verstrichene_zeit = 0
        self.spawn_timer = 0
        self.wolken_timer = 0
        self.naechster_abstand = 400
        self.letzte_art = None
        self.duplikat_zaehler = 0

        # Highscore laden
        try:
            with open("dino_highscore.txt", "r") as f:
                self.highscore = int(f.read().strip())
        except Exception:
            self.highscore = 0

    def zuruecksetzen(self):
        self.dino.zuruecksetzen()
        self.hindernisse.clear()
        self.wolken.clear()
        self.geschwindigkeit = START_GESCHWINDIGKEIT
        self.punkte = 0
        self.spiel_vorbei = False
        self.verstrichene_zeit = 0
        self.spawn_timer = 0
        self.wolken_timer = 0
        self.naechster_abstand = 400
        self.letzte_art = None
        self.duplikat_zaehler = 0

    def starten(self):
        self.zuruecksetzen()
        self.laeuft = True

    def highscore_speichern(self):
        if self.punkte > self.highscore:
            self.highscore = self.punkte
            try:
                with open("dino_highscore.txt", "w") as f:
                    f.write(str(self.highscore))
            except Exception:
                pass

    def hindernis_spawnen(self):
        """Erzeugt ein Hindernis nach den Original-Regeln."""
        if self.verstrichene_zeit < SCHONZEIT:
            return

        moeglichkeiten = [Hindernis.KAKTUS_KLEIN, Hindernis.KAKTUS_GROSS]
        if self.geschwindigkeit > 4:
            moeglichkeiten.append(Hindernis.VOGEL)

        art = random.choice(moeglichkeiten)

        # Nicht 3x dieselbe Art hintereinander
        if art == self.letzte_art:
            self.duplikat_zaehler += 1
            if self.duplikat_zaehler >= 2:
                moeglichkeiten.remove(art)
                art = random.choice(moeglichkeiten)
                self.duplikat_zaehler = 0
        else:
            self.duplikat_zaehler = 0

        self.letzte_art = art
        x = SCREEN_W + 20
        neues_hindernis = Hindernis(art, x, self.geschwindigkeit)

        # Abstand zum nächsten Hindernis (Original-Regel)
        self.naechster_abstand = neues_hindernis.breite * self.geschwindigkeit + random.randint(80, 180)
        self.hindernisse.append(neues_hindernis)

    def aktualisieren(self, dt):
        if not self.laeuft or self.spiel_vorbei:
            return

        self.verstrichene_zeit += dt * 1000
        self.geschwindigkeit = min(MAX_GESCHWINDIGKEIT,
                                   self.geschwindigkeit + BESCHLEUNIGUNG * 60 * dt)

        # Dino
        self.dino.aktualisieren(self.geschwindigkeit)

        # Hindernisse
        for h in self.hindernisse:
            h.aktualisieren(self.geschwindigkeit, dt)
        self.hindernisse = [h for h in self.hindernisse if h.x + h.breite > -50]

        # Wolken
        self.wolken_timer -= dt
        if self.wolken_timer <= 0:
            self.wolken.append(Wolke())
            self.wolken_timer = random.uniform(1.5, 4.0)
        for w in self.wolken:
            w.aktualisieren(self.geschwindigkeit, dt)
        self.wolken = [w for w in self.wolken if not w.ausserhalb]

        # Neue Hindernisse
        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and self.verstrichene_zeit >= SCHONZEIT:
            self.hindernis_spawnen()
            verzogerung_frames = self.naechster_abstand / max(self.geschwindigkeit, 1)
            self.spawn_timer = verzogerung_frames / 60.0

        # Kollision
        dino_rechteck = self.dino.rechteck
        for h in self.hindernisse:
            if dino_rechteck.colliderect(h.rechteck):
                self.dino.sterben()
                self.spiel_vorbei = True
                self.highscore_speichern()
                return

        # Punkte (basierend auf Geschwindigkeit)
        alte_punkte = self.punkte
        self.punkte += self.geschwindigkeit * 60 * dt * 0.05

        # Alle 100 Punkte → Ton
        if int(self.punkte / 100) > int(alte_punkte / 100):
            if SND_PUNKT and not self.spiel_vorbei:
                SND_PUNKT.play()

    def zeichnen(self, flaeche):
        flaeche.fill(HINTERGRUND)

        # Wolken
        for w in self.wolken:
            w.zeichnen(flaeche)

        # Boden
        pygame.draw.line(flaeche, GRAU, (0, BODEN_Y), (SCREEN_W, BODEN_Y), 2)
        # Boden-Textur (bewegte Punkte)
        offset = int((pygame.time.get_ticks() // 30 * self.geschwindigkeit) % 20)
        for i in range(-20, SCREEN_W + 20, 20):
            px = i - offset
            if 0 <= px < SCREEN_W:
                pygame.draw.circle(flaeche, GRAU, (px, BODEN_Y + 6), 1)

        # Hindernisse
        for h in self.hindernisse:
            h.zeichnen(flaeche)

        # Dino
        zeichne_dino(flaeche, int(self.dino.x), int(self.dino.y),
                     self.dino.duckend, not self.dino.lebt)

        # Punkte (rechts oben, wie im Original)
        punkte_text = str(int(self.punkte)).zfill(5)
        if self.highscore > 0:
            hi_text = f"HI {str(int(self.highscore)).zfill(5)}"
            hi_surf = SCHRIFT_KLEIN.render(hi_text, True, GRAU)
            flaeche.blit(hi_surf, (SCREEN_W - 180, 20))

        punkte_surf = SCHRIFT.render(punkte_text, True, GRAU)
        flaeche.blit(punkte_surf, (SCREEN_W - 80, 20))

        # Game-Over-Overlay
        if self.spiel_vorbei:
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200))
            flaeche.blit(overlay, (0, 0))

            go_surf = SCHRIFT_GROSS.render("G A M E   O V E R", True, (80, 80, 80))
            go_rect = go_surf.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 30))
            flaeche.blit(go_surf, go_rect)

            neustart = SCHRIFT.render("Leertaste / Klick zum Neustart", True, GRAU)
            neustart_rect = neustart.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 30))
            flaeche.blit(neustart, neustart_rect)

            endpunkte = SCHRIFT_KLEIN.render(f"Punkte: {int(self.punkte)}", True, GRAU)
            ep_rect = endpunkte.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 60))
            flaeche.blit(endpunkte, ep_rect)

# ═══════════════════════════════════════════════════════════
#  Einstiegspunkt
# ═══════════════════════════════════════════════════════════
def main():
    spiel = Spiel()

    # ─── Startbildschirm ───
    warten = True
    while warten:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                warten = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                warten = False

        screen.fill(HINTERGRUND)
        zeichne_dino(screen, 50, BODEN_Y - 48)
        pygame.draw.line(screen, GRAU, (0, BODEN_Y), (SCREEN_W, BODEN_Y), 2)

        titel = SCHRIFT_GROSS.render("DINO RUNNER", True, (80, 80, 80))
        screen.blit(titel, titel.get_rect(center=(SCREEN_W // 2, 100)))

        hinweis = SCHRIFT.render("Leertaste zum Starten", True, GRAU)
        screen.blit(hinweis, hinweis.get_rect(center=(SCREEN_W // 2, 160)))

        if spiel.highscore > 0:
            hs = SCHRIFT_KLEIN.render(f"Highscore: {int(spiel.highscore)}", True, GRAU)
            screen.blit(hs, hs.get_rect(center=(SCREEN_W // 2, 200)))

        pygame.display.flip()

    # ─── Spiel starten ───
    spiel.starten()
    spiel.spawn_timer = 0.5

    # ─── Hauptschleife ───
    laeuft = True
    while laeuft:
        dt = clock.tick(FPS) / 1000.0
        dt = min(dt, 0.05)  # gegen große Sprünge

        # ─── Events ───
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                laeuft = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    laeuft = False

                if spiel.spiel_vorbei:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_RETURN):
                        spiel.starten()
                        spiel.spawn_timer = 0.5
                else:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        spiel.dino.springen()
                    if event.key == pygame.K_DOWN:
                        spiel.dino.ducken(True)

            if event.type == pygame.KEYUP:
                if not spiel.spiel_vorbei:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        spiel.dino.sprung_loslassen()
                    if event.key == pygame.K_DOWN:
                        spiel.dino.ducken(False)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if spiel.spiel_vorbei:
                    spiel.starten()
                    spiel.spawn_timer = 0.5
                else:
                    spiel.dino.springen()

            if event.type == pygame.MOUSEBUTTONUP:
                if not spiel.spiel_vorbei:
                    spiel.dino.sprung_loslassen()

        # ─── Update & Zeichnen ───
        spiel.aktualisieren(dt)
        spiel.zeichnen(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()