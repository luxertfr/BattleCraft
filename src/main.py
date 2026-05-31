import sqlite3
import pygame
from Button import Button
from Player import Player
from Card import Card, MobCard, FoodCard, EnchantedBookCard, ArtifactCard


pygame.init()

# --- SQL ---

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


# --- Paramétrage de couleur + les img + sons + boutons --- 
black = (0, 0, 0)
white = (255, 255, 255)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
input_rect = pygame.Rect(440, 360, 400, 50)
pygame.font.init()
font = pygame.font.Font("./assets/fonts/Minecraft.ttf", 40)

fond = pygame.image.load("./assets/img/minecraft-fond.jpg")
fond = fond.convert()
fond = pygame.transform.scale(fond, (1280, 720))

play_fond = pygame.image.load("./assets/img/play-fond.jpg")
play_fond = play_fond.convert()
play_fond = pygame.transform.scale(play_fond, (1280, 720))



welcome = pygame.image.load("./assets/img/name.png")
welcome = pygame.transform.scale(welcome, (640, 170))

pygame.mixer.init()
pygame.mixer_music.load("./assets/sounds/skylander.mp3")
pygame.mixer_music.play(-1, 0.0, 0)

bouton_jouer    = Button(None, (505, input_rect.y - 100), "./assets/img/play.png",  (320, 80), "PLAY")
bouton_decks    = Button(None, (505, input_rect.y),       "./assets/img/deck.png",  (320, 80), "DECK")
bouton_boutique = Button(None, (505, input_rect.y + 100), "./assets/img/shop.png",  (320, 80), "SHOP")
bouton_quitter  = Button(None, (505, input_rect.y + 200), "./assets/img/quit.png",  (320, 80), "QUIT")

cursor.execute("SELECT * FROM users")
data = cursor.fetchone()

player = None
if data:
    player = Player(data[0])
    player.set_argent(data[1])

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
        screen.blit(play_fond, (0, 0))
        
        
        COULEUR_GRILLE = (255, 255, 255)  
        COULEUR_ALLIE = (0, 255, 0)       
        COULEUR_ENNEMI = (255, 0, 0)      
        COULEUR_OBJET = (255, 215, 0)     
        
        

        LARGEUR_CARTE = 90
        HAUTEUR_CARTE = 130

        ALLIE_X = 100
        for i in range(3):
            y = 135 + (i * 150)  
            rect_allie = pygame.Rect(ALLIE_X, y, LARGEUR_CARTE, HAUTEUR_CARTE)
            pygame.draw.rect(screen, COULEUR_ALLIE, rect_allie, 2)
            
            txt = font.render(f"M{i+1}", True, COULEUR_ALLIE)
            screen.blit(txt, (ALLIE_X + 25, y + 45))

        
        ENNEMI_X = 1090
        for i in range(3):
            y = 135 + (i * 150)
            rect_ennemi = pygame.Rect(ENNEMI_X, y, LARGEUR_CARTE, HAUTEUR_CARTE)
            pygame.draw.rect(screen, COULEUR_ENNEMI, rect_ennemi, 2)
            
            txt = font.render(f"E{i+1}", True, COULEUR_ENNEMI)
            screen.blit(txt, (ENNEMI_X + 25, y + 45))


        OBJET_Y = 580
        LARGEUR_OBJET = 140   
        HAUTEUR_OBJET = 110

        slot_1_x = 480
        rect_objet1 = pygame.Rect(slot_1_x, OBJET_Y, LARGEUR_OBJET, HAUTEUR_OBJET)
        pygame.draw.rect(screen, COULEUR_OBJET, rect_objet1, 2)
        
        txt_obj1 = font.render("OBJ 1", True, COULEUR_OBJET)
        screen.blit(txt_obj1, (slot_1_x + 15, OBJET_Y + 35))

        slot_2_x = 660
        rect_objet2 = pygame.Rect(slot_2_x, OBJET_Y, LARGEUR_OBJET, HAUTEUR_OBJET)
        pygame.draw.rect(screen, COULEUR_OBJET, rect_objet2, 2)
        
        txt_obj2 = font.render("OBJ 2", True, COULEUR_OBJET)
        screen.blit(txt_obj2, (slot_2_x + 15, OBJET_Y + 35))
        
        # player1_circle = pygame.c
        
        
        

    elif etat == "SHOP":
        pass

    elif etat == "QUIT":
        pygame.quit()
        quit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()