import tkinter as tk
import subprocess

def check_wifi_status():
    try:
        subprocess.run(["iwgetid"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_for_wifi(window):
    if check_wifi_status():
        window.destroy()
    else:
        window.after(1000, check_for_wifi, window)

# Create GUI window
window = tk.Tk()
window.geometry("400x300")
window.title("Please connect to WiFi")
window.attributes("-fullscreen", False)

# Create GUI elements
status_label = tk.Label(window, text="To get started, please \nconnect your device to \na WiFi network. This will \nallow you to access all\nthe features and functions\n of the device. Thank you!", fg="red", font=("Arial", 20, "bold"))

# Add GUI elements to window
status_label.pack(expand=True, fill="both")

# Start checking for WiFi connection
window.after(1000, check_for_wifi, window)

# Start GUI event loop
window.mainloop()
