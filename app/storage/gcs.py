from flask import current_app
from google.cloud import storage
import io
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()
MAX_SIZE = 1024


class GCSImageStorage:
    def __init__(self, app):
        self.bucket_name = app.config['IMAGE_STORAGE_CONTAINER']

    def save(self, image_file, content_item_class, content_item_id, image_uuid):
        # Process image with PIL
        with Image.open(image_file) as img:
            img = img.convert("RGB")
            img.thumbnail((MAX_SIZE, MAX_SIZE))
            buffer = io.BytesIO()
            img.save(buffer, format="PNG", optimize=True)
            buffer.seek(0)

        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(self.bucket_name)
        organized_slug = f'uploads/{content_item_class}/{content_item_id}/images/{image_uuid}'
        blob = bucket.blob(f"{organized_slug}.png")
        blob.upload_from_file(buffer, content_type="image/png")
        blob.make_public()
        
        # Return the public URL or path
        return blob.public_url  # or blob.name if you want relative path