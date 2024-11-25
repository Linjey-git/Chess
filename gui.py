import chess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from board import ChessBoard


class ChessApp:
    def __init__(self, root):
        self.promotion_result = None
        self.root = root
        self.root.title("Chess")

        # Встановлюємо заборону на зміну розміру вікна
        self.root.resizable(False, False)  # Запобігає зміні розміру вікна

        self.board = ChessBoard()

        self.sq_size = 80  # Змінюємо розмір клітинки на більший (наприклад, 80 пікселів)
        self.canvas = tk.Canvas(self.root, width=self.sq_size * 8, height=self.sq_size * 8)  # Канвас для шахівниці
        self.canvas.pack()

        self.selected_square = None  # зберігаємо вибрану клітинку для ходу
        self.selected_piece = None  # зберігаємо вибрану фігуру для ходу

        self.piece_images = {}  # зберігаємо зображення фігур
        self.load_images()
        self.draw_board()
        self.update_board()
        self.yellow_square_image = self.create_transparent_yellow_square()

        self.canvas.bind("<Button-1>", self.on_square_click)

    def create_transparent_yellow_square(self):
        square_size = self.sq_size
        alpha = 128
        img = Image.new("RGBA", (square_size, square_size), (255, 255, 0, alpha))
        return ImageTk.PhotoImage(img)

    def load_images(self):
        """Завантажуємо зображення фігур і змінюємо їх розмір."""
        piece_types = ['r', 'n', 'b', 'q', 'k', 'p']  # типи фігур
        colors = ['w', 'b']  # кольори фігур
        for color in colors:
            for piece in piece_types:
                file_name = f"images/{color}{piece.upper()}.png"
                image = tk.PhotoImage(file=file_name)

                # Масштабуємо зображення відповідно до нового розміру клітинки
                scale_factor = int(self.sq_size * 0.07)  # Масштабування фігур до 75% від розміру клітинки
                image = image.zoom(scale_factor, scale_factor)  # Збільшуємо зображення фігури

                self.piece_images[f"{color}{piece}"] = image

        print(self.piece_images)

    def draw_board(self):
        """Малюємо шахівницю."""
        colors = ["#f0d9b5", "#b58863"]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(col * self.sq_size, row * self.sq_size,
                                             (col + 1) * self.sq_size, (row + 1) * self.sq_size,
                                             fill=color, outline="black")

    def draw_highlight_square(self, row, col):
        """Малюємо жовтий квадрат для підсвічування можливого ходу."""
        self.canvas.create_image(
            col * self.sq_size + self.sq_size / 2,  # x координата (по центру клітинки)
            row * self.sq_size + self.sq_size / 2,  # y координата (по центру клітинки)
            image=self.yellow_square_image,  # Зображення квадрата
            tags="moves"  # Тег для видалення попередніх підсвічувань
        )

    def highlight_legal_moves(self):
        """Підсвічує можливі ходи для вибраної фігури."""
        self.canvas.delete("moves")  # Очищаємо попередні підсвічені ходи

        if self.selected_square is not None:
            legal_moves = self.board.get_legal_moves()
            # print(legal_moves)
            move_count = 0  # Ініціалізуємо лічильник для ходів
            for move in legal_moves:
                if move.from_square == self.selected_square:
                    move_count += 1  # Інкрементуємо лічильник
                    print(f"{move} - Кількість: {move_count}")  # Виводимо хід і кількість виконаних ходів
                    dest_row, dest_col = divmod(move.to_square, 8)
                    dest_row = 7 - dest_row  # Інвертуємо рядок для відображення на перевернутій шахівниці

                    # Викликаємо нову функцію для малювання жовтого квадрату
                    self.draw_highlight_square(dest_row, dest_col)

    def update_board(self):
        """Оновлюємо шахівницю після кожного ходу."""
        self.canvas.delete("pieces")  # очищаємо попередні фігури
        for i in range(8):
            for j in range(8):
                square = 8 * i + j
                piece = self.board.get_board().piece_at(square)
                if piece:
                    # Визначаємо колір фігури та її тип
                    color = 'w' if piece.color else 'b'
                    piece_name = f"{color}{piece.symbol()}".lower()  # Наприклад: 'wr', 'bn'
                    row = 7 - i
                    col = j
                    # Створюємо зображення фігури на нових координатах
                    self.canvas.create_image(col * self.sq_size + self.sq_size / 2,
                                             row * self.sq_size + self.sq_size / 2,
                                             image=self.piece_images[piece_name], anchor="center", tags="pieces")

        self.highlight_legal_moves()  # Підсвічуємо можливі ходи для вибраної фігури

    def on_square_click(self, event):
        """Обробка кліку по клітинці на шахівниці."""
        col = event.x // self.sq_size
        row = event.y // self.sq_size

        # Інвертуємо координату рядка для коректного відображення на перевернутій шахівниці
        row = 7 - row  # Це інвертує рядки шахівниці (для перевернутого відображення)

        square = 8 * row + col  # Обчислюємо клітинку з урахуванням інвертованих рядків

        if self.selected_square is not None:
            move = chess.Move(self.selected_square, square)
            if move in self.board.get_legal_moves():  # Перевірка на допустимість ходу
                if self.selected_piece and self.selected_piece.piece_type == chess.PAWN:
                    print("Перевірку пройдено 1")
                    if (self.selected_piece.color == chess.WHITE and row == 7) or (
                            self.selected_piece.color == chess.BLACK and row == 0):
                        print("Перевірку пройдено 2")
                        print(move)
                        # Виклик функції перетворення пішака
                        promotion_move = self.promote_pawn(self.selected_square, square)
                        if promotion_move:
                            print("Перевірку пройдено 3")
                            move = promotion_move  # Заміна стандартного ходу на хід із перетворенням
                            print(move)

                # Якщо перетворення не потрібне
                self.board.make_move(move)
                self.update_board()

                if self.board.is_game_over():
                    messagebox.showinfo("Гра завершена", "Гра завершена!")
                    self.board.reset()
                    self.update_board()


                self.selected_square = None  # Скидаємо вибір фігури після ходу
            else:
                self.selected_square = None  # Скидаємо вибір, якщо хід недійсний
                self.update_board()  # Оновлюємо шахівницю для видалення підсвічених ходів

        else:
            piece = self.board.get_board().piece_at(square)
            if piece:  # Якщо клітинка містить фігуру
                self.selected_square = square  # Вибираємо фігуру
                self.selected_piece = piece
                self.update_board()  # Оновлюємо шахівницю для відображення можливих ходів

    def promote_pawn(self, square_from, square_to):
        """Показує вікно для вибору фігури, на яку перетворити пішака, і повертає хід."""
        promotion_window = tk.Toplevel(self.root)
        promotion_window.title("Перетворення пішака")

        label = tk.Label(promotion_window, text="Виберіть фігуру для перетворення:")
        label.pack()

        # Кнопки для вибору фігури
        buttons_frame = tk.Frame(promotion_window)
        buttons_frame.pack()

        self.promotion_result = None  # Ініціалізуємо результат

        def on_button_click(promotion_type):
            """Обробляє вибір фігури та закриває вікно."""
            self.promotion_result = promotion_type
            promotion_window.destroy()

        # Кнопки для вибору фігур
        tk.Button(buttons_frame, text="Queen", command=lambda: on_button_click(chess.QUEEN)).grid(row=0, column=0)
        tk.Button(buttons_frame, text="Rook", command=lambda: on_button_click(chess.ROOK)).grid(row=0, column=1)
        tk.Button(buttons_frame, text="Bishop", command=lambda: on_button_click(chess.BISHOP)).grid(row=1, column=0)
        tk.Button(buttons_frame, text="Knight", command=lambda: on_button_click(chess.KNIGHT)).grid(row=1, column=1)

        self.root.wait_window(promotion_window)  # Очікуємо закриття вікна

        if self.promotion_result is not None:
            # Повертаємо хід із вказаним перетворенням
            return chess.Move(square_from, square_to, promotion=self.promotion_result)
        return None
