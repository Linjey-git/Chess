import threading
from ctypes import c_ushort

import chess
from chess.svg import board

import promotion
import queue

from board import ChessBoard
from chess_bot_controller import ChessBotController
from constants import SQUARE_SIZE
from tkinter import messagebox
from threading import Thread, Event


class ChessEvents:
    def __init__(self, chess_board, chess_app):
        """Ініціалізація класу ChessEvents.
        Призначає шахівницю та додаток, ініціалізує початкові значення для вибраних клітинок та фігур.
        Initialization of the ChessEvents class.
        Assigns the chessboard and app, initializes the initial values for selected squares and pieces."""
        self.chess_app = chess_app  # Шаховий додаток / Chess application
        self.board = chess_board  # Шахівниця / Chessboard
        self.selected_square = None  # Зберігає вибрану клітинку для ходу / Stores selected square for move
        self.selected_piece = None  # Зберігає вибрану фігуру для ходу / Stores selected piece for move

        self.help_thread = None  # Потік для Help / Thread for Help
        self.help_active = False  # Індикатор активності кнопки Help / Indicator of Help button activity
        self.help_stop_event = Event()  # Подія для зупинки потоку Help / Event to stop the Help thread
        self.bot_controller = ChessBotController(dfs_depth=4, bfs_depth=3)  # Контролер бота / Bot controller
        self.data_queue = queue.Queue()  # Черга для передачі даних / Queue for data transfer

        self.event = threading.Event()

    def toggle_help(self):
        """Обробник натискання кнопки Help.
        Перемикає стан допомоги: включає/вимикає потік допомоги.
        Handler for Help button click. Toggles the Help state: starts/stops the Help thread."""
        if self.help_active:
            self.help_active = False  # Зупиняємо допомогу / Stop Help
            print("Help зупинено")  # Повідомлення в консолі / Console message
            self.chess_app.help_button_text.set("Help OFF")  # Оновлюємо текст кнопки / Update button text
            self.stop_help()  # Зупиняємо потік допомоги / Stop Help thread
        else:
            self.help_active = True  # Включаємо допомогу / Start Help
            print("Help запущено")  # Повідомлення в консолі / Console message
            self.chess_app.help_button_text.set("Help ON")  # Оновлюємо текст кнопки / Update button text
            self.start_help()  # Запускаємо потік допомоги / Start Help thread

    def start_help(self):
        """Запуск потоку Help.
        Starts the Help thread."""
        self.help_stop_event.clear()  # Скидаємо стан події / Clear event state
        self.help_thread = Thread(target=self.help_thread_function,
                                  args=(self.data_queue, self.bot_controller, self.event,),
                                  daemon=True)
        self.help_thread.start()  # Запускаємо допоміжний потік / Start the help thread

    def stop_help(self):
        """Зупинка потоку Help.
        Stops the Help thread."""
        self.chess_app.canvas.delete("arrow")  # Видаляємо стрілку на шахівниці / Remove the arrow on the chessboard
        self.help_stop_event.set()  # Встановлюємо подію для зупинки потоку / Set event to stop the thread
        # self.help_thread.join()

    def help_thread_function(self, data_queue, bot, event):
        """Функція, яка виконується у потоці Help для отримання кращого ходу від бота.
        Function that runs in the Help thread to get the best move from the bot."""
        while not self.help_stop_event.is_set():  # Перевірка на зупинку потоку / Check if the thread is stopped
            # while True:

            print("Пошук шукає")
            if self.board.is_initial_position():
                print("шахівниця змінилась")
                move = bot.get_best_move(self.board.get_board())  # Отримуємо кращий хід / Get the best move
                data_queue.put(move)  # Додаємо хід в чергу / Add move to the queue

            else:

                print("шахівниця змінилась")
                move = bot.get_best_move(self.board.get_board())  # Отримуємо кращий хід / Get the best move
                data_queue.put(move)  # Додаємо хід в чергу / Add move to the queue

            event.wait()

        # event.set()
        # continue

    def help_thread_function_1(self, data_queue):
        """Функція для введення ходу користувачем через консоль.
        Function for inputting a move from the user via the console."""
        while True:
            move_str = input("Введіть ваш хід (наприклад, e2e4): ").strip()  # Читання ходу / Reading the move
            move = chess.Move.from_uci(
                move_str)  # Перетворення введеного ходу в об'єкт ходу / Convert input move to a move object
            data_queue.put(move)  # Додаємо хід в чергу / Add move to the queue

    def on_square_click(self, event):
        """Обробка кліку по клітинці на шахівниці.
        Визначає, який хід здійснив користувач після вибору клітинки.
        Handler for square click on the chessboard. Determines the move made by the user after selecting a square."""
        col = event.x // SQUARE_SIZE  # Визначаємо стовпчик клітинки / Calculate the column of the clicked square
        row = event.y // SQUARE_SIZE  # Визначаємо рядок клітинки / Calculate the row of the clicked square
        print("Перевірку пройдено 0")  # Debug print / Debug message

        row = 7 - row  # Інвертуємо рядок для перевернутого відображення шахівниці / Invert row for flipped board view

        square = 8 * row + col  # Обчислюємо номер клітинки / Calculate the square index

        if self.selected_square is not None:  # Якщо фігура вже вибрана / If a piece is already selected
            move = chess.Move(self.selected_square, square)  # Створюємо хід / Create the move
            if move in self.board.get_legal_moves():  # Якщо хід допустимий / If the move is legal
                if self.selected_piece and self.selected_piece.piece_type == chess.PAWN:
                    print("Перевірку пройдено 1")  # Debug print / Debug message
                    if (self.selected_piece.color == chess.WHITE and row == 7) or (
                            self.selected_piece.color == chess.BLACK and row == 0):
                        print("Перевірку пройдено 2")  # Debug print / Debug message
                        print(move)
                        # Виклик функції для перетворення пішака / Call the function for pawn promotion
                        promotion_move = promotion.get_promotion_choice(self.selected_square, square)
                        if promotion_move:
                            print("Перевірку пройдено 3")  # Debug print / Debug message
                            move = promotion_move  # Заміна стандартного ходу на хід із перетворенням / Replace move with promotion move
                            print(move)

                self.board.make_move(move)  # Виконуємо хід / Execute the move
                self.chess_app.update_board()  # Оновлюємо шахівницю / Update the chessboard
                self.chess_app.canvas.delete("arrow")
                self.event.set()
                self.event.clear()

                if self.board.is_game_over():  # Перевірка на закінчення гри / Check if the game is over
                    messagebox.showinfo("Game Over",
                                        "Game Over!")  # Повідомлення про завершення гри / Game over message
                    self.board.reset()  # Скидаємо шахівницю / Reset the chessboard
                    self.chess_app.update_board()  # Оновлюємо шахівницю після скидання / Update the board after reset

                self.selected_square = None  # Скидаємо вибір фігури / Reset the selected square
            else:
                self.selected_square = None  # Скидаємо вибір, якщо хід недійсний / Reset if move is invalid
                self.chess_app.update_board()  # Оновлюємо шахівницю для видалення підсвічених ходів / Update the board to remove highlighted moves

        else:
            print("Просто клітина")  # Debug print / Debug message
            piece = self.board.get_board().piece_at(
                square)  # Перевірка, чи є фігура на клітинці / Check if there is a piece on the square
            if piece:  # Якщо є фігура на клітинці / If there is a piece on the square
                print("Є фігура")  # Debug print / Debug message
                self.selected_square = square  # Вибираємо фігуру / Select the piece
                self.selected_piece = piece  # Запам'ятовуємо вибрану фігуру / Store the selected piece
                print(self.selected_piece)  # Debug print / Debug message
                self.chess_app.update_board()  # Оновлюємо шахівницю для відображення можливих ходів / Update the board to show possible moves

    def get_board_state(self):
        """Повертає поточний стан шахівниці у вигляді словника, де ключ — клітинка, а значення — фігура.
        Returns the current state of the chessboard as a dictionary where the key is the square and the value is the piece."""
        # return {square: str(piece) for square, piece in self.board.board.piece_map().items()
        return self.board.get_board
