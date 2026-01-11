import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import logging

# 1. Setup logging for hardware audit trails
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestbedHAL:
    """Hardware Abstraction Layer (HAL). 
    This allows software to interact with 'Components' regardless of physical morphology."""
    def __init__(self, morphology_name):
        self.morphology_name = morphology_name
        
    def run_validation_test(self, component_id, callback):
        """Simulates a hardware validation task in a separate thread."""
        logging.info(f"AUDIT: Starting validation on {self.morphology_name} -> {component_id}")
        
        # Simulate hardware communication/latency
        time.sleep(1.5) 
        
        result = f"{component_id}: OK"
        logging.info(f"AUDIT: Result - {result}")
        
        # Return result to the main thread via the callback
        callback(result)

class ReconfigurableApp:
    def __init__(self, root, config):
        self.root = root
        self.root.title("Co-Design Testbed Controller")
        self.root.geometry("500x450")
        
        # Morphology state
        self.config = config
        self.hal = TestbedHAL(config['name'])
        
        self.setup_ui()

    def setup_ui(self):
        """Constructs the GUI dynamically based on the morphology configuration."""
        # Main Header
        header = ttk.Label(self.root, text=f"Morphology: {self.config['name']}", 
                          font=("Segoe UI", 14, "bold"))
        header.pack(pady=15)

        self.status_var = tk.StringVar(value="System Ready")
        status_display = ttk.Label(self.root, textvariable=self.status_var, foreground="green")
        status_display.pack(pady=5)

        # FIX: Using ttk.LabelFrame which supports the 'padding' argument
        container = ttk.LabelFrame(self.root, text="Control Stack", padding=15)
        container.pack(padx=20, pady=10, fill="both", expand=True)

        # Documentation/Due Diligence: Dynamic Button Generation
        for component in self.config['components']:
            frame = ttk.Frame(container)
            frame.pack(fill="x", pady=2)
            
            lbl = ttk.Label(frame, text=component, width=25)
            lbl.pack(side="left")
            
            btn = ttk.Button(
                frame, 
                text="Validate", 
                command=lambda c=component: self.execute_test_sequence(c)
            )
            btn.pack(side="right")

    def execute_test_sequence(self, component_id):
        """Initializes a non-blocking test sequence."""
        self.status_var.set(f"Validating {component_id}...")
        
        # Execute in a background thread to keep UI responsive
        thread = threading.Thread(
            target=self.hal.run_validation_test, 
            args=(component_id, self.on_test_complete),
            daemon=True # Ensures thread closes if GUI is closed
        )
        thread.start()

    def on_test_complete(self, result):
        """Thread-safe UI update."""
        self.root.after(0, lambda: self.status_var.set(f"Last Result: {result}"))
        self.root.after(0, lambda: messagebox.showinfo("Validation Report", result))

# --- Reconfigurable Configuration Section ---
# This dictionary represents the "Software Stack" discovery of "Hardware Morphology"
CURRENT_MORPHOLOGY = {
    "name": "GOAT_Testing_Rig_v0",
    "components": [
        "Motor_Controller_Alpha",
        "Torque_Sensor_01",
        "Thermal_Probe_A",
        "Thermal_Probe_B",
        "Emergency_Stop_Circuit"
    ]
}

if __name__ == "__main__":
    root = tk.Tk()
    # Apply a theme for a more professional 'testbed' look
    style = ttk.Style()
    style.theme_use('clam') 
    
    app = ReconfigurableApp(root, CURRENT_MORPHOLOGY)
    root.mainloop()