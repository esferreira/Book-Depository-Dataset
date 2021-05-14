#!/usr/bin/env python
# coding: utf-8

# # **Uma breve análise exploratória dos dados.**
# Teste Engenheiro de Dados

# In[158]:


# Importanto bibliotecas necessárias
import pandas as pd
import numpy as np
import operator
import re
from collections import Counter
import itertools
from tabulate import tabulate


# In[159]:


# Carregar arquivos
# authors.csv
# Contém o nome dos autores e o id que o representa no arquivo “dataset”;
# Criar dataframe autores
autores = pd.read_csv('https://raw.githubusercontent.com/esferreira/Book-Depository-Dataset/main/authors.csv')
autores.head()


# In[160]:


# categories.csv
# Contém as categorias e o id que a representa no arquivo “dataset”;

categorias = pd.read_csv('https://raw.githubusercontent.com/esferreira/Book-Depository-Dataset/main/categories.csv')
categorias.head()


# In[161]:


# formats.csv
# Contém o formato em que os livros são disponibilizados (papel, para download, áudio, etc) e o id que o representa no arquivo “dataset”;

formatos = pd.read_csv('https://raw.githubusercontent.com/esferreira/Book-Depository-Dataset/main/formats.csv')
formatos.head()


# In[162]:


# dataset.csv
# Contém a lista de livros e suas informações;
conjunto_dados = pd.read_csv('https://raw.githubusercontent.com/esferreira/Book-Depository-Dataset/main/dataset.csv')
df = pd.DataFrame(data=conjunto_dados)
#df.head()


# ### Adicionar autores ao dataset

# In[163]:


# Criar dicionário apartir do dataframe autores para remapeamento dos ID dos autores pelo seu nome
m = autores.set_index('author_id')['author_name'].to_dict()
#m


# In[164]:


# Converter listas de autores para tipo list
# Armazenar resultado em uma lista temporária
authors_temp = []
for i in range(len(df['authors'])):
    authors_temp.append(df['authors'][i].strip('][').split(","))


# In[165]:


# Criar uma nova coluna no dataset para receber o resultado da lista temporária de autores
df['authors_list'] = authors_temp


# In[166]:


# Remover espaços em branco dos itens da lista
df['authors_list'] = [[s.strip() for s in inner] for inner in df['authors_list']]


# In[167]:


# Converter todas as string da lista para tipo int
# Armazenar resultado numa lista temporária
nova_lista_autores = []

for i in range(len(df['authors_list'])):
    # Criar uma lista do registro atual
    lista = df['authors_list'][i]
    # Remover espaços vazios da lista ['']
    filtered = [x for x in lista if len(x.strip()) > 0]
    # Utilizar o resultado da lista sem espaços vazios [''] para adicionar a lista temporária
    # Converter valores da lista para tipo int
    nova_lista_autores.append(list(map(int, filtered)))

# Atribuir valores atualizados a nova coluna authors_list   
df['authors_list'] = nova_lista_autores


# In[168]:


# Criar função para fazer o remapeamento dos itens da lista pelo seu correspondente no dicionário de autores
def replace_(list, dictionary):
    return [m.get(item, item) for item in list]

# Subistituir ID dos Autores pelo nome do autor
lista_autores_temp = []
for i in range(len(df['authors_list'])):
    lista_autores_temp.append(replace_(df['authors_list'][i],m))


# In[169]:


# Atribuir o resultado a própria coluna authors_list que será sobrescrita
df['authors_list'] = lista_autores_temp


# ### Adicionar categorias ao dataset

# In[170]:


# Criar dicionário apartir do dataframe categorias para remapeamento dos ID das categorias pelo seu nome
n = categorias.set_index('category_id')['category_name'].to_dict()
#n


# In[171]:


# Converter listas de categorias para tipo list
# Armazenar resultado em uma lista temporária
categories_temp = []
for i in range(len(df['categories'])):
    categories_temp.append(df['categories'][i].strip('][').split(","))


# In[172]:


# Criar uma nova coluna no dataset para receber o resultado da lista temporária de categorias
df['categories_list'] = categories_temp


# In[173]:


# Remover espaços em branco dos itens da lista
df['categories_list'] = [[s.strip() for s in inner] for inner in df['categories_list']]


# In[174]:


# Converter os itens da lista para tipo int
nova_lista = []
for i in range(len(df['categories_list'])):
    nova_lista.append(list(map(int, df['categories_list'][i])))
    
# Atribuir valores atualizados a coluna categories_list     
df['categories_list'] = nova_lista


# In[175]:


# Criar função para fazer o remapeamento dos itens da lista pelo seu correspondente no dicionário de categorias
def replace_(list, dictionary):
    return [n.get(item, item) for item in list]

# Subistituir ID da Categoria pelo nome da categoria
lista_categorias_temp = []
for i in range(len(df['categories_list'])):
    lista_categorias_temp.append(replace_(df['categories_list'][i],n))


# In[176]:


# Atribuir o resultado a própria coluna categories_list que será sobrescrita
df['categories_list'] = lista_categorias_temp


# ### Adicionar formatos ao dataset

# In[177]:


# Criar dicionário apartir do dataframe categorias para remapeamento dos ID das categorias pelo seu nome
o = formatos.set_index('format_id')['format_name'].to_dict()
#o


# In[178]:


# Subistituindo valores NaN por 23: 'Undefined'
df['format'] = df['format'].replace(np.nan, 23)


# In[179]:


# Converter valores do tipo float para int e armazenar numa lista temporária
format_temp = []
for i in range(len(df['format'])):
    format_temp.append(int(df['format'][i]))


# In[180]:


# Adicionar valores da lista temporária em uma nova coluna no dataset
df['format_list'] = format_temp


# In[181]:


# Proceder com a subistituição de valores dos formatos dos livros utilizando o dicionário de formatos
df['format_list'] = df['format_list'].map(o) 


# ### Exibir resultado parcial do cruzamento de dados entre os arquivos e o dataset

# In[182]:


# Exibir preview dos cruzamentos de dados no dataset
df[['authors','authors_list','categories','categories_list','format','format_list']]


# ### Perguntas
print("\nPerguntas & Respostas\n")
# #### 01 - Qual a quantidade total de livros da base?

# In[183]:

print("01 - Qual a quantidade total de livros da base?\n")
print('Total de registros sem título do livro é '+str(df['title'].isnull().sum()))
print('A quantidade total de linhas do aquivo dataset é '+str(df.shape[0]))
print('Como não há registros sem título do livro, a quantidade total de livros da base é '+str(df.shape[0]))
print("\n")

# #### 02 - Qual a quantidade de livros que possuí apenas 1 autor?

# In[184]:

print("02 - Qual a quantidade de livros que possuí apenas 1 autor?\n")
# Criar contador para adicionar mais 1 apenas para o registro de livro que contém apenas 1 autor
contador = 0
for i in range(len(df['authors_list'])):
    if len(df['authors_list'][i]) == 1:
        contador = contador + 1

print(str(contador)+" livros possuem apenas 1 autor.")
print("\n")


# #### 03 - Quais os 5 autores com a maior quantidade de livros?

# In[185]:

print("03 - Quais os 5 autores com a maior quantidade de livros?")
# Juntar todas as listas da coluna authors_list em uma unica lista
result = []
for i in range(len(df['authors_list'])):
    result = result + df['authors_list'][i]

# Fazer a contagem de registros por autor
c = Counter(result)
headers = ["Autores", "Qtd Livros"]
# Montar tabela com resultados
table = tabulate(c.most_common(5), headers, tablefmt="github")
# Exibir tabela com quantidade de livros por categoria
print("\nOs 5 autores com maior quantidade de livros são.:")
print("\n"+table)
print("\n")


# #### 04 - Qual a quantidade de livros por categoria?

# In[186]:

print("04 - Qual a quantidade de livros por categoria?")
# Juntar todas as listas da coluna categories_list em uma unica lista
result = []
for i in range(len(df['categories_list'])):
    result = result + df['categories_list'][i]

# Fazer a contagem de registros por categoria
c = Counter(result)
# Definir cabeçalho para tabela de saída
headers = ["Categoria", "Qtd Livros"]
# Montar tabela com resultados
table = tabulate(c.most_common(), headers, tablefmt="github")
# Exibir tabela com quantidade de livros por categoria
print("\n"+table)
print("\n")


# #### 05 - Quais as 5 categorias com a maior quantidade de livros?

# In[187]:

print("05 - Quais as 5 categorias com a maior quantidade de livros?")
table = tabulate(c.most_common(5), headers, tablefmt="github")
# Exibir tabela com quantidade de livros por categoria
print("\n"+table)
print("\n")

# #### 06 - Qual o formato com a maior quantidade de livros?

# In[188]:

print("06 - Qual o formato com a maior quantidade de livros?")
# Juntar todas as listas da coluna format_list em uma unica lista
result = []
for i in range(len(df['format_list'])):
    result.append(df['format_list'][i])

# Fazer a contagem de registros por formato
c = Counter(result)
# Definir cabeçalho para tabela de saída
headers = ["Formato", "Qtd Livros"]
# Montar tabela com resultados
table = tabulate(c.most_common(1), headers, tablefmt="github")
# Exibir tabela com quantidade de livros por categoria
print("\nO formato com maior quantidade de livros é.:")
print("\n"+table)
print("\n")


# #### 07 - Considerando a coluna “bestsellers-rank”, quais os 10 livros mais bem posicionados?

# In[189]:

print("07 - Considerando a coluna “bestsellers-rank”, quais os 10 livros mais bem posicionados?")
print("\n")
sorted_df = df.sort_values(by=['bestsellers-rank'], ascending=False)
print(sorted_df[['title','bestsellers-rank']][:10])
print("\n")

# #### 08 - Considerando a coluna “rating-avg”, quais os 10 livros mais bem posicionados?

# In[190]:

print("08 - Considerando a coluna “rating-avg”, quais os 10 livros mais bem posicionados?")
print("\n")
sorted_df = df.sort_values(by=['rating-avg'], ascending=False)
print(sorted_df[['title','rating-avg']][:10])
print("\n")

# #### 09 - Quantos livros possuem “rating-avg” maior do que 3,5?

# In[191]:

print("09 - Quantos livros possuem “rating-avg” maior do que 3,5?")
contador = 0
for i in range(len(df['rating-avg'])):
    if df['rating-avg'][i] > 3.5:
        contador = contador + 1

print("\nTotal de livros que possuem “rating-avg” maior do que 3,5.: "+str(contador))
print("\n")

# #### 10 - Quantos livros tem data de publicação (publication-date) maior do que 01-01-2020?

# In[192]:

print("10 - Quantos livros tem data de publicação (publication-date) maior do que 01-01-2020?")
# Vamos garantir que a coluna 'publication-date'' esteja no formato de data
df['publication-date'] = pd.to_datetime(df['publication-date'])
# Definindo uma máscara
mask = (df['publication-date'] > '2020-01-01')
# Aplicando máscara ao dataset
df = df.loc[mask]
# Obtendo o total de linhas de acordo com o filtro aplicado
print("\nO total de livros com data de publicação maior que 1 de Janeiro de 2020 é.: "+str(df.shape[0]))


# In[ ]:




