import os
import shutil

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "entry.png")
DESTINATION = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")


def main():
    os.makedirs(os.path.dirname(DESTINATION) or ".", exist_ok=True)
    with open(SOURCE, "rb") as src, open(DESTINATION, "wb") as dst:
        shutil.copyfileobj(src, dst)


if __name__ == "__main__":
    main()
