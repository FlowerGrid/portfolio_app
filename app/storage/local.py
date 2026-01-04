import os
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()
MAX_SIZE = 1024

class LocalImageStorage:
    def __init__(self, app):
        self.upload_dir = app.config['UPLOAD_FOLDER']

    def save(self, image_file, slug):
        with Image.open(image_file) as img:
        # convert to png
            img = img.convert('RGB')

            img.thumbnail((MAX_SIZE, MAX_SIZE)) # MAX_SIZE = 1024

            filename = os.path.join(self.upload_dir, f'{slug}.png')

            img.save(filename, format='PNG', optimize=True)

        return os.path.join('uploads', filename)