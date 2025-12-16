import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        
        # Grid Layout
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=0) # KPIs
        self.grid_rowconfigure(1, weight=1) # Gráfico

        # KPIs
        self.card_receita = self._criar_card(0, "Receita", "text-green")
        self.card_despesa = self._criar_card(1, "Despesas", "text-red")
        self.card_saldo = self._criar_card(2, "Saldo", "text-white")

        # Área do Gráfico
        self.frame_grafico = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_grafico.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.canvas = None

    def _criar_card(self, col, titulo, tipo_cor):
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="ew")
        
        lbl_titulo = ctk.CTkLabel(frame, text=titulo, font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=(10, 0))
        
        lbl_valor = ctk.CTkLabel(frame, text="R$ 0,00", font=("Arial", 20))
        lbl_valor.pack(pady=(5, 10))
        
        # Guardamos referência ao label de valor para atualizar depois
        frame.lbl_valor = lbl_valor
        return frame

    def atualizar_dashboard(self, mes, ano):
        # 1. Buscar Dados
        df = self.controller.buscar_despesas_mes(mes, ano)
        salarios = self.controller.get_configuracoes()
        receita = sum(salarios)
        despesas = df['valor'].sum() if not df.empty else 0.0
        saldo = receita - despesas

        # 2. Atualizar KPIs
        self.card_receita.lbl_valor.configure(text=f"R$ {receita:,.2f}", text_color="#2CC985")
        self.card_despesa.lbl_valor.configure(text=f"R$ {despesas:,.2f}", text_color="#FF4757")
        
        cor_saldo = "#2CC985" if saldo >= 0 else "#FF4757"
        self.card_saldo.lbl_valor.configure(text=f"R$ {saldo:,.2f}", text_color=cor_saldo)

        # 3. Atualizar Gráfico
        self._plotar_grafico(df)

    def _plotar_grafico(self, df):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            plt.close('all')

        if df.empty:
            return

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        # Tema Escuro para Matplotlib
        fig.patch.set_facecolor('#2b2b2b') # Cor de fundo do CustomTkinter padrão
        ax.set_facecolor('#2b2b2b')
        
        dados_cat = df.groupby('categoria')['valor'].sum()
        
        wedges, texts, autotexts = ax.pie(
            dados_cat, 
            labels=dados_cat.index, 
            autopct='%1.1f%%',
            startangle=90,
            textprops=dict(color="white"),
            wedgeprops=dict(width=0.4) # Donut
        )
        
        plt.setp(autotexts, size=10, weight="bold")
        ax.set_title("Despesas por Categoria", color="white")

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
