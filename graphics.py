from PIL import Image, ImageTk


class Graphics:
    def __init__(self, sq_size):
        self.sq_size = sq_size
        self.yellow_square_image = self.create_transparent_yellow_square()
        self.red_square_image = self.create_transparent_red_square()

    def create_transparent_yellow_square(self):
        square_size = self.sq_size
        alpha = 128
        img = Image.new("RGBA", (square_size, square_size), (255, 255, 0, alpha))
        return ImageTk.PhotoImage(img)

    def create_transparent_red_square(self):
        """Створює зображення прозорого червоного квадрата."""
        square_size = self.sq_size
        alpha = 64  # Прозорість
        img = Image.new("RGBA", (square_size, square_size), (255, 0, 0, alpha))
        return ImageTk.PhotoImage(img)
