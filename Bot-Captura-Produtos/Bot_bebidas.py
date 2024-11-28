from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import time
from threading import Thread

app = Flask(__name__)

# Função para rodar as buscas automaticamente
def executar_buscas_automaticas():
    termos_de_busca = ['Heineken','Budweiser','stella artois','corona','skol beats','spaten','cabare ice','Jameson','chivas','black label','red label','blue label','royal salute','old par','jackdaniels','buchanans','passport','white horse','jim beam','Ballantines','velho barreiro','cachaca 51','matuta','ypioca','sagatiba','ypioca 160','cachaça salinas','ypioca 150','Orloff','Smirnoff','Absolut','Ciroc','grey goose','Skyy','rum Montilla','rum Malibu','bacardi','Rum havana','gin tanqueray','Gin Flowers','gin bombay','gin rocks','Gin Beefeater','Gin Seagers','gingordons','Gin Bulldog','Gin Tônica Tanqueray','Bebida Mista Flowers Dry Gin','gin tonica schweppes','agua tonica antarctica','tonica schweppes','schweppes citrus leve em acucares','vermute martini','bitter campari',]  # Termos
    while True:
        for termo in termos_de_busca:
            print(f"Iniciando busca por: {termo}")
            try:
                produtos, erros = buscar_produtos_magazine(termo)  # Função já existente no seu código
                if erros:
                    print("Erros encontrados:")
                    for erro in erros:
                        print(erro)
                else:
                    print(f"Produtos encontrados para o termo '{termo}': {produtos}")
                print(f"Busca finalizada para o termo: {termo}")
            except Exception as e:
                print(f"Erro durante a busca para o termo {termo}: {e}")
            
            print("Aguardando 5 minutos para a próxima busca...")
            time.sleep(300)  # Pausar por 600 segundos (10 minutos)

# Iniciar o loop de busca em um thread separado para não bloquear o restante do código
Thread(target=executar_buscas_automaticas).start()

# Função para configurar o navegador Selenium
def configurar_navegador():
    service = Service('C:/WebDriver/chromedriver.exe')  # Substitua pelo caminho correto do chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executa o navegador em modo headless (sem interface)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Conectar ao banco de dados MySQL
def conectar_banco():
    return mysql.connector.connect(
        host="127.0.0.1",  # Substitua pelo seu host MySQL
        user="root",       # Substitua pelo seu usuário MySQL
        password="SuaSenhaAqui",   # Substitua pela sua senha do MySQL
        database="Bebidas"  # Nome do banco de dados
    )

# Função para salvar produto no banco de dados
def salvar_produto_banco(produto, categoria):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = "INSERT INTO produtos (nome, preco, imagem, link, categoria) VALUES (%s, %s, %s, %s, %s)"
    valores = (produto['nome'], produto['preco'], produto['imagem'], produto['link'], categoria)

    cursor.execute(sql, valores)
    conexao.commit()
    
    cursor.close()
    conexao.close()

# Função para capturar os resultados da pesquisa de produtos e salvar no banco
def buscar_produtos_magazine(termo_busca):
    driver = configurar_navegador()
    url_pesquisa = f"https://www.magazinevoce.com.br/SuaLojaAqui/busca/{termo_busca.replace(' ', '-')}/?from=submit"
    driver.get(url_pesquisa)

    wait = WebDriverWait(driver, 2)
    produtos = []
    erros = []

    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.sc-ksCcjW.lapNIe')))
        elementos_produtos = driver.find_elements(By.CSS_SELECTOR, 'li.sc-ksCcjW.lapNIe')
        
        print(f"Encontrados {len(elementos_produtos)} elementos de produtos.")

        for elemento in elementos_produtos[:2]:
            produto = {}
            
            # Capturar o nome do produto
            try:
                nome_elemento = elemento.find_element(By.CSS_SELECTOR, 'h2.sc-dxlmjS.NMyym')
                produto['nome'] = nome_elemento.text
            except NoSuchElementException:
                produto['nome'] = 'Nome não encontrado'
                erros.append("Erro ao capturar o nome do produto.")

            # Capturar o preço do produto
            try:
                preco_elemento = elemento.find_element(By.CSS_SELECTOR, 'div.sc-imWYAI.bmfVAB p.sc-jXbUNg.fXGDSl.sc-fFlnrN.gtlDuG')
                produto['preco'] = preco_elemento.text
            except NoSuchElementException:
                produto['preco'] = 'Preço não encontrado'
                erros.append("Erro ao capturar o preço do produto.")

            # Capturar o link para a página do produto
            try:
                link_elemento = elemento.find_element(By.CSS_SELECTOR, 'a.sc-cWSHoV.hYaBHR.sc-feNupb.hwpVPV')
                produto['link'] = link_elemento.get_attribute('href')
            except NoSuchElementException:
                produto['link'] = '#'
                erros.append("Erro ao capturar o link do produto.")

            # Capturar a imagem do produto
            try:
                imagem_elemento = elemento.find_element(By.CSS_SELECTOR, 'div.sc-bHvAfQ.YCjdw img')
                produto['imagem'] = imagem_elemento.get_attribute('src')
            except NoSuchElementException:
                produto['imagem'] = 'Imagem não encontrada'
                erros.append("Erro ao capturar a imagem do produto.")

            # Salvar o produto no banco de dados
            salvar_produto_banco(produto, termo_busca)
            produtos.append(produto)

    except Exception as e:
        erros.append(f"Erro geral ao buscar produtos: {str(e)}")
    
    driver.quit()
    return produtos, erros

# Rota inicial para exibir o formulário de busca
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        termo_busca = request.form['termo']
        return redirect(url_for('exibir_resultados', termo=termo_busca))
    return render_template('index.html')

# Rota para exibir a lista de produtos encontrados
@app.route('/resultados')
def exibir_resultados():
    termo = request.args.get('termo')
    produtos, erros = buscar_produtos_magazine(termo)
    return render_template('resultados.html', produtos=produtos, erros=erros, termo=termo)

# Função para obter produtos do banco de dados com filtros
def obter_produtos(pesquisa_nome=None, pesquisa_categoria=None):
    conn = conectar_banco()
    cursor = conn.cursor()

    sql = "SELECT id, nome, preco, imagem, link, categoria FROM produtos WHERE 1=1"

    if pesquisa_nome:
        sql += " AND nome LIKE %s"
        cursor.execute(sql, ('%' + pesquisa_nome + '%',))
    elif pesquisa_categoria:
        sql += " AND categoria = %s"
        cursor.execute(sql, (pesquisa_categoria,))
    else:
        cursor.execute(sql)

    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return produtos

# Função para obter todas as categorias disponíveis
def obter_categorias():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM produtos")
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return [categoria[0] for categoria in categorias]

# Rota para o painel de administração
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    pesquisa_nome = request.args.get('pesquisa_nome')
    pesquisa_categoria = request.args.get('pesquisa_categoria')

    if request.method == 'POST':
        if 'inserir' in request.form:
            nome = request.form['nome']
            preco = request.form['preco']
            imagem = request.form['imagem']
            link = request.form['link']
            categoria = request.form['categoria']
            salvar_produto_banco({
                'nome': nome,
                'preco': preco,
                'imagem': imagem,
                'link': link
            }, categoria)
        elif 'atualizar' in request.form:
            id_produto = request.form['id']
            nome = request.form['nome']
            preco = request.form['preco']
            imagem = request.form['imagem']
            link = request.form['link']
            categoria = request.form['categoria']
            atualizar_produto(id_produto, nome, preco, imagem, link, categoria)
        elif 'excluir' in request.form:
            id_produto = request.form['id']
            excluir_produto(id_produto)

    categorias = obter_categorias()
    produtos = obter_produtos(pesquisa_nome, pesquisa_categoria)

    return render_template('admin.html', produtos=produtos, categorias=categorias, pesquisa_nome=pesquisa_nome, pesquisa_categoria=pesquisa_categoria)

# Função para atualizar produto no banco de dados
def atualizar_produto(id_produto, nome, preco, imagem, link, categoria):
    conn = conectar_banco()
    cursor = conn.cursor()

    sql = "UPDATE produtos SET nome=%s, preco=%s, imagem=%s, link=%s, categoria=%s WHERE id=%s"
    valores = (nome, preco, imagem, link, categoria, id_produto)

    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()

# Função para excluir produto no banco de dados
def excluir_produto(id_produto):
    conn = conectar_banco()
    cursor = conn.cursor()

    sql = "DELETE FROM produtos WHERE id=%s"
    cursor.execute(sql, (id_produto,))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)
