import mysql.connector
from mysql.connector import Error
import time

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="SuaSenhaAqui",
            database="Bebidas"
        )
        if connection.is_connected():
            print("Conexão com o banco de dados bem-sucedida.")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para obter todos os produtos
def obter_produtos(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        consulta = "SELECT id, nome, preco, link, data_hora FROM produtos"
        cursor.execute(consulta)
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao consultar produtos: {e}")
        return []
    finally:
        cursor.close()

# Função para excluir um produto
def excluir_produto(connection, id_produto):
    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM produtos WHERE id = %s"
        cursor.execute(delete_query, (id_produto,))
        connection.commit()
        print(f"Produto com ID {id_produto} excluído com sucesso.")
    except Error as e:
        print(f"Erro ao excluir o produto: {e}")
    finally:
        cursor.close()

# Função para analisar e comparar produtos
def analisar_e_comparar_produtos(connection):
    produtos = obter_produtos(connection)
    produto_dict = {}

    for produto in produtos:
        chave = (produto['nome'], produto['link'])
        if chave not in produto_dict:
            produto_dict[chave] = produto
        else:
            produto_existente = produto_dict[chave]
            # Verifica qual produto é mais recente e exclui o mais antigo
            if produto['data_hora'] > produto_existente['data_hora']:
                # Exclui o produto mais antigo
                excluir_produto(connection, produto_existente['id'])
                produto_dict[chave] = produto
            else:
                # Exclui o produto mais recente
                excluir_produto(connection, produto['id'])

def executar_bot():
    while True:
        try:
            connection = conectar_banco()
            if connection is not None:
                analisar_e_comparar_produtos(connection)
                connection.close()
            # Espera 10 segundos entre as verificações para evitar sobrecarregar o sistema
            time.sleep(10)
        except Exception as e:
            print(f"Erro no loop principal: {e}")
            time.sleep(10)  # Em caso de erro, aguarde antes de tentar novamente

# Executa o bot
executar_bot()
