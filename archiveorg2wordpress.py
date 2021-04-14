# scrap-post.py por pablo castelo 7-7-2020
# Escapeador Wordpress <5.0 desde archive.org
# LLamar con bash #/bin/bash for f in $(find websites/ -name *.html); do python3 scrap-post.py -f $f; done
# Para usarse con wayback_machine_downloader https://github.com/hartator/wayback-machine-downloader
# l25: credenciales wordpress de destino
# l38 l47 l64: elementos a scrapear
# l48 l50 l52 l54: Cadenas de texto a filtrar
# l88: Carpeta contenedora, l133: Periodo de tiempo
# l128: Categoria del post a insertar

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client
import random
import time
from bs4 import BeautifulSoup
from PIL import Image
import argparse
import socket
from datetime import datetime, timedelta

#Establece a donde conectarse antes de los bucles. Imagenes lo requiere para subir las mismas
wordpress = Client('http://example.com/xmlrpc.php', 'user', 'pass')


#Obtiene el archivo a procesar de la linea de comandos.
#LLamar con bash #/bin/bash for f in $(find websites/ -name *.html); do python3 scrap-post.py -f $f; done
parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

#Inicia el parseador de HTML con el archivo a procesar de la linea de comandos
soup = BeautifulSoup(open(args.file), "html.parser")

#Bucles titulo, texto[], etiquetas[], imagenes[]. Se asume que sólo hay un titulo
for titulo in soup.find_all('h2', {'class' : 'sing'}):
    try:
        titulo_post = titulo.text
        print ("OK Titulo")    
    except NameError:
        print ("WW Titulo NameError")
        pass

texto_post = []
for texto in soup.find_all('p'):
    if texto.text == 'cadena_texto':
        pass
    elif texto.text == 'cadena_texto':
        pass
    elif texto.text == 'cadena_texto':
        pass
    elif texto.text == '\n':
        pass
    else:
        try:
            texto_post.append(texto.text + '\n');
            print ("OK Texto")
        except:
            pass

tag_post = []
for tag in soup.find_all('a', {'rel' : 'category tag'}):
    try:
        tag_post.append(tag.text);
        print ("OK etiquetas")
        print(str(tag_post))
    except:
        pass

#Saca las imagenes, les pone el nombre del titulo, le cambia los espacios por guiones(WP), añade unos cutre-numeros0123, guarda las imagenes
#Mete la respuesta del wordpress a un array(response, tipo dict), se queda de forma ineficiente con la primera imagen para usar de featured-WP
# response == {
#       'id': 6,
#       'file': 'picture.jpg'
#       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
#       'type': 'image/jpeg',
# }
identificador_imagen = 0
enlaces_imagenes = []
#No se bien porqué esto funciona bien en todos los casos. Sin titulo da NameError y es antibug?
nombre_archivo = titulo.text
for imagen in soup.find_all('img'):
    try:
        imagen_url= imagen['src']
        #El enlace es a la URL original, pero hemos replicado la estructura en disco; se reemplaza
        imagen_url_disco = Image.open(imagen_url.replace("http://", "$HOME/Escritorio/websites/"))
        print ("OK imagen")
        nombre_archivo = nombre_archivo.replace(' ', '-') + str(identificador_imagen)
        identificador_imagen +=1
        imagen_url_disco.save('%s.jpg' % nombre_archivo)
    except FileNotFoundError:
        print ("WW imagen FileNotFound")
        pass
    except NameError:
        print ("WW imagen NameError")
        pass
    else:
        with open((nombre_archivo + '.jpg'), 'rb') as img:
            data = {
            'name': (nombre_archivo + '.jpg'),
            'type': 'image/jpeg',  # mimetype
            }
            data['bits'] = xmlrpc_client.Binary(img.read())
            #enlaces_imagenes.append(nombre_archivo + '.jpg')
            enlaces_imagenes.append(wordpress.call(media.UploadFile(data)))
            print ("OK Subiendo imagen")
            attachment_id = enlaces_imagenes[0]['id']
                       
#Calcula una fecha aleatoria dentro de los próximos 2 años
comienzo = datetime.now()
fin = comienzo + timedelta(days=730)
fecha = comienzo + (fin - comienzo) * random.random()

#Genera el post wordpress, el bucle genera un array con código de enlace de las imagenes que luego se pastea
post = WordPressPost()
post.title = titulo_post
enlace_formateado = []
for enlace in enlaces_imagenes:
    enlace_formateado.append("<figure class=\"wp-block-image size-large\"> " + "<img src=\"" + enlace['url'] + "\" \"alt=\"" + nombre_archivo + "\"" + "class=\"wp-image\"/></figure>")
    
post.content = (''.join(texto_post) + '<br>'.join(enlace_formateado))
post.date = fecha
post.post_status = 'future'
post.terms_names = {
        'post_tag': list(dict.fromkeys(tag_post)),
        'category': ['Categoria'],
}
post.thumbnail = attachment_id
#Sube el post
wordpress.call(NewPost(post))
#wordpress.call(post.EditPost(post.id, post))

























