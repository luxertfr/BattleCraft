import pygame

class Button:
    def __init__(self, texte, position, image, scale, mode):
        self.image = pygame.image.load(image).convert_alpha()

        if scale:
            self.image = pygame.transform.scale(self.image, scale)

        self.rect = self.image.get_rect()  
        self.rect.topleft = position
        self.mode = mode
        self.clique = False  

        if texte:
            rect_lettre = texte.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
            self.image.blit(texte, rect_lettre)

    def afficher(self, surface):
        """Méthode pour dessiner le bouton à l'écran"""
        surface.blit(self.image, self.rect.topleft)

    def verifier_clic(self, etat, sound_to_play):
        pos_souris = pygame.mouse.get_pos()
        bouton_presse = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(pos_souris) and bouton_presse and not self.clique:
            sound_to_play.play()
            self.clique = True
            return self.mode

        if not bouton_presse:
            self.clique = False

        return etat