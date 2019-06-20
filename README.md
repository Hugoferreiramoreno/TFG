# TFG
SISTEMA DE RECOLECCIÓN, ETIQUETADO Y RECUPERACIÓN DE TEXTOS FINANCIEROS

Manual de instalación

instalar anaconda, elegir la distribución adecuada descargandolo de aquí:
https://www.anaconda.com/distribution/#download-section

Una vez instala anaconda, instalaremos las bibliotecas específicas de nuestro proyecto:

-instalar spacy mediante el comando "conda install -c conda-forge spacy"
 a continuación para descargar el paquete de español, ejecutar el siguiente comando
 "python -m spacy download es"
 
-instalar modulo igraph :
En linux se puede utilizar directamente 
"pip install python-igraph"
En windows hay que instalarlo mediante el archivo whl que está en la carpeta lib mediante el comando "pip install python_igraph-0.7.1.post6-cp37-cp37m-win_amd64.whl" tambien se proporciona el archivo whl para instalaciones en 32 bits.

-Adicionalmente se ha dejado la librería necesaria para instalar la función para pintar los grafos, 
aunque en el código no se llama a esta función, de querer hacerlo instalar esta librería contenida en lib mediante el comando
"pip install pycairo-1.18.0-cp37-cp37m-win_amd64"

 A continuacion para trabajar con la API de elasticsearch hay que instalarla mediante el comando:

"pip install elasticsearch"

 Debido al tamaño de los indices de babelnet no se han podido adjuntar al fichero, por favor descargarlos del siguiente enlace:
 http://lcl.uniroma1.it/nasari/files/NASARI_lexical_spanish.zip
  
 Personalmente he dejado el texto resultante en data.El modulo que lo transforma en JSON toma la dirección absoluta del archivo por lo tanto no debería influir la ubicación del archivo, pero se aconseja dejarlo junto a los otros textox.
 
A continuación, instalar la aplicación de Elasticsearch, del siguiente enlace:
https://www.elastic.co/es/downloads/elasticsearch
Se ha elegido la aplicación en MSI, para el proyecto implantado es más que suificiente, además permite cierto grado de configuración a la hora de instalarlo.
Para configuraciones más específicas (por ejemplo si se quiere añadir RAID o mejorar ciertos aspectos del rendimiento) hay que descargar la versión en formato ZIP, en el siguiente enlace podréis encontrar información al respecto.
https://www.elastic.co/guide/en/elasticsearch/reference/7.1/getting-started-concepts.html -> Explicación de las configuraciones
https://www.elastic.co/guide/en/elasticsearch/reference/7.1/getting-started-install.html -> Detalle de la instalación

Finalmente, para lanzar el servicio simplemente acceder por consola a la carpeta donde lo hayamos descargado, a continuación ir a la carpeta bin, y desde ahí ejecutar el comando "elasticsearch". Añadimos la información de instalación,configuración y ejecutación por si se quisiese optimizar la herramienta.
