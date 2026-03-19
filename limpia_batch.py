#!/usr/bin/env python3

# =====================================
# SCRIPT BATCH - LIMPIEZA MASIVA DE DATOS
# =====================================
# Propósito: Procesa múltiples archivos Excel/CSV de forma batch desde una carpeta.
# Flujo: Detecta archivos → Configuración interactiva → Limpia cada uno → Guarda resultados.
# Dependencia: Módulo Limpienza_Datos.py

"""
SCRIPT BATCH: Limpia MÚLTIPLES Excel/CSV de una vez.
Uso:
py limpia_batch.py carpeta_con_archivos/
O lista manual.
"""

import os
import glob

# =====================================
# IMPORTS NECESARIOS
# =====================================
# os, glob: Manejo de archivos y búsqueda de patrones (*.xlsx, *.csv)
# Limpienza_Datos: Módulo principal con funciones de limpieza y configuración
from Limpieza_Datos import limpiar_datos_completo, ConfigLimpieza

def main():
    # =====================================
    # FUNCIÓN PRINCIPAL - ORQUESTADOR BATCH
    # =====================================
    # Responsabilidades:
    # 1. Solicitar carpeta de entrada
    # 2. Detectar todos los archivos Excel/CSV
    # 3. Configurar parámetros de limpieza
    # 4. Procesar archivo por archivo
    
    print(" Limpieza BATCH - Múltiples archivos")
    # =====================================
    # 1. INGRESO DE CARPETA DE TRABAJO
    # =====================================
    # Solicita ruta interactivamente. '.' = carpeta actual
    carpeta = input("Ruta carpeta con Excel/CSV (Enter para actual): ") or '.'
    
    # =====================================
    # 2. DETECCIÓN AUTOMÁTICA DE ARCHIVOS
    # =====================================
    # Busca todos los archivos Excel (*.xlsx, *.xls) y CSV en la carpeta especificada
    # Encuentra todos CSV/Excel
    archivos = glob.glob(os.path.join(carpeta, '*.xlsx')) + glob.glob(os.path.join(carpeta, '*.xls')) + glob.glob(os.path.join(carpeta, '*.csv'))
    
    if not archivos:
        print(" No archivos encontrados. Pon Excel/CSV en folder.")
        return
    
    print(f"📂 Encontrados {len(archivos)} archivos: { [os.path.basename(f) for f in archivos] }")
    
    # =====================================
    # 3. CONFIGURACIÓN INTERACTIVA
    # =====================================
    # Crea instancia de configuración y permite personalización por usuario
    config = ConfigLimpieza()
    nulos_opt = input("Manejo nulos (delete/fill_mean/fill_median/fill_zero) [delete]: ") or 'delete'
    config.manejar_nulos = nulos_opt
    min_num = input("Min número (0): ") or '0'
    config.min_valor_numerico = float(min_num)
    
    procesados = 0
    for archivo in archivos:
        nombre_base = os.path.basename(archivo)
        salida = nombre_base.rsplit('.', 1)[0] + '_limpio.csv'
        print(f"\n--- Limpiando {nombre_base} ---")
        try:
            df = limpiar_datos_completo(archivo, salida, config)
            print(f" {nombre_base} → {salida} ({df.shape})")
            procesados += 1
        except Exception as e:
            print(f" Error {nombre_base}: {e}")
    
    print(f"\n BATCH completado: {procesados}/{len(archivos)} OK")

if __name__ == '__main__':
    main()
