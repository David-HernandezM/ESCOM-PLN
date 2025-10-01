# Limitations of text vector representation

- The representation of text in vector space in its different variants is helpful for several practical applications such as:
    - Similarity between workds and documents
    - Information retrieval
    - Text classiffication
- However, this representation does not capture the sequential aspects of the text
- When passing the text to a vector representation, the order in which the workds were in the documents is lost and this aspect 
  may be relevant for some applications

-------------

Aplicaciones:

- Recuperacion de informacion en donde se tiene una coleccion de documentos, se tiene una query, y el contenido de esta consulta
  commpara con una metrica de solicitud, y a traves de esa metrica de solicitud se recupera el documento que maximisa esta parte.
- Clasificacion de texto: en el caso de lenguaje natural es clasificacion de texto. consiste en que dada un conjunto de documentos
  se quiere ver a que clase pertenece cada uno de estos documentos, un ejemplo es tener articulos de procesamiento de lenguaje natural
  cryptografia, vision por computadora, se entrena a un algoritmo con un conjunto de datos, despues llega un nuevo articulo y de ahi 
  decir a que parte pertenece, y el moelo que resulto del modelo de entrenamiento hace la clasificacion ahi se usa la representacion
  de espacio vectoral para sacar las caracteristicas y basadas en esta se dice a que tipo de documento pertenece.

Todo tiene sus limites, una deficiencia en la representacion de espacio vectorial es que no es capaz de captar la naturaleza secuencial
del texto, ademas de consistir en palabras de un vocabulario, tiene una serie de reglas para estructurar un vocabulario

---------------


- Given the following documents, generate their binarized vector space representation:
    - El gato persigue al raton
    - El raton persigue al gato

- Is there anu difference in their vector representation?
- Do the vector representations reflect the semantic differences between the documents"

| D1: | el | gato  | persigue | al | raton|
| D2: | el | ratom | persigue | al | gato |
|:---:|:--:|:-----:|:--------:|:--:|:----:| 
| D1  | 1  |   1   |    1     | 1  |  1   |
| D2  | 1  |   1   |    1     | 1  |  1   |

Se tiene que llegar a la parte semantica del documento, se quiere que dos documentos con alto grado de similitud, la similitud lo acerque
de manera semantica.

--------

Si se pasa a un espacio de representacion vectorial, esto seria identico, sin embargo, el contexto no es el mismo, esto no seria util.
Cuando se pasa a una representacion de espacio vectorial, se pierde el orden/secuencia, por lo que no se podria recuperar documentos
semanticamente parecidos, aqui la solucion es incluir en la representacion la secuencia de palabras.

Una primera aproximacion es extender el modelo de lenguaje

--------

## Unigram lenguage model

- The most primitive language model is the unigram model where no sequence information is used, but only the frequency of terms 
- In this model it is assumed that each term in a document is randomly generated independently of the previos terms in the document.
- The unigram model ceates a multinomial distribution of the terms in a document.

------------------

Lo mismo aplica para la voz, si se mete a este conjunto y se quiere sintetizar esta frase, el orden es importante.

------------------

## N-grams language model

- The n-gram model is an extension of the unigram model where 2 or more consecutive terms are taken from the document
- This model already incorporates the effect of the context in which the terms are found
- In the n-gram model we usually take between 2 and 5 consecutive terms
- The incorporation of the context allows us to determine the most frequent associations betweens words

-------------

Ahora en el ejemplo del gato y del raton, se llega a una representacion de espacio vectorial, si ya no se toma un unigramas, y ahora
se toman digramas:

D1: (El gato)  (gato persigue)  (persigue al) (al raton)
D2: (El raton) (raton persigue) (persigue al) (al gato)

|    | (El gato) | (gato persigue) | (persigue al) | (al raton) | (el raton) | (raton persigue) | (al gato) |
|:--:|:---------:|:---------------:|:-------------:|:----------:|:----------:|:----------------:|:---------:|
| D1:|     1     |       1         |       1       |     1      |     0      |        0         |      0    |
| D2:|     0     |       0         |       1       |     0      |     1      |        1         |      1    |


En la practica en el ngram-range el profe va a tener que poder escoger entre los n-gramas, si es uno a uno, es unigrama, si pone 2,2 seria
digramas, si pone 1,2 se ocmbinan digramas con unigramas, sin embargo en la practica solo sera unigramas o digramas.

-------------


## Text representation

- Generate frequency, binarized and TF-IDF vector representations of the columns:
    - Title
    - Abstract
- The characteristics to be extracted are:
    - Unigrams
    - Bigrams
- The resulting representations should be saved in pkl files

----------------

EN la practica podemos generar binario, tf-idf o frecuencia, en el titulo y abstract debemos hacer estas representaciones, el titulo y
el abstract seran utilizado en los queries, el profe puede decir:

El profe que te proporsione, quiero que se compare con los titulos, es dirigida la busqueda.
Tambien nos puede decir, lo que va a estraer del titulo sera unigramas o digramas.
El tercer query sera que representacion quiere utilizar, si binario, frecuencia o tf-idf.

El query tendra estos parametros, cada vez que vaya a lanzar un query ingresara estos tres campos. Lo que espera es que ya tengamos una
coleccion de las distintas formas de representacion del texto previamente ya calculadas, por eso es que pide que generemos los `pkl`, cada
combinacion posible de elemento de generacion, caracteristica y digramas o bigramas, es un pkl

Para arxiv seria: 
- arxiv_Title_unigram_freq
- arxiv_Title_unigram_bin
- arxiv_Title_unigram_tf-idf
- arxiv_Title_bigram_freq
- ...

Esto lo tenemos que calcular previamente, esta semana tenemos que mostrar los csv normalizados donde ya aplicamos lematizacion etc y aparte los pkl 
que ya hemos generado

- csv normalizados
- Los pkl

Igual le debemos de permitir hacer tres cosas, que si title o abstract, que si quiere bigrama o unigrama, que representacion vectorial quiere usar y lo 
unico que va a hacer es dirigirlo al pkl que cumpla estos parametros. Serian dos pkl el de arxiv y pubmed. 

Para la practica es importante saber cuando aplicar fit, transform o ambas

- La funcion fit obtiene el vocabulario de la coleccion de documentos, este de alguna manera genera la lista
- La funcion transform, utiliza el vacabulario calculado por fit para generar el vector space modelde la coleccion de documentos. Este usa el vocabulario
  para asignar que valores si tienen que.

La similitud coseno hace un producto punto, eso lo acumula.

No solo hay que guardar x, tambien hay que guardar los vectorizadores, ocupamos dos objetos

----------------

## Text noralization and representation interface

- This interface should allow specifying the raw corpus
- The expected outputs are the normalized corpus (1 per repository) and the pkl files of the text representation (12 files per repository).
