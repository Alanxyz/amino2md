# amino2md
Script para descargar blogs de Amino en formato Markdown.

Amino es una plataforma horrible. La idea de este script es ayudar en la tarea de migrar el contendo a algun lugar mejor. Para esto, una recomendacion es usar [pandoc](https://github.com/jgm/pandoc) para convertir entre formatos de documentos si se desaea distribuir el contenido como archivo, y [markdown-it](https://github.com/markdown-it/markdown-it) para integrar los blogs en un una pagina web. Probablemente se tengan que hacer ligereas modificaciones dependiendo la variacion de Markdown a usar.


### Instalacion

```bash
git clone https://github.com/AstralCam/amino2md
cd amino2md
python3 amino2md.py -h
```

### Ejemplos

**Descarga de un solo blog**

Link del blog indicado en `-u`

```bash
python3 amino2md.py -u https://aminoapps.com/c/comunity/page/blog/title/id
```

**Descarga de varios blogs**

```bash
python3 amino2md.py -f my_blogs.txt
```

Donde `my_blogs.txt` es un archivo de texto con links de blogs, uno en cada linea.
