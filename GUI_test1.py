import tkinter as tk

# 1. Setup the main application window
root = tk.Tk()
root.title("My Digital Window")
root.geometry("400x300")

# 2. Define a function for the button to call
def on_button_click():
    label.config(text="You clicked the button!", fg="blue")
    print("Button was pressed!")

# 3. Create a Label (text)
label = tk.Label(root, text="Hello! I am a single-threaded window.", font=("Arial", 12))
label.pack(pady=20) # 'pack' adds it to the window with some padding

# 4. Create a Button
button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=10)

# 5. Start the Event Loop
# This is the line that keeps the window open and responsive.
root.mainloop()