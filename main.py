from threading import Thread
import queue
import tkinter as tk

import chess

from gui import ChessApp


# Друге вікно для вводу ходу
def input_window(data_queue):
    while True:
        move_str = input("Введіть ваш хід (наприклад, e2e4): ").strip()
        move = chess.Move.from_uci(move_str)
        data_queue.put(move)



def main():
    root = tk.Tk()
    app = ChessApp(root)

    # Черга для передачі даних
    data_queue = queue.Queue()

    # Запуск другого вікна в окремому потоці
    input_thread = Thread(target=input_window, args=(data_queue,), daemon=True)
    input_thread.start()

    # Постійне оновлення головного вікна для перевірки нових даних
    def check_for_data():
        while not data_queue.empty():
            move = data_queue.get()
            print(f"Отримано хід: {move}")
            app.draw_move_arrow(move)  # Виклик функції для відображення ходу
        root.after(100, check_for_data)

    check_for_data()
    root.mainloop()


if __name__ == "__main__":
    main()
