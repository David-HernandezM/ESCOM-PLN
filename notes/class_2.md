# Natural language systems and applications

## Tarea de la clase pasada:

- What natural language applications are you familiar with?
- Do you consider  the performance of these systems to be good, why yes or why not?
    - Respuestas:
    - 

- What difficulties do these applications face?
- What improvements can be made to these systems?
- Describe a natural language processing application that you would like to develop during the course.

Nos podriamos conectar o en su caso comunicar de manera mas fluida, de manera coloquial, etc.

## Text normalization

- Before any task you want to perform with the text, it is important to apply a process called normalization
- This process generally involves the following tasks:
    - Tokenization
    - Stop words
    - POS Tagging
    - Lemmmatization

> Notas profe: UNo de los primeros retos es, tengo el lenguaje, lo puedo representar con una secuencia de caracteres, como hago 
que la maquina lo pueda procesar, para esto se tiene que hacer una seria de transformaciones para poder adaptarlo y tener una
representacion para que la computadora pueda procesarlo, antes de ejecutar cualquier tarea se tienen que hacer transformacionoes
al texto el cual lleva por nombre *NORMALIZACION*, esto toma el texto crudo (libro, etc) y le hara unas transformaciones, no es
una receta de cocina, ni una regla establecida, pero casi siempre al normalizar se aplican la reglas listadas anteriores (Tolenizacion,
parada de palabras, etc) estas son algunas de las tareas a la que se le aplicaran al texto, estas son las que tienen contacto direecto
con el texto "crudo", ya que lo transforma.

## Tokenization

- One of the first tasks for text normalization is to separate the words and sentences they contain
- In many languages such as Spanish, the words of a sentence are separated by a blank space
- Example:
    - El procesamiento de lenguaje natural es un area de la inteligencia artificial muy relevante hoy en dia
- Separating the previous sentence into words would leave a vector with the following content:
    - ['El', 'procesamiento', 'de', 'lenguaje', ... ]
- How would you implement a program that separates words in a text?
- However, there may be characters other than whitespace that are also user to separate words
    - La tokenizacion es una texnica que permite, entre otras cosas, el separar el texto en las palabras que lo componen. Existen herramientas como NLTK
      que implementan toekenizadores
- *What other characters do you thing you can use to separate words in a text?*
- *What adjustments shoul you make to the above program to consider these new separators?*
- Some characters used for word separation sometimes do not have this functionality
    - El costo de este telefono es de $10,000.36
- *What can we do to solve this problem?*
- In some languages, words are not separated by a character
    - *PALABRAS EN CHINO*
    - *HORACION EN CHINO*
    - Subcadena comun mas larga, agregando texto hasta hacer match ocn un significado
- How would you apply tokenization?
- https://www.atilika.org/

> Notas profe: Es pasar de la representacion original del texto, a una representacion que se identifique los componentes minimos que ya no 
se pueden separar.


## Regular expressions

- Regular expressions are a language for specifying text search strings
- They are very useful to search for strings when you have a defined pattern *IMPORTANTE*
-  The function that implements the regular expression will search for strings that match the established pattern and return them
- There are many variants of the regular expression language, so you should choose the language of your preference to use them

> Nota profe: Serie de secuencia de caracteres que tienen una regularidad, si carecen de esa regularidad no se puede resolver con una expresion regular.
  Podemos buscar en este cadena siempre y cuando exista un patron definido
  Se vera un esquema generico, pero cuando se vaya a python, tenemos que ver expecificaciones para ver unas variantes de la expression regular.

## Basic regular expressions:

|Pattern  | Description|
|:-------:|:-------------------------------:|
| a	  | Matches with the character 'a'|
| abc	  | Matches with the string 'abc'|
| [abc]   | Matches with 'a', 'b' or 'c'|
| [^abc]  | Matches anu character except 'a', 'b' and 'c'|
| abc|def | Matches with 'abc' or 'def'|

# Character classes

Pattern  Description
\d	 Matches with one digit
\D 	 Matches a non-digit character
\w 	 Matches an alphanumeric character (including the '_' character)
\s	 Matches the space character
	 Matches anu character except line break (el pattern era un punto)
[a-z]	 Matches with a character from the sequence 'a' to lowercase 'z'
[A-Z] 	 Matches whit a character from the sequence 'A' to uppercase 'Z'
[0-9] 	 Matches one digit of these sequence from 0 to 9, equivalent to the pattern \d

> Notas profe: EL primer examen escrito pedira expresiones regulares para resolver algo, utilizando lo anterior
  Ejemplo: [a-zA-Z], en este son de 'a' a 'z' o 'A' a 'Z'

## Quatrifiers

Pattern  Description
*  	 Matches 0 or more times
+	 Matches 1 or mor times
?	 Matches 0 or 1 time
{3}	 Matches exactly 3 times
{3,6}	 Matches from 3 to 6 times
{3,}     Matches 3 or more times
{,6}	 Matches up to 6 times

> Notas profe:  los ultimos 4 se ponen a la izquierda de la condicional

## Regular expressions in Python

- Python provides a library called *re* where the following functions are implemented:
    - re.search()
    - re.

### re.search()

- This function checks whether there is a match anywhere in the string
- It receives the parameters pattern and string
- Example: 
    ```python
    import re
    res = res.search("c", "abcdef")
    print(res)

    # Result: <re.Match object; span=(2,3), match='c'>
    ```

> Notas profe: span indica en que posicion de la cadena se encontro el empate (match), si no, retornara un None, si no es None y es un
  objeto es que re si encontro algo
  Encuentra solo la primer aparicion

### re.findall()

- Get a list of all the strings that match a pattern
- Receives pattern and string parameters
- Example:

```pyton
import re
result = re.findall("\s", "Esta es una cadena.")
print(result)

# Result: retornara una lista de todo lo que encontro (es deccir, el patron dadp)
```

> Notas profe: si no encuentra nada findall este retornara una lista vacia

re.split()

- This method separates a string by matching the established pattern
- Receives pattern and string parameters
- Example

```python
import re
result = res.split("\s", "Esta es una cadena.")
print(result)

# Result: ["Esta", "es", "una", "candena"]
```

> Notas profe: Lo unico que hara es que cuando encuentre un patron, separara el string borrando el match
  Si no encuentra nada, retornara la cadena original dentro de una lista.

### res.sub()

- jSearches for a pattern and replaces ir with the specified string
- Receives a pattern, repl and string parameters
- Example

```python
import re
result = re.sub("\s", "\n", "esta es una cadena.")
print(result)

# Resultado: Sera la misma cadena, pero reemplazando los espacios con saltos de linea
```

> Notas profe: este retorna como tal un string, no retorna una cadena, solo reemplazo un caracter por otro

### re.compile()

- Creates a pattern object wich can ve used in a regular expression as a search pattern
- Receives pattern, repl and string parametes
- Example

```python
patron = re.commpile(",") # Se creo un objeto patron
resultado = patron.findall("Cadena1, Cadena2, Cadena3, Cadena4")
print(resultado)
resultado2 = patron.split("Cadena1, Cadena2, Cadena3, Cadena4")
print(resultado2)
```

> Notas profe: un patron es una estructura que estoy buscando, su ventaja es que podemos tener acceso a todas las funciones que hay en la
  biblioteca de re
  Lo que hace es unicamente guardar la expression regular a buscar, asi, ya no se pondria el primer argumento en las funciones re el cual es
  el patron a buscar, a eso se refiere con poder reutilizarlo,


















