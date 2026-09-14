import pytest
import pathlib
import logging

from organizador import clasificar_archivo
from organizador import obtener_nombre_archivo_unico
from organizador import mover_archivo
from organizador import organizar_archivos

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


# --------------------------
# Tests de mover_archivo
# --------------------------

def test_mover_archivo_mueve_el_archivo(tmp_path):
    origen = tmp_path / "foto.jpg"
    destino = tmp_path / "Imagenes"
    destino.mkdir()
    origen.touch()

    mover_archivo(origen, destino)

    assert not origen.exists()
    assert (destino / "foto.jpg").exists()


def test_mover_archivo_renombra_si_destino_existe(tmp_path):
    destino = tmp_path / "Imagenes"
    destino.mkdir()
    (destino / "foto.jpg").touch()
    origen = tmp_path / "foto.jpg"
    origen.touch()

    mover_archivo(origen, destino)

    assert not origen.exists()
    assert (destino / "foto.jpg").exists()
    assert (destino / "foto_1.jpg").exists()


def test_mover_archivo_dry_run_no_mueve(tmp_path):
    origen = tmp_path / "libro.pdf"
    destino = tmp_path / "Libros"
    destino.mkdir()
    origen.touch()

    mover_archivo(origen, destino, dry_run=True)

    assert origen.exists()
    assert list(destino.iterdir()) == []


def test_mover_archivo_inexistente_logs_error(tmp_path, caplog):
    origen = tmp_path / "no_existe.pdf"
    destino = tmp_path / "Libros"
    destino.mkdir()

    with caplog.at_level(logging.ERROR):
        mover_archivo(origen, destino)

    assert not (destino / "no_existe.pdf").exists()
    assert "Archivo no encontrado" in caplog.text


def test_mover_archivo_permiso_denegado_logs_error(tmp_path, caplog):
    destino = tmp_path / "Libros"
    destino.mkdir()

    class ArchivoSinPermiso:
        name = "doc.pdf"

        def rename(self, target):
            raise PermissionError("simulado")

    with caplog.at_level(logging.ERROR):
        mover_archivo(ArchivoSinPermiso(), destino)

    assert "Permiso denegado" in caplog.text


def test_mover_archivo_logs_movimiento_exitoso(tmp_path, caplog):
    origen = tmp_path / "doc.pdf"
    destino = tmp_path / "Libros"
    destino.mkdir()
    origen.touch()

    with caplog.at_level(logging.INFO):
        mover_archivo(origen, destino)

    assert "movido correctamente" in caplog.text


# --------------------------
# Tests de organizar_archivos
# --------------------------

def test_organizar_archivos_clasifica_y_mueve(tmp_path):
    (tmp_path / "foto.jpg").touch()
    (tmp_path / "libro.pdf").touch()
    (tmp_path / "archivo.xyz").touch()

    organizar_archivos(tmp_path, DESGLOSE)

    assert (tmp_path / "Imagenes" / "foto.jpg").exists()
    assert (tmp_path / "Libros" / "libro.pdf").exists()
    # Sin categoría conocida: se queda en la raíz
    assert (tmp_path / "archivo.xyz").exists()


def test_organizar_archivos_crea_carpetas_de_categoria(tmp_path):
    (tmp_path / "foto.png").touch()
    (tmp_path / "documento.docx").touch()
    (tmp_path / "video.mp4").touch()

    organizar_archivos(tmp_path, DESGLOSE)

    assert (tmp_path / "Imagenes").is_dir()
    assert (tmp_path / "Docs").is_dir()
    assert (tmp_path / "Video").is_dir()


def test_organizar_archivos_dry_run_no_mueve(tmp_path):
    (tmp_path / "foto.jpg").touch()
    (tmp_path / "libro.pdf").touch()

    organizar_archivos(tmp_path, DESGLOSE, dry_run=True)

    # Los archivos NO se mueven. (Nota: el código actual sí crea las
    # carpetas de categoría con mkdir() aunque sea en modo dry-run).
    assert (tmp_path / "foto.jpg").exists()
    assert (tmp_path / "libro.pdf").exists()
    assert not (tmp_path / "Imagenes" / "foto.jpg").exists()
    assert not (tmp_path / "Libros" / "libro.pdf").exists()


def test_organizar_archivos_evita_duplicados(tmp_path):
    (tmp_path / "foto.jpg").touch()
    (tmp_path / "Imagenes").mkdir()
    (tmp_path / "Imagenes" / "foto.jpg").touch()

    organizar_archivos(tmp_path, DESGLOSE)

    assert (tmp_path / "Imagenes" / "foto.jpg").exists()
    assert (tmp_path / "Imagenes" / "foto_1.jpg").exists()
    assert not (tmp_path / "foto.jpg").exists()


def test_organizar_archivos_ignora_directorios(tmp_path):
    (tmp_path / "carpeta.mp4").mkdir()
    (tmp_path / "foto.jpg").touch()

    organizar_archivos(tmp_path, DESGLOSE)

    assert (tmp_path / "carpeta.mp4").is_dir()
    assert (tmp_path / "Imagenes" / "foto.jpg").exists()


def test_organizar_archivos_directorio_vacio(tmp_path):
    organizar_archivos(tmp_path, DESGLOSE)

    assert list(tmp_path.iterdir()) == []
