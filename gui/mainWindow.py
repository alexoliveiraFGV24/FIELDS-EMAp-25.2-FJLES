import customtkinter
import gui.config as config
from gui.tab import MyTabView
import tkinter as tk


class App(customtkinter.CTk):
    def __init__(self):

        super().__init__()
    
        customtkinter.set_appearance_mode("Light")
        customtkinter.set_default_color_theme("green")
    
        self.title("Dashboard")
        self.geometry(f"{config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tab_view = MyTabView(master=self, width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT)
        self.tab_view.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()