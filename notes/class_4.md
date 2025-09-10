# 

> Notas profe: de vez en cuando puede que en el texto existan acentos, entonces, es mejor dejarlo con un comodin para poder procesar esa parte
  con el analizador (la expresion regular)
  Grupos con captura, en donde se puede sacar lo que se esta buscando.
  .group(0) tomara el primer encontrado y .group(1) sera lo que se encuentre dentro de los parentesis (en el ejemplo).

## Text Normalization

- Before any task youu want to perform with the text, it is important to apply a process called normalization 

## Lemmatization

- Words can present variatios in their form, but refer to the same idea (inflections)
- The noun fato can have any of the following variations:
    - gata
    - gatos
    - gatas
- All these variations refer to the same thing, a feline animal.
- The process of lemmatization makes it possible to obtain the same form (lemma) for the different inflections of a word.
    - for nouns, the singular form is used
    - for verbs, it is changed to their singular infinitive form
- For these tasks, tools such as those already mentioned in class are used
- Next, an example will be reviewed with the `Spacy tool`.

> Notas profe: Hay varias herramientas, sugirio que podemos buscar mas herramientas, estanddo en python se puede instalar directamente
  esta herramienta para poder procesar el texto primero le tenemos que indicar el idioma con el que vamos a trabajar.
  Es instalar la biblioteca para importarla, y aparte se tiene que instalar otro recurso, el cual es el diccionario para trabajar con el
  idioma español (con gestores con conda, se puede descargar el modelo para trabajar con español). Se trabajara sobre un modelo que se
  trabajo sobre noticias, la cual es la version `small` (este modelo se entreno con noticias para que aprendiera a tokenizar, etc.)
  Asi como el español soporta mas idiomas, como el ingles, el frances, etc. Siempre que se trabaje con spacy se tiene que bajar el modelo,
  dependiendo de la version tendra diferentes tamaños (peso). Instalar biblioteca y recursos con los que trabajara la biblioteca.
  Ya importada la biblioteca, tenemos que cargar el recurso, y si esta cargado, este lo subira a la memoria, para despues crear un objeto
  Con `nlp` se optiene un documento "doc" en donde nos retornara los tokens de la cadena. COn esto podemos iterar y obtener: el texto, la etiqueta 
  y el lemma.
  Cuando detectamos un error tenemos que hacer un posprocesamiento, por ejemplo, en el signo de $ lo toma como un pronombre, pero eso esta 
  incorrecto.
  La etiqueda dep indica analisis *sintactico de dependencia*, este junta los sintagmas y dice la relacion entre un sintagma y otro, ya que ahi
  puede decir que depende de cada cosa, ayuda mejor verlo de forma grafica, esto indica por ejemplo, quien realiza una accion (el sujeto) y un
  auxiliar porque no corre por correr, ahora, no corre en cualquier lugar, tambien describe en donde, seguido puede describir el lugar donde
  se encuentra donde esta corriendo, etc. Entonces, esta hanlandp sobre como se relacionan los sintagmas, esto podria servir para una aplicacion de
  preguntas y respuestas, la accion principal lo diria "root", de ahi se puede preguntar quien realiza la accion (noun-subject) en donde se realiza (objeto),
  propiedades del objeto, etc. Esto a fin de cuentas es un arbol, se puede ir navegando y a partir de las etiquetas se pueden obtener relaciones a partir
  de estas etiquetas, una vez encontrado la accion, se pueden dar detalles de la accion y propiedades de cada cosa. Si se agregan detalles en el texto. La 
  parte mas importante siempre es la accion, quien la realiza y donde la realiza, y las conexiones dan mas detalle a estas conexiones.
  Las entidades nombradas se refieren a un concepto (por ejemplo Instituto Politecnico Nacional) que se refieren a una sola entidad, los sistemas tienen
  que ser capaces de detectar esto. Las entidades nombradas se apoyan mucho de las reglas de escritura. Por ejemplo, mientras siguen siendo mayusculas, 
  entonces el algoritmo sigue pensando que lo que sigue sigue siendo parte de la entidad, funciona bien, excepto en redes sociales
  `Analisis sintactico de constituyentes`, tiene limitantes, ya que crea grupos que suelen ser conflictivos, por ejemplo, generan sintagmas
  en el cual pone la relacion entre dos palabras, pero no indica exactamente cual es la relacion entre estos.
  La recomendacion para el caso de stop words, nosotros debemos de crear nuestras listas, para poder apoyar esta parte, si notamos que no son utiles
  los adverbios, adjetivos, etc, identificandolos en los resultados, podemos modificarlo para poder quitar o agregar cosas, construyendo una funcion que
  quite estos words basado en la parte gramatical de las palabras.

## Text representation

- Once the text has been normalized, the next step is to find a suitable representation for information extraction or machine learning algorithms.
- For example, supervised learning

> Notas profe: Si se utiliza un algoritmo de machine learning, etc, los datos deben de tener una cierta estructura, normalmente es una lista de caracteristicas y 
  los valores asociados a esas caracteristicas, por ejemplo si se tiene un dato de un paciente:
  pacientes   edad   Genero  Tipo sanguineo  Peso  altura  Diabetes  Hip  NIvel colesterol
     1	       30      M          O+	      70    1.7      No      Si       Medio
     2         

  La informacion se puede utilizar para caracterizar a los pacientes y se puede utilizar para predecir algo, pacientes en riesgo, con enfermedad, etc, puede
  predecir esto, una matriz tabular donde se tiene una tabla con renglones y se tienen  rangos que son las columnas, el problema es que se esta trabajando con
  texto   






















