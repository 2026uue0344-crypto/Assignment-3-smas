import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import numpy as np


def show_image():
    if image is None:
        return

    pic = image.copy()
    pic.thumbnail((850, 500))

    photo = ImageTk.PhotoImage(pic)
    image_box.config(image=photo, text="")
    image_box.image = photo


def open_image():
    global image, original

    file = filedialog.askopenfilename(
        title="Choose Image",
        filetypes=[("Images", "*.jpg *.jpeg *.png")]
    )

    if not file:
        return

    image = Image.open(file).convert("RGB")
    original = image.copy()
    show_image()


def rotate():
    global image
    if not check_image():
        return

    angle = simpledialog.askfloat("Rotate", "Enter angle in degrees:")
    if angle is None:
        return

    image = image.rotate(angle, expand=True)
    show_image()


def resize():
    global image
    if not check_image():
        return

    factor = simpledialog.askfloat(
        "Resize",
        "Enter resize factor:\n2 = double, 0.5 = half"
    )

    if factor is None:
        return

    if factor <= 0:
        messagebox.showerror("Error", "Factor must be greater than 0")
        return

    w, h = image.size
    image = image.resize(
        (int(w * factor), int(h * factor)),
        Image.Resampling.LANCZOS
    )
    show_image()


def flip():
    global image
    if not check_image():
        return

    choice = messagebox.askyesno(
        "Flip",
        "YES = Horizontal\nNO = Vertical"
    )

    if choice:
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    else:
        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    show_image()


def shear():
    global image
    if not check_image():
        return

    k = simpledialog.askfloat("Shear", "Enter horizontal shear value:")
    if k is None:
        return

    w, h = image.size
    shift = max(0, -k * h)
    new_w = int(w + abs(k) * h) + 1

    image = image.transform(
        (new_w, h),
        Image.Transform.AFFINE,
        (1, -k, shift, 0, 1, 0),
        resample=Image.Resampling.BICUBIC,
        fillcolor="white"
    )
    show_image()


def custom_matrix():
    global image
    if not check_image():
        return

    print_matrix = "Enter the 2 x 2 matrix"

    a = simpledialog.askfloat("Custom Matrix", print_matrix + "\na11 =")
    if a is None:
        return
    b = simpledialog.askfloat("Custom Matrix", print_matrix + "\na12 =")
    if b is None:
        return
    c = simpledialog.askfloat("Custom Matrix", print_matrix + "\na21 =")
    if c is None:
        return
    d = simpledialog.askfloat("Custom Matrix", print_matrix + "\na22 =")
    if d is None:
        return

    A = np.array([[a, b], [c, d]], dtype=float)

    if abs(np.linalg.det(A)) < 1e-10:
        messagebox.showerror(
            "Error",
            "Determinant is 0. Please enter a non-singular matrix."
        )
        return

    # Apply matrix about the image centre.
    inv = np.linalg.inv(A)
    w, h = image.size
    cx = (w - 1) / 2
    cy = (h - 1) / 2

    r11, r12 = inv[0]
    r21, r22 = inv[1]

    image = image.transform(
        (w, h),
        Image.Transform.AFFINE,
        (
            r11,
            -r12,
            cx - r11 * cx + r12 * cy,
            -r21,
            r22,
            cy + r21 * cx - r22 * cy
        ),
        resample=Image.Resampling.BICUBIC,
        fillcolor="white"
    )
    show_image()


def reset():
    global image
    if original is None:
        messagebox.showwarning("No Image", "Open an image first")
        return

    image = original.copy()
    show_image()


def save_image():
    if not check_image():
        return

    file = filedialog.asksaveasfilename(
        title="Save Image",
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")]
    )

    if file:
        image.save(file)
        messagebox.showinfo("Saved", "Image saved successfully")


def check_image():
    if image is None:
        messagebox.showwarning("No Image", "Click Open Image first")
        return False
    return True


# Main window
root = tk.Tk()
root.title("Image Transformation Toolbox")
root.geometry("1000x700")

image = None
original = None

# Title
tk.Label(
    root,
    text="IMAGE TRANSFORMATION TOOLBOX",
    font=("Arial", 20, "bold")
).pack(pady=10)

# Buttons
buttons = tk.Frame(root)
buttons.pack(pady=5)

names = [
    ("Open Image", open_image),
    ("Rotate", rotate),
    ("Resize", resize),
    ("Flip", flip),
    ("Shear", shear),
    ("Custom Matrix", custom_matrix),
    ("Reset", reset),
    ("Save", save_image)
]

for i, (name, command) in enumerate(names):
    tk.Button(
        buttons,
        text=name,
        width=13,
        height=2,
        command=command
    ).grid(row=0, column=i, padx=3)

# Image display
image_box = tk.Label(
    root,
    text="Click 'Open Image' to choose a JPG or PNG",
    bg="lightgray"
)
image_box.pack(fill="both", expand=True, padx=20, pady=20)

tk.Label(
    root,
    text="SMAS-1 Assignment 3 | IIT Jammu",
    font=("Arial", 10)
).pack(pady=5)

root.mainloop()
