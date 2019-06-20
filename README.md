# TFG
SISTEMA DE RECOLECCIÓN, ETIQUETADO Y RECUPERACIÓN DE TEXTOS FINANCIEROS

Manual de instalación

instalar anaconda, elegir la distribución adecuada descargandolo de aquí:
https://www.anaconda.com/distribution/#download-section

Una vez instala anaconda, instalaremos las bibliotecas específicas de nuestro proyecto:

-instalar spacy mediante el comando "conda install -c conda-forge spacy"

-instalar modulo igraph :
En linux se puede utilizar directamente 
"pip install python-igraph"
En windows hay que instalarlo mediante el archivo whl que está en la carpeta lib mediante el comando "pip install python_igraph-0.7.1.post6-cp37-cp37m-win_amd64.whl" tambien se proporciona el archivo whl para instalaciones en 32 bits.

-Adicionalmente se ha dejado la librería necesaria para instalar la función para pintar los grafos, 
aunque en el código no se llama a esta función, de querer hacerlo instalar esta librería contenida en lib mediante el comando
"pip install pycairo-1.18.0-cp37-cp37m-win_amd64"

A continuacion para trabajar con la API de elasticsearch hay que instalarla mediante el comando:

"pip install elasticsearch"

El resto de bibliotecas vienen con la instalación predeterminada de anaconda(re,request,sys,os etc)
