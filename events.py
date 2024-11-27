import chess
import promotion
import queue

from constants import SQUARE_SIZE
from tkinter import messagebox
from threading import Thread, Event


class ChessEvents:
    def __init__(self, chess_board, chess_app):
        self.chess_app = chess_app
        self.board = chess_board
        self.selected_square = None  # зберігаємо вибрану клітинку для ходу
        self.selected_piece = None  # зберігаємо вибрану фігуру для ходу

        self.help_thread = None
        self.help_active = False  # Індикатор стану кнопки Help
        self.help_stop_event = Event()  # Подія для зупинки потоку Help
        # self.bot_controller = ChessBotController(dfs_depth=4, bfs_depth=3, ucs_depth=3)
        # Черга для передачі даних
        self.data_queue = queue.Queue()

    def toggle_help(self):
        """Обробник натискання кнопки Help."""
        if self.help_active:
            self.help_active = False
            print("Help зупинено")
            self.chess_app.help_button_text.set("Help OFF")
            self.stop_help()
        else:
            self.help_active = True
            print("Help запущено")
            self.chess_app.help_button_text.set("Help ON")
            self.start_help()

    def start_help(self):
        """Запуск потоку Help."""
        self.help_stop_event.clear()  # Скидаємо стан події
        # self.help_thread = Thread(target=self.help_thread_function, args=(self.data_queue,self.chess_app, self.bot_controller,),daemon=True)
        self.help_thread = Thread(target=self.help_thread_function, args=(self.data_queue,),daemon=True)
        self.help_thread.start()

    def stop_help(self):
        """Зупинка потоку Help."""
        self.chess_app.canvas.delete("arrow")
        self.help_stop_event.set()  # Встановлюємо стан події для зупинки потоку

    def help_thread_function_1(self, data_queue, app, bot):
        """Функція, яка виконується у потоці Help."""
        while not self.help_stop_event.is_set():
            print("Help працює")
            # Тут можна додати вашу логіку, наприклад, аналіз або підказки.
            # time.sleep(1)  # Приклад очікування
            while True:
                move = bot.get_best_move(app.events.get_board_state)
                data_queue.put(move)

    # Друге вікно для вводу ходу
    def help_thread_function(self, data_queue):
        while True:
            move_str = input("Введіть ваш хід (наприклад, e2e4): ").strip()
            move = chess.Move.from_uci(move_str)
            data_queue.put(move)

    def on_square_click(self, event):
        """Обробка кліку по клітинці на шахівниці."""
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        print("Перевірку пройдено 0")

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
                        promotion_move = promotion.get_promotion_choice(self.selected_square, square)
                        if promotion_move:
                            print("Перевірку пройдено 3")
                            move = promotion_move  # Заміна стандартного ходу на хід із перетворенням
                            print(move)

                self.board.make_move(move)
                # self.chess_app.draw_move_arrow(move)
                self.chess_app.update_board()

                if self.board.is_game_over():
                    messagebox.showinfo("Гра завершена", "Гра завершена!")
                    self.board.reset()
                    self.chess_app.update_board()

                self.selected_square = None  # Скидаємо вибір фігури після ходу
            else:
                self.selected_square = None  # Скидаємо вибір, якщо хід недійсний
                self.chess_app.update_board()  # Оновлюємо шахівницю для видалення підсвічених ходів

        else:
            print("Просто клітина")
            piece = self.board.get_board().piece_at(square)
            if piece:  # Якщо клітинка містить фігуру
                print("Є фігура")
                self.selected_square = square  # Вибираємо фігуру
                self.selected_piece = piece
                print(self.selected_piece)
                self.chess_app.update_board()  # Оновлюємо шахівницю для відображення можливих ходів

    def get_board_state(self):
        return {square: str(piece) for square, piece in self.board.board.piece_map().items()}
