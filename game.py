import copy
from curses.ascii import SUB
import os
from pickle import TRUE
from turtle import window_width
import pygame
from pygame.locals import *
from constant import *
import board
from copy import deepcopy
import random
from pieces import *
import time

# Game is the class that handles menu/help/game and running the actual game of chess


class Game:
    # initialize the window for menu and game
    def __init__(self):
        self.first_square = None
        self.second_square = None
        self.running = True
        self.currWindow = 'menu'
        self.player_color = 'white'
        self.computer_color = 'black'
        self.first_turn = False

        self.white_in_check = False
        self.black_in_check = False
        self.CPU_CHECK_MATE = False
        self.USER_CHECK_MATE = False
        self.stalemate = False
        self.possible_moves = []

        self.test_castled = False
        self.castled_rook_square = None
        self.castled_king_square = None

        pygame.init()

        # creating the window that everything will exist in (WINDOW_WIDTH, HEIGHT) are constants for the screen size
        self.window = pygame.display.set_mode([WINDOW_WIDTH, HEIGHT])
        # creating the board object
        self.game_board = board.Board()

        pygame.display.set_caption("Chess")
        # pygame.display.update()

        self.clock = pygame.time.Clock()

    ###################### END OF INIT #######################

##############################################################
###################### SCREENS FOR GUI #######################
##############################################################

    ####################### START OF START ####################
    def start(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                key_pressed = pygame.key.get_pressed()
                if self.currWindow == 'play':
                    self.game_window(event)

                if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                    self.running = False
                    exit()

            # winner = self.chess.winner

            if self.currWindow == 'menu':
                self.menu()
            elif self.currWindow == 'help':
                self.help()
            elif self.currWindow == 'select':
                self.select_color()
            elif self.currWindow == 'play':
                self.game()
            elif self.currWindow == 'end':
                self.end()

            pygame.display.update()
            # update events
            pygame.event.pump()

            # call method to stop pygame
        pygame.quit()
        ######################### END OF START ##########################

    ####################### START MENU SCREEN ####################
    def menu(self):
        self.window.fill(BG_COLOR)

        #reset flags for checkmate/stalemate
        self.USER_CHECK_MATE = False
        self.CPU_CHECK_MATE = False
        self.stalemate = False
        self.white_in_check = False
        self.black_in_check = False

        # variables to hold mouse position and whether buttons are pressed mouse_btns[0] = True is left click down,
        # mouse_btns[1] = True is right click down
        mouse_pos = pygame.mouse.get_pos()
        mouse_btns = pygame.mouse.get_pressed()

        # menu buttons
        play_btn = pygame.Rect((WINDOW_WIDTH / 2) - 50, 450, 100, 50)
        pygame.draw.rect(self.window, GREEN, play_btn)
        help_btn = pygame.Rect((WINDOW_WIDTH / 2) - 50, 550, 100, 50)
        pygame.draw.rect(self.window, PURPLE, help_btn)
        # handle mouse hover
        if play_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, LIGHT_GREEN, play_btn)
            pygame.draw.rect(self.window, WHITE, play_btn, 3)

        if help_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, LIGHT_PURPLE, help_btn)
            pygame.draw.rect(self.window, WHITE, help_btn, 3)

        # menu text
        main_menu_txt = MAIN_FONT.render(
            "Welcome to Our Chess Game", True, WHITE)
        sub_menu_txt1 = SUB_FONT.render(
            "Press play to start a game", True, WHITE)
        sub_menu_txt2 = SUB_FONT.render(
            "Press help to see some basic functionality and rules", True, WHITE)
        # menu button text
        play_btn_txt = BUTTON_FONT.render("Play", True, WHITE)
        help_btn_txt = BUTTON_FONT.render("Help", True, WHITE)

        # draw text on window
        self.window.blit(
            main_menu_txt, ((WINDOW_WIDTH - main_menu_txt.get_width()) / 2, 100))
        self.window.blit(
            sub_menu_txt1, ((WINDOW_WIDTH - sub_menu_txt1.get_width()) / 2, 250))
        self.window.blit(
            sub_menu_txt2, ((WINDOW_WIDTH - sub_menu_txt2.get_width()) / 2, 300))
        self.window.blit(play_btn_txt, (play_btn.x + (play_btn.width - play_btn_txt.get_width()) / 2,
                                        play_btn.y + (play_btn.height - play_btn_txt.get_height()) // 2))
        self.window.blit(help_btn_txt, (help_btn.x + (help_btn.width - help_btn_txt.get_width()) / 2,
                                        help_btn.y + (help_btn.height - help_btn_txt.get_height()) / 2))

        # handle button clicks
        if play_btn.collidepoint(mouse_pos):
            if mouse_btns[0]:
                self.currWindow = 'select'

        if help_btn.collidepoint(mouse_pos):
            if mouse_btns[0]:
                self.currWindow = 'help'

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                self.running = False
                exit()

        pygame.display.update()
        self.clock.tick(60)
    ####################### END OF MENU ####################

    ####################### START OF HELP SCREEN ####################
    def help(self):
        self.window.fill(BG_COLOR)

        # mouse position and button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_btns = pygame.mouse.get_pressed()

        back_btn = pygame.Rect(10, 10, 150, 50)
        pygame.draw.rect(self.window, RED, back_btn)
        if back_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, LIGHT_RED, back_btn)
            pygame.draw.rect(self.window, WHITE, back_btn, 3)

        back_btn_txt = BUTTON_FONT.render("Back to Menu", TRUE, WHITE)
        self.window.blit(back_btn_txt, (back_btn.x + (back_btn.width - back_btn_txt.get_width()) / 2,
                                        back_btn.y + (back_btn.height - back_btn_txt.get_height()) / 2))

        main_text = MAIN_FONT.render("Help Screen", True, WHITE)
        self.window.blit(
            main_text, ((WINDOW_WIDTH-main_text.get_width())/2, 100))
        sub_main_text = SUB_FONT.render("See directions below", True, WHITE)
        self.window.blit(
            sub_main_text, ((WINDOW_WIDTH-sub_main_text.get_width())/2, 170))

        # instructions
        intro_line1 = HELP_FONT.render(
            "To start a game press the play button", True, WHITE)
        intro_line2 = HELP_FONT.render(
            "You will be playing as the white pieces against the computer.", True, WHITE)
        move_line1 = HELP_FONT.render("To move:", True, WHITE)
        move_line2 = HELP_FONT.render(
            "-First select a piece and you will see the possible moves", True, WHITE)
        move_line3 = HELP_FONT.render(
            "-Then select one of the possible tiles to move the piece", True, WHITE)
        move_line4 = HELP_FONT.render(
            "Pawns can only move forward and can take pieces diagonally", True, WHITE)
        move_line5 = HELP_FONT.render(
            "Rooks can move any number of tiles up, down, left, or right", True, WHITE)
        move_line6 = HELP_FONT.render(
            "Bishops can move any number of tiles along the diagonals", True, WHITE)
        move_line7 = HELP_FONT.render(
            "Queens can move any number of tiles in any direction", True, WHITE)
        move_line8 = HELP_FONT.render(
            "The king can move one tile in any direction", True, WHITE)
        move_line9 = HELP_FONT.render(
            "-To take any piece simply select the piece you want to move and the tile with the opposing piece", True, WHITE)
        move_line10 = HELP_FONT.render(
            "  (as long as it's valid)", True, WHITE)
        end_line_start = HELP_FONT.render("End Game:", True, WHITE)
        end_line1 = HELP_FONT.render(
            "When the game ends (checkmate or stalemate) the game", True, WHITE)
        end_line2 = HELP_FONT.render(
            "will prompt you to return to the menu or reset.", True, WHITE)
        end_line3 = HELP_FONT.render(
            "If you want to return to the menu press 'e' to exit to menu.", True, WHITE)
        thankyou_line = SUB_FONT.render(
            "Thank you for playing our game, Enjoy!", True, WHITE)
        self.window.blit(intro_line1, (100, 250))
        self.window.blit(intro_line2, (100, 270))
        self.window.blit(move_line1, (100, 310))
        self.window.blit(move_line2, (100, 330))
        self.window.blit(move_line3, (100, 350))
        self.window.blit(move_line4, (100, 370))
        self.window.blit(move_line5, (100, 390))
        self.window.blit(move_line6, (100, 410))
        self.window.blit(move_line7, (100, 430))
        self.window.blit(move_line8, (100, 450))
        self.window.blit(move_line9, (100, 470))
        self.window.blit(move_line10, (100, 490))
        self.window.blit(end_line_start, (100, 530))
        self.window.blit(end_line1, (100, 550))
        self.window.blit(end_line2, (100, 570))
        self.window.blit(end_line3, (100, 590))
        self.window.blit(thankyou_line, (100, 650))

        # handle click of back button, change screen flag
        if back_btn.collidepoint(mouse_pos):
            if mouse_btns[0]:
                self.currWindow = 'menu'

        # handle quitting the game and closing window when user presses esc
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                self.running = False
                exit()

        pygame.display.update()
        self.clock.tick(10)

    ####################### END OF HELP ####################

    ####################### START OF SELECT COLOR SCREEN ####################
    def select_color(self):
        self.window.fill(BG_COLOR)

        # variables to hold mouse position and whether buttons are pressed mouse_btns[0] = True is left click down,
        # mouse_btns[1] = True is right click down
        mouse_pos = pygame.mouse.get_pos()
        mouse_btns = pygame.mouse.get_pressed()

        # menu buttons
        white_btn = pygame.Rect((WINDOW_WIDTH / 2) - 70, 350, 150, 100)
        pygame.draw.rect(self.window, WHITE, white_btn)
        black_btn = pygame.Rect((WINDOW_WIDTH / 2) - 70, 550, 150, 100)
        pygame.draw.rect(self.window, BLACK, black_btn)

        # handle mouse hover
        if white_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, BLACK, white_btn, 3)

        if black_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, WHITE, black_btn, 3)

        main_txt = SUB_FONT.render(
            "Please select which color pieces", True, WHITE)
        main_txt2 = SUB_FONT.render(
            "you would like to play as", True, WHITE)
        white_txt = SUB_FONT2.render(
            "The white pieces play first (this is an advantage):", True, WHITE)
        black_txt = SUB_FONT2.render(
            "The black pieces play second (this is more challenging):", True, WHITE)
        white_btn_txt = BUTTON_FONT.render("White Pieces", True, BLACK)
        black_btn_txt = BUTTON_FONT.render("Black Pieces", True, WHITE)

        self.window.blit(main_txt, ((WINDOW_WIDTH-main_txt.get_width())/2, 75))
        self.window.blit(
            main_txt2, ((WINDOW_WIDTH-main_txt2.get_width())/2, 125))
        self.window.blit(
            white_txt, ((WINDOW_WIDTH-white_txt.get_width())/2, 300))
        self.window.blit(
            black_txt, (((WINDOW_WIDTH-black_txt.get_width())/2, 500)))
        self.window.blit(white_btn_txt, (white_btn.x + (white_btn.width - white_btn_txt.get_width()) / 2,
                                         white_btn.y + (white_btn.height - white_btn_txt.get_height()) / 2))
        self.window.blit(black_btn_txt, (black_btn.x + (black_btn.width - black_btn_txt.get_width()) / 2,
                                         black_btn.y + (black_btn.height - black_btn_txt.get_height()) / 2))

        # handle button clicks
        if white_btn.collidepoint(mouse_pos):
            if mouse_btns[0]:
                self.game_board.set_user_color('white')
                self.game_board.set_comp_color('black')
                self.game_board.initialize_pieces()
                self.currWindow = 'play'

        if black_btn.collidepoint(mouse_pos):
            if mouse_btns[0]:
                self.game_board.set_user_color('black')
                self.game_board.set_comp_color('white')
                self.game_board.initialize_pieces()
                self.currWindow = 'play'

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                self.running = False
                exit()

        pygame.display.update()
        self.clock.tick(60)

    ####################### START OF GAME SCREEN ####################
    def game(self):
        self.game_board.draw(self.window)

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                self.running = False
                exit()

        pygame.display.update()
        self.clock.tick(10)

    ######################## END OF GAME############################

    ####################### START OF END SCREEN###########################
    def end(self):
        self.window.fill(BG_COLOR)

        # reset board to empty
        self.game_board.reset_board()

        # variables to hold mouse position and whether buttons are pressed mouse_btns[0] = True is left click down,
        # mouse_btns[1] = True is right click down
        mouse_pos = pygame.mouse.get_pos()
        mouse_btns = pygame.mouse.get_pressed()

        menu_btn = pygame.Rect((WINDOW_WIDTH / 2) - 70, 650, 150, 75)
        pygame.draw.rect(self.window, RED, menu_btn)

        # handle mouse hover
        if menu_btn.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, WHITE, menu_btn, 3)

        main_txt = MAIN_FONT.render("Game Over", True, WHITE)
        main_txt2 = SUB_FONT.render(
            "Thank you for playing our game!", True, WHITE)
        main_txt3 = SUB_FONT.render(
            "Please return to the menu if you would like to play another game", True, WHITE)
        menu_btn_txt = SUB_FONT2.render("Return To Menu", True, WHITE)
        # text for win, loss, or draw
        win_txt = SUB_FONT.render("Congratulations You Won!", True, WHITE)
        lose_txt = SUB_FONT.render(
            "Sorry You Lost, You Should Try Again!", True, WHITE)
        draw_txt = SUB_FONT.render(
            "This game ended in a stalemate", True, WHITE)

        self.window.blit(main_txt, ((WINDOW_WIDTH-main_txt.get_width())/2, 75))
        self.window.blit(
            main_txt2, ((WINDOW_WIDTH-main_txt2.get_width())/2, 350))
        self.window.blit(
            main_txt3, ((WINDOW_WIDTH-main_txt3.get_width())/2, 400))
        self.window.blit(menu_btn_txt, (menu_btn.x + (menu_btn.width - menu_btn_txt.get_width()) / 2,
                                        menu_btn.y + (menu_btn.height - menu_btn_txt.get_height()) / 2))

        if self.CPU_CHECK_MATE == True:
            self.window.blit(
                win_txt, ((WINDOW_WIDTH-win_txt.get_width())/2, 200))
        elif self.USER_CHECK_MATE == True:
            self.window.blit(
                lose_txt, ((WINDOW_WIDTH-lose_txt.get_width())/2, 200))
        else:
            self.window.blit(
                draw_txt, ((WINDOW_WIDTH-win_txt.get_width())/2, 200))

        if menu_btn.collidepoint(mouse_pos):
            if mouse_btns[0]:
                self.currWindow = 'menu'

        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                self.running = False
                exit()

        pygame.display.update()
        self.clock.tick(10)
    ######################## END OF END SCREEN############################

    ##############################################################
    ####################### END OF SCREENS #######################
    ##############################################################

    def game_window(self, event):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btns = pygame.mouse.get_pressed()

        # Moves computer first if computer is white
        if self.first_turn == False and self.game_board.user_color == 'black':
            time.sleep(1)
            self.computer_move(self.game_board.computer_pieces)
            self.first_turn = True

        self.get_move(event)
        pygame.display.update()

        self.user_in_checkmate(self.game_board.user_pieces)
        self.check_stalemate(self.game_board.user_pieces, self.game_board.computer_pieces)

        self.clock.tick(30)

        # Deselect a square
        if mouse_btns[2]:
            self.game_board.update_board(self.window)
            self.first_square = None

        return None

    # handles getting a move, if the user hasn't selected a tile yet set their selection to 'first_square'
    def get_move(self, event):
        mouse_pos = pygame.mouse.get_pos()
        mouse_btns = pygame.mouse.get_pressed()

        # Select a square:
        if mouse_pos[0] > MARGIN and mouse_pos[0] < WINDOW_WIDTH - MARGIN:
            if event.type == MOUSEBUTTONDOWN and self.first_square is None:
                # Check if first square is occupied by a USER CONTROLLED piece and validates
                self.first_square = self.game_board.find_square(
                    mouse_pos, None)
                if self.first_square is not None:
                    check_occupied = self.game_board.check_occupied(
                        self.game_board.convert_coords_to_index(self.first_square))

                    # If its not occupied reset the board and make another selection
                    if not check_occupied:
                        self.first_square = None
                        self.game_board.update_board(self.window)
                    else:  # if it is occupied get valid moves for that piece and show user where they can move
                        first_square_index = self.game_board.convert_coords_to_index(
                            self.first_square)
                        selected_piece = self.game_board.squares[first_square_index].get_piece(
                        )

                        # check and remove any moves that would result in a check
                        self.possible_moves = self.prevent_check_moves(
                            selected_piece, self.game_board.user_color, 'user')
                        # need to reset first square b/c prevent check modifies it
                        self.first_square = self.game_board.find_square(
                            mouse_pos, None)
                        # DONT NEED 2ND HALF OF STATEMENT --- ALREADY CHECK EARLIER
                        if self.possible_moves and selected_piece.get_color() == self.game_board.user_color:
                            # for the tiles that are possible moves for that piece, set their valid_move flag to true
                            for move in self.possible_moves:
                                self.game_board.squares[move].set_valid_move(True)

                return self.first_square

            # Second sqaure handling
            if event.type == MOUSEBUTTONDOWN and self.first_square is not None:
                self.second_square = self.game_board.find_square(
                    mouse_pos, None)

                if self.second_square is not None:

                    # Get indexs to preform valid moves checks
                    first_square_index = self.game_board.convert_coords_to_index(
                        self.first_square)
                    second_square_index = self.game_board.convert_coords_to_index(
                        self.second_square)
                    selected_piece = self.game_board.squares[first_square_index].get_piece(
                    )

                    # if move is valid
                    if second_square_index in self.possible_moves:
                        self.move(first_square_index,
                                  second_square_index, True)
                        self.game()  # this updates the board so there's a time gap between user and computer moves
                        time.sleep(1)

                        self.computer_move(self.game_board.computer_pieces)

                    # If move isnt valid set second sqaure to none and make another move
                    else:
                        self.second_square = None
                        self.first_square = None
                        for tile in self.game_board.squares:
                            tile.set_valid_move(False)
                        self.game_board.update_board(self.window)
                    return None

        return None

        # handles to movement of pieces on the board, only called after second square is selected

    def move(self, first_square_index, second_square_index, draw):
        # Store captured_piece as none
        captured_piece = None
        first_square = self.game_board.squares[first_square_index]
        second_square = self.game_board.squares[second_square_index]

        # If we're not doing a reset of a castle, proceed normally
        if self.test_castled == False:
            # Gets piece from first square
            move_piece = first_square.get_piece()
            # Changes pieces square to new piece
            move_piece.set_square(second_square)
        else:
            # use previously stored squares if we're resetting a castle
            first_square = self.castled_king_square
            second_square = self.castled_rook_square
            move_piece = first_square.get_piece()

        # If draw option is selected mark peices as moved, as this is occuring on the actual gameboard and not a testboard
        if draw:
            # set has moved to True (rook, king, pawn)
            try:
                move_piece.set_has_moved(True)
            except:
                pass

        # Check for capture
        if second_square.get_occupied() == True and second_square.get_piece().get_color() != move_piece.get_color():
            captured_piece = second_square.get_piece()
            self.capture(captured_piece)

        # check for castle
        if self.white_in_check == False and self.black_in_check == False and second_square.get_occupied() == True and second_square.get_piece().get_color() == move_piece.get_color():
            # if we're making a real move, just castle normally
            if draw:
                self.castle(first_square_index,
                            second_square_index, move_piece)
            else:
                # we know in here we're just testing the castle. based on the flag test_castled, we can figure out if we're castling or resetting the castle
                if self.test_castled == False:  # we're moving and doing actual castle
                    self.castle(first_square_index,
                                second_square_index, move_piece)
                    self.test_castled = True
                else:  # we're resetting the castle
                    self.un_castle(first_square, second_square)
                    self.test_castled = False

        else:
            # Update occupied flags
            first_square.set_occupied(False)
            second_square.set_occupied(True)

            first_square.set_piece(None)
            second_square.set_piece(move_piece)

        # check for a pawn swap
        if draw == True:
            if isinstance(move_piece, Pawn) and (second_square.get_coordinates()[1] == 1 or second_square.get_coordinates()[1] == 8):
                self.pawn_swap(move_piece)

        # If draw option is true then update the board
        if draw:
            # Deselct, reset valid move indicators, and redraw board
            for tile in self.game_board.squares:
                tile.set_valid_move(False)
            self.game_board.update_board(self.window)
            self.first_square = None
        return captured_piece

    # function makes a computer move, where it randomly chooses a piece, and then
    # chooses a move that takes opponents piece if it has one. If not it randomly makes a move
    def computer_move(self, piece_list):
        # shuffle computer's pieces so we can randomly select one
        random.shuffle(piece_list)

        # loop control variables
        valid_move = False
        i = 0
        possible_moves = []

        # loop through all of computer's pieces until you find a piece that has at least one valid move it can make
        while valid_move == False and i < len(piece_list):
            # get valid moves for a piece
            # test for check
            # check for castle
            # doesn't matter what we pass in here, if either is in check castling cannot happen
            self.white_in_check = self.test_check('user')
            self.black_in_check = self.test_check('computer')

            if (self.white_in_check == True or self.black_in_check == True):
                in_check = True
            else:
                in_check = False

            possible_moves = piece_list[i].get_valid_moves(
                self.game_board.squares, 'computer', in_check)
            first_square_index = self.game_board.convert_coords_to_index(
                piece_list[i].get_square().get_coordinates())

            piece = piece_list[i]
            # check to see if move is acceptable check move
            possible_moves = self.prevent_check_moves(
                piece, self.game_board.comp_color, 'computer')
            if possible_moves:
                # if number of valid moves is at least one, exit loop
                valid_move = True
            i += 1

        # There are valid moves still available
        if len(possible_moves) > 0:
            # randomly select one of the moves from the list of possible moves
            random.shuffle(possible_moves)
            # initially set it to first move
            second_square_index = possible_moves[0]

            # check and see if that piece can take any user pieces, if so, set it as best move
            for moves in possible_moves:
                if self.game_board.squares[moves].get_occupied() and self.game_board.squares[moves].get_piece().get_color() == self.game_board.get_user_color():
                    second_square_index = moves

            # call move method
            self.move(first_square_index, second_square_index, True)

            # self.user_in_checkmate(self.game_board.user_pieces)

        # No valid moves remaining - CPU IS IN CHECK MATE
        else:
            self.black_in_check = self.test_check('computer')

            # if computer is in check, then must be checkmate
            if self.black_in_check:
                self.CPU_CHECK_MATE = True
                print("CPU IN CHECK MATE")
            # if not in check but no moves available, then must be a stalemate
            elif self.USER_CHECK_MATE == False:
                self.stalemate = True
                print("STALEMATE")

            time.sleep(5)
            self.currWindow = 'end'

    # capture method to handle when a piece is captured
    def capture(self, captured_piece):
        if captured_piece.get_color() == self.game_board.get_comp_color():
            self.game_board.computer_pieces.remove(captured_piece)
            last = len(self.game_board.computer_pieces_capt)-1

            if not self.game_board.computer_pieces_capt:
                self.game_board.computer_pieces_capt.append(captured_piece)
            else:
                if captured_piece.get_value() <= self.game_board.computer_pieces_capt[0].get_value():
                    self.game_board.computer_pieces_capt.insert(
                        0, captured_piece)
                elif captured_piece.get_value() >= self.game_board.computer_pieces_capt[last].get_value():
                    self.game_board.computer_pieces_capt.insert(
                        last+1, captured_piece)
                else:
                    for x in range(0, len(self.game_board.computer_pieces_capt)-1):
                        if captured_piece.get_value() >= self.game_board.computer_pieces_capt[x].get_value() and captured_piece.get_value() <= self.game_board.computer_pieces_capt[x+1].get_value():
                            if captured_piece.get_value() == self.game_board.computer_pieces_capt[x+1].get_value():
                                if type(captured_piece) == type(self.game_board.computer_pieces_capt[x+1]):
                                    self.game_board.computer_pieces_capt.insert(
                                        x+1, captured_piece)
                                    break
                            else:
                                self.game_board.computer_pieces_capt.insert(
                                    x+1, captured_piece)
                                break

        if captured_piece.get_color() == self.game_board.get_user_color():
            self.game_board.user_pieces.remove(captured_piece)
            last = len(self.game_board.user_pieces_capt)-1

            if not self.game_board.user_pieces_capt:
                self.game_board.user_pieces_capt.append(captured_piece)
            else:
                if captured_piece.get_value() <= self.game_board.user_pieces_capt[0].get_value():
                    self.game_board.user_pieces_capt.insert(0, captured_piece)
                elif captured_piece.get_value() >= self.game_board.user_pieces_capt[last].get_value():
                    self.game_board.user_pieces_capt.insert(
                        last+1, captured_piece)
                else:
                    for x in range(0, len(self.game_board.user_pieces_capt)-1):
                        if captured_piece.get_value() >= self.game_board.user_pieces_capt[x].get_value() and captured_piece.get_value() <= self.game_board.user_pieces_capt[x+1].get_value():
                            if captured_piece.get_value() == self.game_board.user_pieces_capt[x+1].get_value():
                                if type(captured_piece) == type(self.game_board.user_pieces_capt[x+1]):
                                    self.game_board.user_pieces_capt.insert(
                                        x+1, captured_piece)
                                    break
                            else:
                                self.game_board.user_pieces_capt.insert(
                                    x+1, captured_piece)
                                break

    # method to handle pawn swaps (when pawn makes it all the way across the board)
    def pawn_swap(self, pawn):

        # swap pawn for a queen automatically
        cur_square = pawn.get_square().get_coordinates()

        cur_index = convert_coords_to_index(cur_square[0], cur_square[1])
        queen = Queen(pawn.get_color(), self.game_board.squares[cur_index])

        self.game_board.squares[cur_index].set_occupied(True)
        self.game_board.squares[cur_index].set_piece(queen)

        if pawn.get_color() == self.game_board.get_user_color():
            self.game_board.user_pieces.remove(pawn)
            self.game_board.user_pieces.append(queen)

        if pawn.get_color() == self.game_board.get_comp_color():
            self.game_board.computer_pieces.remove(pawn)
            self.game_board.computer_pieces.append(queen)

    # method tests if either cpu/user are in check based on which is passed in
    def test_check(self, player):
        if player == 'user':
            # Finds the user king
            for piece in self.game_board.user_pieces:
                if piece.value == 100:
                    opponent_king = piece
            king_location = self.game_board.convert_coords_to_index(
                opponent_king.get_square().coordinates)
            for piece in self.game_board.computer_pieces:
                moves = piece.get_valid_moves(
                    self.game_board.squares, 'computer', False)
                for move in moves:
                    if king_location == move:
                        return True

        if player == 'computer':
            # Same as above but for cpu king
            for piece in self.game_board.computer_pieces:
                if piece.value == 100:
                    opponent_king = piece
            king_location = self.game_board.convert_coords_to_index(
                opponent_king.get_square().coordinates)
            for piece in self.game_board.user_pieces:
                moves = piece.get_valid_moves(
                    self.game_board.squares, 'user', False)
                for move in moves:
                    if king_location == move:
                        return True
        return False

    # Prevents movement based on checks
    def prevent_check_moves(self, piece, color, player):
        # Gets valid moves from each peice
        # doesn't matter what we pass in here, if either is in check castling cannot happen
        self.white_in_check = self.test_check('user')
        self.black_in_check = self.test_check('computer')

        if (self.white_in_check == True or self.black_in_check == True):
            in_check = True
        else:
            in_check = False

        if player == 'user':
            moves = piece.get_valid_moves(
                self.game_board.squares, 'user', in_check)
        else:
            moves = piece.get_valid_moves(
                self.game_board.squares, 'computer', in_check)

        # Mark current location of the selected peice
        current_location = self.game_board.convert_coords_to_index(
            piece.get_square().coordinates)
        new_valid_moves = []

        if player == 'user':
            # For every valid move of selected peice, make look for a check as a result of that move
            for move in moves:
                # Store postions so board can be restored after testing
                captured_piece = self.move(current_location, move, False)

                # Bad move if move results in a check
                bad_move = self.test_check('user')
                move_coords = self.game_board.squares[move].get_coordinates()

                # If its a good move add it to the valid moves list
                if bad_move == False:
                    new_valid_moves.append(move)

                # move peice back
                self.move(move, current_location, False)

                # If a piece was captured in move testing, restore it
                if captured_piece != None:
                    if captured_piece.get_color() == self.game_board.comp_color:
                        self.game_board.computer_pieces_capt.remove(
                            captured_piece)
                        self.game_board.computer_pieces.append(captured_piece)
                        self.game_board.squares[move].set_occupied(True)
                        self.game_board.squares[move].set_piece(captured_piece)

        if player == 'computer':
            # For every valid move of selected piece, make look for a check as a result of that move
            for move in moves:
                # Store postions so board can be restored after testing
                captured_piece = self.move(current_location, move, False)

                # Bad move if move results in a check
                bad_move = self.test_check('computer')
                move_coords = self.game_board.squares[move].get_coordinates()

                # If its a good move add it to the valid moves list
                if bad_move == False:
                    new_valid_moves.append(move)

                # move peice back
                self.move(move, current_location, False)

                # If a piece was captured in move testing, restore it
                if captured_piece != None:
                    if captured_piece.get_color() == self.game_board.user_color:
                        self.game_board.user_pieces_capt.remove(captured_piece)
                        self.game_board.user_pieces.append(captured_piece)
                        self.game_board.squares[move].set_occupied(True)
                        self.game_board.squares[move].set_piece(captured_piece)

        return new_valid_moves

    # castling movement
    def castle(self, first_square_index, second_square_index, move_piece):

        first_square = self.game_board.squares[first_square_index]
        second_square = self.game_board.squares[second_square_index]
        # king is clicked first, so set it to be 2 to the left/right of it's initial position
        # if it's going to the right
        if (first_square_index < second_square_index):
            # set king to new square it's moving to
            king_square = self.game_board.squares[first_square_index + 2]
            move_piece.set_square(king_square)

            # rook moves one square to the left of king
            rook_piece = second_square.get_piece()
            rook_square = self.game_board.squares[first_square_index + 1]
            rook_piece.set_square(rook_square)

            # update flags
            first_square.set_occupied(False)
            first_square.set_piece(None)

            second_square.set_occupied(False)
            second_square.set_piece(None)

            king_square.set_piece(move_piece)
            king_square.set_occupied(True)

            rook_square.set_piece(rook_piece)
            rook_square.set_occupied(True)

        # check going to the left
        if (first_square_index > second_square_index):
            # set king to new square it's moving to
            king_square = self.game_board.squares[first_square_index - 2]
            move_piece.set_square(king_square)

            # rook moves one square to the left of king
            rook_piece = second_square.get_piece()
            rook_square = self.game_board.squares[first_square_index - 1]
            rook_piece.set_square(rook_square)

            # update flags
            first_square.set_occupied(False)
            first_square.set_piece(None)

            second_square.set_occupied(False)
            second_square.set_piece(None)

            king_square.set_piece(move_piece)
            king_square.set_occupied(True)

            rook_square.set_piece(rook_piece)
            rook_square.set_occupied(True)

        self.castled_rook_square = rook_square
        self.castled_king_square = king_square

    # Method to undo a castle, this is used just for testing check
    def un_castle(self, king_square, rook_square):
        king_piece = king_square.get_piece()
        rook_piece = rook_square.get_piece()
        king_index = king_square.convert_coords_to_index()
        rook_index = rook_square.convert_coords_to_index()

        # if king index is less than rook index, it was castled to the left
        if (king_index < rook_index):
            # set king back to it's original square it's moving to
            king_original_square = self.game_board.squares[king_index + 2]
            king_piece.set_square(king_original_square)

            # rook moves back to the left
            if self.game_board.user_color == 'black':
                move_back = 2
            else:
                move_back = 3

            rook_original_square = self.game_board.squares[rook_index - move_back]
            rook_piece.set_square(rook_original_square)

            # update flags
            king_square.set_occupied(False)
            king_square.set_piece(None)

            rook_square.set_occupied(False)
            rook_square.set_piece(None)

            king_original_square.set_piece(king_piece)
            king_original_square.set_occupied(True)

            rook_original_square.set_piece(rook_piece)
            rook_original_square.set_occupied(True)

        # was castled to the right
        if (king_index > rook_index):
            # set king back to it's original square it's moving to
            king_original_square = self.game_board.squares[king_index - 2]
            king_piece.set_square(king_original_square)

            # rook moves back to the right
            if self.game_board.user_color == 'black':
                move_back = 3
            else:
                move_back = 2

            rook_original_square = self.game_board.squares[rook_index + move_back]
            rook_piece.set_square(rook_original_square)

            # update flags
            king_square.set_occupied(False)
            king_square.set_piece(None)

            rook_square.set_occupied(False)
            rook_square.set_piece(None)

            king_original_square.set_piece(king_piece)
            king_original_square.set_occupied(True)

            rook_original_square.set_piece(rook_piece)
            rook_original_square.set_occupied(True)

    # function to check if user in in checkmate
    def user_in_checkmate(self, piece_list):
        valid_moves = False

        for piece in piece_list:
            # get valid moves for a piece
            possible_moves = piece.get_valid_moves(
                self.game_board.squares, 'user', True)

            # check to see if move is acceptable check move
            possible_moves = self.prevent_check_moves(
                piece, self.game_board.user_color, 'user')
            if possible_moves:
                # if number of valid moves is at least one, exit loop
                valid_moves = True

        if valid_moves == False:
            self.white_in_check = self.test_check('user')

            if self.white_in_check == True:
                self.USER_CHECK_MATE = True
                print("USER IN CHECK MATE")
            else:
                self.USER_CHECK_MATE = False

            # redraw board after move is made and check for checkmate
            self.game()
            time.sleep(5)
            self.currWindow = 'end'

    # function to check for if there's a stalemate in the game
    def check_stalemate(self, user_pieces, comp_pieces):
        user_stale = False
        comp_stale = False

        if len(user_pieces) <= 2:
            for x in user_pieces:
                if isinstance(x, Knight) or isinstance(x, Bishop):
                    user_stale = True
            if len(user_pieces) == 1:
                user_stale = True
        
        if len(comp_pieces) <= 2:
            for x in comp_pieces:
                if isinstance(x, Knight) or isinstance(x, Bishop):
                    comp_stale = True
            if len(comp_pieces) == 1:
                comp_stale = True


        if user_stale and comp_stale:
            print("STALEMATE")
            self.stalemate = True
            self.game()
            time.sleep(2)
            self.currWindow = 'end'
