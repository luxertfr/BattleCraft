import random



class Card:
    def __init__(self,nom, description, type, prix = None):
        self.nom = nom
        self.description = description
        self.type_carte = type
        self.prix = prix

    
    
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

class ArtifactCard(Card):
    def __init__(self, nom, description, degats, prix=None):

        super().__init__(nom, description, type="Artefact", prix=prix)
        
        self.degats = degats

