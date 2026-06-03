import sqlite3
import pygame
import json
from Button import Button
from Player import Player
from Card import Card, MobCard, FoodCard, EnchantedBookCard, ArtifactCard
from shop import Shop
from deck import Deck
from card_manager import ALL_CARDS



pygame.init()

# --- SQL ---
conn = sqlite3.connect('./ma_base.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT,
        argent INTEGER,
        deck TEXT
    )
""")
conn.commit()

# --- JSON ---
with open("./src/cards.json", "r", encoding="utf-8") as f:
    cards_config = json.load(f)

IMG_DECK = {}
for nom_carte, data_carte in cards_config.items():
    chemin_img = f"./assets/img/deck/{data_carte['image']}"
    try:
        loaded_img = pygame.image.load(chemin_img)
        IMG_DECK[nom_carte] = pygame.transform.scale(loaded_img, (120, 180))
    except pygame.error:
        print(f"Attention: impossible de charger l'image de {nom_carte} à {chemin_img}")
        secours = pygame.Surface((120, 180))
        secours.fill((60, 60, 90))
        IMG_DECK[nom_carte] = secours


# --- Instanciation des classes ---
shop = Shop()

# --- Paramétrage de couleur + les img + sons + boutons --- 
black = (0, 0, 0)
white = (255, 255, 255)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
input_rect = pygame.Rect(440, 360, 400, 50)
pygame.font.init()
font = pygame.font.Font("./assets/fonts/Minecraft.ttf", 40)
font_small = pygame.font.Font("./assets/fonts/Minecraft.ttf", 20)
font_XXSMALL = pygame.font.Font("./assets/fonts/Minecraft.ttf", 10)

fond = pygame.image.load("./assets/img/minecraft-fond.jpg")
fond = fond.convert()
fond = pygame.transform.scale(fond, (1280, 720))

play_fond = pygame.image.load("./assets/img/play-fond.jpg")
play_fond = play_fond.convert()
play_fond = pygame.transform.scale(play_fond, (1280, 720))

shop_fond = pygame.image.load("./assets/img/shop-fond.png")
shop_fond = shop_fond.convert()
shop_fond = pygame.transform.scale(shop_fond, (1280, 720))

welcome = pygame.image.load("./assets/img/name.png")
welcome = pygame.transform.scale(welcome, (640, 170))

pygame.mixer.init()
pygame.mixer_music.load("./assets/sounds/skylander.mp3")
pygame.mixer_music.play(-1, 0.0, 0)

son_clic = pygame.mixer.Sound("./assets/sounds/sfx-minecraft.mp3")

bouton_jouer    = Button(None, (505, input_rect.y - 100), "./assets/img/play.png",  (320, 80), "PLAY")
bouton_decks    = Button(None, (505, input_rect.y),       "./assets/img/deck.png",  (320, 80), "DECK")
bouton_boutique = Button(None, (505, input_rect.y + 100), "./assets/img/shop.png",  (320, 80), "SHOP")
bouton_quitter  = Button(None, (505, input_rect.y + 200), "./assets/img/quit.png",  (320, 80), "QUIT")

bouton_retour   = Button(None, (20, 20), "./assets/img/quit.png", (150, 50), "MENU")

scroll_x = 0

# --- Récupération et reconstruction du profil joueur ---
cursor.execute("SELECT * FROM users")
data = cursor.fetchone()

player = None
if data:

    player = Player(data[1])
    player.argent = data[2]
    

    if len(data) > 3 and data[3]:
        player.deck.cartes = [] 
        noms_sauvegardes = data[3].split(",")
        for nom in noms_sauvegardes:
            carte_trouvee = next((c for c in ALL_CARDS.values() if c.nom == nom), None)
            if carte_trouvee:
                player.deck.acheter_carte(carte_trouvee)
                if carte_trouvee in shop.cartes:
                    shop.acheter(carte_trouvee)
                    


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
                    pseudo = text.strip()
                    if pseudo:
                        cursor.execute("INSERT INTO users (name, argent, deck) VALUES (?, ?, ?)", (pseudo, 150, ""))
                        conn.commit()
                        text = ""
                        cursor.execute("SELECT * FROM users WHERE name = ?", (pseudo,))
                        data = cursor.fetchone()
                        if data:
                            player = Player(data[1])
                            player.argent = data[2]
                else:
                    text += event.unicode

        # --- Détection des clics dans la Boutique ---
        elif etat == "SHOP":
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                for index, carte in enumerate(shop.cartes):
                   
                    x = 100 + (index * 220) - scroll_x
                    y = 200
                    rect_carte = pygame.Rect(x, y, 180, 260)
                    
                    if rect_carte.collidepoint(event.pos):
                        if player and player.get_argent() >= carte.prix:
                            player.perdre_argent(carte.prix) 
                            player.ajouter_carte(carte)      
                            shop.acheter(carte)              
                            son_clic.play()
                            break 
                        else:
                            print("Pas assez d'argent !")

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

            etat = bouton_jouer.verifier_clic(etat, son_clic)
            etat = bouton_decks.verifier_clic(etat, son_clic)
            etat = bouton_boutique.verifier_clic(etat, son_clic)
            etat = bouton_quitter.verifier_clic(etat, son_clic)

    elif etat == "PLAY":
        screen.blit(play_fond, (0, 0))
        etat = bouton_retour.verifier_clic(etat, son_clic)
        
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

    elif etat == "DECK":
        screen.fill((40, 30, 40)) 
        etat = bouton_retour.verifier_clic(etat, son_clic)
        bouton_retour.afficher(screen)
        
        if player:
            titre = font.render(f"DECK DE {player.name.upper()}", True, white)
            screen.blit(titre, (450, 30))
            cartes_par_ligne = 7
            
            for index, carte in enumerate(player.deck.cartes):
                colonne = index % cartes_par_ligne
                ligne = index // cartes_par_ligne
                x = 80 + (colonne * 165)
                y = 150 + (ligne * 230)
                
                cle_carte = carte.nom.lower().replace(" ", "_")
                
                if cle_carte in IMG_DECK:
                    screen.blit(IMG_DECK[cle_carte], (x, y))
                else:
                    print(cle_carte)
                    pygame.draw.rect(screen, (60, 60, 90), (x, y, 120, 180))
                    pygame.draw.rect(screen, white, (x, y, 120, 180), 2)
                    

    elif etat == "SHOP":
        screen.blit(shop_fond, (0, 0))
        etat = bouton_retour.verifier_clic(etat, son_clic)
        bouton_retour.afficher(screen)

        txt_boutique = font.render("BOUTIQUE", True, white)
        screen.blit(txt_boutique, (540, 20))
        
        if player:
            txt_argent = font.render(f"Emeraudes: {player.get_argent()}", True, (85, 255, 85))
            screen.blit(txt_argent, (850, 20))


        scroll_x += 1 
        largeur_totale_shop = len(shop.cartes) * 220
        if largeur_totale_shop > 0 and scroll_x > largeur_totale_shop + 100:
            scroll_x = -1280 


        for index, carte in enumerate(shop.cartes):
            x = 100 + (index * 220) - scroll_x 
            y = 200

            if -180 < x < 1280:
                pygame.draw.rect(screen, (40, 40, 40), (x, y, 180, 260))
                pygame.draw.rect(screen, (85, 255, 85), (x, y, 180, 260), 3)
                
                txt_nom = font_small.render(carte.nom, True, white)
                screen.blit(txt_nom, (x + 15, y + 20))

                mots = carte.description.split(' ')
                lignes = []
                ligne_actuelle = ""

                for mot in mots:
                    test_ligne = ligne_actuelle + mot + " "
                    if font_small.size(test_ligne)[0] <= 150:
                        ligne_actuelle = test_ligne
                    else:
                        lignes.append(ligne_actuelle)
                        ligne_actuelle = mot + " "
                lignes.append(ligne_actuelle)

                y_desc = y + 55
                for ligne in lignes:
                    if ligne.strip():
                        txt_desc = font_small.render(ligne.strip(), True, white)
                        screen.blit(txt_desc, (x + 15, y_desc))
                        y_desc += 22


                txt_prix = font_small.render(f"Prix: {carte.prix} EM", True, (255, 215, 0))
                screen.blit(txt_prix, (x + 15, y + 210))

    elif etat == "QUIT":
        pygame.quit()
        quit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()