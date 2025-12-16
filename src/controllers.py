import sqlite3
import pandas as pd
from datetime import datetime
from src.database import Database
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

class FinanceiroController:
    def __init__(self):
        self.db = Database()

    def adicionar_despesa(self, data: str, tipo: str, categoria: str, descricao: str, valor: float):
        """Adiciona uma despesa de forma segura usando prepared statements."""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO despesas (data, tipo, categoria, descricao, valor) VALUES (?, ?, ?, ?, ?)",
                (data, tipo, categoria, descricao, valor)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao adicionar despesa: {e}")
            raise e

    def excluir_despesa(self, despesa_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM despesas WHERE id = ?", (despesa_id,))
        conn.commit()
        conn.close()

    def buscar_despesas_mes(self, mes: int, ano: int) -> pd.DataFrame:
        """Retorna DataFrame com despesas do mês/ano selecionado."""
        conn = self.db.get_connection()
        # Formato da data no banco é YYYY-MM-DD ou DD/MM/YYYY. 
        # Aqui assumimos input padronizado. Filtramos via SQL é mais eficiente.
        # SQLite não tem tipo DATE nativo forte, faremos filtro no Pandas para flexibilidade
        # ou construímos a query com LIKE. Pela robustez, vamos trazer tudo e filtrar no pandas (escala pequena)
        # ou usar strftime do sqlite.
        
        query = "SELECT * FROM despesas"
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return df

        # Conversão segura de datas
        df['data_dt'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
        df = df[
            (df['data_dt'].dt.month == mes) & 
            (df['data_dt'].dt.year == ano)
        ]
        return df.sort_values(by='data_dt')

    def get_configuracoes(self):
        """Retorna (salario_1, salario_2)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT salario_1, salario_2 FROM configuracoes WHERE id = 1")
        resultado = cursor.fetchone()
        conn.close()
        return resultado if resultado else (0.0, 0.0)

    def salvar_configuracoes(self, sal1: float, sal2: float):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE configuracoes SET salario_1 = ?, salario_2 = ? WHERE id = 1", (sal1, sal2))
        conn.commit()
        conn.close()

    def exportar_relatorio(self, mes: int, ano: int, caminho_arquivo: str):
        """Gera Excel estilizado e profissional."""
        df = self.buscar_despesas_mes(mes, ano)
        salarios = self.get_configuracoes()
        receita_total = sum(salarios)
        total_despesas = df['valor'].sum() if not df.empty else 0.0
        saldo = receita_total - total_despesas

        wb = Workbook()
        ws = wb.active
        ws.title = f"{mes:02d}-{ano}"

        # Cabeçalhos
        headers = ["ID", "Data", "Tipo", "Categoria", "Descrição", "Valor (R$)"]
        ws.append(headers)

        # Estilo Cabeçalho
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
        
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")

        # Dados
        for _, row in df.iterrows():
            ws.append([row['id'], row['data'], row['tipo'], row['categoria'], row['descricao'], row['valor']])

        # Formatação Monetária e Auto-fit
        for row in ws.iter_rows(min_row=2, max_col=6):
            # Coluna de valor é a 6 agora
            row[5].number_format = 'R$ #,##0.00'

        # Resumo no final
        last_row = ws.max_row + 2
        ws.cell(row=last_row, column=5, value="RECEITA TOTAL:").font = Font(bold=True)
        ws.cell(row=last_row, column=6, value=receita_total).number_format = 'R$ #,##0.00'
        
        ws.cell(row=last_row+1, column=5, value="TOTAL DESPESAS:").font = Font(bold=True, color="FF0000")
        ws.cell(row=last_row+1, column=6, value=total_despesas).number_format = 'R$ #,##0.00'

        ws.cell(row=last_row+2, column=5, value="SALDO FINAL:").font = Font(bold=True)
        saldo_cell = ws.cell(row=last_row+2, column=6, value=saldo)
        saldo_cell.number_format = 'R$ #,##0.00'
        
        # Cor condicional no Excel
        if saldo >= 0:
            saldo_cell.font = Font(color="006100", bold=True) # Verde
        else:
            saldo_cell.font = Font(color="9C0006", bold=True) # Vermelho

        # Ajuste de largura das colunas
        for column_cells in ws.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            ws.column_dimensions[column_cells[0].column_letter].width = length + 2

        wb.save(caminho_arquivo)
        print(f"Relatório salvo em: {caminho_arquivo}")
