# Practica II

## Objetivo

- Develop a program that allows searching and retrieving articles collected from the arXiv and PubMed repositories using a 
  text query.
- In team of 3-4 memvers do the following activitires:
    1. Collect articles from selected repositories using web scraping
    2. Text normalization using spacy or NLTK
    3. Text representattion in vector space model using scikit-learn
    4. Retrieval of the most similar articles.

# Collection of articles

- From the arXiv repository, articles from the following sections should ve downloaded
    - links
- From the PubMed repository, articles from the `tendring section` should be downloaded
- The collection for both repositories will ben carried out until 300 items from each repository are completed
- In the case of arXiv, 100 articles from each section must be downloaded

## ArXiv articles

- The content to be obtained from the arXiv articles is as follows:

    - DOI
    - Title
    - Authors
    - Abstract
    - Section
    - Publication date

- The articles are available in up to 3 different formats. To facilitate content extraction, the HTML format shoul be used.

## PubMed articles

- The content to be obtained from the PubmED articles is as follows

    - DOI
    - Title
    - Authors
    - Abstract
    - journal name
    - Publication date

- PubMed has a refence format (similar to RIS) from which content can be obtanied

## ArXiv raw corpus

- The articles content from arXiv shol dbe saved in a corpus with the following format:

> Tabla tomada en foto

- *The corpus must be saved in a file named arxiv_raw_corpus.csv using tab character as field separator.*

## PubMed raw corpus

- The articles content from PubMed should be saved in a copus 

## Text normalization

- Apply the following normalization process to the fields Title and Abstract of the raw data corpora:
    - Tokenization
    - Remove stop words from the following grammatical categories: articles, prepositions, conjunctions and pronouns
    - Lemmatization

- For stop words use POS tagging process to identify grammatical category
- The normalized version of corpora should ve saved in csv files, with the same format a the previos ones, called arxiv_normalized_corpus.csv
  and pubmed_normalized_corpus.csv

## Rext representation

- Generate frequency, binarized and TF-IDF vector representations of the columns>
    - Title
    - Abstract
- The characteristics to be extracted are:
    - Unigram
    - Bigrams
- The resulting representations should ve saved in *pkl* files.

## Retrieval of the mos similar articles

- The query provided for this tasks is a BibTeX or RIS file
- Once the file has been selected, the following must be indicated
    - The comparative content of the article (Title or Abstract)
    - The features to be extracted (Unigram or Bigram)
    - The type of vector representation (frequency, binary or TF-IDF)
- Do the following with this document:
    - Applythe same normalization process performed to the normalized copus
    - Extract the specified features
    - Generate the indicated vector representation
    - Apply the consine similiraty algorithm to determine the similarity between the input document and the rest of the documents
      in both corpus using the comparative content
    - Display the 10 most similar documents in descending order

## Interface

- An interface must be created for the three main tasks:
    - Article collections: tiene que haber una interfaz que le pregunte donde buscar (PubMed o arXiv)
    - Text normalization and representation: otra interfaz para cuando se cumpla lo primero, genere los csv normalizados
      y despues mostramos la representacion 
    - Retrieval of similar articles: aqui ya tenemos que poner cual es nuestro query (bib o ris) y tenemos que traer los 10
      mas parecidos

## Article collection interface

- The interface 

-------

Hay que realizar subtareas en donde nos compartira codigo para que sea nuestro punto de partida.

Tenemos que definir una metrica de similutud, tanto la coleccion de documentos como la consulta deben de pasarse por transformaciones
en donde se normalizan, etc, Se tiene que poner con distancia euclidiana (puntos entre un vector), pero esta tecnica es muy sensible a la
longitud de un vector, en oraciones pequeñas son muy cercanas y las grandes no a pesar de que las grandes sean mas similares. Por eso se 
hace la similitud COSENO, por el angulo, ya que es sensible a esto, y gracias a esto se calcula de manera precisa la equivalencia de un
vector a otro, (normalizacion, factorizacion vectorial, metrica de similitud COSENO). Con ello se resulve la practica.

Vamos a utilizar query para buscar y recabar informacion,

Cuando andemos recuperando la informacion con web scrapping si no tiene un formato HTML lo descartemos.

Tenemos que apuntar a la url e irnos a la seccion de trending e irnos a cada href, como pueden ser archivos open access
o privados, dentro de PubMed hay una parte que dice display options, y siempre hay una opcion que dice "PubMed".
Si no tiene ABSTRACT no es necesario que lo recuperemos.

Nosotros tenemos que ir viendo como estan estructurados cada RIS y ver como lo vamos a estructurar.

Cuando accedemos al artigulo, nos sale el mismo url y con el identificador del articulo, y para ver la version de PubMed, solo a la misma url
le agregaremos al variable "?format=pubmed", nada mas hay que concatenar ese parametro de busqueda a la url.

Los diccionarios genericos no nos sirven, estos nos los puede dar el chat, entonces no se usaran diccionarios genericos, por eso se usara
un `post tagging`

Si nuestra coleccion de documentos la normalizamos utilizando una herramienta, si el proceso de lematizacion usamos tambien usamos algo, tenemos 
que aplicar lo mismo al Bip, tenemos que reutilizar lo mismo que ya tenemos para normalizar el archivo de entrada. Tenemos que hacer similitud coseno
y recuperaremos los (y) mas parecidos.

Para la representacion vectorial usaremos scikit learn (features extractions), para usar para manejar k_vectorized, es para generar representacion 
vectorial para el texto. Fix transform saca la representacion vectorial

Bigramas: cuando dos palabras es un token - con n_gram_rench, en donde especificamos esta parte.
Unigramas: cada palabra es un token

SE VA A DAR UNA SEMANA POR TAREAS, ENTONCES PARA LA OTRA SEMANA YA TIENE QUE QUEDAR EL WEB SCRAPPING.

-------