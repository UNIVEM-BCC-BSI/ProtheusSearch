from bs4 import BeautifulSoup
import requests

# URL do site 
url = 'https://terminaldeinformacao.com/wp-content/tabelas/sa3.php'

# Envia uma solicitação GET para a URL e obtém a resposta
response = requests.get(url)

# Verifica se a solicitação foi bem-sucedida (código de resposta 200)
if response.status_code == 200:
    # Obtém o conteúdo HTML da página
    html = response.text

    # Cria um objeto BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(html, 'html.parser')
    table_element = soup.find('table')
    tb=table_element.find('tbody')
    for i in range(len(tb.find_all('tr'))):
        td=table_element.find_all('td')

# Agora, encontre o elemento <a> dentro do <h1>
        a_element = table_element.find_all('a')

# Acesse o texto e o atributo href do elemento <a>
        texto_do_link = a_element[i].text
        url_do_link = a_element[i]['href']
        textterceiro=td[(2+(i*6))].text

        print("Texto do link: ", texto_do_link)
        print("URL do link:", url_do_link)
        print("\n",textterceiro)
else:
    print("nada")