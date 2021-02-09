# Importa as bibliotecas
import requests 
from lxml import html 
import pandas as pd
import time
import sqlite3
import os
from pathlib import Path

# Checa se o db existe, caso não exista, cria o db e conecta. Se já existir, somente conecta no db
if os.name == 'posix':
    if os.path.isfile(os.getcwd() + '/products-database/base_produtos.db'):
        conn = sqlite3.connect(os.getcwd() + '/products-database/base_produtos.db')    
    else: 
        sqlite3.connect(os.getcwd() + '/products-database/base_produtos.db')    
        conn = sqlite3.connect(os.getcwd() + '/products-database/base_produtos.db')    
else: 
    if os.path.isfile(str(Path(os.getcwd()).parent) + '/products-database/base_produtos.db'):
        conn = sqlite3.connect(str(Path(os.getcwd()).parent) + '/products-database/base_produtos.db')
    else:     
        sqlite3.connect(str(Path(os.getcwd()).parent) + '/products-database/base_produtos.db')
        conn = sqlite3.connect(str(Path(os.getcwd()).parent) + '/products-database/base_produtos.db')

# Define a página inicial do site
pagina_inicial = 'https://www.magazineluiza.com.br/'

# Lista as páginas das categorias
paginas = {
    'Acessórios de Tecnologia':'https://www.magazineluiza.com.br/acessorios-de-tecnologia/l/ia/',
    'Ar e Ventilação':'https://www.magazineluiza.com.br/ar-e-ventilacao/l/ar/',
    'Artesanato':'https://www.magazineluiza.com.br/artesanato/l/am/',
    'Artigos para Festa':'https://www.magazineluiza.com.br/artigos-para-festa/l/af/',
    'Áudio':'https://www.magazineluiza.com.br/audio/l/ea/',
    'Automotivo':'https://www.magazineluiza.com.br/automotivo/l/au/',
    'Bebê':'https://www.magazineluiza.com.br/bebe/l/bb/',
    'Beleza e Perfumaria':'https://www.magazineluiza.com.br/beleza-e-perfumaria/l/pf/',
    'Brinquedos':'https://www.magazineluiza.com.br/brinquedos/l/br/',
    'Cama, Mesa e Banho':'https://www.magazineluiza.com.br/cama-mesa-e-banho/l/cm/',
    'Cameras e Drones':'https://www.magazineluiza.com.br/cameras-e-drones/l/cf/',
    'Casa e Construção':'https://www.magazineluiza.com.br/casa-e-construcao/l/cj/',
    'Celulares e Smartphones':'https://www.magazineluiza.com.br/celulares-e-smartphones/l/te/',
    'Colchões':'https://www.magazineluiza.com.br/colchoes/l/co/',
    'Comércio e Indústria':'https://www.magazineluiza.com.br/comercio-e-industria/l/pi/',
    'Decoração':'https://www.magazineluiza.com.br/decoracao/l/de/',
    'Eletrodomésticos':'https://www.magazineluiza.com.br/eletrodomesticos/l/ed/',
    'Eletroportáteis':'https://www.magazineluiza.com.br/eletroportateis/l/ep/',
    'Esport e Lazer':'https://www.magazineluiza.com.br/esporte-e-lazer/l/es/',
    'Ferramentas':'https://www.magazineluiza.com.br/ferramentas/l/fs/',
    'Filmes e Séries':'https://www.magazineluiza.com.br/filmes-e-series/l/fm/',
    'Games':'https://www.magazineluiza.com.br/games/l/ga/',
    'Informática':'https://www.magazineluiza.com.br/informatica/l/in/',
    'Instrumentos Musicais':'https://www.magazineluiza.com.br/instrumentos-musicais/l/im/',
    'Livros':'https://www.magazineluiza.com.br/livros/l/li/',
    'Mercado':'https://www.magazineluiza.com.br/mercado/l/me/',
    'Móveis':'https://www.magazineluiza.com.br/moveis/l/mo/',
    'Moda e Acessórios':'https://www.magazineluiza.com.br/moda-e-acessorios/l/md/',
    'Musica e Shows':'https://www.magazineluiza.com.br/musica-e-shows/l/ms/',
    'Natal':'https://www.magazineluiza.com.br/natal/l/na/',
    'Papelaria':'https://www.magazineluiza.com.br/papelaria/l/pa/',
    'Pet-Shop':'https://www.magazineluiza.com.br/pet-shop/l/pe/',
    'Relógios':'https://www.magazineluiza.com.br/relogios/l/re/',
    'Saúde e Cuidados Pessoais':'https://www.magazineluiza.com.br/saude-e-cuidados-pessoais/l/cp/',
    'Serviços':'https://www.magazineluiza.com.br/servicos/l/se/',
    'Suplementos Alimentares':'https://www.magazineluiza.com.br/suplementos-alimentares/l/sa/',
    'Tables, iPads e e-Reader':'https://www.magazineluiza.com.br/tablets-ipads-e-e-reader/l/tb/',
    'Telefonia Fixa':'https://www.magazineluiza.com.br/telefonia-fixa/l/tf/',
    'TV e Vídeo':'https://www.magazineluiza.com.br/tv-e-video/l/et/',
    'Utilidades Domésticas':'https://www.magazineluiza.com.br/utilidades-domesticas/l/ud/' 
}

# Cria DataFrame auxiliar vazio
df_produtos = pd.DataFrame()

# Cria um contador para que não tenha excesso de acesso ao site e impedir de derrubar ou ser barrado 
contador = 1

# range total de páginas para o contador
range_contador = range(0, 50000001, 10) 

# Inicia o fluxo de acesso ao site passando por cada página > subcategoria e com limite de 100 páginas por subcategoria, gerando até 2500 itens por subcategoria
for item in paginas.keys():
    # Faz conexão com a página inicial
    page = requests.get(paginas[item])
    print(item)
    # Puxa dados do HTML da página inicial
    tree = html.fromstring(page.content)
    # listando as subcategorias de produtos
    subcategorias_pagina = tree.xpath('//*[@id="sideNavigation"]/nav/ul/li[1]/ul/li/a/@href')
    # Fluxo para navagar por subcategoria
    for subitem in subcategorias_pagina:
        print(subitem)
        # Cria link da página de subcategoria com base no padrão do site
        pagina_subcategoria = pagina_inicial[:-1] + subitem
        # Faz conexão com página da subcategoria
        page_subcategoria = requests.get(pagina_subcategoria)
        # Puxa dados do HTML da página de subcategoria
        tree_subcategoria = html.fromstring(page_subcategoria.content) 
        # Traz a contagem do total de páginas no site
        tt_paginas = tree_subcategoria.xpath('//*[@id="showcase"]/ul[2]/li[9]/a/text()')
        # Caso só tenha uma página, adiciona somente '1' ao marcador
        if not tt_paginas:
            tt_paginas = [1]
        # Cria range de páginas para o processo percorrer
        range_paginas = range(1, int(tt_paginas[0])+1, 1)
        # Criando loop para percorrer as páginas e criar o link
        for num in range_paginas:
            # Caso o número da página for menor ou igual a 100, continua o processo. Caso seja maior, para e vai para a próxima subcategoria/página
            if num <= 100: 
                # Cria o novo link com a numeração da página
                pagina_navegada = pagina_subcategoria[:-1] + '?page=' + str(num)
            else: 
                break 
            subcategoria = None 
            while (subcategoria is None) or (not subcategoria):
                try: 
                    # Faz conexão com a página numerada
                    page_subcategoria_nav = requests.get(pagina_navegada)
                    # Puxa dados do HTML da página numerada
                    tree_subcategoria_nav = html.fromstring(page_subcategoria_nav.content) 
                    # Puxando a Subcategoria do Produto:
                    subcategoria = tree_subcategoria_nav.xpath('//*[@id="__next"]/div[4]/div/div[1]/nav/ol/li/a/text()')[-1]
                except:
                    pass 
            print(subcategoria)
            # Puxando a lista com produtos da página (lista com 25 produtos)
            produtos = tree_subcategoria_nav.xpath('//*[@id="showcase"]/ul[1]/a/div/h3/text()')
            # Looping para puxar cada produto da página e criar um dataframe
            for produto in produtos:
                # Cria um dataframe com categoria, subcategoria e nome do produto
                df = pd.DataFrame({
                                        'Categoria':item,
                                        'SubCategoria':subcategoria,
                                        'NomeDoProduto':produto
                                    }, index=[0])
                # Com o dataframe auxiliar criado, faz o append no dataframe final
                df_produtos = df_produtos.append(df).reset_index(drop=True) 
            
            # Looping para jogar os dados no banco de dados do SQLite e aguardar 10 segundos antes de fazer uma nova navegação a cada 10 páginas navegadas
            if contador in range_contador: 
                # Joga os dados no banco do SQLite
                df_produtos.to_sql('produtos', conn, if_exists='append', index=False)
                # Aguarda 10 segundos
                #time.sleep(10)
                # Limpa o dataframe de produtos
                df_produtos = pd.DataFrame()
                # Informa o contador
                print(contador)
                # Adiciona mais 1 ao contador
                contador += 1
            else:
                # Informa o contador
                print(contador)
                # Adiciona mais 1 ao contador
                contador += 1

