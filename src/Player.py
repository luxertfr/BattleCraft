import sqlite3
conn = sqlite3.connect('ma_base.db')
cursor = conn.cursor()

class Player:
    def __init__(self, name):
        self.name = name[0] if isinstance(name, tuple) else name
        self.argent = 0
        
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

    

        