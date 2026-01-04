import time
import os
import random

# Configuration / Constants
CLEAR_SCREEN = "\033[H\033[2J"  # ANSI escape code to clear terminal
FAST = 0.1
SLOW = 1.5

def clear():
    """Clears the terminal window."""
    print(CLEAR_SCREEN, end="", flush=True)

def show_progress_bar(task_name, duration=2):
    """Displays a simple visual loading bar."""
    print(f"{task_name}: ", end="", flush=True)
    steps = 80
    for i in range(steps):
        time.sleep(duration / steps)
        print("█", end="", flush=True)
    print(" [DONE]")

def run_shutdown_sequence():
    """Phase 1: Closing applications and halting the kernel."""
    print("\n--- INITIATING SYSTEM SHUTDOWN ---")
    time.sleep(SLOW)
    
    tasks = ["Saving Session", "Closing Network Sockets", "Unmounting Drives"]
    for task in tasks:
        show_progress_bar(task, duration=1)
    
    print("\nSystem Halted. Powering down...")
    time.sleep(SLOW)

def run_boot_sequence():
    """Phase 3: Hardware checks and OS loading."""
    print("LOGIC-GATE BIOS v4.02")
    print("Checking Memory... 65536MB OK")
    print("Detecting Storage... NVMe Gen4 Found\n")
    time.sleep(1)

    boot_logs = [
        "Loading Linux Kernel 6.1.0...",
        "Initializing Hardware Abstraction Layer...",
        "Starting Security Services...",
        "Setting up Virtual Console...",
        "Starting Graphical Interface..."
    ]

    for log in boot_logs:
        # Vary the speed to look like it's actually "working"
        delay = random.uniform(0.05, 0.5)
        print(f"[  OK  ] {log}")
        time.sleep(delay)

    print("\nWelcome to TerminalOS v1.0")
    print("Login: admin")
    print("Password: ********")
    time.sleep(2)

def main():
    """The main loop that controls the single-thread execution."""
    try:
        while True:
            run_shutdown_sequence()
            
            # Phase 2: The "Blackout" (Simulated power-off state)
            clear()
            time.sleep(3) 
            
            run_boot_sequence()
            
            # Pause so the user can see the "finished" state before it reboots again
            print("\n(System will restart in 5 seconds...)")
            time.sleep(5)
            clear()

    except KeyboardInterrupt:
        print("\n\nSimulation terminated safely.")

if __name__ == "__main__":
    main()