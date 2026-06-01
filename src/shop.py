from card_manager import ALL_CARDS

class Shop:
    def __init__(self):
        self.cartes = [cartes for cartes in ALL_CARDS.values() if cartes.prix != None]
        
    def acheter(self, carte):
        self.cartes.remove(carte)
        