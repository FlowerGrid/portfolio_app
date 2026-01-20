import os
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()
MAX_SIZE = 1024

class LocalImageStorage:
    def __init__(self, app):
        self.upload_dir = app.config['UPLOAD_FOLDER']

    def save(self, image_file, content_item_class, slug, image_name):
        with Image.open(image_file) as img:
        # convert to png
            img = img.convert('RGB')

            img.thumbnail((MAX_SIZE, MAX_SIZE)) # MAX_SIZE = 1024

            class_dir = os.path.join(self.upload_dir, content_item_class)
            content_item_dir = os.path.join(class_dir, slug)

            # Create uploads folder if it doesn't exist
            if not os.path.exists(class_dir):
                os.mkdir(class_dir)

            # Create post fodler
            if not os.path.exists(content_item_dir):
                os.mkdir(content_item_dir)
                

            filename = os.path.join(content_item_dir, f'{image_name}.png')

            img.save(filename, format='PNG', optimize=True)

        return os.path.join('/uploads', f'{slug}.png')