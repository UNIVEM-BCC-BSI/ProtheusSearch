from bs4 import BeautifulSoup
import requests
import json
a=[]
b=[]
c=[]
d=[]
while True:
    if len(do que a pessoa digitou >3):
        url="https://terminaldeinformacao.com/wp-content/tabelas/campo_{}.php".format('alguma coisa')

        response= requests.get(url)
        if response.status_code==200:
            html =response.text
            
            soup = BeautifulSoup(html,'html.parser')
            #procura o primeiro strong que tiver no html
            teste = soup.find("strong")  
            #pega a informação que esta logo apos o final da chave strong, que no caso é a tabela.
            texto = teste.next_sibling


# cria um arquivo .json, esse arquivo sob escreve o anterior 
with open("nometabela.json", "w") as arquivo_json:
    json.dump(texto, arquivo_json)
    #abre um arquivo .json para pegar a informaçao de de qual nome da tabela
    with open ("nometabela.json", encoding="utf-8") as meu_json:
        x = json.load(meu_json)

    #informaçoes pegadas do arquivo json sao trasformadas em minusculas para conseguir entrar na url
    x= x.lower()


    # URL do site 
    url = 'https://terminaldeinformacao.com/wp-content/tabelas/{}.php'.format(x).replace(" ","")
    print(url)

    # Envia uma solicitação GET para a URL e obtém a resposta
    response = requests.get(url)

    #Verifica se a solicitação foi bem-sucedida (código de resposta 200)
    if response.status_code == 200:
        # Obtém o conteúdo HTML da página
        html = response.text

        # Cria um objeto BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(html, 'html.parser')

        #pega o primeiro elemento html que tem table
        table_element = soup.find('table')

        # pega o primeiro elemento tbody dentro da table anterior
        tb=table_element.find('tbody')

        # um for para rodar o nuemro de vezes que tiver tr dentro do tbody 
        for i in range(len(tb.find_all('tr'))):

            #pega todos os td dentro da primeira tabela
            td=table_element.find_all('td')
            #pega o elemento da "a" dentro da table
            a_element = table_element.find_all('a')

            #pega o campo a[i] e trasforma em texto
            texto_do_link = a_element[i].text

            #pega o campo a[i] e trasforma em link
            url_do_link = a_element[i]['href']

            #pega os ekementos td que sao as descrições da posicao começando em 2 e somando 2*i para sempre conseguir pegar a descrição
            textterceiro=td[(2+(i*6))].text

            #faz um append na lista a todos os elementos de texto
            a.append(texto_do_link)

            #faz um append na lista b todos os elementos de link
            b.append(url_do_link)

            #faz um append na lista c todos os elementos da descriçao
            c.append(textterceiro)

            # a lista d recebe as listas a,b,c
            d = [a,b,c]
    
    else:
        print("nada")

#cria um arquivo .json para as informaçoes pegadas, reescreve sob o anterior
with open("todos.json", "w") as arquivo_json:
    json.dump(d, arquivo_json)