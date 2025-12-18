import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox, ttk

class FormView(ctk.CTkFrame):
    def __init__(self, master, controller, refresh_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.refresh_callback = refresh_callback # Função para chamar quando algo mudar

        # -- Área de Inserção --
        self.lbl_titulo = ctk.CTkLabel(self, text="Nova Despesa", font=("Arial", 16, "bold"))
        self.lbl_titulo.pack(pady=10)

        self.ent_data = ctk.CTkEntry(self, placeholder_text="DD/MM/YYYY")
        self.ent_data.pack(pady=5, padx=10, fill="x")
        self.ent_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

        self.cmb_categoria = ctk.CTkComboBox(self, values=["Alimentação", "Transporte", "Casa", "Lazer", "Outros"])
        self.cmb_categoria.pack(pady=5, padx=10, fill="x")

        self.ent_descricao = ctk.CTkEntry(self, placeholder_text="Descrição")
        self.ent_descricao.pack(pady=5, padx=10, fill="x")

        self.ent_valor = ctk.CTkEntry(self, placeholder_text="Valor (R$)")
        self.ent_valor.pack(pady=5, padx=10, fill="x")

        self.btn_add = ctk.CTkButton(self, text="Adicionar", command=self.adicionar, fg_color="#1f6aa5")
        self.btn_add.pack(pady=10, padx=10, fill="x")

        # -- Separador --
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)

        # -- Lista Recente (Simplificada) --
        self.lbl_lista = ctk.CTkLabel(self, text="Histórico do Mês", font=("Arial", 14, "bold"))
        self.lbl_lista.pack(pady=5)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=200)
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def adicionar(self):
        try:
            data = self.ent_data.get()
            cat = self.cmb_categoria.get()
            desc = self.ent_descricao.get()
            valor_str = self.ent_valor.get().replace(",", ".") # Aceitar vírgula
            
            if not valor_str: raise ValueError("Valor vazio")
            valor = float(valor_str)

            # FormView não possui seleção de tipo/recorrência — cadastrar como 'Variável' sem recorrência
            self.controller.adicionar_despesa(data, "Variável", cat, desc, valor, 0)
            
            # Limpar campos e atualizar
            self.ent_descricao.delete(0, "end")
            self.ent_valor.delete(0, "end")
            self.refresh_callback() # Atualiza Dashboard e Lista
            
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido! Use números.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_lista(self, mes, ano):
        # Limpar lista atual
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        df = self.controller.buscar_despesas_mes(mes, ano)
        if df.empty:
            return

        for _, row in df.iterrows():
            f = ctk.CTkFrame(self.scroll_frame, fg_color="#3a3a3a")
            f.pack(fill="x", pady=2)
            
            txt = f"{row['data']} - {row['categoria']}\n{row['descricao']} - R$ {row['valor']:.2f}"
            lbl = ctk.CTkLabel(f, text=txt, anchor="w", justify="left")
            lbl.pack(side="left", padx=5)
            
            btn_del = ctk.CTkButton(f, text="X", width=30, fg_color="#c0392b", 
                                    command=lambda pid=row['id']: self.deletar(pid))
            btn_del.pack(side="right", padx=5)

    def deletar(self, id_despesa):
        if messagebox.askyesno("Confirmar", "Deletar despesa?"):
            self.controller.excluir_despesa(id_despesa)
            self.refresh_callback()
