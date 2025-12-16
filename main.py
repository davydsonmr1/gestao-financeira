import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox, filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.controllers import FinanceiroController

# Configuração Visual Global
ctk.set_appearance_mode("Light") # Fundo Claro conforme imagem
ctk.set_default_color_theme("dark-blue")

# Cores do Tema (Baseado na imagem fornecida)
COR_BG_HEADER = "#E8EAF6" # Azul bem clarinho
COR_BG_CARDS = "#FFFFFF"
COR_TEXTO_AZUL = "#1A237E" # Azul escuro para títulos
COR_DESTAQUE = "#304FFE" # Azul vibrante

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Davydson Finanças")
        self.geometry("1280x720")
        self.controller = FinanceiroController()
        
        # Estado
        hoje = datetime.now()
        self.mes_atual = hoje.month
        self.ano_atual = hoje.year

        # Layout Principal
        self._setup_ui()
        self.refresh_app()

    def _setup_ui(self):
        # Grid Mestre: Header (0) + Conteúdo (1)
        self.grid_rowconfigure(0, weight=0) # Header fixo
        self.grid_rowconfigure(1, weight=1) # Conteúdo expande
        self.grid_columnconfigure(0, weight=1)

        # === 1. HEADER SUPERIOR ===
        self.header = ctk.CTkFrame(self, height=100, fg_color=COR_BG_HEADER, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")
        
        # Ícone/Logo (Placeholder)
        lbl_logo = ctk.CTkLabel(self.header, text="🏠", font=("Arial", 30))
        lbl_logo.pack(side="left", padx=20)

        # Textos do Header
        frm_titles = ctk.CTkFrame(self.header, fg_color="transparent")
        frm_titles.pack(side="left", pady=10)
        
        ctk.CTkLabel(frm_titles, text="Davydson Finanças", font=("Arial", 24, "bold"), text_color=COR_TEXTO_AZUL).pack(anchor="w")
        ctk.CTkLabel(frm_titles, text="Controle de Contas", font=("Arial", 14), text_color="gray").pack(anchor="w")

        # Seletor de Mês/Ano (No Header, conforme design)
        frm_nav = ctk.CTkFrame(self.header, fg_color="transparent")
        frm_nav.pack(side="right", padx=30)
        
        ctk.CTkLabel(frm_nav, text="Mês de Referência:", font=("Arial", 12, "bold")).pack(anchor="e")
        nav_selectors = ctk.CTkFrame(frm_nav, fg_color="transparent")
        nav_selectors.pack()
        
        self.cmb_mes = ctk.CTkComboBox(nav_selectors, values=[str(i) for i in range(1, 13)], width=70, command=self._refresh_trigger)
        self.cmb_mes.set(str(self.mes_atual))
        self.cmb_mes.pack(side="left", padx=5)
        
        self.cmb_ano = ctk.CTkComboBox(nav_selectors, values=[str(i) for i in range(2023, 2030)], width=80, command=self._refresh_trigger)
        self.cmb_ano.set(str(self.ano_atual))
        self.cmb_ano.pack(side="left")

        # === 2. ÁREA DE CONTEÚDO (3 COLUNAS) ===
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Pesos das colunas
        self.main_area.grid_columnconfigure(0, weight=1) 
        self.main_area.grid_columnconfigure(1, weight=2) 
        self.main_area.grid_columnconfigure(2, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

        # --- COLUNA 1: INPUTS E SALÁRIOS ---
        self._setup_col_esquerda()

        # --- COLUNA 2: LISTAS (FIXAS vs VARIÁVEIS) ---
        self._setup_col_central()

        # --- COLUNA 3: GRÁFICOS ---
        self._setup_col_direita()

    def _setup_col_esquerda(self):
        frm = ctk.CTkFrame(self.main_area, fg_color=COR_BG_CARDS, corner_radius=10, border_width=1, border_color="#DDD")
        frm.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Container Interno com Padding
        content = ctk.CTkFrame(frm, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        # -- Salários --
        ctk.CTkLabel(content, text="Salário Julia", font=("Arial", 12, "bold"), text_color=COR_TEXTO_AZUL).pack(anchor="w")
        self.ent_sal_julia = ctk.CTkEntry(content, placeholder_text="0.00")
        self.ent_sal_julia.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(content, text="Salário Davydson", font=("Arial", 12, "bold"), text_color=COR_TEXTO_AZUL).pack(anchor="w")
        self.ent_sal_davydson = ctk.CTkEntry(content, placeholder_text="0.00")
        self.ent_sal_davydson.pack(fill="x", pady=(0, 20))
        
        # Botão discreto para salvar salários
        ctk.CTkButton(content, text="Atualizar Salários", height=25, fg_color="#555", command=self.salvar_salarios).pack(fill="x", pady=(0, 20))

        ttk.Separator(content, orient='horizontal').pack(fill='x', pady=10)

        # -- Nova Despesa --
        ctk.CTkLabel(content, text="Nova Despesa", font=("Arial", 16, "bold"), text_color=COR_DESTAQUE).pack(anchor="w", pady=(10, 5))
        
        self.cmb_tipo = ctk.CTkComboBox(content, values=["Fixa", "Variável", "Investimento"])
        self.cmb_tipo.set("Variável")
        self.cmb_tipo.pack(fill="x", pady=5)

        self.ent_data = ctk.CTkEntry(content, placeholder_text="Data (DD/MM/YYYY)")
        self.ent_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.ent_data.pack(fill="x", pady=5)

        self.cmb_cat = ctk.CTkComboBox(content, values=["Alimentação", "Transporte", "Casa", "Lazer", "Outros"])
        self.cmb_cat.pack(fill="x", pady=5)

        self.ent_val = ctk.CTkEntry(content, placeholder_text="Valor (R$)")
        self.ent_val.pack(fill="x", pady=5)
        
        self.ent_desc = ctk.CTkEntry(content, placeholder_text="Descrição")
        self.ent_desc.pack(fill="x", pady=5)

        ctk.CTkButton(content, text="Adicionar Lançamento", fg_color=COR_DESTAQUE, command=self.adicionar_despesa).pack(fill="x", pady=20)

    def _setup_col_central(self):
        frm = ctk.CTkFrame(self.main_area, fg_color="transparent")
        frm.grid(row=0, column=1, sticky="nsew", padx=10)
        frm.grid_columnconfigure(0, weight=1)
        frm.grid_columnconfigure(1, weight=1)
        frm.grid_rowconfigure(0, weight=1)

        # Lista Fixa (Esquerda do Centro)
        self.frm_fixas = self._criar_lista_container(frm, "Despesas Fixas", 0, 0)
        
        # Lista Variável (Direita do Centro)
        self.frm_variaveis = self._criar_lista_container(frm, "Despesas Variáveis", 0, 1)

    def _criar_lista_container(self, parent, titulo, row, col):
        frame = ctk.CTkFrame(parent, fg_color=COR_BG_CARDS, corner_radius=10, border_width=1, border_color="#DDD")
        frame.grid(row=row, column=col, sticky="nsew", padx=5)
        
        ctk.CTkLabel(frame, text=titulo, font=("Arial", 14, "bold"), text_color=COR_TEXTO_AZUL).pack(pady=10)
        
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=5, pady=5)
        return scroll

    def _setup_col_direita(self):
        frm = ctk.CTkFrame(self.main_area, fg_color=COR_BG_CARDS, corner_radius=10, border_width=1, border_color="#DDD")
        frm.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        # Container Gráfico
        ctk.CTkLabel(frm, text="Distribuição por Categoria", font=("Arial", 14, "bold"), text_color=COR_TEXTO_AZUL).pack(pady=10)
        self.frame_grafico = ctk.CTkFrame(frm, fg_color="transparent")
        self.frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configs Rápidas
        btn_exp = ctk.CTkButton(frm, text="Exportar Excel", fg_color="#27ae60", command=self.exportar)
        btn_exp.pack(fill="x", padx=20, pady=20)

    # --- LÓGICA ---
    
    def _refresh_trigger(self, _=None):
        self.mes_atual = int(self.cmb_mes.get())
        self.ano_atual = int(self.cmb_ano.get())
        self.refresh_app()

    def salvar_salarios(self):
        try:
            s1 = float(self.ent_sal_julia.get().replace(",", "."))
            s2 = float(self.ent_sal_davydson.get().replace(",", "."))
            self.controller.salvar_configuracoes(s1, s2)
            self.refresh_app()
            messagebox.showinfo("Sucesso", "Salários atualizados!")
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido nos salários")

    def adicionar_despesa(self):
        try:
            valor = float(self.ent_val.get().replace(",", "."))
            self.controller.adicionar_despesa(
                self.ent_data.get(),
                self.cmb_tipo.get(),
                self.cmb_cat.get(),
                self.ent_desc.get(),
                valor
            )
            # Limpar
            self.ent_val.delete(0, "end")
            self.ent_desc.delete(0, "end")
            self.refresh_app()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def refresh_app(self):
        # 1. Carregar Salários
        s1, s2 = self.controller.get_configuracoes()
        self.ent_sal_julia.delete(0, "end")
        self.ent_sal_julia.insert(0, str(s1))
        self.ent_sal_davydson.delete(0, "end")
        self.ent_sal_davydson.insert(0, str(s2))

        # 2. Carregar Listas
        df = self.controller.buscar_despesas_mes(self.mes_atual, self.ano_atual)
        
        # Limpar Listas Visuais
        for widget in self.frm_fixas.winfo_children(): widget.destroy()
        for widget in self.frm_variaveis.winfo_children(): widget.destroy()

        if not df.empty:
            for _, row in df.iterrows():
                target = self.frm_fixas if row['tipo'] == "Fixa" else self.frm_variaveis
                self._criar_item_lista(target, row)

        # 3. Gráfico
        self._plotar_grafico(df)

    def _criar_item_lista(self, parent, row):
        f = ctk.CTkFrame(parent, fg_color="#F5F5F5", height=40)
        f.pack(fill="x", pady=2, padx=2)
        
        # Info da despesa
        info_txt = f"{row['data']} | {row['categoria']}\n{row['descricao']}"
        lbl = ctk.CTkLabel(f, text=info_txt, font=("Arial", 10), text_color="black", anchor="w", justify="left")
        lbl.pack(side="left", padx=5, fill="x", expand=True)
        
        # Valor
        val = ctk.CTkLabel(f, text=f"R$ {row['valor']:.2f}", font=("Arial", 11, "bold"), text_color="black")
        val.pack(side="right", padx=5)

        # Botão deletar
        btn = ctk.CTkButton(f, text="×", width=25, height=25, fg_color="#ff5252", 
                            command=lambda: self.deletar(row['id']))
        btn.pack(side="right", padx=2)

    def deletar(self, id_):
        if messagebox.askyesno("Apagar", "Remover este item?"):
            self.controller.excluir_despesa(id_)
            self.refresh_app()

    def _plotar_grafico(self, df):
        for widget in self.frame_grafico.winfo_children(): 
            widget.destroy()
        
        if df.empty: 
            lbl_vazio = ctk.CTkLabel(self.frame_grafico, text="Sem dados para exibir", 
                                     font=("Arial", 12), text_color="gray")
            lbl_vazio.pack(pady=50)
            return

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        fig.patch.set_facecolor(COR_BG_CARDS)
        ax.set_facecolor(COR_BG_CARDS)
        
        dados = df.groupby('categoria')['valor'].sum()
        colors = plt.cm.Set3.colors
        
        wedges, texts, autotexts = ax.pie(
            dados, 
            labels=dados.index, 
            autopct='%1.0f%%',
            startangle=90,
            colors=colors,
            textprops=dict(color="black", fontsize=9)
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')
        
        ax.set_title("", fontsize=10)
        
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def exportar(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if filename:
            try:
                self.controller.exportar_relatorio(self.mes_atual, self.ano_atual, filename)
                messagebox.showinfo("Sucesso", "Relatório exportado!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
