import tkinter as tk
import threading
import keyboard
import win32gui
import macro
import os

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.geometry("100x100+50+50")
        self.attributes("-transparentcolor", "white")

        self.canvas = tk.Canvas(self, width=100, height=100, bg="white", highlightthickness=0)
        self.canvas.pack()

        self.circle = self.canvas.create_oval(10, 10, 90, 90, fill="#A0DD07", outline="")
        self.text = self.canvas.create_text(50, 50, text="▶", fill="white", font=("Arial", 30, "bold"))

        self.canvas.bind("<Button-1>", self.on_click)

        self.macro_thread = None
        self.monitor_thread = None

        self.stop_macro = threading.Event()
        self.pause_macro = threading.Event()

        threading.Thread(target=self.listen_hotkey, daemon=True).start()


    def on_click(self, event=None):
        if self.macro_thread and self.macro_thread.is_alive():
            self.stop_macro.set()
            self.canvas.itemconfig(self.circle, fill="#A0DD07")
            self.canvas.itemconfig(self.text, text="▶")
        else:
            self.stop_macro.clear()
            self.macro_thread = threading.Thread(
                target=macro.run_macro,
                args=(self.stop_macro, self.pause_macro),
                daemon=True
            )
            self.macro_thread.start()

            self.pause_macro.clear()
            self.monitor_thread = threading.Thread(
                target=macro.monitor_pause,
                args=(self.stop_macro, self.pause_macro),
                daemon=True
            )
            self.monitor_thread.start()

            self.canvas.itemconfig(self.circle, fill="#A0DD07")
            self.canvas.itemconfig(self.text, text="■")

    def listen_hotkey(self):
        keyboard.add_hotkey('F8', self.on_click)
        keyboard.wait()

if __name__ == "__main__":
    app = Interface()
    app.mainloop()
