import pygame 

class Button:
    def __init__(self, texte, position, image, scale, mode):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.mode = mode
        
        # On vérifie si un texte a bien été fourni (si ce n'est pas None ou vide)
        if texte:
            rect_lettre = texte.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            self.image.blit(texte, rect_lettre)
        if scale:
            self.image = pygame.transform.scale(self.image, scale)

    def afficher(self, surface):
        """Méthode pour dessiner le bouton à l'écran"""
        surface.blit(self.image, self.rect.topleft)

    def verifier_clic(self, etat):
        pos_souris = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos_souris):
            if pygame.mouse.get_pressed()[0]:
                print("a")
                pygame.time.wait(150)
                return self.mode
        return etat

