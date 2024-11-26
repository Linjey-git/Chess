import tkinter as tk

from board import ChessBoard
from resources import Resources
from events import ChessEvents
from constants import SQUARE_SIZE, BOARD_COLORS
from graphics import Graphics


class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess")

        # Встановлюємо заборону на зміну розміру вікна
        self.root.resizable(False, False)  # Запобігає зміні розміру вікна

        self.board = ChessBoard()

        self.canvas = tk.Canvas(self.root, width=SQUARE_SIZE * 8,
                                height=SQUARE_SIZE * 8)  # Канвас для шахівниці
        self.canvas.pack()

        self.graphics = Graphics(SQUARE_SIZE)
        self.resources = Resources(SQUARE_SIZE)
        self.events = ChessEvents(self.board, self)

        self.resources.load_piece_images()
        self.piece_images = self.resources.get_piece_images()  # зберігаємо зображення фігур
        self.draw_board()
        self.update_board()

        self.canvas.bind("<Button-1>", self.events.on_square_click)

    def draw_board(self):
        """Малюємо шахівницю."""
        colors = BOARD_COLORS
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                             (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                                             fill=color, outline="black")

    def draw_highlight_square(self, row, col):
        """Малюємо жовтий квадрат для підсвічування можливого ходу."""
        self.canvas.create_image(
            col * SQUARE_SIZE + SQUARE_SIZE / 2,  # x координата (по центру клітинки)
            row * SQUARE_SIZE + SQUARE_SIZE / 2,  # y координата (по центру клітинки)
            image=self.graphics.yellow_square_image,  # Зображення квадрата
            tags="moves"  # Тег для видалення попередніх підсвічувань
        )

    def highlight_legal_moves(self):
        """Підсвічує можливі ходи для вибраної фігури."""
        self.canvas.delete("moves")  # Очищаємо попередні підсвічені ходи

        if self.events.selected_square is not None:
            legal_moves = self.board.get_legal_moves()
            move_count = 0  # Ініціалізуємо лічильник для ходів
            for move in legal_moves:
                if move.from_square == self.events.selected_square:
                    move_count += 1  # Інкрементуємо лічильник
                    print(f"{move} - Кількість: {move_count}")  # Виводимо хід і кількість виконаних ходів
                    dest_row, dest_col = divmod(move.to_square, 8)
                    dest_row = 7 - dest_row  # Інвертуємо рядок для відображення на перевернутій шахівниці

                    # Викликаємо нову функцію для малювання жовтого квадрату
                    self.draw_highlight_square(dest_row, dest_col)

    def highlight_check(self):
        """Перевіряє, чи є шах, і підсвічує клітинку короля червоним."""
        if self.board.get_board().is_check():
            king_square = self.board.get_board().king(self.board.get_board().turn)
            if king_square is not None:
                row, col = divmod(king_square, 8)
                row = 7 - row  # Інвертуємо рядок для перевернутої шахівниці
                self.canvas.create_image(
                    col * SQUARE_SIZE + SQUARE_SIZE / 2,
                    row * SQUARE_SIZE + SQUARE_SIZE / 2,
                    image=self.graphics.red_square_image,
                    tags="check"  # Додаємо тег для видалення попереднього шаху
                )

    def update_board(self):
        """Оновлюємо шахівницю після кожного ходу."""
        self.canvas.delete("pieces")  # очищаємо попередні фігури
        self.canvas.delete("check")  # очищаємо попереднє виділення шаху
        # self.canvas.delete("arrow")  # очищаємо попередню стрілку
        for i in range(8):
            for j in range(8):
                square = 8 * i + j
                piece = self.board.get_board().piece_at(square)
                if piece:
                    # Визначаємо колір фігури та її тип
                    color = 'w' if piece.color else 'b'
                    piece_name = f"{color}{piece.symbol()}".lower()  # Наприклад: 'wr', 'bn'
                    print(piece_name)
                    row = 7 - i
                    col = j
                    # Створюємо зображення фігури на нових координатах
                    self.canvas.create_image(col * SQUARE_SIZE + SQUARE_SIZE / 2,
                                             row * SQUARE_SIZE + SQUARE_SIZE / 2,
                                             image=self.piece_images[piece_name], anchor="center", tags="pieces")

        self.highlight_check()  # Виклик нової функції для перевірки шаху
        self.highlight_legal_moves()  # Підсвічуємо можливі ходи для вибраної фігури

    def draw_move_arrow(self, move):
        """Малює червону стрілку, що символізує хід."""
        self.canvas.delete("arrow")  # очищаємо попередню стрілку
        from_square = move.from_square
        to_square = move.to_square

        # Перетворення координат квадратів на координати канваса
        from_col, from_row = from_square % 8, from_square // 8
        to_col, to_row = to_square % 8, to_square // 8

        # Перевернути рахування рядків, щоб нижній ряд був 0, а верхній 7
        from_row = 7 - from_row
        to_row = 7 - to_row

        # Перетворюємо ці координати на координати пікселів на канвасі
        from_x1, from_y1 = from_col * SQUARE_SIZE, from_row * SQUARE_SIZE
        to_x1, to_y1 = to_col * SQUARE_SIZE, to_row * SQUARE_SIZE

        # Малюємо стрілку між клітинками
        self.canvas.create_line(from_x1 + SQUARE_SIZE // 2, from_y1 + SQUARE_SIZE // 2,
                                to_x1 + SQUARE_SIZE // 2, to_y1 + SQUARE_SIZE // 2,
                                arrow=tk.LAST, fill="red", width=3, tags="arrow")