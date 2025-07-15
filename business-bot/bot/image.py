import random
import os

def get_random_image_from_folder(folder_path):
    allowed_extensions = (".jpg", ".jpeg", ".png")
    images = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
              if f.lower().endswith(allowed_extensions)]

    if not images:
        raise Exception("No images found in folder.")

    return random.choice(images)