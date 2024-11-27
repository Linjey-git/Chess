import tkinter as tk


class Resources:
    def __init__(self, sq_size):
        self.sq_size = sq_size
        self.piece_images = {}

    def load_piece_images(self):
        """Завантажує зображення фігур і змінює їх розмір."""
        piece_types = ['r', 'n', 'b', 'q', 'k', 'p']  # Типи фігур
        colors = ['w', 'b']  # Кольори фігур
        for color in colors:
            for piece in piece_types:
                file_name = f"images/{color}{piece.upper()}.png"
                image = tk.PhotoImage(file=file_name)

                # Масштабуємо зображення відповідно до нового розміру клітинки
                scale_factor = int(self.sq_size * 0.07)  # Масштабування фігур до 7% від розміру клітинки
                image = image.zoom(scale_factor, scale_factor)  # Збільшуємо зображення фігури

                self.piece_images[f"{color}{piece}"] = image

        print(self.piece_images)

    def get_piece_images(self):
        """Повертає словник із зображеннями фігур."""
        print(self.piece_images)
        return self.piece_images
