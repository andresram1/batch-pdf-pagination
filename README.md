
# Paginación de múltiples PDF - batch pdf pagination

## Intro

This is a very small project for numbering pages in multiple PDF files according to a file defintion.
- It requires a file definition where the name (Or pattern) of the PDF file is exposed
- The staring page number to be added to the PDF file

This is just a demo project that can be used and refined for advanced configurations.

## Introducción

Este es un pequeño proyecto de ejemplo para incluir una paginación en un grupo considerable de archivos PDF. 
La paginación se realiza teniendo en cuenta un archivo genérico de enumeración que indica:
- El nombre del archivo que se debe paginar.
- El número de página inicial con que debe iniciar la paginación dicho archivo.

Varios proyectos comerciales (e.g. Acrobat) no resuelven este problema del todo ya que:
- Son comerciales y pueden ser costosos.
- Rara vez se utiizan estas características.
- No hacen paginación teniendo en cuenta los archivos previos


## Instalación

Instalar los requerimientos

```bash
pip install -r requirements.txt
```

## Ejecución

Considere las variables de entorno para ejecución

```bash
export FOLDER_PATH=/path/to/folder/of/pdf
export CSV_PATH=/path/to/csv/file
```

Y listo, ejecute el programa


## Comandos útiles de Unix para manipular los archivos


```bash
# Lista los archivos por orden de creación y agrega un prefijo enumerando los archivos
ls -tv --time=birth *_numbered.pdf | cat -n | while read n f; do mv -n "$f" `printf "%04d_%s" $n $f`; done

# Crea un ZIP con los archivos previamente listados y modificados
zip -9 results.zip *_numbered.pdf

# Parte el ZIP en porciones de un tamaño específico. En este caso, 19.5 MB
zipsplit -s -n 19500000 results.zip

# Para eliminar los prefijos previamente configurados
for f in *_numbered.pdf; do mv "$f" "$(echo "$f" | sed 's/\([0-9]\{4\}\_[0-9]\{1\}_\)//')"; done

# Para eliminar un sufijo
for f in *_numbered.pdf; do mv "$f" "$(echo "$f" | sed 's/\_numbered//')"; done


```