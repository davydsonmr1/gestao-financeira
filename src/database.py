import sqlite3
import os
from threading import Lock

class Database:
    """
    Implementação Singleton para conexão com o banco de dados.
    Garante que não haja conflitos de threads ou conexões abertas desnecessárias.
    """
    _instance = None
    _lock = Lock()
    DB_NAME = "data/financeiro.db"

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        """Inicializa as tabelas se não existirem."""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de Despesas ATUALIZADA com coluna 'tipo' e 'recorrencia_meses'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                tipo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                descricao TEXT,
                valor REAL NOT NULL,
                recorrencia_meses INTEGER DEFAULT 0
            )
        ''')

        # Tabela de Configurações (Salários Globais)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                salario_1 REAL DEFAULT 0.0,
                salario_2 REAL DEFAULT 0.0
            )
        ''')
        
        # Tabela de Receitas Extras (Dinheiro Extra por Mês/Ano)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS receitas_extras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mes INTEGER NOT NULL,
                ano INTEGER NOT NULL,
                descricao TEXT,
                valor REAL NOT NULL,
                UNIQUE(mes, ano, descricao)
            )
        ''')
        
        # Tabela de Categorias Personalizadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                icone TEXT NOT NULL
            )
        ''')
        
        # Garante que existe a linha de configuração inicial
        cursor.execute('INSERT OR IGNORE INTO configuracoes (id, salario_1, salario_2) VALUES (1, 0.0, 0.0)')
        
        # Inserir categorias padrão se não existirem
        categorias_padrao = [
            ('Alimentação', '🍔'),
            ('Transporte', '🚗'),
            ('Casa', '🏠'),
            ('Lazer', '🎮'),
            ('Outros', '📦')
        ]
        for nome, icone in categorias_padrao:
            cursor.execute('INSERT OR IGNORE INTO categorias (nome, icone) VALUES (?, ?)', (nome, icone))
        
        conn.commit()
        conn.close()

    def get_connection(self):
        """Retorna uma conexão com o SQLite."""
        return sqlite3.connect(self.DB_NAME)
