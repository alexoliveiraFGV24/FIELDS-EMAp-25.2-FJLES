#módulo ainda nao configurado

import customtkinter

FONT_HEADER = None
FONT_CARD_TITULO = None
FONT_CARD_DADO_DESTAQUE = None
FONT_CARD_DADO_NORMAL = None

def initialize_fonts():
    """Cria as instâncias de fonte. """
    global FONT_HEADER, FONT_CARD_TITULO, FONT_CARD_DADO_DESTAQUE, FONT_CARD_DADO_NORMAL
    
    FONT_HEADER = customtkinter.CTkFont(family="Roboto", size=24, weight="bold")
    FONT_CARD_TITULO = customtkinter.CTkFont(family="Roboto", size=20, weight="bold")
    FONT_CARD_DADO_DESTAQUE = customtkinter.CTkFont(family="Roboto", size=22, weight="bold")
    FONT_CARD_DADO_NORMAL = customtkinter.CTkFont(family="Roboto", size=13)
    