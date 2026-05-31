import random



class Card:
    def __init__(self,nom, description, type, prix = None):
        self.nom = nom
        self.description = description
        self.type = type

    
    
class MobCard(Card):
    def __init__(self, nom, description, vie, attaque, prix=None):
        super().__init__(nom, description, type="Mob", prix = prix)
        self.vie = vie
        self.attack = attaque
        
class FoodCard(Card):
    def __init__(self, nom, description, soin, prix= None):
        super().__init__(nom, description, type ="Soin", prix=prix)
        self.soin = soin

class EnchantedBookCard(Card):
    def __init__(self, nom, description, modif_stat, valeur, cible, prix = None):
        super().__init__(nom, description, type = "Outil",prix = prix)
        self.modif_stat = modif_stat
        self.valeur = valeur
        self.cible = cible


ALL_CARDS = {
    # Carte de base (mob)
    "zombie": MobCard("Zombie", "Lent mais résistant, votre meilleur acolyte pour gagner.", 50, 15),
    "squelette": MobCard("Squelette", "Attaque à distance avec son arc mais fragile.", 25, 10),
    "chien": MobCard("Chien", "Votre chien préféré vous protégera jusqu'à son dernier souffle.", 15, 10),
    
    # Carte de base (artefact)
    "pain": FoodCard("Pain", "Fabriqué avec trois brins de blés, redonne un peu d'énergie.", 10),
    "steak": FoodCard("Steak", "Un steak cuit à point, redonne de l'énergie.", 20),

    # Shop
    "epee_diamant": Card("Épée en Diamant", "Tranche le Nether et le destin.", 0, 45, 0, 15),
    "arc_inifinite": Card("Arc Infinité", "Tir de flèches en rafale.", 0, 35, 0, 10),
    "pomme_dore": Card("Pomme d'Or", "Régénération massive de PV.", 0, 0, 60, 12),
    "totem": Card("Totem d'Immortalité", "Soin d'urgence ultime.", 0, 0, 100, 25),
    "golem_fer": Card("Invoc: Golem de Fer", "Un énorme tank pour encaisser.", 150, 15, 0, 20),
    "tnt": Card("Bloc de TNT", "Explose et fait d'immenses dégâts.", 0, 60, 0, 14)
}