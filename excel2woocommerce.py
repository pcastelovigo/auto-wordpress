#excel2woocommerce V1.0, por PABLO MANUEL CASTELO VIGO, 04-09-2020 A CORUÑA 

from woocommerce import API
import json
import xlrd

#CONEXIÓN API WOOCOMMERCE
wcapi = API(
    url="url",
    consumer_key="ck_000000000000000000000000000000000",
    consumer_secret="cs_0000000000000000000000000000000000",
    version="wc/v3"
)

#NOMBRE DEL EXCEL A CARGAR
excel = ("test.xlsx")
wb = xlrd.open_workbook(excel) 
sheet = wb.sheet_by_index(0) 
  
# DESDE COLUMNA,LINEA 0,0 -- VARIAR PARA PERMITIR MARCOS
sheet.cell_value(0, 0) 
  
#PARA CADA LINEA, SUBE LA CATEGORIA, SI NO EXISTE LA CREA, SI YA EXISTE LO MANEJA, LUEGO SE REESCRIBE EL VALOR 'DATA' Y SUBE EL PRODUCTO
for i in range(sheet.nrows):
    carta = sheet.row_values(i)
    data = { "name": carta[4] }
    insertar_categorias = wcapi.post("products/categories/", data).json()
    if 'id' in insertar_categorias.keys():
        categoria = insertar_categorias["id"]
        print("categoria creada num " + str(categoria))
    else:
        print(insertar_categorias["data"]["resource_id"])
        categoria = insertar_categorias["data"]["resource_id"]
        print("categoria ya existe! num " + str(categoria))
    data = {
    "name": carta[0],
    "type": "simple",
    "regular_price": str(carta[1]),
    "description": carta[2],
    "short_description": carta[3],
    "categories": [
        {
            "id": categoria
        }
    ] }
    print("producto introducido! producto " + carta[0] + ' precio ' + str(carta[1]) + ' descripcion ' + carta[2] + ' descripcion corta ' + carta[3] + " categoria " + str(categoria))
    wcapi.post("products", data).json()


#JSON PARA AÑADIR IMAGENES
#,
#    "images": [
#        {
#            "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_2_front.jpg"
#        },
#        {
#            "src": "http://demo.woothemes.com/woocommerce/wp-content/uploads/sites/56/2013/06/T_2_back.jpg"
#        }
#    ]



