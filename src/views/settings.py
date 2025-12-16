import customtkinter as ctk
from tkinter import messagebox

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, master, controller, callback_atualizar):
        super().__init__(master)
        self.title("Configurar Salários")
        self.geometry("300x250")
        self.controller = controller
        self.callback = callback_atualizar
        
        # Carregar valores atuais
        s1, s2 = self.controller.get_configuracoes()

        ctk.CTkLabel(self, text="Salário Principal (R$):").pack(pady=5)
        self.ent_s1 = ctk.CTkEntry(self)
        self.ent_s1.pack(pady=5)
        self.ent_s1.insert(0, str(s1))

        ctk.CTkLabel(self, text="Renda Extra (R$):").pack(pady=5)
        self.ent_s2 = ctk.CTkEntry(self)
        self.ent_s2.pack(pady=5)
        self.ent_s2.insert(0, str(s2))

        ctk.CTkButton(self, text="Salvar", command=self.salvar).pack(pady=20)

    def salvar(self):
        try:
            s1 = float(self.ent_s1.get().replace(",", "."))
            s2 = float(self.ent_s2.get().replace(",", "."))
            self.controller.salvar_configuracoes(s1, s2)
            self.callback()
            self.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos.")
