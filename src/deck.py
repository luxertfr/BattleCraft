from card_manager import ALL_CARDS

class Deck:
    def __init__(self):
        # Initialise avec les cartes gratuites par défaut
        self.cartes = [cartes for cartes in ALL_CARDS.values() if cartes.prix == None]
        
    def acheter_carte(self, carte):
        self.cartes.append(carte)