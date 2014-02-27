##Información
Esta web es solo una muestra de la plataforma que esta en desarrollo y puede no contener la última versión de desarrollo, la base de datos puede ser eliminada en cualquier momento, que la página este caida... Además seguramente la web este llena de bugs y cosas feas, no os asustéis.

He generado una encuesta *¿Como son nuestros voluntarios?* No está entera, por ejemplo faltan preguntas de algun bloque, incluso algun bloque entero, como toda la parte tres con dinero ficticio. Y es mas es la primera vez que genero una encuesta entera y compleja y se observan varios errores de visualizaciones como secciones sin texto, todo poco a poco irá mejorando

A pesar de no estar hecha toda la encuesta, llevo entre 45-60 minutos creándola y eso que me se la página web entera, cuando cree la opcion de copiar esto será mas rápido.
 
###Investigadores
Por ahora cualquiera puede crear una encuesta y editar las encuestas creadas por otros, para ello vamos a **researcher**->New Survey. En Title, pues el título de la encuesta, descripción de la encuesta. Para rellenar este campo se utiliza el lenguaje Markdown, que es una sencilla forma de dar formato a un texto para una pagina web. 

Una vez creada la encuesta, se puende añadir consentimiendos que los usuarios deben aceptar para realizar la encuesta.

**Add section** sirve para añadir una sección a la encuesta, a su vez una sección puede tener mas subsecciones. El campo *Sequence* indica el orden de la sección en la que deseas que aparezca la encuesta. Si dos secciones tienen la mismo Sequence, se eligirá al azar el orden entre las secciones con la misma secuencia.

El campo *percent* indica el porcentaje de usuarios que deseas que pase por esa sección.

Tanto percent como Sequence se aplica a las secciones del mismo nivel y rama.

Ejemplo tenemos este arbol en la encuesta

**Encuesta1**

* seccion1 sequence=1, percent=1
* * seccion 1.2 sequence=1, percent=0.5
* * seccion 1.3 sequence=1, percent=0.5
* seccion2 sequence=2, percent=1
* seccion3 sequence=2, percent=1

Un usuario responderá primero a la seccion1, luego se eligirá al azar si el usuario realiza la seccion1.2 o 1.3 (si realiza la 1.2 no hará la 1.3 y viceversa) Después hará la sección2 o la sección3. si hace primero la sección 2, después hará la 3, si hace primero la 3 luego le tocará la 2


Dentro de cada sección se pueden crear preguntas. Estas pueden ser de distinto tipo:

* **yes/no** preguntas de si o no
* **numerical** en las que esperas una contestación numérica
* **Text** en las que una contestación con texto
* **Choice** Das varias opciones de respuesta al usuario, además en esta cuestiónes deberás indicar el número de opcciones en "number of fileds in..." asi como escribir cada opción en las casillas answer1, answer2...
* **likert scale** para las preguntas con escala, además se puede seleccionar el rango de la escala en los campos "scale" "to", así como dos etiquetas opcionales para el min y el max
* **Part two** pregunta especial para el apartado2, cada pregunta del apartado dos, habrá que indicar que es de este tipo y rellenar las opcciones answer 1 y answer2
* **decision one** pregunta especial para la decisión una del apartado 3, solo habrá que marcar como decision one a la pregunta  de cuanto invierte en esta loteria
* **decision two** pregunta especial para la decisión dos del apartado 3, solo habrá que marcar como decision two a la pregunta  de cuanto invierte en el fondo
* **decision three** pregunta especial para la decisión tres del apartado 3, solo habrá que marcar como decision three a la pregunta  de cuanto invierte en el fondo
* **decision four** pregunta especial para la decisión cuato del apartado 3, solo habrá que marcar como decision four a la pregunta  de cuanto envias al usuario
* **decision five** pregunta especial para la decisión five del apartado 3, habrá que marcar todas las cuestiones como decision five, además de indicar en answer 1 la cantidad de dinero que se le manda al jugador
* **decision six** pregunta especial para la decisión six del apartado 3.

Así mismo el investigador puede seleccionar cual debería de ser la respuesta de control así como el numero maximo de intentos.

###Usuarios
Para poder realizar una encuesta tienen que estar logueados, para ello deben usar algun servicio que implemente openid, como puede ser gmail, facebook, twitter, steam... 

Una vez loggueados pueden ver todas las encuestas disponibles, pinchando en cualquiera se empieza la encuesta. Deberán de aceptar los consentimientos para poder realizar la encuesta. Después se le irá mostrando las distintas secciones (generadas en el orden/orden aleatorio descrito por el investigador)

Una vez finalizada una encuesta no se puede volver a hacer.


###Bugs y otras cuestiones
Hay varios bugs, algunos conocidos y otros desconocidos (da un error feo al borrar una pregutna en la que un usuario ya ha contestado, pero es que esto no debería de pasar, se puede realmente volver a realizar las encuestas ya hechas...)

Los algoritmos de matching ya estan implementados, pero estos hay que realizarlos de una manera bastante manual (ya se automatizara el proceso...)

Aun no se mide el tiempo.

La forma de crear encuestas cambiará seguramente de manera drástica. Los cuestionarios para los usuarios mejorarán en aspecto... Los usuarios aun no pueden dejar una sección a medias (tampoco se si es deseable o no...)

Se añadiran opciones de en que fechas se hace publica una encuesta. Opciones para copiar encuestas/secciones...

Los investigadores tambien tendrán acceso a los resultados via de las encuestas via web

Opciones de encuestas ¿multilenguaje?

Y mas cosas que me dejo en el tintero...

