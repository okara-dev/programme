import pygame
import os
import math

#pygame starten
pygame.init()
pygame.mixer.init()

#fenster einrichten
BREITE = 800
HOEHE = 600
bildschirm = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Area51")
takt = pygame.time.Clock()

#farben
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
GELB = (255, 255, 0)
GRUEN = (0, 255, 0)
BLAU = (100, 150, 255)
ROT = (255, 0, 0)

# Highscore
highscore_datei = "highscore.txt"

def lade_highscore():
    #lädt highscore aus datei
    if os.path.exists(highscore_datei):
        try:
            with open(highscore_datei, "r") as datei:
                return int(datei.read())
        except:
            print("Datei konnte nicht gelsen werden..")
            return 0
    else:
        print("Datei existiert nicht")
        return 0

def speichere_highscore(punkte):
    #speichert highscore in datei
    with open(highscore_datei, "w") as datei:
        datei.write(str(punkte))

# Bilder und Musik

#hintergrundbild laden
try:
    hintergrund = pygame.image.load("h.jpg")
    hintergrund = pygame.transform.scale(hintergrund, (BREITE, HOEHE))
except:
    print("Fehler: hintergrund.jpg nicht gefunden!")
    hintergrund = None

#hintergrundmusik laden
try:
    pygame.mixer.music.load("musik.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("Fehler: musik.mp3 nicht gefunden!")

# Spieler 
class Spieler:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.groesse = 20
        self.geschwindigkeit = 6
    
    def bewege(self, links, rechts):
        #bewegt spieler nur innerhalb des bildschirms
        if links and self.x > 0:
            self.x -= self.geschwindigkeit
        if rechts and self.x < BREITE - self.groesse:
            self.x += self.geschwindigkeit
    
    def zeichne(self, bildschirm):
        #strichmännchen zeichnen
        mitte_x = self.x + self.groesse // 2
        mitte_y = self.y + 10
        
        #kopf
        pygame.draw.circle(bildschirm, WEISS, (mitte_x, mitte_y - 8), 6)
        #korper
        pygame.draw.line(bildschirm, WEISS, (mitte_x, mitte_y - 2), (mitte_x, mitte_y + 8), 2)
        #arme
        pygame.draw.line(bildschirm, WEISS, (mitte_x, mitte_y + 2), (mitte_x - 6, mitte_y + 4), 2)
        pygame.draw.line(bildschirm, WEISS, (mitte_x, mitte_y + 2), (mitte_x + 6, mitte_y + 4), 2)
        #beine
        pygame.draw.line(bildschirm, WEISS, (mitte_x, mitte_y + 8), (mitte_x - 4, mitte_y + 14), 2)
        pygame.draw.line(bildschirm, WEISS, (mitte_x, mitte_y + 8), (mitte_x + 4, mitte_y + 14), 2)
        #augen
        pygame.draw.circle(bildschirm, BLAU, (mitte_x - 2, mitte_y - 10), 1)
        pygame.draw.circle(bildschirm, BLAU, (mitte_x + 2, mitte_y - 10), 1)

# Gegner
class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.groesse = 25
        self.geschwindigkeit = 3
    
    def bewege(self):
        #bewegt sich hin und her
        self.x += self.geschwindigkeit
        if self.x <= 0 or self.x >= BREITE - self.groesse:
            self.geschwindigkeit = -self.geschwindigkeit
    
    def schiesse(self, spieler):
        #erzeugt neuen laser der auf spieler zielt
        return Laser(
            self.x + self.groesse // 2,
            self.y + self.groesse,
            spieler.x + spieler.groesse // 2,
            spieler.y + spieler.groesse // 2
        )
    
    def zeichne(self, bildschirm):
        #alien zeichnen
        mitte_x = self.x + self.groesse // 2
        mitte_y = self.y + 12
        
        #korper
        pygame.draw.ellipse(bildschirm, GRUEN, (mitte_x - 10, mitte_y - 12, 20, 18))
        pygame.draw.rect(bildschirm, GRUEN, (mitte_x - 6, mitte_y - 2, 12, 15))
        #beine
        pygame.draw.line(bildschirm, GRUEN, (mitte_x - 4, mitte_y + 13), (mitte_x - 6, mitte_y + 18), 3)
        pygame.draw.line(bildschirm, GRUEN, (mitte_x + 4, mitte_y + 13), (mitte_x + 6, mitte_y + 18), 3)
        #augen
        pygame.draw.circle(bildschirm, GELB, (mitte_x - 4, mitte_y - 8), 3)
        pygame.draw.circle(bildschirm, GELB, (mitte_x + 4, mitte_y - 8), 3)
        pygame.draw.circle(bildschirm, SCHWARZ, (mitte_x - 4, mitte_y - 8), 1)
        pygame.draw.circle(bildschirm, SCHWARZ, (mitte_x + 4, mitte_y - 8), 1)
        #mund
        pygame.draw.arc(bildschirm, SCHWARZ, (mitte_x - 5, mitte_y - 6, 10, 8), 0, 3.14, 2)

# Laser
class Laser:
    def __init__(self, x, y, ziel_x, ziel_y):
        self.x = x
        self.y = y
        self.breite = 6
        self.hoehe = 12
        self.geschwindigkeit = 18
        
        #berechnet richtung zum ziel
        abstand_x = ziel_x - x
        abstand_y = ziel_y - y
        entfernung = math.sqrt(abstand_x**2 + abstand_y**2)
        
        if entfernung != 0:
            self.vx = abstand_x / entfernung * self.geschwindigkeit
            self.vy = abstand_y / entfernung * self.geschwindigkeit
        else:
            self.vx = 0
            self.vy = self.geschwindigkeit
    
    def bewege(self):
        #laser bewegen
        self.x += self.vx
        self.y += self.vy
    
    def zeichne(self, bildschirm):
        #laser zeichnen
        pygame.draw.rect(bildschirm, GELB, (int(self.x), int(self.y), self.breite, self.hoehe))
    
    def hol_rechteck(self):
        #gibt die hitbox zurück für kollisionsprüfung
        return pygame.Rect(int(self.x), int(self.y), self.breite, self.hoehe)


# Haupt Klasse für das ganze spiel
class Game:
    def __init__(self):
        #spiel starten
        self.highscore = lade_highscore()
        self.zuruecksetzen()
    
    def zuruecksetzen(self):
        # Alles auf Anfang setzen
        self.spieler = Spieler(BREITE // 2, HOEHE - 70)
        self.alien = Alien(BREITE // 2, 60)
        self.laser_liste = []
        self.schuss_timer = 0
        self.punkte = 0
        self.laeuft = True
    
    def startbildschirm_zeigen(self):
        #startbildschirm anzeigen
        bildschirm.fill(SCHWARZ)
        if hintergrund:
            bildschirm.blit(hintergrund, (0, 0))
        
        schrift_gross = pygame.font.SysFont("Arial", 64)
        schrift_mittel = pygame.font.SysFont("Arial", 36)
        schrift_klein = pygame.font.SysFont("Arial", 28)
        
        #titel
        titel = schrift_gross.render("AREA 51", True, GELB)
        bildschirm.blit(titel, (BREITE // 2 - titel.get_width() // 2, HOEHE // 4))
        
        #highscore
        highscore_text = schrift_mittel.render(f"Highscore: {self.highscore}", True, GELB)
        bildschirm.blit(highscore_text, (BREITE // 2 - highscore_text.get_width() // 2, HOEHE // 4 + 80))
        
        #optionen
        start_text = schrift_klein.render("Drücke LEERTASTE zum Starten", True, WEISS)
        beenden_text = schrift_klein.render("Drücke T zum Beenden", True, ROT)
        bildschirm.blit(start_text, (BREITE // 2 - start_text.get_width() // 2, HOEHE // 2))
        bildschirm.blit(beenden_text, (BREITE // 2 - beenden_text.get_width() // 2, HOEHE // 2 + 50))
        
        pygame.display.flip()
        
        #warte auf eingabe
        warte = True
        while warte:
            for ereignis in pygame.event.get():
                if ereignis.type == pygame.QUIT:
                    return False
                if ereignis.type == pygame.KEYDOWN:
                    if ereignis.key == pygame.K_SPACE:
                        return True
                    if ereignis.key == pygame.K_t:
                        return False
    
    def gameover_zeigen(self):
        # Game Over Bildschirm anzeigen
        bildschirm.fill(SCHWARZ)
        if hintergrund:
            bildschirm.blit(hintergrund, (0, 0))
        
        #prüfen ob neuer Highscore
        neuer_highscore = False
        if self.punkte > self.highscore:
            self.highscore = self.punkte
            speichere_highscore(self.highscore)
            neuer_highscore = True
        
        schrift_gross = pygame.font.SysFont("Arial", 64)
        schrift_mittel = pygame.font.SysFont("Arial", 36)
        schrift_klein = pygame.font.SysFont("Arial", 32)
        
        #game over text
        gameover_text = schrift_gross.render("GAME OVER!", True, ROT)
        bildschirm.blit(gameover_text, (BREITE // 2 - gameover_text.get_width() // 2, HOEHE // 4))
        
        #punkte anzeigen
        punkte_text = schrift_mittel.render(f"Deine Punkte: {self.punkte}", True, WEISS)
        bildschirm.blit(punkte_text, (BREITE // 2 - punkte_text.get_width() // 2, HOEHE // 2 - 40))
        
        #highscore anzeigen
        if neuer_highscore:
            highscore_text = schrift_klein.render(f"NEUER HIGHSCORE: {self.highscore}!", True, GELB)
        else:
            highscore_text = schrift_klein.render(f"Highscore: {self.highscore}", True, GELB)
        bildschirm.blit(highscore_text, (BREITE // 2 - highscore_text.get_width() // 2, HOEHE // 2))
        
        #optionen
        neustart_text = schrift_klein.render("Drücke R für Neustart", True, GRUEN)
        beenden_text = schrift_klein.render("Drücke T zum Beenden", True, ROT)
        bildschirm.blit(neustart_text, (BREITE // 2 - neustart_text.get_width() // 2, HOEHE // 2 + 80))
        bildschirm.blit(beenden_text, (BREITE // 2 - beenden_text.get_width() // 2, HOEHE // 2 + 120))
        
        pygame.display.flip()
        
        #warte auf eingabe
        warte = True
        while warte:
            for ereignis in pygame.event.get():
                if ereignis.type == pygame.QUIT:
                    return False
                if ereignis.type == pygame.KEYDOWN:
                    if ereignis.key == pygame.K_r:
                        return True
                    if ereignis.key == pygame.K_t:
                        return False


    # HAUPTSPIEL SCHLEIFE    
    def spielen(self):
        while self.laeuft:
            takt.tick(60)
            
            #hintergrund zeichnen
            if hintergrund:
                bildschirm.blit(hintergrund, (0, 0))
            else:
                bildschirm.fill(BLAU)
            
            #events prüfen
            for ereignis in pygame.event.get():
                if ereignis.type == pygame.QUIT:
                    self.laeuft = False
                if ereignis.type == pygame.KEYDOWN and ereignis.key == pygame.K_t:
                    self.laeuft = False
            
            #spieler bewegen
            tasten = pygame.key.get_pressed()
            self.spieler.bewege(tasten[pygame.K_LEFT], tasten[pygame.K_RIGHT])
            
            #alien bewegen
            self.alien.bewege()
            
            #alien schießt alle 45 frames
            self.schuss_timer += 1
            if self.schuss_timer > 45:
                self.laser_liste.append(self.alien.schiesse(self.spieler))
                self.schuss_timer = 0
            
            #laser bewegen und kollision prüfen
            for laser in self.laser_liste[:]:
                laser.bewege()
                
                #laser verschwindet unten -> punkt
                if laser.y > HOEHE:
                    self.laser_liste.remove(laser)
                    self.punkte += 1
                    continue
                
                #prüfen ob spieler getroffen wurde
                if laser.hol_rechteck().colliderect(pygame.Rect(
                    self.spieler.x, self.spieler.y, 
                    self.spieler.groesse, self.spieler.groesse
                )):
                    if self.gameover_zeigen():
                        self.zuruecksetzen()
                    else:
                        self.laeuft = False
                    break
            
            #alles zeichnen
            self.spieler.zeichne(bildschirm)
            self.alien.zeichne(bildschirm)
            for laser in self.laser_liste:
                laser.zeichne(bildschirm)
            
            #punkte anzeigen (oben links)
            punkte_text = pygame.font.SysFont("Arial", 30).render(f"Punkte: {self.punkte}", True, WEISS)
            pygame.draw.rect(bildschirm, SCHWARZ, (5, 5, 120, 35))
            pygame.draw.rect(bildschirm, WEISS, (5, 5, 120, 35), 2)
            bildschirm.blit(punkte_text, (10, 10))
            
            #highscore anzeigen (oben rechts)
            highscore_text = pygame.font.SysFont("Arial", 30).render(f"Bester: {self.highscore}", True, GELB)
            pygame.draw.rect(bildschirm, SCHWARZ, (BREITE - 120, 5, 115, 35))
            pygame.draw.rect(bildschirm, GELB, (BREITE - 120, 5, 115, 35), 2)
            bildschirm.blit(highscore_text, (BREITE - 115, 10))
            
            #steuerungshinweis unten
            steuerung = pygame.font.SysFont("Arial", 20).render("← → Bewegen | T = Beenden", True, WEISS)
            bildschirm.blit(steuerung, (BREITE // 2 - 100, HOEHE - 30))
            
            pygame.display.flip()

# Spiel starten
spiel = Game()

if spiel.startbildschirm_zeigen():
    spiel.spielen()

pygame.quit()