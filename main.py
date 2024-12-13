import tkinter as tk

from gui import ChessApp


def main():
    root = tk.Tk()
    app = ChessApp(root)
    app.events.event.set()
    app.events.event.clear()

    # Постійне оновлення головного вікна для перевірки нових даних /
    # Constantly refreshing the main window to check for new data
    def check_for_data():
        while not app.events.data_queue.empty():
            move = app.events.data_queue.get()
            print(f"Move obtained: {move}")  # Received move
            app.draw_move_arrow(move)  # Виклик функції для відображення ходу / Calling the function to display the move
        root.after(100, check_for_data)

    check_for_data()
    root.mainloop()


if __name__ == "__main__":
    main()
