import pathlib
import json
import argparse
import logging

def parse_arguments():
    parser = argparse.ArgumentParser(description="Organizador de archivos por categorías.")
    parser.add_argument("--dry-run", action="store_true", help="Simula la organización sin mover archivos.")
    return parser.parse_args()

            
def cargar_categorias():
    CATEGORIAS = {
        "Imagenes": [".jpg", ".png", ".jpeg"],
        "Libros": [".pdf", ".epub"],
        "Docs": [".docx", ".xml", ".pptx"],
        "Video": [".mp4"]
        }
    try:
        with open("categorias.json", "r") as archivo:
            CATEGORIAS = json.load(archivo)
            return CATEGORIAS
    except FileNotFoundError:
        print("El archivo categorias.JSON no se encontró. Se utilizarán las categorías predeterminadas.")
        return CATEGORIAS
    except json.JSONDecodeError:
        print("Error al decodificar el archivo categorias.JSON. Se utilizarán las categorías predeterminadas.")
        return CATEGORIAS
        
def organizar_categorias(CATEGORIAS):
    DESGLOSE = {}
    for categoria, extensiones in CATEGORIAS.items():
        for extension in extensiones:
            DESGLOSE[extension] = categoria
    return DESGLOSE

def clasificar_archivo(nombre_archivo, DESGLOSE):
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


def mover_archivo(archivo, carpeta_destino, dry_run=False):
    nombre_archivo_unico = obtener_nombre_archivo_unico(carpeta_destino, archivo.name)

    if dry_run:
        logger.info(f"[DRY RUN] Archivo {archivo.name} se movería a {carpeta_destino}")
        return
    try:
        archivo.rename(carpeta_destino / nombre_archivo_unico)
        logger.info(f"Archivo {archivo.name} movido correctamente a {carpeta_destino}")
        return
    except FileNotFoundError as e:
        logger.error(f"Archivo no encontrado al mover {archivo.name}: {e}")
    except PermissionError as e:
        logger.error(f"Permiso denegado al mover {archivo.name}: {e}")

def organizar_archivos(ruta, DESGLOSE, dry_run=False):
    for archivo in ruta.iterdir():
        if archivo.is_file():
            categoria = clasificar_archivo(archivo.name, DESGLOSE)
            if categoria:
                if dry_run:
                    logger.info(f"[DRY RUN] Archivo {archivo.name} se moveria a la carpeta {categoria}")
                    return
                carpeta_destino = ruta / categoria
                carpeta_destino.mkdir(exist_ok=True)
                mover_archivo(archivo, carpeta_destino, dry_run)



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler('organizador.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)


if __name__ == "__main__":
    args = parse_arguments()
    dry_run = args.dry_run
    CATEGORIAS = cargar_categorias()
    DESGLOSE = organizar_categorias(CATEGORIAS)
    ruta = obtener_ruta()
    organizar_archivos(ruta, DESGLOSE, dry_run)



