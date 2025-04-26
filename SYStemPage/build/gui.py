
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"SYStemPage/build/assets/frame0")


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
    627.0,
    419.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    399.0,
    198.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    904.0,
    198.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    399.0,
    551.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    904.0,
    555.0,
    image=image_image_6
)

canvas.create_text(
    278.0,
    16.0,
    anchor="nw",
    text="Driver Monitoring",
    fill="#FFFFFF",
    font=("InstrumentSans Regular", 30 * -1)
)

canvas.create_text(
    784.0,
    16.0,
    anchor="nw",
    text="CARLA CAMERA",
    fill="#FFFFFF",
    font=("InstrumentSans Bold", 30 * -1)
)

canvas.create_text(
    231.0,
    363.0,
    anchor="nw",
    text="Voice-Activated Controls",
    fill="#FFFFFF",
    font=("InstrumentSans Bold", 30 * -1)
)

canvas.create_text(
    747.0,
    363.0,
    anchor="nw",
    text="Front-Facing Camera",
    fill="#FFFFFF",
    font=("InstrumentSans Bold", 30 * -1)
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    87.0,
    383.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    88.0,
    419.0,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    90.0,
    509.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    88.0,
    604.0,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    90.0,
    326.0,
    image=image_image_11
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    90.0,
    234.0,
    image=image_image_12
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    90.0,
    142.0,
    image=image_image_13
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    415.0,
    765.0,
    image=image_image_14
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    278.0,
    765.0,
    image=image_image_15
)

image_image_16 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(
    409.0,
    765.0,
    image=image_image_16
)

image_image_17 = PhotoImage(
    file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(
    539.0,
    765.0,
    image=image_image_17
)

image_image_18 = PhotoImage(
    file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(
    1049.0,
    763.0,
    image=image_image_18
)

canvas.create_text(
    982.0,
    736.0,
    anchor="nw",
    text="HOME",
    fill="#FFFFFF",
    font=("Instrument Sans Bold", 45 * -1)
)

image_image_19 = PhotoImage(
    file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(
    1202.0,
    385.0,
    image=image_image_19
)

image_image_20 = PhotoImage(
    file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(
    1202.0,
    161.0,
    image=image_image_20
)

image_image_21 = PhotoImage(
    file=relative_to_assets("image_21.png"))
image_21 = canvas.create_image(
    1202.0,
    161.0,
    image=image_image_21
)

image_image_22 = PhotoImage(
    file=relative_to_assets("image_22.png"))
image_22 = canvas.create_image(
    1200.0,
    427.0,
    image=image_image_22
)

image_image_23 = PhotoImage(
    file=relative_to_assets("image_23.png"))
image_23 = canvas.create_image(
    1200.0,
    427.0,
    image=image_image_23
)

image_image_24 = PhotoImage(
    file=relative_to_assets("image_24.png"))
image_24 = canvas.create_image(
    1202.0,
    265.0,
    image=image_image_24
)

image_image_25 = PhotoImage(
    file=relative_to_assets("image_25.png"))
image_25 = canvas.create_image(
    1202.0,
    265.0,
    image=image_image_25
)

image_image_26 = PhotoImage(
    file=relative_to_assets("image_26.png"))
image_26 = canvas.create_image(
    1202.0,
    351.0,
    image=image_image_26
)

image_image_27 = PhotoImage(
    file=relative_to_assets("image_27.png"))
image_27 = canvas.create_image(
    1202.0,
    351.0,
    image=image_image_27
)

image_image_28 = PhotoImage(
    file=relative_to_assets("image_28.png"))
image_28 = canvas.create_image(
    1200.0,
    503.0,
    image=image_image_28
)

image_image_29 = PhotoImage(
    file=relative_to_assets("image_29.png"))
image_29 = canvas.create_image(
    1200.0,
    503.0,
    image=image_image_29
)
window.resizable(False, False)
window.mainloop()
