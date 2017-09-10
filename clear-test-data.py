import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
media_dir = os.path.join(BASE_DIR, "media")

for x in os.listdir(media_dir):
    if x == "yo.jpg" or x.startswith("yo_"):
        os.remove(os.path.join(media_dir, x))