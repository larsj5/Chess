import pygame

# pixel width and height of sprite.png
IMG_WIDTH = 450 / 6
IMG_HEIGHT = 150 / 2
UNQ_PIECES = 6


# takes sprite.png and loads each individual img into a dictionary
def get_piece_sprites(filename, width, height):
    # Dictionary to hold image for every peice
    piece_dict = {
        "white": {"king": None, "queen": None, "bishop": None, "knight": None, "rook": None, "pawn": None},
        "black": {"king": None, "queen": None, "bishop": None, "knight": None, "rook": None, "pawn": None}
    }

    sprite_sheet = pygame.image.load(filename)

    # Load white pieaces into dictionary
    frame = 0
    for x in piece_dict["white"]:
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sprite_sheet, (0, 0), (frame * width, 0, width, height))
        piece_dict["white"][x] = image
        frame += 1

    # Load black pieces into dictionary
    frame = 0
    for x in piece_dict["black"]:
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sprite_sheet, (0, 0), (frame * width, height, width, height))
        piece_dict["black"][x] = image
        frame += 1

    return piece_dict


