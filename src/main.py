import sqlite3
import pygame
import json
import random
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
        deck TEXT,
        jeu TEXT
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

with open("./src/ennemi.json", "r", encoding="utf-8") as f:
    ennemi_config = json.load(f)

IMG_ENNEMI = {}
for id_ennemi, data_ennemi in ennemi_config.items():
    chemin_img = f"./assets/img/ennemies/{data_ennemi['image']}"
    try:
        loaded_img = pygame.image.load(chemin_img)
        IMG_ENNEMI[id_ennemi] = pygame.transform.scale(loaded_img,(120, 180))
    except pygame.error:
        secours = pygame.Surface((120, 180))
        secours.fill((150, 50, 50))
        IMG_ENNEMI[id_ennemi] = secours


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

# --- Récupération du profil joueur ---
cursor.execute("SELECT * FROM users")
data = cursor.fetchone()
player = None


# --- VARIABLES POUR LA LOTERIE ---
loterie_en_cours = False
loterie_terminee = False
temps_debut_loterie = 0
dernier_changement_img = 0
vitesse_defilement = 50  
duree_loterie = 2000     

ennemi_defilement_actuel = None  
ennemi_choisi = None    
temps_arret_loterie = 0

if data:

    player = Player(data[1])
    player.argent = data[2]
    

    if len(data) > 3 :
        if data[3]:
            player.deck.cartes = [] 
            noms_sauvegardes = data[3].split(",")
            for nom in noms_sauvegardes:
                carte_trouvee = next((c for c in ALL_CARDS.values() if c.nom == nom), None)
                if carte_trouvee:
                    player.deck.acheter_carte(carte_trouvee)
                    if carte_trouvee in shop.cartes:
                        shop.acheter(carte_trouvee)
        if data[4]:
            player.jeu = []
            noms_sauvegardes = data[4].split(",")
            for nom in noms_sauvegardes:
                carte_trouvee = next((c for c in ALL_CARDS.values() if c.nom == nom), None)
                if carte_trouvee:
                    player.select_jeu(carte_trouvee)
    
                    


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
                        cursor.execute("INSERT INTO users (name, argent, deck, jeu) VALUES (?, ?, ?, ?)", (pseudo, 150, "", ""))
                        conn.commit()
                        text = ""
                        cursor.execute("SELECT * FROM users WHERE name = ?", (pseudo,))
                        data = cursor.fetchone()
                        if data:
                            player = Player(data[1])
                            player.argent = data[2]
                else:
                    text += event.unicode
        elif etat == "DECK":
            if event.type == pygame.MOUSEBUTTONDOWN:
                cartes_par_ligne = 7
                for index, carte in enumerate(player.deck.cartes):
                    colonne = index % cartes_par_ligne
                    ligne = index // cartes_par_ligne
                    x = 80 + (colonne * 165)
                    y = 150 + (ligne * 230)
                    
                    rect_carte = pygame.Rect(x, y, 120, 180)
                    
                    if rect_carte.collidepoint(event.pos):
                        
                        son_clic.play()
                        if carte in player.jeu:
                            player.deselect_jeu(carte)
                        else:
                            nb_mobs = sum(1 for c in player.jeu if c.type_carte == "Mob")
                            nb_autres = sum(1 for c in player.jeu if c.type_carte != "Mob")
                            
                            if carte.type_carte == "Mob":
                                if nb_mobs < 3:
                                    player.select_jeu(carte)
                                else:
                                    print("Limite atteinte : Maximum 3 Mobs autorisés")
                                    break
                            
                            else:
                                if nb_autres < 2:
                                    player.select_jeu(carte)
                                else:
                                    print("Limite atteinte : Maximum 2 cartes de soutien (Soin/Livre/TNT)")
                                    break
                            if len(player.jeu) < 5:
                                player.select_jeu(carte)
                        if player:
                            player.sauvegarder_jeu_db()
                        break
                                            

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

            prochain_etat = bouton_jouer.verifier_clic(etat, son_clic)
            if prochain_etat == 'PLAY' and etat != "PLAY":
                etat = "PLAY"
                loterie_en_cours = True
                loterie_terminee = False
                temps_debut_loterie = pygame.time.get_ticks()
                ennemi_choisi = None
            etat = bouton_decks.verifier_clic(etat, son_clic)
            etat = bouton_boutique.verifier_clic(etat, son_clic)
            etat = bouton_quitter.verifier_clic(etat, son_clic)

    elif etat == "PLAY":
        screen.blit(play_fond, (0, 0))
        etat = bouton_retour.verifier_clic(etat, son_clic)
        bouton_retour.afficher(screen)
        
        temps_actuel = pygame.time.get_ticks()
        liste_cles_ennemis = list(ennemi_config.keys())

        if loterie_en_cours:
            if temps_actuel - temps_debut_loterie < duree_loterie:
                if temps_actuel - dernier_changement_img > vitesse_defilement:
                    ennemi_defilement_actuel = random.choice(liste_cles_ennemis)
                    dernier_changement_img = temps_actuel
            else:
                loterie_en_cours = False
                loterie_terminee = True
                ennemi_choisi = ennemi_defilement_actuel
                temps_arret_loterie = temps_actuel 
                


        MILIEU_X = 580  
        MILIEU_Y = 200  

        if loterie_en_cours and ennemi_defilement_actuel:
            screen.blit(IMG_ENNEMI[ennemi_defilement_actuel], (MILIEU_X, MILIEU_Y))
            
            txt_roulette = font_small.render("??? CHOIX DE L'ENNEMI ???", True, (255, 255, 255))
            screen.blit(txt_roulette, (500, MILIEU_Y - 40))

        elif loterie_terminee and ennemi_choisi:
            screen.blit(IMG_ENNEMI[ennemi_choisi], (MILIEU_X, MILIEU_Y))
            
            infos = ennemi_config[ennemi_choisi]
            
            if temps_actuel - temps_arret_loterie < 4000:
                
                pygame.draw.rect(screen, (20, 20, 20), (340, MILIEU_Y + 200, 600, 100))
                pygame.draw.rect(screen, (255, 0, 0), (340, MILIEU_Y + 200, 600, 100), 2)
                
                
                txt_nom = font.render(infos["nom"].upper(), True, (255, 85, 85))
                screen.blit(txt_nom, (360, MILIEU_Y + 210))
                
                txt_desc = font_small.render(infos["description"], True, (255, 255, 255))
                screen.blit(txt_desc, (360, MILIEU_Y + 260))

        
        mobs_actifs = [c for c in player.jeu if c.type_carte == "Mob"]
        soins_actifs = [c for c in player.jeu if c.type_carte != "Mob"]
        
        COULEUR_ALLIE = (0, 255, 0)      
        COULEUR_OBJET = (255, 215, 0)     
        
        LARGEUR_CARTE = 90
        HAUTEUR_CARTE = 130

        ALLIE_X = 100
        for i in range(3):
            y = 100 + (i * 200)  

            if i < len(mobs_actifs):
                carte = mobs_actifs[i]
                cle_carte = carte.nom.lower().replace(" ", "_")
                
                if cle_carte in IMG_DECK:
                    screen.blit(IMG_DECK[cle_carte], (ALLIE_X, y))
                else:
                    pygame.draw.rect(screen, (0, 255, 0), (ALLIE_X, y, LARGEUR_CARTE, HAUTEUR_CARTE), 2)
            else:
                pygame.draw.rect(screen, (0, 100, 0), (ALLIE_X, y, LARGEUR_CARTE, HAUTEUR_CARTE), 1)
                txt_vide = font_small.render(f"Mob {i+1}", True, (0, 100, 0))
                screen.blit(txt_vide, (ALLIE_X + 30, y + 80))
        
        OBJET_Y = 510
        slots_x = [480, 640] 

        for i in range(2):
            x = slots_x[i]
            
            if i < len(soins_actifs):
                carte = soins_actifs[i]
                cle_carte = carte.nom.lower().replace(" ", "_")
                
                if cle_carte in IMG_DECK:
                    screen.blit(IMG_DECK[cle_carte], (x, OBJET_Y))
                else:
                    pygame.draw.rect(screen, (255, 215, 0), (x, OBJET_Y, LARGEUR_CARTE, HAUTEUR_CARTE), 2)
            else:
                pygame.draw.rect(screen, (139, 117, 0), (x, OBJET_Y, LARGEUR_CARTE, HAUTEUR_CARTE), 1)
                txt_vide = font_small.render("Vide", True, (139, 117, 0))
                screen.blit(txt_vide, (x + 40, OBJET_Y + 80))

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
                if carte in player.jeu:
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, 120, 180), 4)
                    

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