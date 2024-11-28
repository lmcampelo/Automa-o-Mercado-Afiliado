import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import time

# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="SuaSenhaAqui",
        database="Bebidas"
    )

# Função para capturar todos os produtos
def obter_dados_produtos():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    query = "SELECT id, Nome, preco, link FROM produtos"  # Use 'id' para rastrear produtos já enviados
    cursor.execute(query)
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

# Função para enviar mensagem pelo WhatsApp Web
def enviar_mensagem_whatsapp(mensagem):
    try:
        # Encontrar a caixa de mensagem
        message_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="x1hx0egp x6ikm8r x1odjw0f x1k6rcq7 x6prxxf"]/p[@class="selectable-text copyable-text x15bjb6t x1n2onr6"]'))
        )
        message_box.click()

        # Copiar a mensagem para o clipboard e colar na caixa de mensagem
        pyperclip.copy(mensagem)
        message_box.send_keys(Keys.CONTROL + 'v')
        
        # Esperar 6 segundos antes de enviar a mensagem
        time.sleep(12)

        # Enviar a mensagem
        message_box.send_keys(Keys.ENTER)
        print("Mensagem enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar a mensagem: {e}")

# Função para selecionar o grupo uma vez
def selecionar_grupo(grupo_nome):
    time.sleep(30)
    try:
        # Encontrar a caixa de pesquisa e procurar pelo grupo
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(grupo_nome)
        search_box.send_keys(Keys.ENTER)

        time.sleep(30)  # Aguarda o grupo carregar
        print(f"Grupo '{grupo_nome}' selecionado com sucesso!")
    except Exception as e:
        print(f"Erro ao selecionar o grupo: {e}")

# Função para verificar e enviar novos produtos
def monitorar_produtos():
    produtos_enviados = set()  # Armazena os IDs dos produtos já enviados

    while True:
        produtos = obter_dados_produtos()

        for produto in produtos:
            # Verificar se o produto já foi enviado
            if produto['id'] not in produtos_enviados:
                mensagem = f"Nome: {produto['Nome']}\nPreço: {produto['preco']}\nLink: {produto['link']}\n"
                enviar_mensagem_whatsapp(mensagem)
                produtos_enviados.add(produto['id'])  # Adicionar o produto aos enviados
                time.sleep(15)  # Intervalo entre o envio de cada produto

        # Espera antes de verificar o banco novamente
        print("Verificando por novos produtos...")
        time.sleep(30)  # Espera 30 segundos antes de verificar novamente

# Inicializar o driver do Selenium para WhatsApp Web
service = Service(executable_path='C:\\WebDriver\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Acessa o WhatsApp Web
driver.get('https://web.whatsapp.com/')
print("Escaneie o QR code do WhatsApp Web")
time.sleep(15)  # Tempo para escanear o QR code

# Seleciona o grupo apenas uma vez
selecionar_grupo('Seu grupo aqui!')

# Inicia a função de monitoramento
monitorar_produtos()
