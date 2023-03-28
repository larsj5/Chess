import square
from pieces import *
from square import *
import pygame
from constant import *
from pickle import TRUE

# constants
NUM_PAWNS = 8
NUM_KING = 1
NUM_QUEEN = 1
NUM_ROOKS = 2
NUM_BISHOPS = 2
NUM_KNIGHTS = 2

# Class Board represents the board in a game of chess
class Board(pygame.sprite.Sprite):
    # List of squares on the board (64 squares total for an 8x8 board)
    squares = []

    # lists of user and computer pieces
    computer_pieces = []
    user_pieces = []

    # lists of captured user and computer pieces
    user_pieces_capt = []
    computer_pieces_capt = []

    # user and computers colors
    user_color = None
    comp_color = None

    # Constructor
    def __init__(self):
        self.fill_squares() # Fills the board with square objects

    # getters and setters

    def get_user_color(self):
        return self.user_color

    def set_user_color(self, color):
        self.user_color = color

    def get_user_color(self):
        return self.user_color

    def set_comp_color(self, color):
        self.comp_color = color

    def get_comp_color(self):
        return self.comp_color

    #method to fill board with square objects
    # X cords are columns while y cords are rows, first square [1,1] is on the top left of the board
    def fill_squares(self):
        # Index for iterating
        index = 0

        # Columns
        x_coordinate = 1
        # Rows
        y_coordinate = 1

        # color of square
        color = 'light'

        # Iterates through length of the board and creates a square
        while index < 64:

            # Resets the x cord and increases the y cord when a row has been filled
            if x_coordinate > 8:
                x_coordinate = 1
                y_coordinate += 1
            # Alternates between colors
            if color == 'light':
                current_square = Square([x_coordinate, y_coordinate], color)
                if x_coordinate != 8:
                    color = 'dark'
            # Special case if at end of row
            else:
                current_square = Square([x_coordinate, y_coordinate], color)
                if x_coordinate != 8:
                    color = 'light'
            self.squares.append(current_square)
            x_coordinate += 1
            index += 1

    # method fills squares with pieces
    def initialize_pieces(self):
        # first do computer pieces, which are on top of screen
        # pawns first, on row 2 across all columns
        for pawns in range(NUM_PAWNS):
            # create a pawn object
            pawn = Pawn(self.comp_color, self.squares[8 + pawns])
            self.squares[8 + pawns].set_occupied(True)
            self.squares[8 + pawns].set_piece(pawn)
            self.computer_pieces.append(pawn)

        # draw king/queen in different postions depending on what color user is 
        if self.user_color == 'white':
            king = King(self.comp_color, self.squares[4])
            self.squares[4].set_occupied(True)
            self.squares[4].set_piece(king)
            self.computer_pieces.append(king)

            # queen
            queen = Queen(self.comp_color, self.squares[3])
            self.squares[3].set_occupied(True)
            self.squares[3].set_piece(queen)
            self.computer_pieces.append(queen)

        else:
            king = King(self.comp_color, self.squares[3])
            self.squares[3].set_occupied(True)
            self.squares[3].set_piece(king)
            self.computer_pieces.append(king)

            # queen
            queen = Queen(self.comp_color, self.squares[4])
            self.squares[4].set_occupied(True)
            self.squares[4].set_piece(queen)
            self.computer_pieces.append(queen)

        # rooks
        rook1 = Rook(self.comp_color, self.squares[0])
        self.squares[0].set_occupied(True)
        self.squares[0].set_piece(rook1)
        self.computer_pieces.append(rook1)

        rook2 = Rook(self.comp_color, self.squares[7])
        self.squares[7].set_piece(rook2)
        self.squares[7].set_occupied(True)
        self.computer_pieces.append(rook2)

        # bishops
        bishop1 = Bishop(self.comp_color, self.squares[2])
        self.squares[2].set_piece(bishop1)
        self.squares[2].set_occupied(True)
        self.computer_pieces.append(bishop1)

        bishop2 = Bishop(self.comp_color, self.squares[5])
        self.squares[5].set_piece(bishop2)
        self.squares[5].set_occupied(True)
        self.computer_pieces.append(bishop2)

        # knights
        knight1 = Knight(self.comp_color, self.squares[1])
        self.squares[1].set_piece(knight1)
        self.squares[1].set_occupied(True)
        self.computer_pieces.append(knight1)

        knight2 = Knight(self.comp_color, self.squares[6])
        self.squares[6].set_piece(knight2)
        self.squares[6].set_occupied(True)
        self.computer_pieces.append(knight2)

        # do user pieces, drawn on bottom of screen
        for pawns in range(NUM_PAWNS):
            # create a pawn object
            pawn = Pawn(self.user_color, self.squares[48 + pawns])
            self.squares[48 + pawns].set_occupied(True)
            self.squares[48 + pawns].set_piece(pawn)
            self.user_pieces.append(pawn)

        # king
        if self.user_color == 'white':
            king = King(self.user_color, self.squares[60])
            self.squares[60].set_occupied(True)
            self.squares[60].set_piece(king)
            self.user_pieces.append(king)

            # queen
            queen = Queen(self.user_color, self.squares[59])
            self.squares[59].set_occupied(True)
            self.squares[59].set_piece(queen)
            self.user_pieces.append(queen)
        else:
            king = King(self.user_color, self.squares[59])
            self.squares[59].set_occupied(True)
            self.squares[59].set_piece(king)
            self.user_pieces.append(king)

            # queen
            queen = Queen(self.user_color, self.squares[60])
            self.squares[60].set_occupied(True)
            self.squares[60].set_piece(queen)
            self.user_pieces.append(queen)


        # rooks
        rook1 = Rook(self.user_color, self.squares[56])
        self.squares[56].set_occupied(True)
        self.squares[56].set_piece(rook1)
        self.user_pieces.append(rook1)

        rook2 = Rook(self.user_color, self.squares[63])
        self.squares[63].set_occupied(True)
        self.squares[63].set_piece(rook2)
        self.user_pieces.append(rook2)

        # bishops
        bishop1 = Bishop(self.user_color, self.squares[58])
        self.squares[58].set_occupied(True)
        self.squares[58].set_piece(bishop1)
        self.user_pieces.append(bishop1)

        bishop2 = Bishop(self.user_color, self.squares[61])
        self.squares[61].set_occupied(True)
        self.squares[61].set_piece(bishop2)
        self.user_pieces.append(bishop2)

        # knights
        knight1 = Knight(self.user_color, self.squares[57])
        self.squares[57].set_occupied(True)
        self.squares[57].set_piece(knight1)
        self.user_pieces.append(knight1)

        knight2 = Knight(self.user_color, self.squares[62])
        self.squares[62].set_occupied(True)
        self.squares[62].set_piece(knight2)
        self.user_pieces.append(knight2)

    # Draws all squares and pieces in board
    def draw(self, window):
        window.fill(BG_COLOR)
        #draw squares
        for square in self.squares:
            square.draw(window)

        #draw computer pieces
        for Cpiece in self.computer_pieces:
            Cpiece.draw(window)

        #draw user pieces
        for Upiece in self.user_pieces:
            Upiece.draw(window)
        
        #draw move indicators
        for square in self.squares:
            square.draw_indicator(window)
    
        #draw captured user_pieces
        for x in range(len(self.user_pieces_capt)):
            self.user_pieces_capt[x].draw_capt(window, MARGIN/4, 0 + (x*HEIGHT/16))

        #draw captured computer pieces
        for x in range(len(self.computer_pieces_capt)):
            self.computer_pieces_capt[x].draw_capt(window, WINDOW_WIDTH - (3/4*MARGIN), 0 + (x*HEIGHT/16))

    # function finds square given mouse coordinates
    def find_square(self, mouse_coordinates, constraint):
        coords = None
        for square in self.squares:
            square.selected = False
            square.was_selected(mouse_coordinates)
            if square.selected:
                coords = square.coordinates
        return coords

    # method updates square and deselects any selected squares
    def update_board(self, window):
        for square in self.squares:
            if square.selected == True:
                square.selected = False
                square.draw(window)

    # takes in coordinates in form [x, y] and converts to the index in the squares list of the 
    # corresponding square
    def convert_coords_to_index(self, coords):
        index = (coords[0] - 1) + (coords[1] - 1) * 8
        return index



    # Only returns True if square is occuppied by user controlled piece
    def check_occupied(self, index):
        check_square = self.squares[index]
        if check_square.get_occupied() == True and check_square.get_piece().get_color() == self.user_color:
            return True
        return False

    # Pass in sqaure index and white or black pieces depending on turn
    def get_piece(self, index, pieces):
        index_square = self.squares[index]
        for piece in pieces:
            if piece.get_square() == index_square:
                return piece
        return None

    # Method to reset the board
    def reset_board(self):
        self.squares = []

        # lists of user and computer pieces
        self.computer_pieces = []
        self.user_pieces = []

        # lists of captured user and computer pieces
        self.user_pieces_capt = []
        self.computer_pieces_capt = []

        # user and computers colors
        self.user_color = None
        self.comp_color = None

        # refill squares
        self.fill_squares()

