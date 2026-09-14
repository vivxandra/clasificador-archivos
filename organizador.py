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


def obtener_ruta():
    ruta = input("Ingrese la ruta del directorio: ")
    ruta = pathlib.Path(ruta)
    while not ruta.is_dir(follow_symlinks=True):
        print("La ruta no es una carpeta. Por favor, ingrese una ruta válida.")
        ruta = input("Ingrese la ruta del directorio: ")
        ruta = pathlib.Path(ruta)
    return ruta

def obtener_nombre_archivo_unico(carpeta_destino, nombre_archivo):
    contador = 1
    nombre_archivo_unico = nombre_archivo
    while (carpeta_destino / nombre_archivo_unico).exists():
        nombre_archivo_unico = f"{pathlib.Path(nombre_archivo).stem}_{contador}{pathlib.Path(nombre_archivo).suffix}"
        contador += 1
    return nombre_archivo_unico

def organizar_archivos(ruta):
    for archivo in ruta.iterdir():
        if archivo.is_file():
            categoria = clasificar_archivo(archivo.name)
            if categoria:
                carpeta_destino = ruta / categoria
                carpeta_destino.mkdir(exist_ok=True)
                nombre_archivo_unico = obtener_nombre_archivo_unico(carpeta_destino, archivo.name)
                archivo.rename(carpeta_destino / nombre_archivo_unico)
                
                print(f"Archivo {archivo.name} movido a {carpeta_destino}")
            else:
                print(f"Archivo {archivo.name} no pertenece a ninguna categoría.")

if __name__ == "__main__":
    ruta = obtener_ruta()
    organizar_archivos(ruta)



