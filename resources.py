import tkinter as tk


class Resources:
    def __init__(self, sq_size):
        self.sq_size = sq_size
        self.piece_images = {}

    def load_piece_images(self):
        """Loads chess piece images and resizes them."""
        piece_types = ['r', 'n', 'b', 'q', 'k', 'p']  #Types of pieces
        colors = ['w', 'b']  # Colors of pieces
        for color in colors:
            for piece in piece_types:
                file_name = f"images/{color}{piece.upper()}.png"
                image = tk.PhotoImage(file=file_name)

                # Scale the image according to the new cell size
                scale_factor = int(self.sq_size * 0.07)  # Scaling figures to 7% of the cell size
                image = image.zoom(scale_factor, scale_factor)  # Enlarging the figure image

                self.piece_images[f"{color}{piece}"] = image

        print(self.piece_images)

    def get_piece_images(self):
        """Returns a dictionary of figure images."""
        print(self.piece_images)
        return self.piece_images
