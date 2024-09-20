import pygame
from samba.dcerpc.smb_acl import group

from settings import *
from tile import Tile
from player import Player
from support import *
from npc import *

class Level:
    def __init__(self):
        # Get display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()  # Group for NPCs

        # Sprite setup
        self.create_map()

        # Dialogue box setup
        self.dialogue_box = False
        self.current_dialogue = []
        self.dialogue_index = 0
        self.space_pressed = False #tracks if space key pressed

    def create_map(self):
        layouts = {
            "boundary": import_csv_layout("Maps/map_floor_blocks.csv"),
            "characters": import_csv_layout("Maps/map_entities.csv"),
        }
        for style, layouts in layouts.items():
            for row_index, row in enumerate(layouts):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacles_sprites], "invisible")
                        if style == "characters":
                            if col == "0":
                                npc_abe = NPC((x, y), [self.visible_sprites, self.npc_sprites], "Abe.png", "abe")
                                print(col)
                            if col == "1":
                                npc_ben = NPC((x, y), [self.visible_sprites, self.npc_sprites], "ben.png", "ben")
                                print(col)
                            if col == "2":
                                npc_declan = NPC((x, y), [self.visible_sprites, self.npc_sprites], "declan.png", "declan")
                                print(col)
                            if col == "3":
                                npc_archie = NPC((x, y), [self.visible_sprites, self.npc_sprites], "archie.png", "archie")
                                print(col)
                            if col == "4":
                                npc_cowdrey = NPC((x, y), [self.visible_sprites, self.npc_sprites], "cowdrey.png", "cowdrey")
                                print(col)
                            if col == "5":
                                npc_ella = NPC((x, y), [self.visible_sprites, self.npc_sprites], "ella.png", "ella")
                                print(col)
                            if col == "6":
                                npc_izaac = NPC((x, y), [self.visible_sprites, self.npc_sprites], "izaac.png", "izaac")
                                print(col)
                            if col == "7":
                                npc_james = NPC((x, y), [self.visible_sprites, self.npc_sprites], "james.png", "james")
                            if col == "8":
                                npc_beaver = NPC((x, y), [self.visible_sprites, self.npc_sprites], "archie.png", "beaver")
                            if col == "9":
                                npc_sikes = NPC((x, y), [self.visible_sprites, self.npc_sprites], "cowdrey.png", "sikes")
                            if col == "10":
                                npc_warren = NPC((x, y), [self.visible_sprites, self.npc_sprites], "declan.png", "warren")
                            if col == "11":
                                npc_adrian = NPC((x, y), [self.visible_sprites, self.npc_sprites], "ben.png", "adrian")
                                print(col)
        self.player = Player((1344, 2944), [self.visible_sprites], self.obstacles_sprites)


    def run(self):
        # Update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

        # Handle NPC interaction
        self.handle_npc_interaction()

        # Handle dialogue advancing (spacebar press to move to next line)
        self.handle_dialogue_advance()

        # Render dialogue box if active
        if self.dialogue_box:
            self.display_dialogue()

    def handle_npc_interaction(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()  # Get mouse button status

        if mouse_click[0]:  # Left click
            print(f"Mouse clicked at: {mouse_pos}")  # Debugging

            for npc in self.npc_sprites:
                # Calculate NPC’s screen position considering camera offset
                npc_screen_pos = npc.rect.topleft - self.visible_sprites.offset
                if pygame.Rect(npc_screen_pos, npc.rect.size).collidepoint(mouse_pos):
                    print(f"NPC clicked: {npc}")  # Debugging
                    self.current_dialogue = npc.interact()
                    self.dialogue_index = 0
                    self.dialogue_box = True  # Display dialogue box
                    print(f"Dialogue triggered: {self.current_dialogue}")
                    return  # Exit after the first successful click

    def display_dialogue(self):
        if self.dialogue_index < len(self.current_dialogue):
            # Set up the font for rendering the dialogue
            font = pygame.font.Font(None, 36)
            dialogue_text = font.render(self.current_dialogue[self.dialogue_index], True, (255, 255, 255))

            # Create a rect to position the dialogue text
            dialogue_rect = dialogue_text.get_rect(center=(self.display_surface.get_width() // 2, 50))

            # Draw a background for the dialogue box
            pygame.draw.rect(self.display_surface, (0, 0, 0), dialogue_rect.inflate(20, 20))

            # Draw the dialogue text
            self.display_surface.blit(dialogue_text, dialogue_rect)
        else:
            self.dialogue_box = False  # Hide dialogue box when all dialogue has been displayed

    def handle_dialogue_advance(self):
        keys = pygame.key.get_pressed()
        space_pressed_now = keys[pygame.K_SPACE]
        escape_pressed = keys[pygame.K_ESCAPE]

        # Exit the conversation immediately if ESCAPE is pressed
        if escape_pressed:
            self.dialogue_box = False
            self.dialogue_index = 0  # Reset dialogue index if desired
            self.space_pressed = False  # Reset space_pressed flag
            return

        # Advance the dialogue if SPACE is pressed
        if space_pressed_now and not self.space_pressed:
            if self.dialogue_index < len(self.current_dialogue) - 1:
                self.dialogue_index += 1  # Move to the next line of dialogue
            else:
                self.dialogue_box = False  # Close the dialogue box when done
            self.space_pressed = True  # Mark space key as pressed

        # Reset the space_pressed flag if SPACE is released
        if not space_pressed_now:
            self.space_pressed = False



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf = pygame.image.load("Maps/map.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):

        #Getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)