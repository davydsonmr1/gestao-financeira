# Sistema de Gestão Financeira Pessoal 💰

Sistema desktop completo para controle de despesas pessoais, desenvolvido com Python e CustomTkinter.

## 📋 Características

- **Interface Moderna**: Dark mode com CustomTkinter
- **Dashboard Visual**: Gráficos de pizza (donut chart) para visualização de gastos por categoria
- **KPIs em Tempo Real**: Acompanhe receitas, despesas e saldo instantaneamente
- **Gestão de Despesas**: CRUD completo com categorização
- **Navegação Temporal**: Filtragem por mês e ano
- **Relatórios Excel**: Exportação estilizada com formatação profissional
- **Banco de Dados Local**: SQLite com padrão Singleton

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **customtkinter** - Interface gráfica moderna
- **pandas** - Manipulação de dados
- **matplotlib** - Visualização de gráficos
- **openpyxl** - Exportação Excel estilizada
- **sqlite3** - Banco de dados local

## 📁 Estrutura do Projeto

```
gestao_financeira/
├── data/                   # Banco de dados SQLite
├── src/
│   ├── database.py         # Gerenciamento de conexão (Singleton)
│   ├── controllers.py      # Lógica de negócios
│   └── views/              # Interface gráfica
│       ├── dashboard.py    # Gráficos e KPIs
│       ├── forms.py        # Formulários de despesas
│       └── settings.py     # Configurações de salários
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências
└── README.md
```

## ⚙️ Instalação e Configuração

### 1. Clone ou baixe o projeto

```bash
cd gestao_financeira
```

### 2. Crie um ambiente virtual

```powershell
# Windows PowerShell
python -m venv venv
```

### 3. Ative o ambiente virtual

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Se houver erro de política de execução, execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Instale as dependências

```powershell
pip install -r requirements.txt
```

### 5. Execute a aplicação

```powershell
python main.py
```

## 📖 Como Usar

### Configuração Inicial

1. **Configure os Salários**:
   - Clique no botão "Configurar Salários" na sidebar
   - Insira o Salário Principal e a Renda Extra
   - Clique em "Salvar"

### Adicionar Despesas

1. Preencha o formulário na sidebar:
   - **Data**: Formato DD/MM/YYYY (padrão: hoje)
   - **Categoria**: Alimentação, Transporte, Casa, Lazer ou Outros
   - **Descrição**: Descrição da despesa
   - **Valor**: Valor em R$ (aceita vírgula ou ponto)
2. Clique em "Adicionar"

### Visualizar Dados

- **Dashboard**: Mostra 3 KPIs principais (Receita, Despesas, Saldo)
- **Gráfico**: Donut chart com distribuição de gastos por categoria
- **Histórico**: Lista de despesas do mês na sidebar

### Navegação

- Use os dropdowns de **Mês** e **Ano** no topo da sidebar
- A interface atualiza automaticamente ao trocar o período

### Excluir Despesas

- Clique no botão "X" ao lado de cada despesa no histórico
- Confirme a exclusão

### Exportar Relatório

1. Clique em "Exportar Excel"
2. Escolha o local e nome do arquivo
3. O relatório incluirá:
   - Lista completa de despesas do mês
   - Formatação profissional com cabeçalhos coloridos
   - Valores em formato de moeda brasileira (R$)
   - Resumo financeiro (Receita, Despesas, Saldo)
   - Cores condicionais (verde para saldo positivo, vermelho para negativo)

## 🎨 Funcionalidades Principais

### Dashboard Interativo

- **Card de Receita**: Soma dos salários configurados (verde)
- **Card de Despesas**: Total de gastos do mês (vermelho)
- **Card de Saldo**: Diferença entre receita e despesas (verde/vermelho)
- **Gráfico Donut**: Visualização por categoria com percentuais

### Categorias Disponíveis

- 🍔 Alimentação
- 🚗 Transporte
- 🏠 Casa
- 🎮 Lazer
- 📦 Outros

### Validações

- Valores numéricos obrigatórios
- Tratamento de erros em todas as operações
- Confirmação antes de excluir despesas

## 🔧 Arquitetura

O sistema segue o padrão **MVC (Model-View-Controller)**:

- **Model**: Camada de dados (SQLite via `database.py`)
- **View**: Interface gráfica (`views/`)
- **Controller**: Lógica de negócios (`controllers.py`)

### Padrões Implementados

- **Singleton**: Única instância do banco de dados
- **Observer**: Atualização automática da UI
- **Separation of Concerns**: Cada módulo tem responsabilidade única

## 🛡️ Segurança

- **Prepared Statements**: Todas as queries SQL usam parametrização (?)
- **Validação de Entradas**: Tratamento de exceções em todos os formulários
- **Isolamento de Dados**: Banco de dados local (não compartilhado)

## 📊 Banco de Dados

### Tabela: despesas

| Coluna    | Tipo    | Descrição           |
| --------- | ------- | ------------------- |
| id        | INTEGER | Chave primária      |
| data      | TEXT    | Data (DD/MM/YYYY)   |
| categoria | TEXT    | Categoria da despesa |
| descricao | TEXT    | Descrição           |
| valor     | REAL    | Valor em R$         |

### Tabela: configuracoes

| Coluna     | Tipo | Descrição      |
| ---------- | ---- | -------------- |
| id         | INTEGER | Sempre 1       |
| salario_1  | REAL | Salário principal |
| salario_2  | REAL | Renda extra    |

## 🐛 Solução de Problemas

### Erro ao importar customtkinter

```powershell
pip install --upgrade customtkinter
```

### Erro de permissão no PowerShell

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Gráfico não aparece

Certifique-se de ter instalado o matplotlib corretamente:

```powershell
pip install --force-reinstall matplotlib
```

## 📝 Notas Técnicas

- O banco de dados é criado automaticamente na primeira execução
- Todos os valores são armazenados como REAL (float)
- Datas são armazenadas como TEXT no formato DD/MM/YYYY
- O tema escuro é configurado globalmente no `main.py`

## 🤝 Contribuições

Projeto desenvolvido seguindo princípios de **Clean Code** e **SOLID**.

## 📄 Licença

Projeto de uso livre para fins educacionais e pessoais.

---

**Desenvolvido com Python 🐍 e ❤️**
