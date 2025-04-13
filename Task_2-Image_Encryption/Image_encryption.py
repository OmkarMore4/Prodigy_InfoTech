import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES  # type: ignore
import hashlib
import os
from PIL import Image, ImageTk  # type: ignore
import numpy as np  # type: ignore

# Padding for AES
def pad(data):
    return data + b"\0" * (16 - len(data) % 16)

# Generate AES key from password
def get_key(password):
    return hashlib.sha256(password.encode()).digest()[:16]

# Encrypt image
def encrypt_image(input_path, output_path, key):
    img = Image.open(input_path).convert("RGB")
    img_array = np.array(img)
    img_bytes = img_array.tobytes()

    # Padding to ensure length is multiple of 16
    pad_length = 16 - (len(img_bytes) % 16)
    padded_bytes = img_bytes + bytes([pad_length]) * pad_length  # PKCS7-like padding

    cipher = AES.new(get_key(key), AES.MODE_ECB)
    encrypted_bytes = cipher.encrypt(padded_bytes)

    encrypted_array = np.frombuffer(encrypted_bytes, dtype=np.uint8)
    
    # Ensure the encrypted data can be reshaped back
    try:
        encrypted_array = encrypted_array[: img_array.size].reshape(img_array.shape)
        encrypted_img = Image.fromarray(encrypted_array)
        encrypted_img.save(output_path)
        return output_path
    except ValueError:
        messagebox.showerror("Error", "Encryption failed due to incorrect reshaping.")
        return None

# Decrypt image
def decrypt_image(input_path, output_path, key):
    img = Image.open(input_path).convert("RGB")
    img_array = np.array(img)
    img_bytes = img_array.tobytes()

    cipher = AES.new(get_key(key), AES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(img_bytes).rstrip(b"\0")

    try:
        decrypted_array = np.frombuffer(decrypted_bytes, dtype=np.uint8).reshape(img_array.shape)
        decrypted_img = Image.fromarray(decrypted_array)
        decrypted_img.save(output_path)
        return output_path  # Return path of saved decrypted image
    except ValueError:
        messagebox.showerror("Error", "Decryption failed. Incorrect key?")
        return None

# GUI functions
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)
    show_image(file_path, img_label_original)

def process_image(action):
    file_path = entry_file.get()
    key = entry_key.get()

    if not file_path or not key:
        messagebox.showerror("Error", "Please select an image and enter a key!")
        return

    output_path = os.path.splitext(file_path)[0] + ("_encrypted.png" if action == "encrypt" else "_decrypted.png")

    try:
        if action == "encrypt":
            result_path = encrypt_image(file_path, output_path, key)
        else:
            result_path = decrypt_image(file_path, output_path, key)

        if result_path:
            show_result_window(result_path)  # Show new window with output image
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_image(image_path, label):
    img = Image.open(image_path).resize((250, 250))  # Resize for display
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

def show_result_window(output_path):
    result_window = tk.Toplevel(root)
    result_window.title("Result")

    tk.Label(result_window, text=f"Image saved at:\n{output_path}", wraplength=300).pack(pady=10)

    img = Image.open(output_path).resize((300, 300))
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(result_window, image=img)
    img_label.image = img
    img_label.pack(pady=10)

    # Buttons to go back or exit
    tk.Button(result_window, text="Go Back", command=result_window.destroy).pack(pady=5)
    tk.Button(result_window, text="Exit", command=root.quit).pack(pady=5)

# Main GUI window
root = tk.Tk()
root.title("Image Encryption & Decryption")

# Input Section
tk.Label(root, text="Select Image:").grid(row=0, column=0, padx=10, pady=10)
entry_file = tk.Entry(root, width=40)
entry_file.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Enter Key:").grid(row=1, column=0, padx=10, pady=10)
entry_key = tk.Entry(root, width=20, show="*")
entry_key.grid(row=1, column=1, padx=10, pady=10)

# Buttons for encryption and decryption
tk.Button(root, text="Encrypt", command=lambda: process_image("encrypt")).grid(row=2, column=0, padx=10, pady=20)
tk.Button(root, text="Decrypt", command=lambda: process_image("decrypt")).grid(row=2, column=1, padx=10, pady=20)

# Original Image Display
tk.Label(root, text="Original Image").grid(row=3, column=0, columnspan=3)
img_label_original = tk.Label(root)
img_label_original.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
