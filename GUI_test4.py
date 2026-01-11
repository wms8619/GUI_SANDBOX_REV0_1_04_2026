import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import logging
import os
from datetime import datetime
import random

# Matplotlib integration for the Live Graph
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class TestbedHAL:
    """Hardware Abstraction Layer with Sensor Simulation."""
    def __init__(self):
        self.is_running = True

    def get_sensor_reading(self):
        """Simulates a real-time sensor stream (e.g., Voltage or Torque)."""
        # Simulating a noisy sine wave or random data
        return 50 + (random.random() * 10) 

class ReconfigurableApp:
    def __init__(self, root, config):
        self.root = root
        self.root.title("Advanced Co-Design Testbed v2.0")
        self.root.geometry("800x600")
        
        self.config = config
        self.hal = TestbedHAL()
        self.data_points = [] # Store telemetry for the graph
        
        # 1. Setup Logging Directory and File
        self.setup_logging()
        
        # 2. Build UI
        self.setup_ui()
        
        # 3. Start the Live Telemetry Loop
        self.update_telemetry()

    def setup_logging(self):
        """Creates a timestamped log file in the script's directory."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_test1_logging_data.txt"
        self.log_path = os.path.join(script_dir, filename)
        
        # Configure standard logging to point to this file
        logging.basicConfig(
            filename=self.log_path,
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )
        logging.info(f"Test Session Started. Morphology: {self.config['name']}")

    def setup_ui(self):
        """UI with Integrated Matplotlib Graph."""
        # Top Control Panel
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(side="top", fill="x")
        
        ttk.Label(top_frame, text=f"Active Morphology: {self.config['name']}", 
                  font=("Arial", 12, "bold")).pack(side="left")
        
        self.status_var = tk.StringVar(value="System Logging Active")
        ttk.Label(top_frame, textvariable=self.status_var, foreground="blue").pack(side="right")

        # Main Layout: Left (Buttons) | Right (Graph)
        main_container = ttk.PanedWindow(self.root, orient="horizontal")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Frame: Control Stack
        btn_frame = ttk.LabelFrame(main_container, text="Component Validation", padding=10)
        main_container.add(btn_frame, weight=1)

        for comp in self.config['components']:
            ttk.Button(btn_frame, text=f"Validate {comp}", 
                       command=lambda c=comp: self.log_event(c)).pack(fill="x", pady=5)

        # Right Frame: Live Graph
        graph_frame = ttk.LabelFrame(main_container, text="Real-Time Telemetry", padding=10)
        main_container.add(graph_frame, weight=3)

        # Matplotlib Figure Setup
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Sensor Load (Real-time)")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Value")
        self.line, = self.ax.plot([], [], lw=2, color='red')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def log_event(self, component):
        """Logs a manual validation event to the file."""
        msg = f"MANUAL_VALIDATION: {component} triggered."
        logging.info(msg)
        self.status_var.set(f"Logged: {component}")

    def update_telemetry(self):
        """The heartbeat of the application: updates data and the graph."""
        # 1. Get new data
        val = self.hal.get_sensor_reading()
        self.data_points.append(val)
        
        # 2. Keep only last 50 points for the graph
        if len(self.data_points) > 50:
            self.data_points.pop(0)

        # 3. Update the Graph
        self.line.set_data(range(len(self.data_points)), self.data_points)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        # 4. Periodically log raw telemetry to file (every 2 seconds approximately)
        if len(self.data_points) % 10 == 0:
            logging.info(f"TELEMETRY_SAMPLE: Current Value {val:.2f}")

        # Schedule next update (100ms = 10Hz refresh rate)
        self.root.after(100, self.update_telemetry)

# Configuration for the testbed
CURRENT_MORPHOLOGY = {
    "name": "Propulsion_System_v4",
    "components": ["Thrust_Vector_Servo", "Fuel_Pressure_Valve", "Ignition_Module"]
}

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    app = ReconfigurableApp(root, CURRENT_MORPHOLOGY)
    root.mainloop()