import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image
import stepic
import os  # We'll use this to get the filename for saving


# --- 1. Core Functions (The "Backend") ---

def embed_message():
    """
    Hides a text message inside an image and saves it as a new PNG file.
    """
    # Get the image path from the GUI
    image_path = image_path_entry.get()

    # Get the text message from the GUI
    # "1.0" means "line 1, character 0" (the beginning)
    # "end-1c" means "the end, minus 1 character" (to remove the extra newline)
    message = text_entry.get("1.0", "end-1c")

    # --- Validation ---
    if not image_path:
        messagebox.showerror("Error", "Please select an image first.")
        return

    if not message:
        messagebox.showerror("Error", "Please enter a message to hide.")
        return

    try:
        # Open the original image using Pillow
        original_image = Image.open(image_path)

        # Convert message to bytes (stepic requires bytes)
        message_bytes = message.encode('utf-8')

        # Use stepic to embed the bytes into the image
        # 'copy()' ensures the original image is not changed
        stego_image = stepic.encode(original_image.copy(), message_bytes)

        # --- Ask user where to save the new file ---

        # Get the directory and name of the original file
        original_dir = os.path.dirname(image_path)
        original_name = os.path.basename(image_path)

        # Suggest a new name, e.g., "my_image.png" -> "my_image_hidden.png"
        new_name = f"{os.path.splitext(original_name)[0]}_hidden.png"

        save_path = filedialog.asksaveasfilename(
            initialdir=original_dir,
            initialfile=new_name,
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )

        if not save_path:
            # User cancelled the save dialog
            return

        # Save the new image with the hidden data
        # We MUST save as a lossless format like PNG. JPEG will not work.
        stego_image.save(save_path, 'PNG')

        messagebox.showinfo("Success", f"Message hidden successfully!\nSaved as: {save_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def extract_message():
    """
    Extracts a hidden message from a steganographic image.
    """
    # Get the image path from the GUI
    image_path = image_path_entry.get()

    if not image_path:
        messagebox.showerror("Error", "Please select an image first.")
        return

    try:
        # Open the image
        stego_image = Image.open(image_path)

        # Use stepic to decode the data
        decoded_data = stepic.decode(stego_image)

        # The decoded data is already a string, so we just assign it
        hidden_message = decoded_data

        # Clear the text box and insert the new message
        text_entry.delete("1.0", "end")

        # Insert the message at "line 1, character 0"
        text_entry.insert("1.0", hidden_message)

        messagebox.showinfo("Success", "Message extracted and displayed in the text box.")

    except Exception as e:
        # This error often means no hidden message was found
        messagebox.showerror("Error", f"Could not extract message. Is this the right image?\n\nDetails: {e}")

    except Exception as e:
        # This error often means no hidden message was found
        messagebox.showerror("Error", f"Could not extract message. Is this the right image?\n\nDetails: {e}")


def select_image():
    """
    Opens a file dialog for the user to select an image.
    """
    # Ask the user to select a file
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.png *.bmp"),
            ("All files", "*.*")
        ]
    )

    if file_path:
        # Clear the old path and insert the new one
        image_path_entry.delete(0, "end")
        image_path_entry.insert(0, file_path)


# --- 2. GUI Setup (The "Frontend") ---

# Create the main window
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("500x400")  # Set a window size

# Create a main frame to hold all widgets
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill="both", expand=True)

# --- Image Selection Widgets ---
image_frame = tk.Frame(main_frame)
image_frame.pack(fill="x", pady=5)

image_label = tk.Label(image_frame, text="Image File:")
image_label.pack(side="left", padx=5)

image_path_entry = tk.Entry(image_frame, width=40)
image_path_entry.pack(side="left", fill="x", expand=True)

image_button = tk.Button(image_frame, text="Select...", command=select_image)
image_button.pack(side="left", padx=5)

# --- Text Entry Widget ---
text_label = tk.Label(main_frame, text="Enter Secret Message (to hide) or See Extracted Message (below):")
text_label.pack(anchor="w", pady=(10, 0))

# Use ScrolledText for a text box with a scrollbar
text_entry = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=10, width=50)
text_entry.pack(fill="both", expand=True, pady=5)

# --- Button Widgets ---
button_frame = tk.Frame(main_frame)
button_frame.pack(fill="x", pady=10)

embed_button = tk.Button(button_frame, text="Embed Message", command=embed_message, bg="#4CAF50", fg="white")
embed_button.pack(side="left", fill="x", expand=True, padx=5, pady=5)

extract_button = tk.Button(button_frame, text="Extract Message", command=extract_message, bg="#2196F3", fg="white")
extract_button.pack(side="left", fill="x", expand=True, padx=5, pady=5)

# Start the GUI event loop
root.mainloop()