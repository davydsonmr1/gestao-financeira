import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox, filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.controllers import FinanceiroController

# Configuração Visual Global
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Paleta de Cores Moderna e Clean
COR_PRIMARY = "#5B7FFF"        # Azul principal
COR_SECONDARY = "#E8EEFF"      # Azul bem claro
COR_SUCCESS = "#10B981"        # Verde
COR_DANGER = "#EF4444"         # Vermelho
COR_WARNING = "#F59E0B"        # Laranja
COR_BG_LIGHT = "#F8F9FA"       # Fundo claro
COR_BG_WHITE = "#FFFFFF"       # Branco
COR_TEXT_DARK = "#1F2937"      # Texto escuro
COR_TEXT_GRAY = "#6B7280"      # Texto cinza
COR_BORDER = "#E5E7EB"         # Borda suave

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("💰 Davydson Finanças")
        self.geometry("1400x800")
        self.configure(fg_color=COR_BG_LIGHT)
        self.controller = FinanceiroController()
        
        # Estado
        hoje = datetime.now()
        self.mes_atual = hoje.month
        self.ano_atual = hoje.year

        # Layout Principal
        self._setup_ui()
        self.carregar_categorias()
        self.refresh_app()

    def _setup_ui(self):
        # Grid Mestre
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # === HEADER SUPERIOR ===
        self._criar_header()

        # === ÁREA DE CONTEÚDO (3 COLUNAS) ===
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=1, column=0, sticky="nsew", padx=25, pady=25)
        
        self.main_area.grid_columnconfigure(0, weight=1, minsize=350) 
        self.main_area.grid_columnconfigure(1, weight=2) 
        self.main_area.grid_columnconfigure(2, weight=1, minsize=400)
        self.main_area.grid_rowconfigure(0, weight=1)

        self._setup_col_esquerda()
        self._setup_col_central()
        self._setup_col_direita()
    
    def _criar_header(self):
        header = ctk.CTkFrame(self, height=140, fg_color=COR_BG_WHITE, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        
        # Container interno
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Lado Esquerdo - Título e Subtítulo
        left_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        left_frame.pack(side="left", fill="y")
        
        title_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        title_frame.pack(anchor="w")
        
        ctk.CTkLabel(title_frame, text="💰", font=("Segoe UI", 32)).pack(side="left", padx=(0, 10))
        
        text_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        text_frame.pack(side="left")
        
        ctk.CTkLabel(text_frame, text="Davydson Finanças", 
                     font=("Segoe UI", 28, "bold"), text_color=COR_TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(text_frame, text="Controle Financeiro Pessoal", 
                     font=("Segoe UI", 13), text_color=COR_TEXT_GRAY).pack(anchor="w")
        
        # Lado Direito - KPIs e Navegação
        right_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=(20, 0))
        
        # Seletor de período
        nav_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        nav_frame.pack(side="top", pady=(0, 15))
        
        ctk.CTkLabel(nav_frame, text="📅 Período:", font=("Segoe UI", 11, "bold"), 
                     text_color=COR_TEXT_GRAY).pack(side="left", padx=(0, 8))
        
        self.cmb_mes = ctk.CTkComboBox(nav_frame, values=[str(i) for i in range(1, 13)], 
                                       width=60, height=32, command=self._refresh_trigger,
                                       button_color=COR_PRIMARY, border_color=COR_BORDER,
                                       dropdown_fg_color=COR_BG_WHITE)
        self.cmb_mes.set(str(self.mes_atual))
        self.cmb_mes.pack(side="left", padx=3)
        
        self.cmb_ano = ctk.CTkComboBox(nav_frame, values=[str(i) for i in range(2023, 2031)], 
                                       width=75, height=32, command=self._refresh_trigger,
                                       button_color=COR_PRIMARY, border_color=COR_BORDER,
                                       dropdown_fg_color=COR_BG_WHITE)
        self.cmb_ano.set(str(self.ano_atual))
        self.cmb_ano.pack(side="left", padx=3)
        
        # KPIs Cards
        kpis_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        kpis_frame.pack(side="top")
        
        self.card_receita = self._criar_kpi_mini(kpis_frame, "Receitas", "R$ 0,00", COR_SUCCESS, 0)
        self.card_despesas = self._criar_kpi_mini(kpis_frame, "Despesas", "R$ 0,00", COR_DANGER, 1)
        self.card_saldo = self._criar_kpi_mini(kpis_frame, "Saldo", "R$ 0,00", COR_PRIMARY, 2)
    
    def _criar_kpi_mini(self, parent, titulo, valor, cor, col):
        card = ctk.CTkFrame(parent, fg_color=COR_BG_LIGHT, corner_radius=12, 
                           width=140, height=65)
        card.grid(row=0, column=col, padx=4)
        card.grid_propagate(False)
        
        ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 10), 
                     text_color=COR_TEXT_GRAY).pack(pady=(10, 2))
        lbl_valor = ctk.CTkLabel(card, text=valor, font=("Segoe UI", 18, "bold"), 
                                 text_color=cor)
        lbl_valor.pack()
        
        card.lbl_valor = lbl_valor
        return card

    def _setup_col_esquerda(self):
        frm = ctk.CTkScrollableFrame(self.main_area, fg_color=COR_BG_WHITE, 
                                     corner_radius=15, border_width=0)
        frm.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        
        # Container com padding
        container = ctk.CTkFrame(frm, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # === SALÁRIOS ===
        ctk.CTkLabel(container, text="💼 Salários Mensais", 
                     font=("Segoe UI", 18, "bold"), text_color=COR_TEXT_DARK).pack(anchor="w", pady=(0, 15))
        
        # Julia
        sal_frame1 = ctk.CTkFrame(container, fg_color=COR_BG_LIGHT, corner_radius=10)
        sal_frame1.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(sal_frame1, text="👤 Julia", font=("Segoe UI", 11, "bold"), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w", padx=12, pady=(10, 2))
        self.ent_sal_julia = ctk.CTkEntry(sal_frame1, placeholder_text="R$ 0,00", height=38,
                                          border_color=COR_BORDER, fg_color=COR_BG_WHITE)
        self.ent_sal_julia.pack(fill="x", padx=12, pady=(0, 10))
        
        # Davydson
        sal_frame2 = ctk.CTkFrame(container, fg_color=COR_BG_LIGHT, corner_radius=10)
        sal_frame2.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(sal_frame2, text="👤 Davydson", font=("Segoe UI", 11, "bold"), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w", padx=12, pady=(10, 2))
        self.ent_sal_davydson = ctk.CTkEntry(sal_frame2, placeholder_text="R$ 0,00", height=38,
                                             border_color=COR_BORDER, fg_color=COR_BG_WHITE)
        self.ent_sal_davydson.pack(fill="x", padx=12, pady=(0, 10))

        # Botão salvar
        ctk.CTkButton(container, text="💾 Salvar Salários", height=35, 
                      fg_color=COR_TEXT_GRAY, hover_color="#4B5563",
                      corner_radius=10, font=("Segoe UI", 12, "bold"),
                      command=self.salvar_salarios).pack(fill="x", pady=(0, 25))

        # Separador visual
        ctk.CTkFrame(container, height=2, fg_color=COR_BORDER).pack(fill="x", pady=15)

        # === DINHEIRO EXTRA ===
        ctk.CTkLabel(container, text="💵 Dinheiro Extra", 
                     font=("Segoe UI", 18, "bold"), text_color=COR_TEXT_DARK).pack(anchor="w", pady=(0, 15))
        
        extra_frame = ctk.CTkFrame(container, fg_color=COR_BG_LIGHT, corner_radius=10)
        extra_frame.pack(fill="x", pady=(0, 10))
        
        # Container interno
        extra_content = ctk.CTkFrame(extra_frame, fg_color="transparent")
        extra_content.pack(fill="x", padx=12, pady=10)
        
        # Período
        periodo_frame = ctk.CTkFrame(extra_content, fg_color="transparent")
        periodo_frame.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(periodo_frame, text="📅 Período:", font=("Segoe UI", 10), 
                     text_color=COR_TEXT_GRAY).pack(side="left", padx=(0, 5))
        
        self.cmb_extra_mes = ctk.CTkComboBox(periodo_frame, values=[str(i) for i in range(1, 13)], 
                                             width=60, height=32, button_color=COR_PRIMARY)
        self.cmb_extra_mes.set(str(datetime.now().month))
        self.cmb_extra_mes.pack(side="left", padx=3)
        
        self.cmb_extra_ano = ctk.CTkComboBox(periodo_frame, values=[str(i) for i in range(2023, 2031)], 
                                             width=75, height=32, button_color=COR_PRIMARY)
        self.cmb_extra_ano.set(str(datetime.now().year))
        self.cmb_extra_ano.pack(side="left", padx=3)
        
        # Descrição
        ctk.CTkLabel(extra_content, text="📝 Descrição", font=("Segoe UI", 10), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w", pady=(0, 3))
        self.ent_extra_desc = ctk.CTkEntry(extra_content, placeholder_text="Ex: Bônus, Freela", 
                                           height=32, border_color=COR_BORDER, fg_color=COR_BG_WHITE)
        self.ent_extra_desc.pack(fill="x", pady=(0, 8))
        
        # Valor
        ctk.CTkLabel(extra_content, text="💰 Valor", font=("Segoe UI", 10), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w", pady=(0, 3))
        self.ent_extra_valor = ctk.CTkEntry(extra_content, placeholder_text="R$ 0,00", 
                                            height=32, border_color=COR_BORDER, fg_color=COR_BG_WHITE)
        self.ent_extra_valor.pack(fill="x", pady=(0, 8))
        
        # Botão adicionar
        ctk.CTkButton(extra_content, text="➕ Adicionar Extra", height=32, 
                      fg_color=COR_SUCCESS, hover_color="#059669",
                      corner_radius=8, font=("Segoe UI", 11, "bold"),
                      command=self.adicionar_receita_extra).pack(fill="x")
        
        # Separador
        ctk.CTkFrame(container, height=2, fg_color=COR_BORDER).pack(fill="x", pady=15)

        # === NOVA DESPESA ===
        ctk.CTkLabel(container, text="➕ Nova Despesa", 
                     font=("Segoe UI", 18, "bold"), text_color=COR_TEXT_DARK).pack(anchor="w", pady=(0, 15))
        
        # Recorrência
        ctk.CTkLabel(container, text="🔄 Recorrência", font=("Segoe UI", 11, "bold"), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w", pady=(0, 5))
        self.cmb_tipo = ctk.CTkComboBox(container, 
                                        values=["Fixa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
                                        height=38, button_color=COR_PRIMARY, border_color=COR_BORDER,
                                        dropdown_fg_color=COR_BG_WHITE)
        self.cmb_tipo.set("1")
        self.cmb_tipo.pack(fill="x", pady=(0, 12))

        # Data
        ctk.CTkLabel(container, text="📅 Data", font=("Segoe UI", 11, "bold"), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w", pady=(0, 5))
        self.ent_data = ctk.CTkEntry(container, placeholder_text="MM/AA", height=38,
                                     border_color=COR_BORDER, fg_color=COR_BG_WHITE)
        self.ent_data.insert(0, datetime.now().strftime("%m/%y"))
        self.ent_data.pack(fill="x", pady=(0, 12))

        # Categoria
        ctk.CTkLabel(container, text="📁 Categoria", font=("Segoe UI", 11, "bold"), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w", pady=(0, 5))
        self.cmb_cat = ctk.CTkComboBox(container, 
                                       values=["Carregando..."],
                                       height=38, button_color=COR_PRIMARY, border_color=COR_BORDER,
                                       dropdown_fg_color=COR_BG_WHITE)
        self.cmb_cat.pack(fill="x", pady=(0, 12))

        # Valor
        ctk.CTkLabel(container, text="💵 Valor", font=("Segoe UI", 11, "bold"), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w", pady=(0, 5))
        self.ent_val = ctk.CTkEntry(container, placeholder_text="R$ 0,00", height=38,
                                    border_color=COR_BORDER, fg_color=COR_BG_WHITE)
        self.ent_val.pack(fill="x", pady=(0, 12))
        
        # Descrição
        ctk.CTkLabel(container, text="📝 Descrição", font=("Segoe UI", 11, "bold"), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w", pady=(0, 5))
        self.ent_desc = ctk.CTkEntry(container, placeholder_text="Ex: Supermercado", height=38,
                                     border_color=COR_BORDER, fg_color=COR_BG_WHITE)
        self.ent_desc.pack(fill="x", pady=(0, 20))

        # Botão Adicionar - DESTAQUE
        ctk.CTkButton(container, text="✅ Adicionar Despesa", height=45, 
                      fg_color=COR_PRIMARY, hover_color="#4A6FE8",
                      corner_radius=12, font=("Segoe UI", 14, "bold"),
                      command=self.adicionar_despesa).pack(fill="x")

    def _setup_col_central(self):
        frm = ctk.CTkFrame(self.main_area, fg_color="transparent")
        frm.grid(row=0, column=1, sticky="nsew", padx=12)
        frm.grid_columnconfigure(0, weight=1)
        frm.grid_columnconfigure(1, weight=1)
        frm.grid_rowconfigure(0, weight=1)

        self.frm_fixas = self._criar_lista_container(frm, "📌 Despesas Fixas", 0, 0)
        self.frm_variaveis = self._criar_lista_container(frm, "💸 Despesas Variáveis", 0, 1)

    def _criar_lista_container(self, parent, titulo, row, col):
        frame = ctk.CTkFrame(parent, fg_color=COR_BG_WHITE, corner_radius=15, border_width=0)
        frame.grid(row=row, column=col, sticky="nsew", padx=6)
        
        # Header da lista
        header = ctk.CTkFrame(frame, fg_color=COR_SECONDARY, corner_radius=12, height=50)
        header.pack(fill="x", padx=15, pady=15)
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text=titulo, font=("Segoe UI", 15, "bold"), 
                     text_color=COR_PRIMARY).pack(expand=True)
        
        # Área scrollável
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent", border_width=0)
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        return scroll

    def _setup_col_direita(self):
        frm = ctk.CTkFrame(self.main_area, fg_color=COR_BG_WHITE, corner_radius=15, border_width=0)
        frm.grid(row=0, column=2, sticky="nsew", padx=(12, 0))
        
        # Header
        header = ctk.CTkFrame(frm, fg_color=COR_SECONDARY, corner_radius=12, height=50)
        header.pack(fill="x", padx=15, pady=15)
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text="📊 Análise por Categoria", font=("Segoe UI", 15, "bold"), 
                     text_color=COR_PRIMARY).pack(expand=True)
        
        # Gráfico
        self.frame_grafico = ctk.CTkFrame(frm, fg_color="transparent")
        self.frame_grafico.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Botão gerenciar categorias
        ctk.CTkButton(frm, text="🏷️ Gerenciar Categorias", height=42, 
                      fg_color=COR_PRIMARY, hover_color="#4A6FEE",
                      corner_radius=12, font=("Segoe UI", 13, "bold"),
                      command=self.abrir_gerenciar_categorias).pack(fill="x", padx=15, pady=(0, 10))
        
        # Botão exportar
        ctk.CTkButton(frm, text="📥 Exportar para Excel", height=42, 
                      fg_color=COR_SUCCESS, hover_color="#059669",
                      corner_radius=12, font=("Segoe UI", 13, "bold"),
                      command=self.exportar).pack(fill="x", padx=15, pady=(0, 15))

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
    
    def adicionar_receita_extra(self):
        try:
            mes = int(self.cmb_extra_mes.get())
            ano = int(self.cmb_extra_ano.get())
            descricao = self.ent_extra_desc.get()
            valor = float(self.ent_extra_valor.get().replace(",", "."))
            
            if not descricao:
                descricao = "Extra"
            
            self.controller.adicionar_receita_extra(mes, ano, descricao, valor)
            
            # Limpar campos
            self.ent_extra_desc.delete(0, "end")
            self.ent_extra_valor.delete(0, "end")
            
            # Atualizar se for o mês atual
            if mes == self.mes_atual and ano == self.ano_atual:
                self.refresh_app()
            
            messagebox.showinfo("Sucesso", f"Receita extra adicionada para {mes:02d}/{ano}!")
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def adicionar_despesa(self):
        try:
            valor = float(self.ent_val.get().replace(",", "."))
            tipo_selecionado = self.cmb_tipo.get()
            
            # Determinar tipo e recorrência
            if tipo_selecionado == "Fixa":
                tipo = "Fixa"
                recorrencia = 12  # Fixas se repetem por 12 meses
            else:
                tipo = "Variável"
                recorrencia = int(tipo_selecionado)  # Número de meses
            
            self.controller.adicionar_despesa(
                self.ent_data.get(),
                tipo,
                self.cmb_cat.get(),
                self.ent_desc.get(),
                valor,
                recorrencia
            )
            # Limpar
            self.ent_val.delete(0, "end")
            self.ent_desc.delete(0, "end")
            self.refresh_app()
            messagebox.showinfo("Sucesso", f"Despesa adicionada para {recorrencia} mês(es)!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def refresh_app(self):
        # 1. Carregar Salários
        s1, s2 = self.controller.get_configuracoes()
        self.ent_sal_julia.delete(0, "end")
        self.ent_sal_julia.insert(0, str(s1))
        self.ent_sal_davydson.delete(0, "end")
        self.ent_sal_davydson.insert(0, str(s2))

        # 2. Atualizar KPIs (Receita, Despesas, Saldo)
        receita, despesas, saldo = self.controller.calcular_totais_mes(self.mes_atual, self.ano_atual)
        
        self.card_receita.lbl_valor.configure(text=f"R$ {receita:,.2f}")
        self.card_despesas.lbl_valor.configure(text=f"R$ {despesas:,.2f}")
        
        cor_saldo = "#4CAF50" if saldo >= 0 else "#FF5252"
        self.card_saldo.lbl_valor.configure(text=f"R$ {saldo:,.2f}", text_color=cor_saldo)

        # 3. Carregar Listas
        df = self.controller.buscar_despesas_mes(self.mes_atual, self.ano_atual)
        
        # Limpar Listas Visuais
        for widget in self.frm_fixas.winfo_children(): widget.destroy()
        for widget in self.frm_variaveis.winfo_children(): widget.destroy()

        if not df.empty:
            for _, row in df.iterrows():
                target = self.frm_fixas if row['tipo'] == "Fixa" else self.frm_variaveis
                self._criar_item_lista(target, row)

        # 4. Gráfico
        self._plotar_grafico(df)

    def _criar_item_lista(self, parent, row):
        f = ctk.CTkFrame(parent, fg_color=COR_BG_LIGHT, corner_radius=10, height=70)
        f.pack(fill="x", pady=5, padx=5)
        f.pack_propagate(False)
        
        # Container interno
        content = ctk.CTkFrame(f, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=12, pady=10)
        
        # Lado esquerdo - Info
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)
        
        # Categoria e descrição
        categoria_limpa = row['categoria'].replace("🍔 ", "").replace("🚗 ", "").replace("🏠 ", "").replace("🎮 ", "").replace("📦 ", "")
        titulo = f"📁 {categoria_limpa}"
        ctk.CTkLabel(left, text=titulo, font=("Segoe UI", 11, "bold"), 
                     text_color=COR_TEXT_DARK, anchor="w").pack(anchor="w")
        
        subtexto = f"📅 {row['data']}  •  {row['descricao'][:30]}"
        ctk.CTkLabel(left, text=subtexto, font=("Segoe UI", 10), 
                     text_color=COR_TEXT_GRAY, anchor="w").pack(anchor="w")
        
        # Lado direito - Valor e botão
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.pack(side="right", fill="y")
        
        valor_frame = ctk.CTkFrame(right, fg_color="transparent")
        valor_frame.pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(valor_frame, text=f"R$ {row['valor']:.2f}", 
                     font=("Segoe UI", 14, "bold"), text_color=COR_DANGER).pack()
        
        # Botão deletar moderno
        btn = ctk.CTkButton(right, text="🗑️", width=35, height=35, 
                           fg_color=COR_DANGER, hover_color="#DC2626",
                           corner_radius=8, font=("Segoe UI", 14),
                           command=lambda: self.deletar(row['id']))
        btn.pack()

    def deletar(self, id_):
        if messagebox.askyesno("Confirmar Exclusão", "Deseja remover esta despesa?"):
            self.controller.excluir_despesa(id_)
            self.refresh_app()

    def _plotar_grafico(self, df):
        for widget in self.frame_grafico.winfo_children(): 
            widget.destroy()
        
        if df.empty: 
            # Mensagem quando não há dados
            empty_frame = ctk.CTkFrame(self.frame_grafico, fg_color=COR_BG_LIGHT, corner_radius=12)
            empty_frame.pack(fill="both", expand=True, padx=20, pady=40)
            
            ctk.CTkLabel(empty_frame, text="📊", font=("Segoe UI", 48)).pack(pady=(30, 10))
            ctk.CTkLabel(empty_frame, text="Sem despesas neste mês", 
                        font=("Segoe UI", 14, "bold"), text_color=COR_TEXT_GRAY).pack()
            ctk.CTkLabel(empty_frame, text="Adicione despesas para ver a análise", 
                        font=("Segoe UI", 11), text_color=COR_TEXT_GRAY).pack(pady=(5, 30))
            return

        # Criar gráfico moderno
        fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        
        # Remover emojis das categorias para o gráfico
        dados = df.copy()
        dados['categoria'] = dados['categoria'].str.replace("🍔 ", "").str.replace("🚗 ", "").str.replace("🏠 ", "").str.replace("🎮 ", "").str.replace("📦 ", "")
        dados_cat = dados.groupby('categoria')['valor'].sum()
        
        # Cores modernas
        colors = ['#5B7FFF', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
        
        wedges, texts, autotexts = ax.pie(
            dados_cat, 
            labels=dados_cat.index, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(dados_cat)],
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
            textprops=dict(color='black', fontsize=10, weight='bold')
        )
        
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_weight('bold')
            autotext.set_fontsize(11)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def exportar(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if filename:
            try:
                self.controller.exportar_relatorio(self.mes_atual, self.ano_atual, filename)
                messagebox.showinfo("✅ Sucesso", "Relatório exportado com sucesso!")
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Falha ao exportar: {e}")    
    def abrir_gerenciar_categorias(self):
        """Abre janela modal para gerenciar categorias"""
        modal = ctk.CTkToplevel(self)
        modal.title("🏷️ Gerenciar Categorias")
        modal.geometry("600x500")
        modal.configure(fg_color=COR_BG_LIGHT)
        modal.transient(self)
        modal.grab_set()
        
        # Container principal
        container = ctk.CTkFrame(modal, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(container, text="🏷️ Minhas Categorias", 
                     font=("Segoe UI", 22, "bold"), text_color=COR_TEXT_DARK).pack(pady=(0, 20))
        
        # Frame para adicionar nova categoria
        add_frame = ctk.CTkFrame(container, fg_color=COR_BG_WHITE, corner_radius=12)
        add_frame.pack(fill="x", pady=(0, 15))
        
        add_content = ctk.CTkFrame(add_frame, fg_color="transparent")
        add_content.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(add_content, text="➕ Nova Categoria", 
                     font=("Segoe UI", 14, "bold"), text_color=COR_TEXT_DARK).pack(anchor="w", pady=(0, 10))
        
        # Nome e Ícone lado a lado
        input_frame = ctk.CTkFrame(add_content, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 10))
        
        # Dropdown de ícones
        icones_disponiveis = [
            "🍔", "🍕", "🍜", "🥗", "🍱", "☕", "🛒",  # Alimentação
            "🚗", "🚕", "🚌", "🚇", "✈️", "🚲", "⛽",  # Transporte
            "🏠", "🏡", "🏢", "🔑", "🛋️", "🚰", "💡",  # Casa
            "🎮", "🎬", "🎵", "📚", "🎨", "🏋️", "⚽",  # Lazer
            "💊", "🏥", "💉", "🩺", "🦷",              # Saúde
            "📱", "💻", "🖥️", "⌚", "📷", "🎧",        # Tecnologia
            "👕", "👗", "👠", "👜", "💄",              # Vestuário
            "🎓", "📖", "✏️", "🎒",                    # Educação
            "💰", "💳", "🏦", "💸", "📊",              # Financeiro
            "🎁", "🎉", "🎂", "💐",                    # Presentes/Eventos
            "🐕", "🐈", "🐾",                          # Pets
            "📦", "🔧", "⚙️", "🔨", "📍"              # Outros
        ]
        
        left_inputs = ctk.CTkFrame(input_frame, fg_color="transparent")
        left_inputs.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(left_inputs, text="Nome:", font=("Segoe UI", 11), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w")
        ent_nome = ctk.CTkEntry(left_inputs, placeholder_text="Ex: Academia", 
                                height=35, border_color=COR_BORDER)
        ent_nome.pack(fill="x", pady=(3, 0))
        
        right_inputs = ctk.CTkFrame(input_frame, fg_color="transparent")
        right_inputs.pack(side="left", fill="x", padx=(10, 0))
        
        ctk.CTkLabel(right_inputs, text="Ícone:", font=("Segoe UI", 11), 
                     text_color=COR_TEXT_GRAY).pack(anchor="w")
        cmb_icone = ctk.CTkComboBox(right_inputs, values=icones_disponiveis, 
                                     width=80, height=35, button_color=COR_PRIMARY)
        cmb_icone.set(icones_disponiveis[0])
        cmb_icone.pack(pady=(3, 0))
        
        def adicionar_cat():
            nome = ent_nome.get().strip()
            icone = cmb_icone.get()
            if not nome:
                messagebox.showerror("Erro", "Digite um nome para a categoria!")
                return
            try:
                self.controller.adicionar_categoria(nome, icone)
                ent_nome.delete(0, "end")
                self.carregar_categorias()
                atualizar_lista()
                messagebox.showinfo("Sucesso", f"Categoria '{nome}' adicionada!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        
        ctk.CTkButton(add_content, text="➕ Adicionar Categoria", height=35,
                      fg_color=COR_SUCCESS, hover_color="#059669",
                      command=adicionar_cat).pack(fill="x")
        
        # Lista de categorias existentes
        list_frame = ctk.CTkFrame(container, fg_color=COR_BG_WHITE, corner_radius=12)
        list_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(list_frame, text="📋 Categorias Existentes", 
                     font=("Segoe UI", 14, "bold"), text_color=COR_TEXT_DARK).pack(pady=(15, 10))
        
        scroll_frame = ctk.CTkScrollableFrame(list_frame, fg_color="transparent", height=200)
        scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        def atualizar_lista():
            for widget in scroll_frame.winfo_children():
                widget.destroy()
            
            categorias_df = self.controller.buscar_categorias()
            if categorias_df.empty:
                ctk.CTkLabel(scroll_frame, text="Nenhuma categoria cadastrada", 
                             text_color=COR_TEXT_GRAY).pack(pady=20)
                return
            
            for _, row in categorias_df.iterrows():
                cat_item = ctk.CTkFrame(scroll_frame, fg_color=COR_BG_LIGHT, corner_radius=8)
                cat_item.pack(fill="x", pady=3)
                
                ctk.CTkLabel(cat_item, text=f"{row['icone']} {row['nome']}", 
                             font=("Segoe UI", 12), text_color=COR_TEXT_DARK).pack(side="left", padx=15, pady=10)
                
                def excluir_cat(nome=row['nome']):
                    if messagebox.askyesno("Confirmar", f"Excluir categoria '{nome}'?"):
                        try:
                            self.controller.excluir_categoria(nome)
                            self.carregar_categorias()
                            atualizar_lista()
                            messagebox.showinfo("Sucesso", "Categoria excluída!")
                        except Exception as e:
                            messagebox.showerror("Erro", str(e))
                
                ctk.CTkButton(cat_item, text="🗑️", width=40, height=30, 
                              fg_color=COR_DANGER, hover_color="#DC2626",
                              command=excluir_cat).pack(side="right", padx=10)
        
        atualizar_lista()

    def carregar_categorias(self):
        """Atualiza o dropdown de categorias com as do banco de dados"""
        try:
            categorias_df = self.controller.buscar_categorias()
            if not categorias_df.empty:
                categorias_lista = [f"{row['icone']} {row['nome']}" for _, row in categorias_df.iterrows()]
                self.cmb_cat.configure(values=categorias_lista)
        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
if __name__ == "__main__":
    app = App()
    app.mainloop()
