import pathlib


CATEGORIAS = {
    "Imagenes": [".jpg", ".png", ".jpeg"], "Libros": [".pdf", ".epub"], "Docs": [".docx", ".xml", ".pptx"], "Video": [".mp4"]
}
DESGLOSE = {}

for categoria, extensiones in CATEGORIAS.items():
    for extension in extensiones:
        DESGLOSE[extension] = categoria
            

def clasificar_archivo(nombre_archivo):
    nombre_archivo = nombre_archivo.lower()
    return DESGLOSE.get(pathlib.Path(nombre_archivo).suffix, None)
print(clasificar_archivo("imagen.jpg"))

def obtener_ruta():
    ruta = input("Ingrese la ruta del directorio: ")
    ruta = pathlib.Path(ruta)
    while not ruta.is_dir(follow_symlinks=True):
        print("La ruta no es una carpeta. Por favor, ingrese una ruta válida.")
        ruta = input("Ingrese la ruta del directorio: ")
        ruta = pathlib.Path(ruta)
    return ruta

print(obtener_ruta())


