from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage
import cv2
import numpy as np
from PIL import Image, ImageTk
import websocket  # Changed from websockets to websocket
import json
import threading
import time

# WebSocket client for handling flag data
class FlagWebSocketClient:
    def __init__(self, url, on_flag_update=None):
        self.url = url
        self.on_flag_update = on_flag_update
        self.ws = None
        self.is_connected = False
        self.reconnect_interval = 3  # seconds
        self.thread = None
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_websocket, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()

    def _run_websocket(self):
        websocket.enableTrace(False)
        while self.running:
            try:
                self.ws = websocket.WebSocketApp(self.url,
                                               on_message=self._on_message,
                                               on_error=self._on_error,
                                               on_close=self._on_close,
                                               on_open=self._on_open)
                self.ws.run_forever()
                
                # If we get here, the connection was closed
                if self.running:
                    print(f"WebSocket disconnected, attempting to reconnect in {self.reconnect_interval} seconds...")
                    time.sleep(self.reconnect_interval)
            except Exception as e:
                print(f"WebSocket error: {e}")
                time.sleep(self.reconnect_interval)

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            if isinstance(data, dict) and self.on_flag_update:
                self.on_flag_update(data)
        except json.JSONDecodeError:
            print(f"Invalid JSON received: {message}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def _on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        self.is_connected = False
        print(f"WebSocket connection closed: {close_status_code} - {close_msg}")

    def _on_open(self, ws):
        self.is_connected = True
        print("WebSocket connection established")

        # Send initial connection message
        try:
            ws.send(json.dumps({"type": "subscribe", "channel": "flags"}))
        except Exception as e:
            print(f"Error sending initial message: {e}")


def relative_to_assets(path: str, assets_path: Path) -> Path:
    return assets_path / Path(path)


class ImageBlinker:
    def __init__(self, img_num, pos, canvas, window):
        self.img_num = img_num
        self.pos = pos
        self.canvas = canvas
        self.window = window
        self.img_ref = None
        self.img_id = None
        self.active = False
        self.after_id = None
        self.visible = True

    def create_image(self, img):
        self.img_ref = img
        self.img_id = self.canvas.create_image(*self.pos, image=img)

    def toggle(self, active):
        if self.active == active:
            return

        self.active = active

        if not active:
            if self.after_id:
                self.window.after_cancel(self.after_id)
                self.after_id = None
            self.canvas.itemconfig(self.img_id, state='normal')
            self.visible = True
            return

        def blink():
            if not self.active:
                return

            if self.visible:
                self.canvas.itemconfig(self.img_id, state='hidden')
                self.visible = False
            else:
                self.canvas.itemconfig(self.img_id, state='normal')
                self.visible = True

            self.after_id = self.window.after(800, blink)

        blink()


def open_system_page():
    # Close the main window
    window.destroy()

    # Create the system window
    system_window = Tk()
    system_window.geometry("1255x836")
    system_window.configure(bg="#FFFFFF")
    system_window.resizable(False, False)

    # System page canvas
    system_canvas = Canvas(
        system_window,
        bg="#FFFFFF",
        height=836,
        width=1255,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    system_canvas.place(x=0, y=0)

    # System page assets path
    system_assets_path = Path("SYStemPage/build/assets/frame0")

    # Load and place all system page images
    images = []

    # Variables for image 28-29 toggle
    image_28_ref = None
    image_29_ref = None
    image_28_id = None
    image_29_id = None

    # Create blinkers for images 8-13, 15-17
    blinker_positions = {
        8: (88.0, 419.0),
        9: (90.0, 509.0),
        10: (88.0, 604.0),
        11: (90.0, 326.0),
        12: (90.0, 234.0),
        13: (90.0, 142.0),
        15: (278.0, 765.0),
        16: (409.0, 765.0),
        17: (539.0, 765.0)
    }

    blinkers = {}
    for img_num, pos in blinker_positions.items():
        blinkers[img_num] = ImageBlinker(img_num, pos, system_canvas, system_window)
    # Video capture objects and references
    video_captures = {
        3: None,
        4: None,
        5: None,
        6: None
    }
    video_labels = {}
    video_imagetk_refs = {}  # To keep references to PhotoImage objects

    def toggle_28_29(show_29):
        """Toggle between image_28 and image_29"""
        if show_29:
            system_canvas.itemconfig(image_28_id, state='hidden')
            system_canvas.itemconfig(image_29_id, state='normal')
        else:
            system_canvas.itemconfig(image_29_id, state='hidden')
            system_canvas.itemconfig(image_28_id, state='normal')

    # Add this class definition near the top with other class definitions

    # Image pair variables and toggle functions
    class ImagePair:
        def __init__(self, img1_num, img2_num, pos):
            self.img1_ref = None
            self.img2_ref = None
            self.img1_id = None
            self.img2_id = None
            self.img1_num = img1_num
            self.img2_num = img2_num
            self.pos = pos
            self.after_id = None
            self.active = False

        def create_images(self, img1, img2):
            self.img1_ref = img1
            self.img2_ref = img2
            self.img1_id = system_canvas.create_image(*self.pos, image=img1)
            self.img2_id = system_canvas.create_image(*self.pos, image=img2)
            system_canvas.itemconfig(self.img2_id, state='hidden')

        def toggle(self, active):
            if self.active == active:
                return

            self.active = active

            if not active:
                if self.after_id:
                    system_window.after_cancel(self.after_id)
                    self.after_id = None
                system_canvas.itemconfig(self.img2_id, state='hidden')
                system_canvas.itemconfig(self.img1_id, state='normal')
                return

            def cycle():
                if not self.active:
                    return

                if system_canvas.itemcget(self.img1_id, 'state') == 'normal':
                    system_canvas.itemconfig(self.img1_id, state='hidden')
                    system_canvas.lift(self.img2_id)
                    system_canvas.itemconfig(self.img2_id, state='normal')
                else:
                    system_canvas.itemconfig(self.img2_id, state='hidden')
                    system_canvas.lift(self.img1_id)
                    system_canvas.itemconfig(self.img1_id, state='normal')

                self.after_id = system_window.after(1000, cycle)

            cycle()

    # Create image pairs
    pair20_21 = ImagePair(20, 21, (1202.0, 161.0))
    pair22_23 = ImagePair(22, 23, (1200.0, 427.0))
    pair24_25 = ImagePair(24, 25, (1202.0, 265.0))
    pair26_27 = ImagePair(26, 27, (1202.0, 351.0))

    all_pairs = [pair20_21, pair22_23, pair24_25, pair26_27]

    def update_video_feed(img_num, pos):
        if img_num not in video_captures or video_captures[img_num] is None:
            return

        ret, frame = video_captures[img_num].read()
        if ret:
            # Resize frame to match expected dimensions
            if img_num in [3, 4 ,5,6]:  # Larger video feeds
                frame = cv2.resize(frame, (426, 240))
            else:  # Smaller video feeds
                frame = cv2.resize(frame, (400, 225))

            # Convert color from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            # Store reference to prevent garbage collection
            video_imagetk_refs[img_num] = imgtk

            # Update the label
            if img_num in video_labels:
                system_canvas.itemconfig(video_labels[img_num], image=imgtk)

            # Schedule the next update
            system_window.after(30, lambda: update_video_feed(img_num, pos))
        else:
            # If video ends, restart it
            video_captures[img_num].set(cv2.CAP_PROP_POS_FRAMES, 0)
            system_window.after(30, lambda: update_video_feed(img_num, pos))

    for i in range(1, 30):
        try:
            # Skip video images (they'll be handled separately)
            if i in [3, 4, 5, 6]:
                # Initialize video capture for these images
                if i == 3:
                    video_path = "Driver Monitoring-Carla.mp4"  # Replace with actual path
                    pos = (399.0, 198.0)
                elif i == 4:
                    video_path = "CARLA camera-TEST1.mp4"  # Replace with actual path
                    pos = (904.0, 198.0)
                elif i == 5:
                    video_path = "Voice-Activated Controls-TEST1.mp4"  # Replace with actual path
                    pos = (399.0, 551.0)
                elif i == 6:
                    video_path = "FrontCameraTest-1.mp4"  # Replace with actual path
                    pos = (904.0, 555.0)

                # Create video capture with higher buffer size
                video_captures[i] = cv2.VideoCapture(video_path)
                video_captures[i].set(cv2.CAP_PROP_BUFFERSIZE, 2)  # Smaller buffer for less lag
                video_captures[i].set(cv2.CAP_PROP_FPS, 30)  # Set expected FPS

                # Create placeholder image
                img = PhotoImage(file=relative_to_assets(f"image_{i}.png", system_assets_path))
                images.append(img)
                video_labels[i] = system_canvas.create_image(*pos, image=img)

                # Start video update
                system_window.after(100, lambda i=i, pos=pos: update_video_feed(i, pos))
                continue

            img = PhotoImage(file=relative_to_assets(f"image_{i}.png", system_assets_path))
            images.append(img)

            # Handle image 28 and 29 specially
            if i == 28:
                image_28_ref = img
                image_28_id = system_canvas.create_image(1200.0, 503.0, image=img)
            elif i == 29:
                image_29_ref = img
                image_29_id = system_canvas.create_image(1200.0, 503.0, image=img)
                system_canvas.itemconfig(image_29_id, state='hidden')  # Hide initially

            # Check if image belongs to any pair
            placed = False
            for pair in all_pairs:
                if i == pair.img1_num:
                    pair.img1_ref = img
                    if pair.img2_ref:  # If both images are loaded
                        pair.create_images(img, pair.img2_ref)
                    placed = True
                elif i == pair.img2_num:
                    pair.img2_ref = img
                    if pair.img1_ref:  # If both images are loaded
                        pair.create_images(pair.img1_ref, img)
                    placed = True

            if not placed and i not in [28, 29, 3, 4, 5, 6]:  # Skip video images
                # Place non-paired images
                if i == 1:
                    system_canvas.create_image(627.0, 418.0, image=img)
                elif i == 2:
                    system_canvas.create_image(627.0, 419.0, image=img)
                elif i == 7:
                    system_canvas.create_image(87.0, 383.0, image=img)
                elif i in blinkers:
                    blinkers[i].create_image(img)
                elif i == 14:
                    system_canvas.create_image(415.0, 765.0, image=img)
                elif i == 18:
                    system_canvas.create_image(1049.0, 763.0, image=img)
                elif i == 19:
                    system_canvas.create_image(1202.0, 385.0, image=img)
        except:
            break

    # Add system page text elements
    system_canvas.create_text(
        278.0, 16.0,
        anchor="nw",
        text="Driver Monitoring",
        fill="#FFFFFF",
        font=("Instrument Sans Bold", 30 * -1)
    )

    system_canvas.create_text(
        784.0, 16.0,
        anchor="nw",
        text="CARLA CAMERA",
        fill="#FFFFFF",
        font=("Instrument Sans Bold", 30 * -1)
    )

    system_canvas.create_text(
        231.0, 363.0,
        anchor="nw",
        text="Voice-Activated Controls",
        fill="#FFFFFF",
        font=("Instrument Sans Bold", 30 * -1)
    )

    system_canvas.create_text(
        747.0, 363.0,
        anchor="nw",
        text="Front-Facing Camera",
        fill="#FFFFFF",
        font=("Instrument Sans Bold", 30 * -1)
    )

    # HOME text - make it clickable to return to main page
    home_text = system_canvas.create_text(
        982.0, 736.0,
        anchor="nw",
        text="HOME",
        fill="#FFFFFF",
        font=("Instrument Sans Bold", 45 * -1),
        tags="home_text"
    )
    system_canvas.tag_bind("home_text", "<Button-1>", lambda e: return_to_main(system_window))

    # Make image_18 (HOME button) clickable
    img_18_bbox = (1049 - 200, 763 - 50, 1049 + 200, 763 + 50)
    home_clickable = system_canvas.create_rectangle(
        img_18_bbox,
        outline="",
        fill="",
        tags="home_clickable"
    )
    system_canvas.tag_bind("home_clickable", "<Button-1>", lambda e: return_to_main(system_window))

    # Store references to prevent garbage collection
    system_window.images = images
    system_window.image_28_ref = image_28_ref
    system_window.image_29_ref = image_29_ref
    system_window.video_imagetk_refs = video_imagetk_refs  # Store video image references

    for pair in all_pairs:
        system_window.__setattr__(f"image_{pair.img1_num}_ref", pair.img1_ref)
        system_window.__setattr__(f"image_{pair.img2_num}_ref", pair.img2_ref)
    # Store blinker references
    system_window.blinkers = blinkers

#####################################ControlPanel#####################################
    # Initialize with default values
    blinkers[8].toggle(False)  # Image 8 (Violence)
    blinkers[9].toggle(False)  # Image 9 (Air Safety Warning)
    blinkers[10].toggle(False)  # Image 10 (Health Warning)
    blinkers[11].toggle(False)  # Image 11 (Driver Distraction Warning)
    blinkers[12].toggle(False)  # Image 12 (Driver Drowsiness Warning)
    blinkers[13].toggle(False)  # Image 13 (Lane Departure Warning)
    blinkers[15].toggle(False)  # Image 15 (Emotion Recognition)
    blinkers[16].toggle(False)  # Image 16 (blind spot detection mirrors -Left)
    blinkers[17].toggle(False)  # Image 17 (blind spot detection mirrors -Right)
    
    pair20_21.toggle(False)  # Start 20-21 toggle (UP arrow)
    pair22_23.toggle(False)  # Start 22-23 toggle (Left arrow)
    pair24_25.toggle(False)  # Stop 24-25 toggle (Down arrow)
    pair26_27.toggle(False)  # Start 26-27 toggle (Right arrow)
    toggle_28_29(False)  # Brakes
    
    # Flag-to-element mapping
    flag_mapping = {
        'violence': 8,
        'air_safety': 9,
        'health': 10,
        'distraction': 11,
        'drowsiness': 12,
        'lane_departure': 13,
        'emotion': 15,
        'blind_spot_left': 16,
        'blind_spot_right': 17,
        'up_arrow': (pair20_21, True),
        'left_arrow': (pair22_23, True),
        'down_arrow': (pair24_25, True),
        'right_arrow': (pair26_27, True),
        'brakes': True  # For toggle_28_29 function
    }
    
    # WebSocket flag handling function
    def handle_flags(flag_data):
        print(f"Received flags: {flag_data}")
        
        # Process each flag in the data
        for flag_name, flag_value in flag_data.items():
            if flag_name in flag_mapping:
                element = flag_mapping[flag_name]
                
                # Handle different types of UI elements
                if isinstance(element, int):
                    # This is a blinker image
                    blinkers[element].toggle(flag_value)
                elif isinstance(element, tuple) and isinstance(element[0], ImagePair):
                    # This is an image pair
                    pair, _ = element
                    pair.toggle(flag_value)
                elif flag_name == 'brakes':
                    # Special case for brake toggle
                    toggle_28_29(flag_value)
                    
        # Update UI immediately
        system_window.update()
    
    # Initialize WebSocket client
    ws_client = FlagWebSocketClient("ws://localhost:8765", handle_flags)
    ws_client.start()
    
    # Store WebSocket client reference to prevent garbage collection and allow cleanup
    system_window.ws_client = ws_client
###########################################################################################
    # Clean up WebSocket client when window is closed
    def on_window_close():
        if hasattr(system_window, 'ws_client'):
            system_window.ws_client.stop()
        system_window.destroy()
    
    system_window.protocol("WM_DELETE_WINDOW", on_window_close)
    
    system_window.mainloop()


def return_to_main(current_window):
    # Release all video captures before destroying window
    for cap in [3, 4, 5, 6]:
        if hasattr(current_window, 'video_captures') and current_window.video_captures.get(cap):
            current_window.video_captures[cap].release()
    current_window.destroy()
    show_main_page()


def open_map_page():
    # Close the main window
    window.destroy()

    # Create the map window
    map_window = Tk()
    map_window.geometry("1255x836")
    map_window.configure(bg="#FFFFFF")
    map_window.resizable(False, False)

    canvas = Canvas(
        map_window,
        bg="#FFFFFF",
        height=836,
        width=1255,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=-1)

    # Load map page assets
    assets_path = Path(r"Mappage_TEST/build/assets/frame0")

    # Load and place map page images
    image_image_1 = PhotoImage(file=assets_path / "image_1.png")
    image_1 = canvas.create_image(627.0, 419.0, image=image_image_1)

    image_image_2 = PhotoImage(file=assets_path / "image_2.png")
    image_2 = canvas.create_image(627.0, 420.0, image=image_image_2)

    image_image_3 = PhotoImage(file=assets_path / "image_3.png")
    image_3 = canvas.create_image(122.0, 441.0, image=image_image_3)

    image_image_4 = PhotoImage(file=assets_path / "image_4.png")
    image_4 = canvas.create_image(122.0, 484.0, image=image_image_4)

    image_image_5 = PhotoImage(file=assets_path / "image_5.png")
    image_5 = canvas.create_image(123.0, 382.0, image=image_image_5)

    image_image_6 = PhotoImage(file=assets_path / "image_6.png")
    image_6 = canvas.create_image(313.0, 763.0, image=image_image_6)

    image_image_7 = PhotoImage(file=assets_path / "image_7.png")
    image_7 = canvas.create_image(672.0, 763.0, image=image_image_7)

    image_image_8 = PhotoImage(file=assets_path / "image_8.png")
    image_8 = canvas.create_image(961.0, 776.0, image=image_image_8)

    # Add HOME text
    home_text = canvas.create_text(
        246.0, 736.0,
        anchor="nw",
        text="HOME",
        fill="#FFFFFF",
        font=("Instrument Sans Bold", 45 * -1),
        tags="home_text"
    )

    # Store references to prevent garbage collection
    map_window.images = [
        image_image_1, image_image_2, image_image_3,
        image_image_4, image_image_5, image_image_6,
        image_image_7, image_image_8
    ]

    # Add HOME button functionality
    def return_to_main():
        map_window.destroy()
        show_main_page()

    # Make HOME text and image clickable
    canvas.tag_bind("home_text", "<Button-1>", lambda e: return_to_main())
    canvas.tag_bind(image_6, "<Button-1>", lambda e: return_to_main())

    map_window.mainloop()

def show_main_page():
    global window
    window = Tk()
    window.geometry("1255x836")
    window.configure(bg="#FFFFFF")

    # Main assets path
    main_assets_path = Path(r"Mainpage-TEST/build/assets/frame0")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=836,
        width=1255,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Load and place main window images
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png", main_assets_path))
    image_1 = canvas.create_image(627.0, 418.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png", main_assets_path))
    image_2 = canvas.create_image(348.0, 675.0, image=image_image_2)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png", main_assets_path))
    image_3 = canvas.create_image(436.0, 417.0, image=image_image_3)

    image_image_4 = PhotoImage(file=relative_to_assets("image_4.png", main_assets_path))
    image_4 = canvas.create_image(857.0, 417.0, image=image_image_4)

    image_image_5 = PhotoImage(file=relative_to_assets("image_5.png", main_assets_path))
    image_5 = canvas.create_image(733.0, 692.0, image=image_image_5)

    # Add text elements
    map_text = canvas.create_text(
        385.0, 391.0,
        anchor="nw",
        text="MAP",
        fill="#FFFBFB",
        font=("Instrument Sans Bold", 45 * -1),
        tags="map_text"
    )

    system_text = canvas.create_text(
        758.0, 391.0,
        anchor="nw",
        text="SYSTEM",
        fill="#FFFBFB",
        font=("Instrument Sans Bold", 45 * -1),
        tags="system_text"
    )

    # Make MAP text and image clickable
    canvas.tag_bind("map_text", "<Button-1>", lambda e: open_map_page())
    canvas.tag_bind(image_3, "<Button-1>", lambda e: open_map_page())

    # Make SYSTEM text clickable
    canvas.tag_bind("system_text", "<Button-1>", lambda e: open_system_page())

    # Make image_4 (SYSTEM background) clickable
    img_4_bbox = (857 - 192, 417 - 55, 857 + 192, 417 + 55)
    clickable_area = canvas.create_rectangle(
        img_4_bbox,
        outline="",
        fill="",
        tags="clickable_area"
    )
    canvas.tag_bind("clickable_area", "<Button-1>", lambda e: open_system_page())

    # Store references to prevent garbage collection
    window.images = [image_image_1, image_image_2, image_image_3, image_image_4, image_image_5]

    window.resizable(False, False)
    window.mainloop()

# Start the application
show_main_page()