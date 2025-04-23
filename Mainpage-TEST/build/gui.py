from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\PycharmProjects\INNOVADRIVEfinal\Mainpage-TEST\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1255x836")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 836,
    width = 1255,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    627.0,
    418.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    348.0,
    675.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    436.0,
    417.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    857.0,
    417.0,
    image=image_image_4
)

canvas.create_text(
    385.0,
    391.0,
    anchor="nw",
    text="MAP",
    fill="#FFFBFB",
    font=("Instrument Sans Bold", 45 * -1)
)

canvas.create_text(
    758.0,
    391.0,
    anchor="nw",
    text="SYSTEM",
    fill="#FFFBFB",
    font=("Instrument Sans Bold", 45 * -1)
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    733.0,
    692.0,
    image=image_image_5
)
window.resizable(False, False)
window.mainloop()
