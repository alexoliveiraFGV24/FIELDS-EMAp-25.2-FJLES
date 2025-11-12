def refresh_dashboard(tab_view):
    """
    Função global para atualizar todos os dashboards.
    
    :param tab_view: Instância da classe MyTabView que contém todas as páginas.
    """
    # A página PaginaStatusHospital (hospitalStatusFrame) já tem um loop de atualização próprio
    # (self.after(1000, self.atualizar_dados)).
    # No entanto, se o loop estiver pausado, o refresh global pode ser útil.
    # Vamos chamar o método de atualização de dados, que também verifica se está pausado.
    if hasattr(tab_view.hospitalStatusFrame, 'atualizar_dados'):
        # Chama a atualização de dados da página de status da fila
        tab_view.hospitalStatusFrame.atualizar_dados() 
        
    # A página PaginaStatusPaciente não tem um loop, mas tem um método para recarregar o paciente selecionado.
    # Não é necessário um refresh periódico, mas se houver um método 'refresh', ele deve ser chamado.
    # Pelo que vi, a PaginaStatusPaciente não tem um método 'refresh' que atualiza dados externos.
    # Se a intenção for apenas atualizar a PaginaComparacaoTemporal, chamamos apenas ela.
    
    # Chamada para a nova página
    if hasattr(tab_view.comparacaoTemporalFrame, 'refresh'):
        tab_view.comparacaoTemporalFrame.refresh()
        
    # Se houver necessidade de forçar a atualização de outros componentes, adicionar aqui.
    # Exemplo: tab_view.pacientesFrame.refresh() # Se for implementado