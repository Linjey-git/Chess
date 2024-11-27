import tkinter as tk

from board import ChessBoard
from resources import Resources
from events import ChessEvents
from constants import SQUARE_SIZE, BOARD_COLORS
from graphics import Graphics


class ChessApp:
    def __init__(self, root):
        """Ініціалізація шахового додатку.
        Initializes the Chess app."""
        self.root = root
        self.root.title("Chess")

        # Встановлюємо заборону на зміну розміру вікна
        # Disable window resizing
        self.root.resizable(False, False)

        self.board = ChessBoard()

        # Канвас для шахівниці
        # Canvas for the chessboard
        self.canvas = tk.Canvas(self.root, width=SQUARE_SIZE * 8 + 100, height=SQUARE_SIZE * 8)
        self.canvas.pack()

        self.graphics = Graphics(SQUARE_SIZE)
        self.resources = Resources(SQUARE_SIZE)
        self.events = ChessEvents(self.board, self)

        self.resources.load_piece_images()
        self.piece_images = self.resources.get_piece_images()  # Зберігаємо зображення фігур / Store piece images
        self.draw_board()
        self.update_board()

        # Додаємо кнопку Help
        # Add Help button
        self.help_button_text = tk.StringVar(value="Help OFF")  # Початковий текст / Initial text
        self.help_button = tk.Button(
            self.root,
            textvariable=self.help_button_text,
            command=self.events.toggle_help,  # Викликає функцію обробки / Calls handler function
            width=8,
            bg="lightgray"
        )
        self.help_button.place(x=SQUARE_SIZE * 8, y=SQUARE_SIZE * 4)  # Розташування кнопки праворуч / Position button to the right

        self.canvas.bind("<Button-1>", self.events.on_square_click)

    def draw_board(self):
        """Малюємо шахівницю.
        Draws the chessboard."""
        colors = BOARD_COLORS
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                             (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                                             fill=color, outline="black")

    def draw_highlight_square(self, row, col):
        """Малюємо жовтий квадрат для підсвічування можливого ходу.
        Draws yellow square to highlight a possible move."""
        self.canvas.create_image(
            col * SQUARE_SIZE + SQUARE_SIZE / 2,  # x координата (по центру клітинки) / x coordinate (center of the square)
            row * SQUARE_SIZE + SQUARE_SIZE / 2,  # y координата (по центру клітинки) / y coordinate (center of the square)
            image=self.graphics.yellow_square_image,  # Зображення квадрата / Square image
            tags="moves"  # Тег для видалення попередніх підсвічувань / Tag to remove previous highlights
        )

    def highlight_legal_moves(self):
        """Підсвічує можливі ходи для вибраної фігури.
        Highlights legal moves for the selected piece."""
        self.canvas.delete("moves")  # Очищаємо попередні підсвічені ходи / Clear previous highlights

        if self.events.selected_square is not None:
            legal_moves = self.board.get_legal_moves()
            move_count = 0  # Ініціалізуємо лічильник для ходів / Initialize move counter
            for move in legal_moves:
                if move.from_square == self.events.selected_square:
                    move_count += 1  # Інкрементуємо лічильник / Increment the counter
                    print(f"{move} - Кількість: {move_count}")  # Виводимо хід і кількість виконаних ходів / Print move and count
                    dest_row, dest_col = divmod(move.to_square, 8)
                    dest_row = 7 - dest_row  # Інвертуємо рядок для відображення на перевернутій шахівниці / Invert row for flipped board

                    # Викликаємо нову функцію для малювання жовтого квадрату / Call new function to draw yellow square
                    self.draw_highlight_square(dest_row, dest_col)

    def highlight_check(self):
        """Перевіряє, чи є шах, і підсвічує клітинку короля червоним.
        Checks for check and highlights the king's square in red."""
        if self.board.get_board().is_check():
            king_square = self.board.get_board().king(self.board.get_board().turn)
            if king_square is not None:
                row, col = divmod(king_square, 8)
                row = 7 - row  # Інвертуємо рядок для перевернутої шахівниці / Invert row for flipped board
                self.canvas.create_image(
                    col * SQUARE_SIZE + SQUARE_SIZE / 2,
                    row * SQUARE_SIZE + SQUARE_SIZE / 2,
                    image=self.graphics.red_square_image,
                    tags="check"  # Додаємо тег для видалення попереднього шаху / Add tag for removing previous check
                )

    def update_board(self):
        """Оновлюємо шахівницю після кожного ходу.
        Updates the chessboard after every move."""
        self.canvas.delete("pieces")  # Очищаємо попередні фігури / Clear previous pieces
        self.canvas.delete("check")  # Очищаємо попереднє виділення шаху / Clear previous check highlight
        # self.canvas.delete("arrow")  # очищаємо попередню стрілку / Clear previous arrow
        for i in range(8):
            for j in range(8):
                square = 8 * i + j
                piece = self.board.get_board().piece_at(square)
                if piece:
                    # Визначаємо колір фігури та її тип / Determine piece color and type
                    color = 'w' if piece.color else 'b'
                    piece_name = f"{color}{piece.symbol()}".lower()  # Наприклад: 'wr', 'bn' / Example: 'wr', 'bn'
                    print(piece_name)
                    row = 7 - i
                    col = j
                    # Створюємо зображення фігури на нових координатах / Create piece image at new coordinates
                    self.canvas.create_image(col * SQUARE_SIZE + SQUARE_SIZE / 2,
                                             row * SQUARE_SIZE + SQUARE_SIZE / 2,
                                             image=self.piece_images[piece_name], anchor="center", tags="pieces")

        self.highlight_check()  # Виклик нової функції для перевірки шаху / Call the new function to check for check
        self.highlight_legal_moves()  # Підсвічуємо можливі ходи для вибраної фігури / Highlight legal moves for selected piece

    def draw_move_arrow(self, move):
        """Малює червону стрілку, що символізує хід.
        Draws a red arrow to represent a move."""
        self.canvas.delete("arrow")  # Очищаємо попередню стрілку / Clear previous arrow
        from_square = move.from_square
        to_square = move.to_square

        # Перетворення координат квадратів на координати канваса / Convert square coordinates to canvas coordinates
        from_col, from_row = from_square % 8, from_square // 8
        to_col, to_row = to_square % 8, to_square // 8

        # Перевернути рахування рядків, щоб нижній ряд був 0, а верхній 7 / Flip row counting so bottom row is 0, top is 7
        from_row = 7 - from_row
        to_row = 7 - to_row

        # Перетворюємо ці координати на координати пікселів на канвасі / Convert these to pixel coordinates on the canvas
        from_x1, from_y1 = from_col * SQUARE_SIZE, from_row * SQUARE_SIZE
        to_x1, to_y1 = to_col * SQUARE_SIZE, to_row * SQUARE_SIZE

        # Малюємо стрілку між клітинками / Draw arrow between squares
        self.canvas.create_line(from_x1 + SQUARE_SIZE // 2, from_y1 + SQUARE_SIZE // 2,
                                to_x1 + SQUARE_SIZE // 2, to_y1 + SQUARE_SIZE // 2,
                                arrow=tk.LAST, fill="red", width=3, tags="arrow")