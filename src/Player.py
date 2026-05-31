import sqlite3
from card_manager import ALL_CARDS
from Card import Card, MobCard, FoodCard, EnchantedBookCard
conn = sqlite3.connect('ma_base.db')
cursor = conn.cursor()

class Player:
    def __init__(self, name):
        self.name = name
        self.argent = 0
        self.deck = [cartes for cartes in ALL_CARDS.values() if cartes.prix is None]
        
    def get_deck(self):
        return self.deck
        
    def get_argent(self):
        return self.argent
    
    def set_argent(self, montant):
        self.argent = montant
        cursor.execute("UPDATE users SET argent = ? WHERE name = ?", (self.argent, self.name))
        conn.commit()

    def gagner_argent(self, montant):
        self.argent += montant
        cursor.execute("UPDATE users SET argent = ? WHERE name = ?", (self.argent, self.name))
        conn.commit()
        

    def perdre_argent(self, montant):
        self.argent -= montant
        cursor.execute("UPDATE users SET argent = ? WHERE name = ?", (self.argent, self.name))
        conn.commit()

    

        