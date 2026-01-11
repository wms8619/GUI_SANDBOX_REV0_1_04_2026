import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import logging

# Setup logging for validation audits
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestbedHAL:
    """Hardware Abstraction Layer to simulate co-design streamline."""
    def __init__(self, morphology_name):
        self.morphology_name = morphology_name
        
    def run_validation_test(self, component_id, callback):
        """Simulates a hardware validation task in a separate thread."""
        logging.info(f"Starting validation on {self.morphology_name}: {component_id}")
        # Simulate hardware latency
        time.sleep(2) 
        result = f"Component {component_id} PASSED"
        logging.info(result)
        callback(result)

class ReconfigurableApp:
    def __init__(self, root, config):
        self.root = root
        self.root.title("Co-Design Testbed Controller")
        self.root.geometry("500x400")
        
        # 1. Load Morphology Configuration
        self.config = config
        self.hal = TestbedHAL(config['name'])
        
        self.setup_ui()

    def setup_ui(self):
        """Builds the UI dynamically based on the morphology config."""
        # Header
        header = tk.Label(self.root, text=f"Active Morphology: {self.config['name']}", 
                         font=("Arial", 14, "bold"))
        header.pack(pady=10)

        # Dynamic Component Frame
        self.status_label = tk.Label(self.root, text="System Ready", fg="green")
        self.status_label.pack(pady=5)

        container = tk.LabelFrame(self.root, text="Hardware Components", padding=10)
        container.pack(padx=20, pady=10, fill="both", expand=True)

        # Generate buttons based on configuration
        for component in self.config['components']:
            btn = ttk.Button(
                container, 
                text=f"Test {component}", 
                command=lambda c=component: self.start_test_thread(c)
            )
            btn.pack(fill="x", pady=2)

    def update_ui_result(self, message):
        """Updates the label safely from the main thread."""
        self.status_label.config(text=message, fg="blue")
        messagebox.showinfo("Test Complete", message)

    def start_test_thread(self, component_id):
        """Due Diligence: Run hardware tasks in background to prevent GUI hang."""
        self.status_label.config(text=f"Testing {component_id}...", fg="orange")
        
        # Dispatch task to background thread
        test_thread = threading.Thread(
            target=self.hal.run_validation_test, 
            args=(component_id, self.update_ui_result)
        )
        test_thread.start()

# --- Configuration Section ---
# In a real system, this would be loaded from a YAML or JSON file.
CURRENT_MORPHOLOGY = {
    "name": "Quadruped_v2_Beta",
    "components": ["Front_Left_Servo", "Front_Right_Servo", "IMU_Sensor", "Battery_Management"]
}

if __name__ == "__main__":
    root = tk.Tk()
    app = ReconfigurableApp(root, CURRENT_MORPHOLOGY)
    root.mainloop()
    
    
    
    
    ''' Traceback (most recent call last):
  File "C:\Users\Amelia Williams\OneDrive\Desktop\GUI_test2.py", line 84, in <module>
    app = ReconfigurableApp(root, CURRENT_MORPHOLOGY)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Amelia Williams\OneDrive\Desktop\GUI_test2.py", line 34, in __init__
    self.setup_ui()
  File "C:\Users\Amelia Williams\OneDrive\Desktop\GUI_test2.py", line 47, in setup_ui
    container = tk.LabelFrame(self.root, text="Hardware Components", padding=10)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\ProgramData\anaconda3\Lib\tkinter\__init__.py", line 4418, in __init__
    Widget.__init__(self, master, 'labelframe', cnf, kw)
  File "C:\ProgramData\anaconda3\Lib\tkinter\__init__.py", line 2628, in __init__
    self.tk.call(
_tkinter.TclError: unknown option "-padding" '''


Getting the above error in this version