# Semantic text processing and information extraction 

------------

Notas profe: con el nombre y la extension se puedde hacer la definicion, lo que le permita al profe es que podamos especificar
el nombre del archivo que el ingrese (ya que el profe nos va a dar pruebas adicionales).

La address si viene mas de un dato tomamos el primer dato y nosotros decidimos si lo mandamos a cy o pp

-----------

Los datos se representan para ser explotados por el algoritmo. Adicionalmente estas caracteristicas deben de estar en un tipo de 
dato, en un representacion numerica para que estos valores los pueda procesar. Pero en el caso del texto, a pesar de que ya se 
normalizo, siguendo le secuencia de caracteres ya que estos no puedes ser analizados por los algoritmos, ya que necesitan ser procesados
de manera tabular, matricial, etc.

# Text representation

- The text normalizae din the previos practices dos not have the representation expected by the mentioned algorithms.

"Concluir la construccion de 2 mil 750 nuevas sucursales del banco de bienestar en dos años fue una tarea 'titanica y muy dificil', que
enfrento diversos retos, pero que hoy se trafuce en una 'gran obra de caracter social', afirmo Victor Lamoyi...

- What features can we extract from the text?
- How can we represent the text as a list of features and values?


----------

### Notas profe:

Cuando extraemos unas caracteristicas de nuestros casosd e uso, este debe de tener "discriminacion", entonces para poder caracterizarlo y
que sea diferente de otras, para poder representarlo con sus caracteristicas. Ejemplo, en un paciente las caracteristicas comunes se descartan
y nos quedariamos con los signos que son sobresalientes, en este caso con el manto matricial.

----------

## Vectors and documents

- A `vector` can ve considered a list or array of numbers
- A `vector space` is a colecction of vectors, characterized by its dimension.
- jOn the other hand, a documents is a collection of words.
- This collection of words is kknown as a `vocabulary`.

## Vector space model

- We can represent a `document as a vector` by counting the words that appear in that document.
- This representation is known as a `vector space model` (modelo de espacion vectorial).

## Vector representation of texts

- Given the following documents:
    - D1 = "El precio del dolar aumento 2 pesos la semana pasada pero bajo 1 peso esta semana".
    - D2 = "Facebook perdio millones de dolares y bajo el valor dolar accion al perder usuarios".

- The vocabulary in these documents is composed of 27 words.
- If normalization process is not applied, the vocabulary becomes very large and the vectors very sparse (sparse curse).


-------

Notas profe:

Primero se va a extraer el vocabulario. Cuando se empeice a contar las palabras que hay en los textos, se encuentra que hay palabras que estan 
relacionadas entre un documento y otro pero como no estan formalizadas, el vocabulario lo tomara como palabras distintas. (Ejemplo la palabra dolar,
existe dolas y dolares, y si no se normaliza se contarian como dos palabras distintas.). EL problema de trabajar con vocabulario es que entre mas grande
es mi vocabulario mas complejo sera procesarlo en cuestion de memoria y procesamiento.

Entra mas palabras distintas tenga en el vocabulario, una cantidad muy infima muy pequeña de las palabras del vocabulario apareceran en un documento en
particular, pero si cada noticia tiene en promedio 100 a 1000 palabras, el resto del millon seran palabras que no apareceran en el documento, teniendo asi
vectores dispersos, estos son aquellos en que los valores significativos seran pocos y el resto seran puros ceros, es decir, no son importantes, por eso
trabajar con vectores muy dispersos entra la posibilidad que entre esos vectores las caracteristicas iguales seran muy pocas ya que estan muy dispersos, entonces
los vectores dispersos no ayudan a encontrar estas similitudes.

Una forma de lidiar con vectoers muy grandes y dispersos es aplicar normalizacion, pero no lo soluciona del todo, pero ayuda al proceso de la representacion
del texto, pero ayuda.

--------


## Vector representation by frequency

- Documents:
   - D1 = "El precio del dolar aumento 2 pesos la semana pasada pero bajo 1 peso esta semana".
   - D2 = "Facebook perdio millones de dolares y bajo el valor dolar accion al perder usuarios".

> Insertar tabla que se explico en la clase.


--------

Notas profe:

La forma mas facil de asignar valores es asignar su frecuencia. EL ejemplo anterior tiene muchos ceros pero tiene algunas que si tienen ambos documentos.
Una vez teniendo la el vector de representacion de frecuencia ya se puede mandar a un algoritmo. Los valores que se asocian existen diferentes alternativas
para calcular estos valores (aqui se uso conteo de frecuentia)

-------

## Binarized vector representation

- The text representatino in vector space makes it possible to associate a value to each characteristic.
- In addition to the frequency of words, the presence or absence of words can also be indicated.
- This representation is known as `binarized` o `one-hot`

----------------

Notas profe:

La diferencia esta en que el conteo de la frecuencia solo mostramos el conteo o la presencia de algo, con un 0 o con un 1 a diferencia de la representacion por 
frecuencia.

Para poder saber cual usar todo depende de lo que queramos hacer, si solo conocer si aparece o en su caso cuantas veces aparece.

---------


## Spatial visualization of vector representation.

> Imagen dada en la clase.


--------

Notas profe:

Una ventaja de esta representacion es que se puede usar para acercarnos a la parte semantica.


## Information retrieval

- Two similar documents tend to have similar words, and if two docuemnts have similar words, their vector representation will tend to be similar.
- Given the above, this representation is very useful for a task called `Information Retrieval` (IR)
- This task consists of finding the document *d* in a collection of documents *D* that are most like what is specified in a query *q*.

--------

Notas profe:

Dos documentos seran similares cuando compartan palabras, esto cuando se pase a representacion vectorial, sus vectores tambien deberian de ser similares.
Recuperacion de informacion, documentos que sean lo mas parecido a partir de un query o consulta.

-------

## Words as vectors

- Vector space can also be used to represent the "meaning" of words
- THIs is done by associating wach word with a row vector instead of a column vector
- The principle that similar documents have similar vectors also applies to words, where similar words have similar vectors since they tend to occur in similar documents.
- AN alternative to this representation is to label the columns with words instead of documents.
- The words used inn the columns represent the `cooccurrence` of the row words within the context of the


----------

Notas profe

Usando la misma representacion vectorial ahora se asocia cada palabra con los documentos en donde aparece cada palabra.
Se puede tener la palabra "gol" y la palabra "futbol" asi tanto como "inflacion" y "cantante", entones si se habla de palabras similares, como gol o anotacion, deberian
de aparecer en documentos similares, como de deportes, etc. de tal forma que estan mas cercanas las palabras gol y anotacion que las otras ya que suelen aparacer en los
mismos documentos planteando esta idea del principio podemos plantear la similitud o cercania de palabras en un documento.

EL contexto nos sirve para "des ambiguar" sin el contexto no podemos definir a que se refiere algo (como banco) es una ventana de cocurrencia y esa ventana se define
a partir de una cantidad de palabras hacia la izquierda o a la derecha.

Tomando solo el vocabulario, como renglones y columnas se tendria el vocabulario unicamente, lo que se hace es buscar que palabras "coocurren" con una palabra, por ejemplo,
con "are" se tendria uno a la izquierda y n a la derecha. Tambien me pueden aproximar a identificar que palabras son mas cercanas a otras. Palabras similares tienen contexto
similareslas palabras mas cercanas estaran rodeadas de mas o menos las mismas palabras, por ejemplo, si se habla de computadora y programa, no son sinonimos pero no solamenta
van a ocurrir o van a presentarse en los mismos documentos si no que ademas cuando veamos las palabras que rodean a estas dos palabras, tambien estaran mas o menos similares
sus contextos, por ejemplo "software de compuradora", "crear un programa", "lengua de programacion para realizar un programa", etc. Otas palabras como oido, construccion no van a
rodear a compuradora o programa. Documentos similares tienen palabras similares, palabras similares tienen un contexto similar.

Es importante definir esta similitud para poder recuperar un documento, la comparacion es entre la query y el contenido del documento y recuperar el mas parecido.

------

## Weight of terms in vectors

- Frequency in vectors can ve very biased and not very discrimimnative.
- In a document about fruits, words like *cherry* and *strawberry* might appear, while in a document about computers, words like *computers* and *program* might appear.
- These high frequency words can be discriminative.
- However, words like great and good may appear with the same frequency in both documents, but they do not help to discriminate
- The same happens with the word good in Shakespeare's plays
- Words that appear frequently near other words (red near apple) are more important than other words that appear once or twice.
- However, words that are very frequent like good are not as important
- How to solve this conflict
- AN algorithm that can help in this problem is *tf-idf*

--------------

Palabras con altas frecuencias muy significaticas y alto poder de discriminacion. en ambargo hay algunas palabras que no son stop-words.

Se tiene que buscar una forma de identificar las palabras dentro del documento, y una forma es asignarle un peso a estas palabras, indicando la importancia de la palabra, una
cosa es cuantas veces se usa, pero otra es que tan relevante es en el documento. Se tiene que hacer una ponderacion.

Palabras como battle a pessar de su frecuencia tengan mas peso, se tienen que identificar las palabras con mayor poder de discriminacion, no por su frecuencia.

----------------









