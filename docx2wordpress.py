from wordpress_xmlrpc import Client, WordPressPost, WordPressPage, WordPressMedia
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
#from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc import AuthenticatedMethod
from wordpress_xmlrpc import WordPressPage
from docx2python import docx2python
#import docx2txt
#import docx
import argparse
from bs4 import BeautifulSoup


wordpress = Client('https://example.com/xmlrpc.php', 'user', 'pass')
parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=True)
parser.add_argument("--id", type=int, required=False)
args = parser.parse_args()

resultadohtml = docx2python(args.file, html=True)
htmltemporal = resultadohtml.text
#####DEBUG
#print(htmltemporal)
#print("***********")
titulo = args.file
titulo = titulo.replace('.docx', '')


soup = BeautifulSoup(htmltemporal, 'html.parser')
for tag in soup('font'):
    if tag['size'] == '36':
        del tag ['size']
        tag.name = "h2"
    elif tag['size'] == '28':
        del tag ['size']
        tag.name = "h3"
    elif tag['size'] == '24':
        tag.unwrap()
    else:
        pass

#ENTRADA DE DATOS PPAL
print("*************")
print("INTRODUCIR ENLACE")
enlace_principal = input()
boton = """<!-- wp:button {"align":"center"} -->
<div class="wp-block-button aligncenter"><a class="wp-block-button__link" href=""" + '"' + enlace_principal + '"' + """ target="_blank" rel="nofollow noopener noreferrer"> Texto </a></div>
<!-- /wp:button --><br>"""
shortcode = "[shortocode func=" + '"' + titulo + '"' + """ opciones="1" mas_opciones="3"]""" + "\n"
guiones = "--"
resultado = str(soup).replace(guiones, "").splitlines(True) # 
resultado.insert( 0, shortcode + boton)

inserciones = []
for linea in resultado:
    #print(linea)
    if linea.startswith("<h2>"):
        inserciones.insert(len(inserciones), resultado.index(linea))
    elif linea.startswith("<h3>"):
        inserciones.insert(len(inserciones), resultado.index(linea))
    else:
        pass
#ENTRADA DE DATOS
contador = 0
for lista in inserciones:
    if contador == 2: break
    print("*************")
    print("INTRODUCIR VARIANTE")
    variante_seo = input()
    print("*************")
    print("INTRODUCIR ENLACE")
    enlace = input()
    variacion1 = '<h3>' + titulo + ' ' + variante_seo  + ' texto</h3>' + "\n"
    variacion2 = '<h3>Novedades en ' + titulo + ' ' + variante_seo  + '</h3>' + "\n"
    shortcodeseo = """[shortcode bestseller=""" + '"' + titulo + ' ' + variante_seo  + '"' + """ items="4" grid="4"]""" + "\n"
    boton = """<!-- wp:button {"align":"center"} -->
<div class="wp-block-button aligncenter"><a class="wp-block-button__link" href=""" + '"' + enlace + '"' + """ target="_blank" rel="nofollow noopener noreferrer"> Texto </a></div>
<!-- /wp:button --><br>""" + "\n"
    if contador == 0:
        resultado.insert(lista + 2, variacion2 + shortcodeseo + boton)
        contador += 1
    elif contador == 1 :
        if len(resultado) > lista + 3:
            resultado.insert(lista + 3 , variacion1 + shortcodeseo + boton)
            contador += 1
        else:
            resultado.insert(len(resultado), variacion1 + shortcodeseo + boton)
    else: break

if len(inserciones) < 2:
    print("*************")
    print("INTRODUCIR VARIANTE")
    variante_seo = input()
    print("*************")
    print("INTRODUCIR ENLACE shortcode")
    enlace = input()
    variacion1 = '<h3>' + titulo + ' ' + variante_seo  + ' en oferta</h3>' + "\n"
    shortcodeseo = """[shortcode funcion=""" + '"' + titulo + ' ' + variante_seo  + '"' + """ opcion="4" otra_opcion="4"]""" + "\n"
    boton = """<!-- wp:button {"align":"center"} -->
<div class="wp-block-button aligncenter"><a class="wp-block-button__link" href=""" + '"' + enlace + '"' + """ target="_blank" rel="nofollow noopener noreferrer"> Texto </a></div>
<!-- /wp:button --><br>""" + "\n"
    resultado.insert(len(resultado), variacion1 + shortcodeseo + boton)
else: pass

       

#print(resultado)
#print("*************")
#print(*resultado, sep = "\n")


page = WordPressPage()
page.id = args.id
page.title = titulo
page.content = ''.join(resultado)
page.post_status = 'publish'
wordpress.call(posts.EditPost(page.id, page))
#wordpress.call(NewPost(page))

