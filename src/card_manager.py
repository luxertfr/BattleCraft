
import json
import os 
from Card import MobCard, FoodCard, EnchantedBookCard, ArtifactCard


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATH_TO_JSON = os.path.join(BASE_DIR, "cards.json")

with open(PATH_TO_JSON, "r", encoding="utf-8") as file:
    cards_data = json.load(file)
    
ALL_CARDS = {}

for key, data in cards_data.items():
    if data["type_carte"] == "Mob":
        ALL_CARDS[key] = MobCard(data["nom"], data["description"], data["vie"], data["attaque"], prix=data["prix"])
        
    elif data["type_carte"] == "Food":
        ALL_CARDS[key] = FoodCard(data["nom"], data["description"], data["soin"], prix=data["prix"])
        
    elif data["type_carte"] == "EnchantedBook":
        ALL_CARDS[key] = EnchantedBookCard(data["nom"], data["description"], data["stat_modifiee"], data["multiplicateur"], data["cible"], prix=data["prix"])
        
    elif data["type_carte"] == "Artifact":
        ALL_CARDS[key] = ArtifactCard(data["nom"], data["description"], data["degats"], prix=data["prix"])
