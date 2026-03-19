# Limpieza de Datos - ETL Profesional Python
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Status](https://img.shields.io/badge/Status-Activo-success)

Automatización de limpieza de datos para pipelines ETL en entornos analíticos.

---

## Descripción

**Herramienta para limpieza automática de datasets Excel/CSV**

### Funcionalidades Principales
- **6 pasos ETL secuenciales**: Duplicados, nulos, texto, fechas, validaciones
- **Multi-formato**: CSV, XLS, XLSX
- **Configuración flexible**: CLI + interactivo
- **Logging completo**: Auditoría en `limpieza.log`
- **Batch masivo**: Múltiples archivos simultáneos
- **Pipeline pandas .pipe**: Código idiomático moderno

## Estructura del Proyecto

```
Limpieza_de_Datos/
├── Limpieza_Datos.py     ← Módulo principal (núcleo)
├── limpia_batch.py       ← Procesamiento masivo carpetas
├── test_excel.py         ← Pruebas rápidas individuales
├── README.md             ← Esta documentación
├── LICENSE.md            ← Licencia MIT
└── limpieza.log          ← Logs automáticos (generado)
```

---

## ⚙️ Tecnologías utilizadas

| Tecnología | Uso                            |
| ---------- | ------------------------------ |
| Python     | Lenguaje principal             |
| pandas     | Manipulación de datos          |
| numpy      | Operaciones numéricas          |
| logging    | Registro de procesos           |
| argparse   | Interfaz por línea de comandos |
| glob/os    | Manejo archivos batch          |

---

## Uso

### 1. **Módulo Principal (CLI profesional)**
```bash
# Ayuda
python Limpienza_Datos.py -h

# Limpieza básica
python Limpienza_Datos.py -i datos.xlsx

# Config avanzada
python Limpienza_Datos.py -i ventas.xlsx -o ventas_limpias.csv --nulos fill_mean --min-num 0.01
```

### 2. **Batch Masivo (múltiples archivos)**
```
1. Coloca tus Excel/CSV en una carpeta
2. python limpia_batch.py /ruta/carpeta/
3. Config interactiva → Auto-procesa TODOS
```

### 3. **Test Rápido (demo)**
```bash
python test_excel.py
# Modifica ruta_excel en código → Ejecuta instantáneo
```

## Ejemplo Entrada/Salida

**Entrada** (`ventas.xlsx` sucio):
```
ID,Nombre,Precio,Fecha
1, juan ,, 2023-1-12
, \"PEDRO\", -5.0, 15/03/2023
1, JUAN , 10.0,
```

**Salida** (`ventas_limpio.csv`):
```
ID,NOMBRE,PRECIO,FECHA
1,JUAN,10.0,2023-01-12
```

## Instalación

```bash
# Dependencias (automáticas con pandas)
pip install pandas openpyxl xlrd
```

## Ejemplo Pipeline Completo

```
Excel sucio → [Limpieza_Datos.py] → CSV limpio + log auditoría
     ↓ batch
Carpeta con 100 Excel → [limpia_batch.py] → 100 CSV limpios
```

## Sugerencias Mejoras Futuras (sin cambiar código)

1. **Docker**: `docker run -v $(pwd):/data python-limpieza`
2. **API FastAPI**: `/clean?file=ventas.xlsx`
3. **Jupyter Notebook**: Demo interactivo
4. **Tests pytest**: Validación unitaria pipeline
5. **Config YAML**: Parámetros externos

---

## Autor

**KENNY D. VERA JEREZ**
Proyecto de práctica enfocado en análisis y limpieza de datos para pipelines ETL.

---

---

## Licencia

Este proyecto está bajo la Licencia MIT.
Consulta el archivo LICENSE para más detalles.