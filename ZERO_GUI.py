import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import threading
import cv2
import pygame
from PIL import Image, ImageTk
import ZERO_main

class VoiceControlApp:

    def start_move(self, event):
            self.x = event.x
            self.y = event.y

    def on_move(self, event):
        x_root = self.root.winfo_x() + (event.x - self.x)
        y_root = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x_root}+{y_root}")


    def __init__(self, root):
        self.root = root
        self.root.title("ZEROv1.0.1")
        self.root.geometry("700x550")
        self.style = ttk.Style("cyborg")

        # NO TITLE BAR
        # self.root.overrideredirect(True)

        # Move Window ON or OFF
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)


        # Welcome Voice
        pygame.mixer.init()
        pygame.mixer.music.load("voice.mp3")
        pygame.mixer.music.play()

        # Title 
        self.label_title = ttk.Label(root, text="🎤 Voice Control System", font=("Arial", 18, "bold"))
        self.label_title.pack(pady=10)

        # Video Show
        self.video_frame = ttk.Frame(root)
        self.video_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.video_label = ttk.Label(self.video_frame)
        self.video_label.pack()

        # Control buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=10)

        self.button_start = ttk.Button(self.button_frame, text="🎙️ Start Listening", bootstyle="success-outline", command=self.toggle_voice_control)
        self.button_start.grid(row=0, column=0, padx=10, pady=5)

        self.button_exit = ttk.Button(self.button_frame, text="❌ Say Exit", bootstyle="danger-outline", command=self.exit_program)
        self.button_exit.grid(row=0, column=1, padx=10, pady=5)

        self.running = False
        self.video_running = True
        self.video_path = "Robot.mp4"
        self.cap = cv2.VideoCapture(self.video_path)
        self.update_video()

        self.create_command_window()

        self.root.bind("<Configure>", self.update_command_window_position)
        self.root.bind("<Map>", self.show_command_window)
        self.root.bind("<Unmap>", self.hide_command_window)

    def create_command_window(self):
        
        self.command_window = tk.Toplevel(self.root)
        self.command_window.title("Recognized Commands")
        self.command_window.geometry("300x550+710+150")
        self.command_window.overrideredirect(True)
        self.command_window.attributes('-alpha', 0.95)  # Trans Window
        # self.command_window.attributes('-topmost', 1)
        self.command_window.attributes("-topmost", False)

        self.command_listbox = tk.Listbox(self.command_window, font=("Arial", 12), height=25, bg="#222", fg="#00FF00")
        self.command_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.command_listbox.insert(tk.END, "🔍 Waiting for commands...")

    def update_command_window_position(self, event):
        
        if self.root.winfo_viewable():
            x = self.root.winfo_x() + self.root.winfo_width() + 15
            y = self.root.winfo_y() + 28
            self.command_window.geometry(f"300x{self.root.winfo_height()}+{x}+{y}")

    def show_command_window(self, event):
        self.command_window.deiconify()

    def hide_command_window(self, event):
        self.command_window.withdraw()

    def toggle_voice_control(self):
        if self.running:
            self.running = False
            self.button_start.config(text="🎙️ Start Listening", bootstyle="success-outline")
        else:
            self.running = True
            self.button_start.config(text="⏳ Listening...", bootstyle="warning-outline")
            threading.Thread(target=self.listen_for_commands, daemon=True).start()

    def listen_for_commands(self):
        for command in ZERO_main.recognize_audio():
            if not self.running:
                break
            self.root.after(0, self.update_command_window, command)

    def update_command_window(self, command):
        
        if command in ZERO_main.COMMANDS:  # Check Commands
            self.command_listbox.insert(tk.END, "")
            self.command_listbox.insert(tk.END, f"📌 {command}")
            self.command_listbox.insert(tk.END, "")
            self.command_listbox.yview(tk.END)

    def update_video(self):
        if self.video_running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (700, 400))
                img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.video_label.config(image=img)
                self.video_label.image = img
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.root.after(30, self.update_video)

    def exit_program(self):
        self.running = False
        self.video_running = False
        self.cap.release()
        self.root.destroy()
        pygame.mixer.quit()

if __name__ == "__main__":
    root = ttk.Window(themename="cyborg")
    app = VoiceControlApp(root)
    root.mainloop()
