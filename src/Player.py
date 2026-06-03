import sqlite3
from card_manager import ALL_CARDS
from deck import Deck

conn = sqlite3.connect('./ma_base.db')
cursor = conn.cursor()

class Player:
    def __init__(self, name):
        self.name = name
        self.argent = 0
        self.deck = Deck()
        self.jeu = []
        
    def get_deck(self):
        return self.deck
        
    def get_argent(self):
        return self.argent
    
    def set_argent(self, montant):
        self.argent = montant
        cursor.execute("UPDATE users SET argent = ? WHERE name = ?", (self.argent, self.name))
        conn.commit()

    def set_deck(self, nouveau_deck):
        self.deck = nouveau_deck
        self.sauvegarder_deck_db()

    def ajouter_carte(self, carte):
        self.deck.acheter_carte(carte)
        self.sauvegarder_deck_db()

    def sauvegarder_deck_db(self):
        noms_cartes = [carte.nom for carte in self.deck.cartes] 
        deck_texte = ",".join(noms_cartes)
        cursor.execute("UPDATE users SET deck = ? WHERE name = ?", (deck_texte, self.name))
        conn.commit()

    def gagner_argent(self, montant):
        self.argent += montant
        cursor.execute("UPDATE users SET argent = ? WHERE name = ?", (self.argent, self.name))
        conn.commit()
        
    def perdre_argent(self, montant):
        self.argent -= montant
        cursor.execute("UPDATE users SET argent = ? WHERE name = ?", (self.argent, self.name))
        conn.commit()
    
    def select_jeu(self, carte):
        self.jeu.append(carte)
        self.sauvegarder_jeu_db()
        
    def deselect_jeu(self, carte):
        self.jeu.remove(carte)
    
    def sauvegarder_jeu_db(self):
        noms_cartes = [carte.nom for carte in self.jeu]
        jeu_texte = ",".join(noms_cartes)
        cursor.execute("UPDATE users SET jeu = ? WHERE name = ?", (jeu_texte, self.name))
        conn.commit()