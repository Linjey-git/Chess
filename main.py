import tkinter as tk

from gui import ChessApp


# # Друге вікно для вводу ходу
# def input_window(data_queue):
#     while True:
#         move_str = input("Введіть ваш хід (наприклад, e2e4): ").strip()
#         move = chess.Move.from_uci(move_str)
#         data_queue.put(move)

# def get_best_move(data_queue, app, bot):
#     while True:
#         move = bot.get_best_move(app.events.get_board_state)
#         data_queue.put(move)


def main():
    root = tk.Tk()
    app = ChessApp(root)
    # bot_controller = ChessBotController(dfs_depth=4, bfs_depth=3, ucs_depth=3)

    # Черга для передачі даних
    # data_queue = queue.Queue()

    # Запуск другого вікна в окремому потоці
    # input_thread = Thread(target=input_window, args=(data_queue,), daemon=True)
    # input_thread.start()

    # Постійне оновлення головного вікна для перевірки нових даних
    def check_for_data():
        while not app.events.data_queue.empty():
            move = app.events.data_queue.get()
            print(f"Отримано хід: {move}")
            app.draw_move_arrow(move)  # Виклик функції для відображення ходу
        root.after(100, check_for_data)

    check_for_data()
    root.mainloop()


if __name__ == "__main__":
    main()
