# =====================================
# SCRIPT TEST INTERACTIVO - PRUEBAS RÁPIDAS
# =====================================
# Propósito: Demo simple para probar el módulo principal
# Uso: Copiar/pegar tu ruta Excel → Ejecuta limpieza automática
# Config por default optimizada (fill_mean)
# Ideal para prototipado rápido

# Script test INTERACTIVO para cualquier Excel/CSV
from Limpieza_Datos import limpiar_datos_completo, ConfigLimpieza
import os

# =====================================
# INTERFAZ USUARIO SIMPLE
# =====================================
print(" TEST LIMPIEZA - Ingresa ruta de tu archivo")

ruta_excel = r'C:\Users\Usuario\Nombre_del_Archivo.xlsx'   # Agregar la direccion de la ubicacion en donde se encuentra el Excel
ruta_salida = ruta_excel.rsplit('.',1)[0] + '_limpio.csv'  # Auto en mismo folder

# =====================================
# VALIDACIÓN Y EJECUCIÓN
# =====================================
if os.path.exists(ruta_excel):
    print(f' Limpiando {ruta_excel}...')
    config = ConfigLimpieza()
    config.manejar_nulos = 'fill_mean'  # Automático: fill_mean (bueno para mayoría datasets)
    df = limpiar_datos_completo(ruta_excel, ruta_salida, config)
    print(f' FORMA FINAL: {df.shape}')
    print(df.head())
    print(f' Guardado: {ruta_salida}')
else:
    print('Archivo no encontrado. Verifica ruta.')

# =====================================
# INSTRUCCIONES USO
# =====================================
# Uso: py test_excel.py → pide tu ruta → analiza cualquier dataset
# Personaliza 'ruta_excel' con tu archivo

