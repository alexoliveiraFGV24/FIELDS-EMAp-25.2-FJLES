import customtkinter
from gui.paginaStatusFila import PaginaStatusHospital
from gui.paginaStatusPaciente import PaginaStatusPaciente
from gui.paginaComparacaoTemporal import PaginaComparacaoTemporal

class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs): 
        super().__init__(master=master, **kwargs)

        self.add("Status Fila Hospital")
        self.add("Pacientes")
        self.add("Temporal")

        # Frames fila
        self.hospitalStatusFrame = PaginaStatusHospital(master=self.tab("Status Fila Hospital"))
        self.hospitalStatusFrame.pack(fill="both", expand=True)

        #Frames paciente
        self.pacientesFrame = PaginaStatusPaciente(master=self.tab("Pacientes"))
        self.pacientesFrame.pack(expand=True, fill='both')

        #Frames temporal
        self.comparacaoTemporalFrame = PaginaComparacaoTemporal(master=self.tab("Temporal"))
        self.comparacaoTemporalFrame.pack(expand=True, fill='both')

    def refresh_all(self):
        """Chama o método refresh de todas as páginas que o possuem."""
        # A PaginaStatusHospital já tem um loop de atualização próprio (self.after), mas podemos chamar o atualizar_dados para forçar uma atualização imediata.
        if hasattr(self.hospitalStatusFrame, 'atualizar_dados'):
            self.hospitalStatusFrame.atualizar_dados()
        
        # A PaginaStatusPaciente não tem um refresh de dados externos, mas a PaginaComparacaoTemporal sim.
        if hasattr(self.comparacaoTemporalFrame, 'refresh'):
            self.comparacaoTemporalFrame.refresh()