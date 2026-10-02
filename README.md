# 📂 Organizador & Clasificador Automatizado de Archivos

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-green.svg)](https://docs.pytest.org/)

Herramienta CLI en Python diseñada para automatizar la clasificación, organización y limpieza de directorios mediante reglas configurables en JSON. Cuenta con gestión segura de nombres duplicados, trazabilidad con logs y una suite de pruebas unitarias con `pytest`.

---

## 🌟 Características Principales

- **Reglas Dinámicas en JSON (`categorias.JSON`)**: Define categorías y sus extensiones asociadas de forma modular sin alterar el código fuente.
- **Manejo Seguro de Colisiones**: Si un archivo ya existe en la carpeta destino, genera automáticamente un sufijo único (ej. `documento_1.pdf`) para prevenir la sobrescritura accidental de datos.
- **Trazabilidad y Registros (Logging)**:
  - Salida informativa por consola.
  - Registro persistente de operaciones en `organizador.log`.
  - Generación de reportes de ejecución en `reporte.txt`.
- **Suite de Pruebas Unitarias**: Cobertura de funciones clave utilizando `pytest` para garantizar el comportamiento correcto en casos bordes.

---

## 📁 Estructura del Proyecto

```text
clasificador_archivos/
├── organizador.py          # Lógica principal de clasificación y movimiento de archivos
├── categorias.JSON         # Mapeo de categorías (Imágenes, Documentos, Audio, etc.)
├── test_organizador.py     # Suite de pruebas unitarias con pytest
└── requirements.txt        # Dependencias del proyecto
```

---

## 🛠️ Requisitos e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/vivxandra/clasificador-archivos.git
   cd clasificador-archivos
   ```

2. **Instalar dependencias de pruebas:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Uso del Proyecto

### 1. Ejecutar el Organizador
```bash
python3 organizador.py /ruta/a/tu/carpeta_desorganizada
```

### 2. Ejecutar Pruebas Unitarias
Para verificar que todas las funciones pasan las pruebas correctamente:
```bash
pytest test_organizador.py -v
```

---

## 👤 Autor

Desarrollado por **Vivian Suastegui** ([@vivxandra](https://github.com/vivxandra)).
