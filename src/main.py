import sqlite3
import pygame
from Button import Button

import os



pygame.init()

conn = sqlite3.connect('./ma_base.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT,
        argent INTEGER
    )
""")
conn.commit()

black = (0, 0, 0)
white = (255, 255, 255)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
input_rect = pygame.Rect(440, 360, 400, 50)
pygame.font.init()
font = pygame.font.Font("./assets/Minecraft.ttf", 40)

fond = pygame.image.load("./assets/minecraft-fond.jpg")
fond = fond.convert()
fond = pygame.transform.scale(fond, (1280, 720))

welcome = pygame.image.load("./assets/name.png")
welcome = pygame.transform.scale(welcome, (640, 170))

pygame.mixer.init()
pygame.mixer_music.load("./assets/skylander.mp3")
pygame.mixer_music.play(-1, 0.0, 0)

bouton_jouer    = Button(None, (505, input_rect.y - 100), "./assets/play.png",  (320, 80), "PLAY")
bouton_decks    = Button(None, (505, input_rect.y),       "./assets/deck.png",  (320, 80), "DECK")
bouton_boutique = Button(None, (505, input_rect.y + 100), "./assets/shop.png",  (320, 80), "SHOP")
bouton_quitter  = Button(None, (505, input_rect.y + 200), "./assets/quit.png",  (320, 80), "QUIT")

cursor.execute("SELECT * FROM users")
data = cursor.fetchone()

running = True
text = ""
active = False
etat = "MENU"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        if etat == "MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_rect.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_RETURN:
                    if text.strip():
                        cursor.execute("INSERT INTO users (name, argent) VALUES (?, ?)", (text.strip(), 0))
                        conn.commit()
                        text = ""
                        cursor.execute("SELECT * FROM users")
                        data = cursor.fetchone()
                else:
                    text += event.unicode

    screen.fill((30, 30, 30))

    if etat == "MENU":
        screen.blit(fond, (0, 0))
        screen.blit(welcome, (335, input_rect.y - 300))
        if data is None:
            pygame.draw.rect(screen, black, input_rect, 2)
            text_surface = font.render(text, True, black)
            screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))
        else:
            
            bouton_jouer.afficher(screen)
            bouton_decks.afficher(screen)
            bouton_boutique.afficher(screen)
            bouton_quitter.afficher(screen)

            etat = bouton_jouer.verifier_clic(etat)
            etat = bouton_decks.verifier_clic(etat)
            etat = bouton_boutique.verifier_clic(etat)
            etat = bouton_quitter.verifier_clic(etat)

    elif etat == "PLAY":
        pass

    elif etat == "SHOP":
        pass

    elif etat == "QUIT":
        pygame.quit()
        quit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()