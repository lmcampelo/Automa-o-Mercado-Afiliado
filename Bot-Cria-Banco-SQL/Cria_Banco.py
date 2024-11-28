import mysql.connector
from mysql.connector import Error

def criar_bancos_e_tabelas():
    try:
        # Conexão ao servidor MySQL
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="SuaSenhaAqui"
        )

        if conexao.is_connected():
            cursor = conexao.cursor()

            # Lista de comandos SQL para criar os bancos e tabelas
            comandos_sql = [
                "CREATE DATABASE IF NOT EXISTS Bebidas;",
                "USE Bebidas;",
                """CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255),
                    preco VARCHAR(50),
                    categoria VARCHAR(255),
                    imagem TEXT,
                    link TEXT,
                    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
                );""",
                "CREATE DATABASE IF NOT EXISTS Eletro;",
                "USE Eletro;",
                """CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255),
                    preco VARCHAR(50),
                    categoria VARCHAR(255),
                    imagem TEXT,
                    link TEXT,
                    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
                );""",
                "CREATE DATABASE IF NOT EXISTS Eletroportateis;",
                "USE Eletroportateis;",
                """CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255),
                    preco VARCHAR(50),
                    categoria VARCHAR(255),
                    imagem TEXT,
                    link TEXT,
                    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
                );""",
                "CREATE DATABASE IF NOT EXISTS Informatica;",
                "USE Informatica;",
                """CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255),
                    preco VARCHAR(50),
                    categoria VARCHAR(255),
                    imagem TEXT,
                    link TEXT,
                    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
                );""",
                "CREATE DATABASE IF NOT EXISTS Petshop;",
                "USE Petshop;",
                """CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255),
                    preco VARCHAR(50),
                    categoria VARCHAR(255),
                    imagem TEXT,
                    link TEXT,
                    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
                );""",
                "CREATE DATABASE IF NOT EXISTS Tv;",
                "USE Tv;",
                """CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255),
                    preco VARCHAR(50),
                    categoria VARCHAR(255),
                    imagem TEXT,
                    link TEXT,
                    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
                );""",
                "CREATE DATABASE IF NOT EXISTS Smartphones;",
                "USE Smartphones;",
                """CREATE TABLE IF NOT EXISTS produtos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255),
                    preco VARCHAR(50),
                    categoria VARCHAR(255),
                    imagem TEXT,
                    link TEXT,
                    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
                );"""
            ]

            # Executar cada comando SQL
            for comando in comandos_sql:
                cursor.execute(comando)

            # Confirmar as alterações no banco de dados
            conexao.commit()
            print("Bancos de dados e tabelas criados com sucesso!")

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão ao MySQL encerrada.")

# Chamar a função para criar os bancos e tabelas
criar_bancos_e_tabelas()
