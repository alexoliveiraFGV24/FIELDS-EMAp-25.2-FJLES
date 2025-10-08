from gui.mainWindow import App
import gui.fonts

def main():
    app = App()
    gui.fonts.initialize_fonts()
    app.mainloop()    

if __name__ == "__main__":
    main()