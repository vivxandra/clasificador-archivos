import pytest
import pathlib

from organizador import clasificar_archivo
from organizador import obtener_nombre_archivo_unico

CAT = {
    "Imagenes": [".jpg", ".png", ".jpeg"],
    "Libros":   [".pdf", ".epub"],
    "Docs":     [".docx", ".xml", ".pptx"],
    "Video":    [".mp4"],
}
DESGLOSE = {}
for categoria, extensiones in CAT.items():
    for extension in extensiones:
        DESGLOSE[extension] = categoria

def test_jpg_es_imagen():
    assert clasificar_archivo("foto.jpg", DESGLOSE) == "Imagenes"

def test_ext_mayuscula():
    assert clasificar_archivo("documento.PDF", DESGLOSE) == "Libros"

def test_ext_desconocida():
    assert clasificar_archivo("archivo.unknown", DESGLOSE) is None

def test_sin_extension():
    assert clasificar_archivo("archivo", DESGLOSE) is None

def test_vacio():
    assert clasificar_archivo("", DESGLOSE) is None

def test_doble_extension():
    assert clasificar_archivo("archivo.tar.gz", DESGLOSE) is None



def test_nombre_archivo_unico(tmp_path):
    assert obtener_nombre_archivo_unico(tmp_path, "foto.jpg") == "foto.jpg"

def test_nombre_archivo_1(tmp_path):
    (tmp_path / "archivo.txt").touch()

    assert obtener_nombre_archivo_unico(tmp_path, "archivo.txt") == "archivo_1.txt"

def test_nombre_archivo_2(tmp_path):
    (tmp_path / "archivo1.txt").touch()

    assert obtener_nombre_archivo_unico(tmp_path, "archivo1.txt") == "archivo1_1.txt"
