import re
import streamlit as st

# CORPO
## Cabeçalho: Título do trabalho e apresentação do pesquisador
st.markdown("""
            # Conversor de números por extenso e abreviados
            #### Por Cíntia Dantas, bolsista do programa Diversidade Tech da Ada em parceria com a Suzano
            ---
            """)

## Introdução: contém o objetivo/propósito da análise
st.markdown("""
            #### Trata-se de trabalho de conclusão do módulo II - Lógica de programação II, ministrado por Telson Fernandes.
            #### O objetivo é tratar os dados e criar uma aplicação que receba um número escrito por extenso ou com determinadas abreviações e converta em valor numérico. 
            ##### Ex:
            ##### Entrada: Mil duzentos e cinquenta ---- Saída: 1250
            ##### Entrada: 1k ---- Saída: 1000
            ##### Entrada: 1.3k ---- Saída: 1300
            #### OBS: 
            - #### Os valores por extenso não devem conter erros de digitação nem caracteres especiais. Eles vão até a casa de bilhões.
            - #### Os valores abreviados aceitam as seguintes abreviações: 
                - #### k referente a 1.000 reais
                - #### m referente a 1.000.000 de reais
                - #### g referente a 1.000.000.000 de reais.
            ---
            """)

dict_numeros = {
    'zero': 0,
    'um': 1,
    'hum': 1,
    'dois': 2,
    'tres': 3,
    'quatro': 4,
    'cinco': 5,
    'seis': 6,
    'sete': 7,
    'oito': 8,
    'nove': 9,
    'dez': 10,
    'onze': 11,
    'doze': 12,
    'treze': 13,
    'catorze': 14,
    'quatorze': 14,
    'quinze': 15,
    'dezesseis': 16,
    'dezessete': 17,
    'dezoito': 18,
    'dezenove': 19,
    'vinte': 20,
    'trinta': 30,
    'quarenta': 40,
    'cinquenta': 50,
    'sessenta': 60,
    'setenta': 70,
    'oitenta': 80,
    'noventa': 90,
    'cem': 100,
    'cento': 100,
    'duzentos': 200,
    'trezentos': 300,
    'quatrocentos': 400,
    'quinhentos': 500,
    'seiscentos': 600,
    'setecentos': 700,
    'oitocentos': 800,
    'novecentos': 900,
    'mil': 1000,
    'milhao': 1000000,
    'milhoes': 1000000,
    'bilhao': 1000000000,
    'bilhoes': 1000000000,
    'k': 1000,
    'm': 1000000,
    'g': 1000000000,
    }

#Função para tratar o texto da entrada, que é o número escrito por extenso
def trata_string(string):
    string = re.sub('[ãâáàä]', 'a', string)
    string = re.sub('[éêẽë]', 'e', string)
    string = re.sub('[íìîï]', 'i', string)
    string = re.sub('[óòôõ]', 'o', string)
    string = re.sub('[úùü]', 'u', string)
    string = re.sub('[^A-Za-z0-9\.\,\ ]+', '', string)
    string = string.replace('reais', '')
    string = string.replace('bilhao', 'bilhoes')
    string = string.replace('milhao', 'milhoes')
    return string

#Função para converter os textos da entrada em números
def converte_numero(parte):
    numero = []
    for i in parte:
        if i == 'e':
            numero.append(0)
        else:
            item = dict_numeros[i]
            numero.append(item)

    return numero

#Função para somar os números de cada unidade numérica
def soma_unidade(numero):
    soma = sum(numero[0:len(numero)-1])
    return soma, numero[len(numero)-1]

#Função para multiplicar a soma pela unidade numérica
def multiplica_unidade(tupla_soma):
    multiplicacao = tupla_soma[0]*tupla_soma[1]
    return multiplicacao

#Função principal para fazer a junção das partes tratadas
def converte_string(string):
    string = trata_string(string)
    lista = string.replace(',', '').split()

    multi_bilhoes = 0
    multi_milhoes = 0
    multi_mil = 0

    if 'bilhoes' in lista:
        if lista[0] == 'bilhoes':
            lista.insert(0,'um')
        parte1 = lista[:lista.index('bilhoes')+1]
        for i in lista and parte1:
            lista.remove(i)
        conversao = converte_numero(parte1)
        soma_bilhoes = soma_unidade(conversao)
        multi_bilhoes = multiplica_unidade(soma_bilhoes)
    
    if 'milhoes' in lista:
        if lista[0] == 'milhoes':
            lista.insert(0,'um')
        parte2 = lista[:lista.index('milhoes')+1]
        for i in lista and parte2:
            lista.remove(i)
        conversao = converte_numero(parte2)
        soma_milhoes = soma_unidade(conversao)
        multi_milhoes = multiplica_unidade(soma_milhoes)

    if 'mil' in lista:
        if lista[0] == 'mil':
            lista.insert(0,'um')
        parte3 = lista[:lista.index('mil')+1]
        for i in lista and parte3:
            lista.remove(i)
        conversao = converte_numero(parte3)
        soma_mil = soma_unidade(conversao)
        multi_mil = multiplica_unidade(soma_mil)
        
    parte4 = lista
    conversao = converte_numero(parte4)
    soma = sum(conversao) + multi_bilhoes + multi_milhoes + multi_mil
    return int(soma)

#Função para tratar e converter a entrada formada por dígitos e as letras k, m ou g
def converte_abreviado(string):
    string = trata_string(string)
    string = string.replace(',', '.').lower()
    string = string.replace(' ', '')

    letra = re.search('[a-z]', string)
    letra.group(0)

    if '.' in string:
        num = re.search('\d*.\d*', string)
        lista = [num.group(0), letra.group(0)]

    else:
        num = string[:-1]
        if num == '':
            num = 1
        lista = [num, letra.group(0)]
    
    letra = dict_numeros[lista[1]]

    calculo = float(lista[0])*letra
    return int(calculo)

#Função para identificar o padrão da entrada e aplicar as funções adequadas
resultado = ''
def trata_dados(string):
    if string == '':
        return 'Escreva alguma coisa!'
        
    else:
        string = string.replace('-', '').lower()
        teste = string.replace(" ", '')
        teste = teste.replace(",", '')
        teste = teste.replace("\n", '')

        if teste.isalpha():
            resultado = converte_string(string)

        elif teste.isnumeric():
            resultado = int(string)

        elif re.match('\d', string):
            resultado = converte_abreviado(string)
        
        return resultado

# CORPO
## Para converter o número inserido
texto_inserido = st.text_input('Digite o número por extenso ou abreviado:', value='Dois bilhões, novecentos e trinta milhões, setecentos e quarenta e três mil e cinquenta')
texto_inserido = trata_dados(texto_inserido)

html_str = f"""
<style>
p.a {{
  font-family: Helvetica;
  font-size:130%;
}}
</style>
<p class="a">{texto_inserido}</p>
"""
st.write('O resultado da conversão é:', html_str, unsafe_allow_html=True)