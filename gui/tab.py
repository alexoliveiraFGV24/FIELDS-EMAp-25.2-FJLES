import customtkinter
from gui.paginaStatusFila import PaginaStatusHospital
from gui.paginaStatusPaciente import PaginaStatusPaciente
from gui.paginaStatusOperacoes import PaginaStatusOperacoes



class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs): 
        super().__init__(master=master, **kwargs)

        self.add("Status Fila Hospital")
        self.add("Pacientes")
        self.add("Operações")

        # Frames fila
        self.hospitalStatusFrame = PaginaStatusHospital(master=self.tab("Status Fila Hospital"))
        self.hospitalStatusFrame.pack(fill="both", expand=True)

        #Frames paciente
        self.pacientesFrame = PaginaStatusPaciente(master=self.tab("Pacientes"))
        self.pacientesFrame.pack(expand=True, fill='both')

        #Frames operação
        self.pacientesFrame = PaginaStatusOperacoes(master=self.tab("Operações"))
        self.pacientesFrame.pack(expand=True, fill='both')


    