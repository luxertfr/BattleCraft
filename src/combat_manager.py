def gerer_attaque_mob(attaquant, cible):
    cible.vie -= attaquant.attaque
    if cible.vie <= 0:
        cible.vie = 0


def appliquer_soin(carte_soin, cible_mob):
    montant_soin = getattr(carte_soin, "soin", 10)
    cible_mob.vie += montant_soin
    
    if hasattr(cible_mob, "vie_max") and cible_mob.vie > cible_mob.vie_max:
        cible_mob.vie = cible_mob.vie_max
    print("bien heal")
    
def appliquer_boost_attaque(carte_book, cible_mob):
    cible_mob.attaque *= carte_book.boost

def appliquer_boost_def(carte_book, cible_mob):
    cible_mob.vie //= carte_book.boost
    
