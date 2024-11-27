from PIL import Image, ImageTk


class Graphics:
    def __init__(self, sq_size):
        self.sq_size = sq_size
        # Створення зображення прозорого жовтого квадрата /
        # Creates an image of a transparent yellow square
        self.yellow_square_image = self.create_transparent_yellow_square()
        # Створення зображення прозорого червоного квадрата /
        # Creates an image of a transparent red square
        self.red_square_image = self.create_transparent_red_square()

    def create_transparent_yellow_square(self):
        """Створює зображення прозорого жовтого квадрата / Creates an image of a transparent yellow square."""
        square_size = self.sq_size
        alpha = 128  # Прозорість / Transparency
        img = Image.new("RGBA", (square_size, square_size), (255, 255, 0, alpha))
        return ImageTk.PhotoImage(img)

    def create_transparent_red_square(self):
        """Створює зображення прозорого червоного квадрата / Creates an image of a transparent red square."""
        square_size = self.sq_size
        alpha = 64  # Прозорість / Transparency
        img = Image.new("RGBA", (square_size, square_size), (255, 0, 0, alpha))
        return ImageTk.PhotoImage(img)