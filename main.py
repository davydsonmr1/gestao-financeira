import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog, messagebox

from src.controllers import FinanceiroController
from src.views.dashboard import DashboardView
from src.views.forms import FormView
from src.views.settings import SettingsDialog

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PySec Finance Manager")
        self.geometry("1000x600")
        
        self.controller = FinanceiroController()
        
        # Estado Global
        hoje = datetime.now()
        self.mes_atual = hoje.month
        self.ano_atual = hoje.year

        self._setup_layout()
        self.refresh_app()

    def _setup_layout(self):
        # Grid Principal: 2 Colunas (Lateral, Conteúdo)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -- Sidebar (Esquerda) --
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Título
        ctk.CTkLabel(self.sidebar, text="Gestão Financeira", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Navegação
        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=10)
        
        self.cmb_mes = ctk.CTkComboBox(self.nav_frame, values=[str(i) for i in range(1, 13)], width=70, command=self._mudanca_data)
        self.cmb_mes.set(str(self.mes_atual))
        self.cmb_mes.pack(side="left", padx=5)

        self.cmb_ano = ctk.CTkComboBox(self.nav_frame, values=[str(i) for i in range(2023, 2030)], width=90, command=self._mudanca_data)
        self.cmb_ano.set(str(self.ano_atual))
        self.cmb_ano.pack(side="left", padx=5)

        # Formulário de Adição
        self.form_view = FormView(self.sidebar, self.controller, self.refresh_app)
        self.form_view.pack(fill="both", expand=True, pady=10)

        # Botões Rodapé Sidebar
        ctk.CTkButton(self.sidebar, text="Configurar Salários", command=self.abrir_settings, fg_color="#555").pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="Exportar Excel", command=self.exportar_excel, fg_color="#27ae60").pack(pady=(5, 20), padx=10, fill="x")

        # -- Área Principal (Direita) --
        self.dashboard = DashboardView(self, self.controller)
        self.dashboard.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def _mudanca_data(self, _):
        self.mes_atual = int(self.cmb_mes.get())
        self.ano_atual = int(self.cmb_ano.get())
        self.refresh_app()

    def refresh_app(self):
        """Atualiza toda a UI com base no mês/ano selecionado."""
        self.dashboard.atualizar_dashboard(self.mes_atual, self.ano_atual)
        self.form_view.atualizar_lista(self.mes_atual, self.ano_atual)

    def abrir_settings(self):
        SettingsDialog(self, self.controller, self.refresh_app)

    def exportar_excel(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if filename:
            try:
                self.controller.exportar_relatorio(self.mes_atual, self.ano_atual, filename)
                messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao exportar: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
