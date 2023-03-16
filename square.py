from constant import *
from pieces import *

# Square class represents a single square on the chess board
class Square:
    # Coordinates of the square
    coordinates = []
    # Whether the square is occupied by a piece
    occupied = False
    # The piece (if any) that is occupying the square
    piece = None
    # The color of the square, either light or dark
    color = 'light'
    # Whether the user has selected that square
    selected = False
    # Valid move highlight
    valid_move = False

    # Constructer
    def __init__(self, coordinates, color):
        self.coordinates = coordinates
        self.color = color

    # Getters and setters
    def get_coordinates(self):
        return self.coordinates

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_occupied(self):
        return self.occupied

    def set_occupied(self, occupied):
        self.occupied = occupied

    def set_piece(self, piece):
        self.piece = piece

    def get_piece(self):
        return self.piece

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_selected(self):
        return self.selected

    def set_set(self, selected):
        self.selected = selected

    def get_valid_move(self):
        return self.valid_move

    def set_valid_move(self, valid):
        self.valid_move = valid

    # Calculates pygame coordinates for a square from game coordinates
    def get_draw_cord(self):
        square_dimension = WIDTH / 8
        x = (self.coordinates[0] * square_dimension) - square_dimension + MARGIN
        y = (self.coordinates[1] * square_dimension) - square_dimension
        return [x, y]

    # method draws square
    def draw(self, window):
        # Get square drawing dimensions
        size = WIDTH / 8
        draw_coordinates = self.get_draw_cord()

        # Creates square to be drawn
        square = pygame.Rect(
            draw_coordinates[0], draw_coordinates[1], size, size)

        # Draws square depending on color
        if self.color == 'dark':
            if self.selected:
                pygame.draw.rect(window, SELECTED_DARK_BROWN, square)
            else:
                pygame.draw.rect(window, DARK_BROWN, square)

        else:
            if self.selected:
                pygame.draw.rect(window, SELECTED_LIGHT_BROWN, square)
            else:
                pygame.draw.rect(window, LIGHT_BROWN, square)

    # method to draw a move indicator, which is a blue square
    def draw_indicator(self, window):
        # Get square drawing dimensions
        draw_coordinates = self.get_draw_cord()

        if self.valid_move:
            pygame.draw.circle(window, BLUE, (draw_coordinates[0]+(WIDTH/8)/2,
                                              draw_coordinates[1]+(HEIGHT/8)/2), 10)

    # Method to select/deselect a square
    def was_selected(self, mouse_coordinates):
        draw_coordinates = self.get_draw_cord()
        square_dimension = WIDTH / 8
        if mouse_coordinates[0] > draw_coordinates[0] and mouse_coordinates[0] < (draw_coordinates[0] + square_dimension) and mouse_coordinates[1] > draw_coordinates[1] and mouse_coordinates[1] < (draw_coordinates[1] + square_dimension):
            if self.selected:
                self.selected = False
            else:
                self.selected = True

    # method to convert the [x, y] coordinates of itself to the index in the square list in board class
    def convert_coords_to_index(self):
        index = (self.coordinates[0] - 1) + (self.coordinates[1] - 1) * 8
        return index
