import os
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()
MAX_SIZE = 1024

class LocalImageStorage:
    def __init__(self, app):
        self.upload_dir = app.config['UPLOAD_FOLDER']

    def save(self, image_file, content_item_class, slug, image_uuid):
        with Image.open(image_file) as img:
        # convert to png
            img = img.convert('RGB')

            img.thumbnail((MAX_SIZE, MAX_SIZE)) # MAX_SIZE = 1024

            class_dir = os.path.join(self.upload_dir, content_item_class)
            content_item_dir = os.path.join(class_dir, slug)
            images_dir = os.path.join(content_item_dir, 'images')

            # Create uploads folder if it doesn't exist
            if not os.path.exists(class_dir):
                os.mkdir(class_dir)

            # Create content item fodler
            if not os.path.exists(content_item_dir):
                os.mkdir(content_item_dir)

            # create the images folder
            if not os.path.exists(images_dir):
                os.mkdir(images_dir)
                

            filename = os.path.join(images_dir, f'{image_uuid}.png')
            print(f'>>>> filename: {filename}')

            img.save(filename, format='PNG', optimize=True)

        return os.path.join('/uploads', f'{slug}.png')