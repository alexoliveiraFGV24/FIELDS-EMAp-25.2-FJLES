import customtkinter
from gui.paginaStatusFila import PaginaStatusHospital
from gui.paginaStatusPaciente import PaginaStatusPaciente


class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs): 
        super().__init__(master=master, **kwargs)

        self.add("Status Fila Hospital")
        self.add("Pacientes")
        self.hospitalStatusFrame = PaginaStatusHospital(master=self.tab("Status Fila Hospital"))
        self.hospitalStatusFrame.pack(fill="both", expand=True)

        #frames paciente
        self.pacientesFrame = PaginaStatusPaciente(master=self.tab("Pacientes"))
        self.pacientesFrame.pack(expand=True, fill='both')
    