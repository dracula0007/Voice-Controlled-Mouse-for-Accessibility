import tkinter as tk

def show_help():
    help_text =  """🔹 Available Commands 🔹

📌 Mouse Control:  
up, down, left, right, Click, Double click, Right click, Scroll up, Scroll down  

📌 Application Control:  
Open browser, Open file explorer, Open notepad, Open settings, Open task manager, Open calculator, cmd

📌 Window Management:  
Close window, Minimize window, Maximize window, Switch window, Show desktop, Snap left, Snap right  

📌 Media Control:  
Play media, Pause media, Next track, Previous track, Volume up, Volume down, Mute  

📌 Text Editing:  
Copy, Paste, Cut, Delete, Undo, Redo, New line, Space, Enter  

📌 Browsing:  
Open Google, Open YouTube, New tab, Close tab, Refresh page  

📌 File Management:  
Create folder, Delete folder, Open downloads, Open documents  

📌 System Control:  
Lock screen, Shut down, Restart, Sleep, Take screenshot, Toggle fullscreen  

📌 Greating:
How are you, What is your name, Who Developed you, Say

📌 Exit:  
Say 'exit' to close the program."""

    help_window = tk.Toplevel()
    help_window.title("ZERO Help")
    help_window.geometry("700x550")
    help_window.configure(bg="#222") 

    listbox = tk.Listbox(help_window, font=("Arial", 12), bg="#222", fg="#0f0", highlightthickness=0, bd=0)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    for line in help_text.split("\n"):
        listbox.insert(tk.END, line)
        listbox.insert(tk.END, " ")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_help()
    root.mainloop()
