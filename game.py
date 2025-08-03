import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
FONT = pygame.font.SysFont("Segoe UI Symbol", 44)
TITLE_FONT = pygame.font.SysFont("Arial", 28)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
BLUE = (66, 135, 245)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Scoreboard and names
player1 = "White"
player2 = "Black"
scores = {"White": 0, "Black": 0}

# Unicode chess pieces
PIECE_SYMBOLS = {
    "br": "♜", "bn": "♞", "bb": "♝", "bq": "♛", "bk": "♚", "bp": "♟",
    "wr": "♖", "wn": "♘", "wb": "♗", "wq": "♕", "wk": "♔", "wp": "♙"
}

# Piece values for scoring
PIECE_VALUES = {
    "p": 1,
    "n": 3,
    "b": 3,
    "r": 5,
    "q": 9,
    "k": 0  # King usually not scored
}

# Chess board setup
def create_board():
    return [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp"] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        ["wp"] * 8,
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
    ]

board = create_board()
selected = None
turn = "w"
game_over = False

# Drawing functions
def draw_board():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE + 100, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if piece:
                text = FONT.render(PIECE_SYMBOLS[piece], True, BLACK)
                screen.blit(text, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 110))

    # Draw names and scores
    white_text = TITLE_FONT.render(f"White: {scores['White']}", True, BLACK)
    black_text = TITLE_FONT.render(f"Black: {scores['Black']}", True, BLACK)
    screen.blit(white_text, (20, 20))
    screen.blit(black_text, (350, 20))

    # Draw turn indicator
    turn_text = TITLE_FONT.render(f"Turn: {'White' if turn == 'w' else 'Black'}", True, BLUE)
    screen.blit(turn_text, (220, 60))

    # Draw reset button
    pygame.draw.rect(screen, BLUE, (500, 60, 80, 30))
    reset_text = TITLE_FONT.render("Reset", True, WHITE)
    screen.blit(reset_text, (505, 63))

def reset_game():
    global board, selected, turn, game_over, scores
    board = create_board()
    selected = None
    turn = "w"
    game_over = False
    scores = {"White": 0, "Black": 0}

def is_valid_position(pos):
    row, col = pos
    return 0 <= row < 8 and 0 <= col < 8

def is_valid_move(start, end):
    sr, sc = start
    er, ec = end
    if not is_valid_position(start) or not is_valid_position(end):
        return False

    moving_piece = board[sr][sc]
    target_piece = board[er][ec]
    if moving_piece == "":
        return False

    if target_piece != "" and moving_piece[0] == target_piece[0]:
        return False

    return True  # Simplified. Will add actual piece logic next

def move_piece(start, end):
    sr, sc = start
    er, ec = end
    global scores

    captured_piece = board[er][ec]
    if captured_piece != "":
        capturing_color = "White" if board[sr][sc][0] == "w" else "Black"
        captured_type = captured_piece[1]
        scores[capturing_color] += PIECE_VALUES.get(captured_type, 0)

    board[er][ec] = board[sr][sc]
    board[sr][sc] = ""

def main():
    global selected, turn
    clock = pygame.time.Clock()

    while True:
        draw_board()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 500 <= x <= 580 and 60 <= y <= 90:
                    reset_game()
                    continue
                if y < 100:
                    continue
                row = (y - 100) // SQUARE_SIZE
                col = x // SQUARE_SIZE

                if selected:
                    if is_valid_move(selected, (row, col)):
                        move_piece(selected, (row, col))
                        turn = "b" if turn == "w" else "w"
                    selected = None
                else:
                    if board[row][col] != "" and board[row][col][0] == turn:
                        selected = (row, col)

        clock.tick(60)

if __name__ == "__main__":
    main()
