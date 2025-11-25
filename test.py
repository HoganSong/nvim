import chess
import chess.engine
import chess.polyglot
import pygame
import time
from ai import SimpleChessAI

# Board Visualization
WIDTH, HEIGHT = 800, 800
SQ_SIZE = WIDTH // 8


def load_images():
    symbol_to_file = {
        'p': 'p.png', 'r': 'r.png', 'n': 'n.png', 'b': 'b.png', 'q': 'q.png', 'k': 'k.png',
        'P': 'pp.png', 'R': 'rr.png', 'N': 'nn.png', 'B': 'bb.png', 'Q': 'qq.png', 'K': 'kk.png'
    }
    images = {}
    for symbol, filename in symbol_to_file.items():
        images[symbol] = pygame.image.load(f'C:/Users/hogan/codes/chessai/image/{filename}')
    return images


IMAGES = load_images()


def draw_board(screen, board):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(8):
        for col in range(8):
            draw_row = row  # Flip row index
            draw_col = col  # Flip column index
            
            color = colors[(draw_row + draw_col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
            piece = board.piece_at(chess.square(draw_col, 7 - draw_row))  # Adjust for flipped view
            if piece:
                scaled_image = pygame.transform.scale(IMAGES[piece.symbol()], (SQ_SIZE, SQ_SIZE))
                screen.blit(scaled_image, (col * SQ_SIZE, row * SQ_SIZE))


def get_square_from_mouse(pos):
    """Convert mouse position to chessboard square (0-7, 0-7)"""
    x, y = pos
    row = y // SQ_SIZE
    col = x // SQ_SIZE
    return col, 7 - row


def show_promotion_menu(screen, square, board):
    """ Display a hovering selection box for promotion. """
    pieces = {'Q': chess.QUEEN, 'R': chess.ROOK, 'B': chess.BISHOP, 'N': chess.KNIGHT}
    piece_order = ['Q', 'R', 'B', 'N']

    # Get the screen position of the promotion menu
    col = chess.square_file(square)
    row = chess.square_rank(square)
    menu_x = col * SQ_SIZE  # Horizontal position (same as the promotion square)
    menu_y = (7 - row) * SQ_SIZE  # Vertical position (at the promotion square)

    # Ensure the menu stays on screen horizontally (check if it goes off the right edge)
    if menu_x + len(piece_order) * SQ_SIZE > WIDTH:
        menu_x = WIDTH - len(piece_order) * SQ_SIZE  # Adjust to fit within screen

    # Ensure the menu stays on screen vertically (check if it goes off the bottom edge)
    if menu_y + SQ_SIZE > HEIGHT:
        menu_y = HEIGHT - SQ_SIZE  # Adjust to fit within screen

    # Store rectangles for clicking
    menu_rects = []
    for i, piece in enumerate(piece_order):
        rect = pygame.Rect(menu_x + i * SQ_SIZE, menu_y, SQ_SIZE, SQ_SIZE)  # Spread out horizontally
        menu_rects.append((rect, piece))

    # Draw the menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for rect, piece in menu_rects:
                    if rect.collidepoint(mouse_x, mouse_y):
                        temp_board = board.copy()  # Create a temporary board without modifying the real board
                        temp_board.remove_piece_at(square)
                        temp_board.set_piece_at(square, pieces[piece])
                        draw_board(screen, temp_board)
                        return pieces[piece]  # Return selected piece

        # Redraw screen
        draw_board(screen, board)

        # Draw promotion box
        for rect, piece in menu_rects:
            pygame.draw.rect(screen, pygame.Color("light gray"), rect)

            # Scale the images for promotion menu
            scaled_image = pygame.transform.scale(IMAGES[piece], (SQ_SIZE // 2, SQ_SIZE // 2))
            image_pos = (rect.x + (SQ_SIZE - scaled_image.get_width()) // 2,
                         rect.y + (SQ_SIZE - scaled_image.get_height()) // 2)
            screen.blit(scaled_image, image_pos)

        pygame.display.flip()


def animate_move(screen, board, move):
    """Smoothly animate a piece moving from one square to another without breaking board state."""
    start_square = move.from_square
    end_square = move.to_square
    start_col, start_row = chess.square_file(start_square), chess.square_rank(start_square)
    end_col, end_row = chess.square_file(end_square), chess.square_rank(end_square)

    piece = board.piece_at(start_square)
    if not piece:
        return  # No piece to animate

    piece_image = IMAGES[piece.symbol()]
    start_x, start_y = start_col * SQ_SIZE, (7 - start_row) * SQ_SIZE
    end_x, end_y = end_col * SQ_SIZE, (7 - end_row) * SQ_SIZE

    frames = 10  # Adjust for speed: Higher = slower, Lower = faster

    temp_board = board.copy()  # Create a temporary board without modifying the real board
    temp_board.remove_piece_at(start_square)  # Hide moving piece from its original square

    for i in range(1, frames + 1):
        alpha = i / frames  # Interpolation factor (0 to 1)
        current_x = start_x + (end_x - start_x) * alpha
        current_y = start_y + (end_y - start_y) * alpha

        draw_board(screen, temp_board)  # Draw the temporary board without the moving piece
        screen.blit(pygame.transform.scale(piece_image, (SQ_SIZE, SQ_SIZE)), (current_x, current_y))
        pygame.display.flip()
        pygame.time.delay(10)  # Adjust for smoother/slower animation
    
    if board.piece_at(end_square):
        temp_board.remove_piece_at(end_square)
        temp_board.set_piece_at(end_square, piece)
        draw_board(screen, temp_board)  # Draw the temporary board without the captured piece
        pygame.display.flip()


def start_screen(screen):
    font = pygame.font.Font(None, 50)  # Choose font and size
    text_color = pygame.Color("red")

    # Render the text
    text_surface = font.render("Choose Color", True, text_color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    # Buttons
    button_font = pygame.font.Font(None, 40)
    white_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 4, 50)
    black_button = pygame.Rect(WIDTH // 2, HEIGHT // 2, WIDTH // 4, 50)

    running = True
    while running:
        screen.fill(pygame.Color("lightgray"))
        screen.blit(text_surface, text_rect)

        # Draw buttons
        pygame.draw.rect(screen, pygame.Color("white"), white_button)
        pygame.draw.rect(screen, pygame.Color("black"), black_button)

        white_text = button_font.render("White", True, text_color)
        black_text = button_font.render("Black", True, text_color)
        screen.blit(white_text, white_button.move(60, 10))
        screen.blit(black_text, black_button.move(60, 10))

        pygame.display.flip()

        # Handle button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if white_button.collidepoint(event.pos):
                    return chess.WHITE
                elif black_button.collidepoint(event.pos):
                    return chess.BLACK


def game_over_screen(screen, result):
    """Display the game over screen with options to restart or exit."""
    font = pygame.font.Font(None, 50)  # Choose font and size
    text_color = pygame.Color("black")

    # Determine the message based on the result
    if result == "white":
        message = "White Wins!"
    elif result == "black":
        message = "Black Wins!"
    else:
        message = "Game Drawn"

    # Render the text
    text_surface = font.render(message, True, text_color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    # Buttons
    button_font = pygame.font.Font(None, 40)
    rematch_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 4, 50)
    end_button = pygame.Rect(WIDTH // 2, HEIGHT // 2, WIDTH // 4, 50)

    running = True
    while running:
        screen.fill(pygame.Color("white"))
        screen.blit(text_surface, text_rect)

        # Draw buttons
        pygame.draw.rect(screen, pygame.Color("lightgray"), rematch_button)
        pygame.draw.rect(screen, pygame.Color("red"), end_button)

        rematch_text = button_font.render("Rematch", True, text_color)
        end_text = button_font.render("End", True, text_color)
        screen.blit(rematch_text, rematch_button.move(45, 10))
        screen.blit(end_text, end_button.move(70, 10))

        pygame.display.flip()

        # Handle button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rematch_button.collidepoint(event.pos):
                    return "rematch"
                elif end_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()


def check_game_over(screen, board):
    """Check if the game is over and show the game over screen."""
    if board.is_checkmate():
        winner = "white" if board.turn == chess.BLACK else "black"
        result = game_over_screen(screen, winner)
        return result
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_repetition(3):
        result = game_over_screen(screen, "draw")
        return result
    return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess AI Visualization")
    player_turn = start_screen(screen)
    player_turn == chess.BLACK
    if player_turn == chess.WHITE:
        ai_white = False
    else:
        ai_white = True
        flipped = True
    board = chess.Board()
    ai = SimpleChessAI(depth=3)
    running = True
    move_from = None  # To track the start of a user's move

    while running:
        screen.fill(pygame.Color("white"))
        draw_board(screen, board, flipped)
        # Draw the highlight for the selected piece (if move_from is not None)
        if move_from is not None:
            # Create a transparent red highlight for piece
            highlight_surface = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
            highlight_surface.fill((255, 0, 0, 100))
            screen.blit(highlight_surface, (col * SQ_SIZE, (7-row) * SQ_SIZE))
            
            move_to_squares = set([move.to_square for move in board.legal_moves if move.from_square == move_from])
            for to_square in move_to_squares:
                r, c = divmod(to_square, 8)
                # Create a transparent green highlight for possible moves
                move_surface = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                move_surface.fill((0, 255, 0, 100))
                screen.blit(move_surface, (c * SQ_SIZE, (7-r) * SQ_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and board.turn == player_turn:
                mouse_pos = pygame.mouse.get_pos()
                col, row = get_square_from_mouse(mouse_pos, flipped)
                square = chess.square(col, row)

                if move_from is None:
                    # Select piece to move and show possible moves
                    if board.piece_at(square) is not None and board.piece_at(square).color == player_turn:
                        move_from = square
                        pygame.draw.rect(screen, (255, 0, 0, 100), pygame.Rect(col * SQ_SIZE, (7-row) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                        move_to_squares = [move.to_square for move in board.legal_moves if move.from_square == move_from]
                        for to_square in move_to_squares:
                            r, c = divmod(to_square, 8)
                            pygame.draw.rect(screen, (0, 255, 0, 100), pygame.Rect(c * SQ_SIZE, (7-r) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

                else:
                    # Make move
                    move_to = square
                    move = chess.Move(move_from, move_to)
                    if board.piece_at(move_from).piece_type == chess.PAWN and (chess.square_rank(move_to) == 7 or chess.square_rank(move_to) == 0):
                        # Show promotion menu and wait for user input
                        promotion_piece = show_promotion_menu(screen, move_to, board)
                        move = chess.Move(move_from, move_to, promotion=promotion_piece)
                    if move in board.legal_moves:
                        animate_move(screen, board, move)  # Animate the movement
                        board.push(move)  # Apply the move after animation
                        ai.board.push(move)
                        move_from = None  # Reset after the move

                        # Check if the game is over
                        result = check_game_over(screen, board)
                        if result == "rematch":
                            board = chess.Board()  # Reset the board
                            ai.board = chess.Board()  # Reset AI's board
                    else:
                        move_from = None  # Invalid move, reset

            if board.turn != player_turn:
                start_time = time.time()
                ai_move = ai.get_best_move(ai_white)
                end_time = time.time()
                time_taken = end_time - start_time

                print(f"AI plays: {ai_move}")
                print(f"AI thought for {time_taken:.2f} seconds.")

                animate_move(screen, board, ai_move)  # Animate the AI move before applying it
                board.push(ai_move)  # Apply the move after animation
                ai.board.push(ai_move)

                # Check if the game is over
                result = check_game_over(screen, board)
                if result == "rematch":
                    board = chess.Board()
                    ai.board = chess.Board()

        pygame.display.flip()

    pygame.quit()


main()
