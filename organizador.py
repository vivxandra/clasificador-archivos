import pathlib


CATEGORIAS = {
    "Imagenes": [".jpg", ".png", ".jpeg"], "Libros": [".pdf", ".epub"], "Docs": [".docx", ".xml", ".pptx"], "Video": [".mp4"]
}
DESGLOSE = {}

for categoria, extensiones in CATEGORIAS.items():
    for extension in extensiones:
        DESGLOSE[extension] = categoria
            

print(DESGLOSE)

def clasificar_archivo(nombre_archivo):
    nombre_archivo = nombre_archivo.lower()
    return DESGLOSE.get(pathlib.Path(nombre_archivo).suffix, None)
print(clasificar_archivo("imagen.jpg"))


