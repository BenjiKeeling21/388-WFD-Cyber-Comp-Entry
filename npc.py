import pygame
import sys
from support import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, position, groups, image, name):
        super().__init__(groups)
        self.image = pygame.image.load("characters/npcs/"+image).convert_alpha()  # Load your NPC image
        self.rect = self.image.get_rect(topleft=position)
        self.mask = pygame.mask.from_surface(self.image)

        #assigning dialouge
        if name == "abe":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "ben":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "declan":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "archie":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "cowdrey":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "ella":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "izaac":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "james":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "beaver":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "sikes":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "adrian":
            self.dialogue = read_file_to_list("characters/npc_scripts/"+name+".txt")
        if name == "warren":
            self.dialogue = read_file_to_list("characters/npc_scripts/" + name + ".txt")


    def interact(self):
        # Function to handle interaction
        return self.dialogue

