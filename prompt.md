# Role (Papel)
Atue como um Arquiteto de Software Sênior e Especialista em Python. Sua missão é desenvolver um "Sistema de Gestão Financeira Pessoal" (Desktop) completo, robusto, escalável e com código limpo (Clean Code).

# Context & Goal (Contexto e Objetivo)
Preciso de uma aplicação desktop local para controlar despesas pessoais. O sistema deve ser simples de usar, mas com engenharia robusta por trás. O foco é visualizar o saldo mensal baseado em salários fixos (globais) e despesas variáveis, com capacidade de exportação formatada para Excel.

# Tech Stack (Tecnologias Obrigatórias)
1.  **Linguagem:** Python 3.10+.
2.  **Interface Gráfica (GUI):** `customtkinter` (para visual moderno/Dark Mode).
3.  **Banco de Dados:** `sqlite3` nativo (com padrão Singleton para conexão).
4.  **Manipulação de Dados:** `pandas` (para DataFrames) e `openpyxl` (para estilização do Excel).
5.  **Visualização:** `matplotlib` (integrado ao CustomTkinter via `FigureCanvasTkAgg`).

# Architecture & File Structure (Arquitetura MVC)
Não crie um único arquivo gigante. Organize o código em módulos claros:
* `main.py`: Ponto de entrada da aplicação.
* `database.py`: Gerenciamento de conexão e criação de tabelas.
* `models/`: Classes de dados (Ex: `Expense`, `Settings` para os salários).
* `controllers/`: Lógica de negócios (Cálculos de saldo, CRUD de despesas).
* `views/`: Interface gráfica (Dividida em componentes: `Sidebar`, `Dashboard`, `ExpenseForm`).

# Functional Requirements (Requisitos Funcionais)

### 1. Gestão de Salários (Global)
* O sistema deve ter uma tabela no banco de dados chamada `settings` para armazenar o "Salário 1" e "Salário 2".
* Crie um botão de "Configurações" ou ícone de engrenagem na interface para editar esses valores.
* Esses valores são globais: o cálculo do saldo mensal será sempre: `(Salário 1 + Salário 2) - Total Despesas do Mês Selecionado`.

### 2. Navegação Temporal
* Barra superior com Dropdowns para selecionar **Mês** e **Ano**.
* Ao trocar a data, a Dashboard, a Lista de Despesas e os Gráficos devem atualizar imediatamente (Observer Pattern ou Callback simples).

### 3. Gestão de Despesas (CRUD)
* Formulário para adicionar despesa: Valor (R$), Data (padrão hoje, mas editável), Categoria (Dropdown: Alimentação, Transporte, Casa, Lazer, Outros) e Descrição.
* Lista de despesas (Treeview ou ScrollableFrame) mostrando itens do mês selecionado, ordenada por data. Permite excluir itens.

### 4. Dashboard (Visualização)
* **KPIs (Cards):** Mostre 3 cartões grandes:
    1.  Receita Total (Soma dos Salários Globais).
    2.  Despesas do Mês (Soma das despesas filtradas).
    3.  Saldo Restante (Receita - Despesas). Cor verde se positivo, vermelho se negativo.
* **Gráfico:** Um "Donut Chart" (Rosca) do Matplotlib mostrando a distribuição de gastos por Categoria. Fundo do gráfico deve combinar com o tema escuro do CustomTkinter.

### 5. Exportação Excel (Relatórios)
* Botão "Exportar Relatório".
* Gere um arquivo `.xlsx` usando `openpyxl`.
* **Requisito de Design do Excel:** O arquivo NÃO pode ser cru. Deve ter:
    * Cabeçalho em Negrito com fundo colorido.
    * Colunas com largura ajustada (Auto-fit).
    * Coluna de "Valor" formatada como Moeda Brasileira (R$).
    * Soma total no final da planilha.

# Deliverables (Entregáveis)
1.  Forneça o código completo de todos os arquivos, separado por blocos de código com o nome do arquivo no topo.
2.  Inclua um arquivo `requirements.txt`.
3.  Inclua um breve guia de como rodar a aplicação.
4.  O código deve ter tratamento de erros (Try/Except) para operações de banco de dados e entradas inválidas (ex: digitar letras no campo valor).
5.  Todo o código (variáveis, funções, comentários) deve estar em **Português**.

Comece planejando a estrutura de pastas e depois forneça o código.