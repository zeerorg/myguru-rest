import os


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    media_dir = os.path.join(base_dir, "media")

    for x in os.listdir(media_dir):
        if x == "yo.jpg" or x.startswith("yo_"):
            os.remove(os.path.join(media_dir, x))

if __name__ == "__main__":
    main()