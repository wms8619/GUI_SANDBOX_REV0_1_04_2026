import tkinter as tk
from PIL import Image, ImageTk  # This handles the images

def submit_name():
    # This function gets the text from the input field
    user_name = name_entry.get()
    result_label.config(text=f"Hello, {user_name}!", fg="green")

# 1. Create the main window
root = tk.Tk()
root.title("Advanced Digital Window")
root.geometry("500x500")

# 2. Add an Image
# Note: Replace 'your_image.png' with a real file path on your computer
try:
    original_img = Image.open("your_image.png") 
    resized_img = original_img.resize((150, 150)) # Resize for the window
    img = ImageTk.PhotoImage(resized_img)
    
    image_label = tk.Label(root, image=img)
    image_label.pack(pady=10)
except:
    # If the image file isn't found, we show this text instead
    tk.Label(root, text="(Image not found)", fg="gray").pack()

# 3. Add a Text Input (Entry)
tk.Label(root, text="Enter your name below:", font=("Arial", 10)).pack(pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

# 4. Add a Button to process the input
submit_btn = tk.Button(root, text="Submit Name", command=submit_name)
submit_btn.pack(pady=10)

# 5. Label to show the output
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack(pady=20)

# Start the application
root.mainloop()