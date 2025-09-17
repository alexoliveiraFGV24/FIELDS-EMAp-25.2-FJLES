import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import gui.config as config

class PaginaStatusPaciente(customtkinter.CTkFrame):
    """
    Uma classe de página placeholder para o status do paciente.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)