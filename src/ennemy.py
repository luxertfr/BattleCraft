import pygame
import json

class Ennemy:
    def __init__(self, vie, attaque, description, nom):
        self.vie = vie
        self.attaque = attaque
        self.description = description
        self.nom = nom
        

with open("./src/ennemi.json", "r", encoding="utf-8") as f:
    ennemi_config = json.load(f)

ALL_ENNEMI = {}
IMG_ENNEMI = {}
for id_ennemi, data_ennemi in ennemi_config.items():
    chemin_img = f"./assets/img/ennemies/{data_ennemi['image']}"
    ALL_ENNEMI[id_ennemi] = Ennemy(data_ennemi["vie"], data_ennemi["attaque"], data_ennemi["description"], data_ennemi["nom"])
    try:
        loaded_img = pygame.image.load(chemin_img)
        IMG_ENNEMI[id_ennemi] = pygame.transform.scale(loaded_img,(120, 180))
    except pygame.error:
        secours = pygame.Surface((120, 180))
        secours.fill((150, 50, 50))
        IMG_ENNEMI[id_ennemi] = secours

