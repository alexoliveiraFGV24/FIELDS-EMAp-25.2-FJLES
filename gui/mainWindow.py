import customtkinter
import gui.config as config
from gui.tab import MyTabView
import gui.fonts


class App(customtkinter.CTk):
    def __init__(self):

        super().__init__()
        gui.fonts.initialize_fonts()
        customtkinter.set_appearance_mode("Light")
        customtkinter.set_default_color_theme("green")
    
        self.title("Dashboard")
        self.geometry(f"{config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tab_view = MyTabView(master=self, width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT)
        self.tab_view.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")

        self.refresh_button = customtkinter.CTkButton(self, text="Atualizar Dados", command=self.refresh_all_tabs)
        self.refresh_button.grid(row=1, column=0, padx=20, pady=10, sticky="se")

    def refresh_all_tabs(self):
        self.tab_view.refresh_all()

if __name__ == "__main__":
    app = App()
    app.mainloop()