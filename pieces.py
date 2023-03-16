from numpy import diag
import pygame
from pygame.locals import *
from hashlib import new
from square import *
from game import *
from constant import *


# takes sprite.png and loads each individual img into a dictionary
def get_piece_sprites(filename, width, height):
    # Dictionary to hold image for every peice
    piece_dict = {
        "white": {"king": None, "queen": None, "bishop": None, "knight": None, "rook": None, "pawn": None},
        "black": {"king": None, "queen": None, "bishop": None, "knight": None, "rook": None, "pawn": None}
    }

    sprite_sheet = pygame.image.load(filename)

    # Load white pieces into dictionary
    frame = 0
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    for x in piece_dict["white"]:
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sprite_sheet, (0, 0), (frame * width, 0, width, height))
        piece_dict["white"][x] = image
        frame += 1

    # Load black pieces into dictionary
    frame = 0
    for x in piece_dict["black"]:
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sprite_sheet, (0, 0),
                   (frame * width, height, width, height))
        piece_dict["black"][x] = image
        frame += 1

    return piece_dict


# global variable to hold all sprites of the pieces
piece_sprites_dict = get_piece_sprites(
    "sprite_test.png", IMG_WIDTH, IMG_HEIGHT)


# global method to convert coords to an index in game_board
def convert_coords_to_index(x, y):
    index = (x - 1) + (y - 1) * 8
    return index


# Piece class is the generic parent class of all the pieces on the chess game_board
# Fields of the class:
#   color of the piece
#   the current square on the game_board that the piece is occupying
#   if the piece is selected or not
#   the value of the piece
class Piece:
    # constructor takes in the color of the piece and the square it occupies, and sets selected to be false initially
    def __init__(self, color, current_square):
        self.color = color
        self.current_square = current_square
        self.selected = False
        self.value = 0

    # Might change point2D (coordinates) to square --> square which pieace occupies

    # getters
    def get_square(self):
        return self.current_square

    def getPoint2D(self):
        return self.current_square.get_draw_cord()

    def get_color(self):
        return self.color

    def get_value(self):
        return self.value

    def is_selected(self):
        return self.selected

    def get_valid_moves(self):
        # this will be implemented in each individual piece's class
        return []

    # setters
    def setColor(self, color):
        self.color = color

    def set_square(self, new_square):
        self.current_square = new_square

    def setPoint2D(self, coordinates):
        self.current_square.set_coordinates(coordinates)

    def set_selected(self, selected):
        self.selected = selected

    # Load sprite image
    def assign_image(self, sprite):
        self.__sprite = sprite

    # Draw
    # pass in coordinates where you want it to be drawn, will draw sprite attribute of piece object
    def draw(self, screen):
        point2D = self.current_square.get_draw_cord()
        screen.blit(self.__sprite, (point2D[0] + 10, point2D[1] + 8))

    # draws captured pieces
    def draw_capt(self, screen, pos_x, pos_y):
        screen.blit(pygame.transform.scale(self.__sprite,
                    (int(IMG_WIDTH/2), int(IMG_HEIGHT/2))), (pos_x, pos_y))


# King class represents the king piece in Chess
# Unique fields of the king:
#   in_check represents if the king is currently in the state of being in check
#   has_moved is used to keep track of if the King has moved or not, with the purpose of
#       using that information to check if it can castle
class King(Piece):
    # constructer
    def __init__(self, color, current_square):
        super().__init__(color, current_square)

        self.value = 100  # Technically the King has no value, so just putting a really high value
        self.in_check = False
        self.has_moved = False
        if self.color == 'white':
            self.assign_image(piece_sprites_dict['white']['king'])
        else:
            self.assign_image(piece_sprites_dict['black']['king'])

    # getters
    def get_in_check(self):
        return self.in_check

    def get_has_moved(self):
        return self.has_moved

    # setters
    def set_in_check(self, in_check):
        self.in_check = in_check

    def set_has_moved(self, has_moved):
        self.has_moved = has_moved

    # returns valid moves for the king
    def get_valid_moves(self, squares, player, in_check):
        moves = []

        cur_square = self.current_square.get_coordinates()
        cur_x = cur_square[0]
        cur_y = cur_square[1]

        # look at moves 1 away from king's current location in every direction
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = cur_x
                y = cur_y

                x += i
                y += j
                if x >= 1 and x <= 8 and y >= 1 and y <= 8:
                    index = convert_coords_to_index(x, y)
                    if squares[index].get_occupied() == False:
                        moves.append(index)
                    else:
                        if squares[index].get_piece().get_color() != self.color:
                            moves.append(index)

        # check and see if castling is available
        # first check if king hasn't moved
        if self.has_moved == False and in_check == False:

            # check to the left
            # check and make sure rook hasn't moved
            valid = 'true'
            rook_index = convert_coords_to_index(1, cur_y)
            if squares[rook_index].get_occupied() == True and type(squares[rook_index].get_piece()) == Rook and squares[rook_index].get_piece().get_has_moved() == False:
                for i in range(cur_x - 1, 1, -1):
                    index = convert_coords_to_index(i, cur_y)
                    # make sure all squares are unoccupied
                    if squares[index].get_occupied() == True:
                        valid = 'false'

                # if everything okay, add move to castle to the left
                if valid == 'true':
                    moves.append(rook_index)

            # check to the right
            # check and make sure rook hasn't moved
            valid = 'true'
            rook_index = convert_coords_to_index(8, cur_y)
            if squares[rook_index].get_occupied() == True and type(squares[rook_index].get_piece()) == Rook and squares[rook_index].get_piece().get_has_moved() == False:
                for i in range(cur_x + 1, 8, 1):
                    # get square from coordinates
                    index = convert_coords_to_index(i, cur_y)
                    # make sure all squares are unoccupied
                    if squares[index].get_occupied() == True:
                        valid = 'false'

                # if everything okay, add move to castle to the right
                if valid == 'true':
                    moves.append(rook_index)

        return moves


# Queen class represents the queen in chess
# Has no unique fields
class Queen(Piece):
    # constructor
    def __init__(self, color, current_square):
        super().__init__(color, current_square)

        self.value = 9
        if self.color == 'white':
            self.assign_image(piece_sprites_dict['white']['queen'])
        else:
            self.assign_image(piece_sprites_dict['black']['queen'])

    # look at valid moves for queen, unlimited squares in every direction (until occupied square/ edge of board)
    def get_valid_moves(self, squares, player, in_check):
        moves = []

        cur_square = self.current_square.get_coordinates()
        cur_x = cur_square[0]
        cur_y = cur_square[1]

        right = 8 - cur_x
        # Look at moves to the right
        for i in range(1, right + 1):
            x = cur_x
            x += i
            if x >= 1 and x <= 8:
                index = convert_coords_to_index(x, cur_y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        # Look at moves to the left
        for i in range(1, cur_x):
            x = cur_x
            x -= i
            if x >= 1 and x <= 8:
                index = convert_coords_to_index(x, cur_y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        # Look at moves down
        down = 8 - cur_y
        for i in range(1, down + 1):
            y = cur_y
            y += i
            if y >= 1 and y <= 8:
                index = convert_coords_to_index(cur_x, y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        # Look at moves up
        for i in range(1, cur_y):
            y = cur_y
            y -= i
            if y >= 1 and y <= 8:
                index = convert_coords_to_index(cur_x, y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        # Diagonal right up
        diagonal = min(8 - cur_x, cur_y - 1)
        for i in range(1, diagonal + 1):
            x = cur_x
            y = cur_y

            x += i
            y -= i
            if x >= 1 and x <= 8 and y >= 1 and y <= 8:
                index = convert_coords_to_index(x, y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        # Diagonal right down
        diagonal = min(8 - cur_x, 8 - cur_y)
        for i in range(1, diagonal + 1):
            x = cur_x
            y = cur_y

            x += i
            y += i
            if x >= 1 and x <= 8 and y >= 1 and y <= 8:
                index = convert_coords_to_index(x, y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        # Diagonal left up
        diagonal = min(cur_x - 1, cur_y - 1)
        for i in range(1, diagonal + 1):
            x = cur_x
            y = cur_y

            x -= i
            y -= i
            if x >= 1 and x <= 8 and y >= 1 and y <= 8:
                index = convert_coords_to_index(x, y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        # Diagonal left down
        diagonal = min(cur_x - 1, 8 - cur_y)
        for i in range(1, diagonal + 1):
            x = cur_x
            y = cur_y

            x -= i
            y += i
            if x >= 1 and x <= 8 and y >= 1 and y <= 8:
                index = convert_coords_to_index(x, y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        return moves


# Rook class represents the rook in chess
# Unique fields:
#   has_moved is used to keep track of if the Rook has moved or not, with the purpose of
#       using that information to check if it can castle
class Rook(Piece):
    # constructor
    def __init__(self, color, current_square):
        super().__init__(color, current_square)

        self.value = 5
        self.has_moved = False
        if self.color == 'white':
            self.assign_image(piece_sprites_dict['white']['rook'])
        else:
            self.assign_image(piece_sprites_dict['black']['rook'])

    # getters
    def get_has_moved(self):
        return self.has_moved

    # setter
    def set_has_moved(self, has_moved):
        self.has_moved = has_moved

    # look at all valid moves for a rook, up/down/left/right
    def get_valid_moves(self, squares, player, in_check):
        moves = []

        cur_square = self.current_square.get_coordinates()
        cur_x = cur_square[0]
        cur_y = cur_square[1]

        right = 8 - cur_x
        # Look at moves to the right
        for i in range(1, right + 1):
            x = cur_x
            x += i
            if x >= 1 and x <= 8:
                index = convert_coords_to_index(x, cur_y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        # Look at moves to the left
        for i in range(1, cur_x):
            x = cur_x
            x -= i
            if x >= 1 and x <= 8:
                index = convert_coords_to_index(x, cur_y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        # Look at moves down
        down = 8 - cur_y
        for i in range(1, down + 1):
            y = cur_y
            y += i
            if y >= 1 and y <= 8:
                index = convert_coords_to_index(cur_x, y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        # Look at moves up
        for i in range(1, cur_y):
            y = cur_y
            y -= i
            if y >= 1 and y <= 8:
                index = convert_coords_to_index(cur_x, y)
                if squares[index].get_occupied() == False:
                    moves.append(index)
                else:
                    if squares[index].get_piece().get_color() != self.color:
                        moves.append(index)
                    break

        return moves


# Bishop class represents the bishop in chess
# No unique fields
class Bishop(Piece):
    # constructor
    def __init__(self, color, current_square):
        super().__init__(color, current_square)

        self.value = 3
        if self.color == 'white':
            self.assign_image(piece_sprites_dict['white']['bishop'])
        else:
            self.assign_image(piece_sprites_dict['black']['bishop'])

    def get_valid_moves(self, squares, player, in_check):
        # this is where we need to implement rules/moves
        # current location will be list of [x, y] position
        current_location = self.current_square.get_coordinates()
        current_loc_x = current_location[0]
        current_loc_y = current_location[1]

        # dictionary to hold all valid moves
        valid_moves = []

        # look at movement diagonally up and to the left, increment by 1 until you hit an occupied square
        i = 1
        while (current_loc_x - i) > 0 and (current_loc_y - i) > 0:
            # if square is not occupied, add to list of valid moves
            move_index = convert_coords_to_index(
                current_loc_x - i, current_loc_y - i)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)

            # if square is occupied, check if it's the same color as the piece. if it isn't add the move
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)
                # can't move past an occupied square, so set i to a high number so we exit loop
                i = 100

            else:
                i = 100  # piece of same color occupies, so just exit loop
            i += 1

        # look at movement diagonally up and to the right, increment by 1 until you hit an occupied square
        i = 1
        while (current_loc_x + i) < 9 and (current_loc_y - i) > 0:
            # if square is not occupied, add to list of valid moves
            move_index = convert_coords_to_index(
                current_loc_x + i, current_loc_y - i)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)

            # if square is occupied, check if it's the same color as the piece. if it isn't add the move
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)
                # can't move past an occupied square, so set i to a high number so we exit loop
                i = 100

            else:
                i = 100  # piece of same color occupies, so just exit loop

            i += 1

        i = 1
        # look at movement diagonally down and to the left, increment by 1 until you hit an occupied square
        while (current_loc_x - i) > 0 and (current_loc_y + i) < 9:
            # if square is not occupied, add to list of valid moves
            move_index = convert_coords_to_index(
                current_loc_x - i, current_loc_y + i)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)

            # if square is occupied, check if it's the same color as the piece. if it isn't add the move
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)
                # can't move past an occupied square, so set i to a high number so we exit loop
                i = 100

            else:
                i = 100  # piece of same color occupies, so just exit loop

            i += 1

        i = 1
        # look at movement diagonally down and to the right, increment by 1 until you hit an occupied square
        while (current_loc_x + i) < 9 and (current_loc_y + i) < 9:
            # if square is not occupied, add to list of valid moves
            move_index = convert_coords_to_index(
                current_loc_x + i, current_loc_y + i)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)

            # if square is occupied, check if it's the same color as the piece. if it isn't add the move
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)
                # can't move past an occupied square, so set i to a high number so we exit loop
                i = 100

            else:
                i = 100  # piece of same color occupies, so just exit loop

            i += 1

        return valid_moves


# Knight class represents the knight in chess
# No unique fields
class Knight(Piece):
    # constructor
    def __init__(self, color, current_square):
        super().__init__(color, current_square)

        self.value = 3
        if self.color == 'white':
            self.assign_image(piece_sprites_dict['white']['knight'])
        else:
            self.assign_image(piece_sprites_dict['black']['knight'])

    # look at all valid moves for knight, which are all L shaped moves
    def get_valid_moves(self, squares, player, in_check):
        # current location will be list of [x, y] position
        current_location = self.current_square.get_coordinates()
        current_loc_x = current_location[0]
        current_loc_y = current_location[1]

        # dictionary to hold all valid moves
        valid_moves = []

        # look at movement up 2 and to the left 1
        if (current_loc_x > 1 and current_loc_y > 2):
            move_index = convert_coords_to_index(
                current_loc_x - 1, current_loc_y - 2)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)

        # look at movement up 2 and to the right 1
        if (current_loc_x < 8 and current_loc_y > 2):
            move_index = convert_coords_to_index(
                current_loc_x + 1, current_loc_y - 2)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)

        # look at movement down 2 and to the left 1
        if (current_loc_x > 1 and current_loc_y < 7):
            move_index = convert_coords_to_index(
                current_loc_x - 1, current_loc_y + 2)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)

        # look at movement down 2 and to the right 1
        if (current_loc_x < 8 and current_loc_y < 7):
            move_index = convert_coords_to_index(
                current_loc_x + 1, current_loc_y + 2)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)

        # look at movement left 2 and up 1
        if (current_loc_x > 2 and current_loc_y > 1):
            move_index = convert_coords_to_index(
                current_loc_x - 2, current_loc_y - 1)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)

        # look at movement left 2 and down 1
        if (current_loc_x > 2 and current_loc_y < 8):
            move_index = convert_coords_to_index(
                current_loc_x - 2, current_loc_y + 1)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)

        # look at movement right 2 and up 1
        if (current_loc_x < 7 and current_loc_y > 1):
            move_index = convert_coords_to_index(
                current_loc_x + 2, current_loc_y - 1)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)

        # look at movement right 2 and down 1
        if (current_loc_x < 7 and current_loc_y < 8):
            move_index = convert_coords_to_index(
                current_loc_x + 2, current_loc_y + 1)
            if squares[move_index].get_occupied() == False:
                valid_moves.append(move_index)
            elif squares[move_index].get_piece().get_color() != self.color:
                valid_moves.append(move_index)

        return valid_moves


# Pawn class represents the pawn in chess
# Unique fields:
#   has_moved keeps track of if the pawn has moved or not, which is used to check if it can move forward 2 spaces
#   has_moved2 is used to check if en passent is available to another pawn
class Pawn(Piece):
    # constructor
    def __init__(self, color, current_square):
        super().__init__(color, current_square)

        self.value = 1
        self.has_moved = False
        self.has_moved2 = False
        if self.color == 'white':
            self.assign_image(piece_sprites_dict['white']['pawn'])
        else:
            self.assign_image(piece_sprites_dict['black']['pawn'])

    # getters
    def get_has_moved(self):
        return self.has_moved

    def get_has_moved2(self):
        return self.has_moved2

     # setters
    def set_has_moved(self, has_moved):
        self.has_moved = has_moved

    def set_has_moved2(self, has_moved2):
        self.has_moved2 = has_moved2

    # look at all valid moves for the pawn, moves forward 1, 2, and diagonal taking of pieces
    def get_valid_moves(self, squares, player, in_check):
        current_location = self.current_square.get_coordinates()
        current_loc_x = current_location[0]
        current_loc_y = current_location[1]

        # list to hold indices in list of squares in game_board that piece can move to
        valid_moves = []

        # if it's a user's piece then look at moves that go "up" the game_board
        if player == 'user':

            # look at movement of 1
            if (current_loc_y > 1):
                move_index = convert_coords_to_index(
                    current_loc_x, current_loc_y - 1)
                if squares[move_index].get_occupied() == False:
                    valid_moves.append(move_index)

                    # check if pawn has moved yet or not. If it hasn't, check if move forward 2 is available
                    if (current_loc_y > 2):
                        move_index = convert_coords_to_index(
                            current_loc_x, current_loc_y - 2)
                        if self.has_moved == False and squares[move_index].get_occupied() == False:
                            valid_moves.append(move_index)

            # check and see if we can take any pieces
            if (current_loc_x > 1 and current_loc_y > 1):
                move_index = convert_coords_to_index(
                    current_loc_x - 1, current_loc_y - 1)
                if squares[move_index].get_occupied() == True and squares[move_index].get_piece().get_color() != self.color:
                    valid_moves.append(move_index)

            if (current_loc_x < 8 and current_loc_y > 1):
                move_index = convert_coords_to_index(
                    current_loc_x + 1, current_loc_y - 1)
                if squares[move_index].get_occupied() == True and squares[move_index].get_piece().get_color() != self.color:
                    valid_moves.append(move_index)

            # this is where we'd poteneitally implement en passent

        # if piece is computer's then look at moves that go "down" the game_board
        if player == 'computer':

            # look at movement of 1
            if (current_loc_y < 8):
                move_index = convert_coords_to_index(
                    current_loc_x, current_loc_y + 1)
                if squares[move_index].get_occupied() == False:
                    valid_moves.append(move_index)

                    # check if pawn has moved yet or not. If it hasn't, check if move forward 2 is available
                    if (current_loc_y < 7):
                        move_index = convert_coords_to_index(
                            current_loc_x, current_loc_y + 2)
                        if self.has_moved == False and squares[move_index].get_occupied() == False:
                            valid_moves.append(move_index)

            # check and see if we can take any pieces
            if (current_loc_x > 1 and current_loc_y < 8):
                move_index = convert_coords_to_index(
                    current_loc_x - 1, current_loc_y + 1)
                if squares[move_index].get_occupied() == True and squares[move_index].get_piece().get_color() != self.color:
                    valid_moves.append(move_index)

            if (current_loc_x < 8 and current_loc_y < 8):
                move_index = convert_coords_to_index(
                    current_loc_x + 1, current_loc_y + 1)
                if squares[move_index].get_occupied() == True and squares[move_index].get_piece().get_color() != self.color:
                    valid_moves.append(move_index)

            # this is where we'd poteneitally implement en passent

        # return list of valid moves
        return valid_moves
