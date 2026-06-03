def gerer_attaque_mob(attaquant, cible):
    cible.vie -= attaquant.attaque
    if cible.vie <= 0:
        cible.vie = 0


def appliquer_soin(carte_soin, cible_mob):
    cible_mob.vie += carte_soin.soin
    
def appliquer_boost_attaque(carte_book, cible_mob):
    cible_mob.attaque *= carte_book.boost

def appliquer_boost_def(carte_book, cible_mob):
    cible_mob.vie //= carte_book.boost
    
