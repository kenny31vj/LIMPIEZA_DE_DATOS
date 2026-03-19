# -*- coding: utf-8 -*-

# =====================================
# MÓDULO PRINCIPAL LIMPINZA_DE_DATOS.PY
# =====================================
# Desarrollador profesional: Pipeline ETL para limpieza automática de datasets
# Características:
# - Soporte CSV/Excel
# - Logging completo (auditoría)
# - Configuración flexible
# - Pipeline funcional (.pipe)
# - CLI con argparse
# - 6 pasos de limpieza secuenciales

import pandas as pd
import numpy as np
import logging
from typing import Optional, List
import argparse
import os

# =====================================
# CONFIGURACIÓN LOGGING AVANZADA
# =====================================
# Doble salida: Consola + archivo 'limpieza.log'
# Nivel INFO para tracking detallado
# Formato profesional con timestamp
# LOGGING (consola + archivo)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('limpieza.log'), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# =====================================
# CLASE CONFIGURACIÓN FLEXIBLE
# =====================================
# Centraliza todos los parámetros de limpieza
# Permite personalización sin tocar código
class ConfigLimpieza:
    def __init__(self):
        self.manejar_nulos = 'delete'  # 'delete', 'fill_mean', 'fill_median', 'fill_zero'
        self.estandarizar_texto = True
        self.validar_numericos = True
        self.min_valor_numerico = 0.0
        self.guardar_salida = True
        self.columnas_texto = None
        self.columnas_numericas = None

# =====================================
# FUNCIÓN 1: CARGA DE DATOS MULTI-FORMATO
# =====================================
# Detecta formato automáticamente (CSV/Excel)
# Logging de dimensiones iniciales
def cargar_datos(ruta: str) -> pd.DataFrame:
    logger.info(f"Cargando: {ruta}")
    if ruta.endswith('.csv'):
        df = pd.read_csv(ruta)
    elif ruta.endswith('.xlsx') or ruta.endswith('.xls'):
        df = pd.read_excel(ruta)
    else:
        raise ValueError("Solo CSV/Excel")
    logger.info(f"Cargado: {df.shape}")
    return df

# =====================================
# FUNCIÓN 2: ELIMINACIÓN DUPLICADOS
# =====================================
# Remueve filas duplicadas completas
# Reporta cantidad eliminada
def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    inicial = len(df)
    df = df.drop_duplicates()
    logger.info(f"Duplicados eliminados: {inicial-len(df)}")
    return df

# =====================================
# FUNCIÓN 3: MANEJO NULOS INTELIGENTE
# =====================================
# 4 estrategias configurables
# Estadísticas de nulos procesados
def manejar_nulos(df: pd.DataFrame, config: ConfigLimpieza) -> pd.DataFrame:
    nulos = df.isnull().sum().sum()
    if nulos == 0:
        logger.info("Sin nulos")
        return df
    if config.manejar_nulos == 'delete':
        df = df.dropna()
    elif config.manejar_nulos == 'fill_mean':
        df = df.fillna(df.mean(numeric_only=True))
    elif config.manejar_nulos == 'fill_median':
        df = df.fillna(df.median(numeric_only=True))
    elif config.manejar_nulos == 'fill_zero':
        df = df.fillna(0)
    logger.info(f"Nulos {config.manejar_nulos}: {nulos}")
    return df

# =====================================
# FUNCIÓN 4: ESTANDARIZACIÓN TEXTO
# =====================================
# Uppercase + strip en columnas object
# Auto-detecta columnas de texto
def estandarizar_texto(df: pd.DataFrame, config: ConfigLimpieza) -> pd.DataFrame:
    if not config.estandarizar_texto:
        return df
    texto_cols = config.columnas_texto or df.select_dtypes(include=['object']).columns
    for col in texto_cols:
        df[col] = df[col].astype(str).str.upper().str.strip()
        logger.info(f"Texto std: {col}")
    return df

# =====================================
# FUNCIÓN 5: CONVERSIÓN AUTOMÁTICA FECHAS
# =====================================
# Detecta columnas fecha (>50% parseables)
# errors='coerce' para robustez
def convertir_fechas(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include=['object']).columns:
        try:
            test = pd.to_datetime(df[col], errors='coerce')
            if test.notna().sum() / len(df) > 0.5:
                df[col] = test
                logger.info(f"Fechas: {col}")
        except:
            pass
    return df

# =====================================
# FUNCIÓN 6: VALIDACIÓN NÚMERICOS
# =====================================
# Filtra valores < min_valor_numerico
# Por columna numérica, logging warnings
def validar_numericos(df: pd.DataFrame, config: ConfigLimpieza) -> pd.DataFrame:
    if not config.validar_numericos:
        return df
    num_cols = config.columnas_numericas or df.select_dtypes(np.number).columns
    for col in num_cols:
        mask = df[col] < config.min_valor_numerico
        count = mask.sum()
        if count > 0:
            df = df[~mask]
            logger.warning(f"Eliminados {count} inválidos {col}")
    return df

# =====================================
# PIPELINE PRINCIPAL - FUNCIÓN ORQUESTADORA
# =====================================
# Secuencia fija de 6 pasos usando .pipe (pandas idiomático)
# Guarda salida CSV si ruta_salida proporcionada
# Retorna DataFrame limpio para chaining
def limpiar_datos_completo(ruta_entrada: str, ruta_salida: Optional[str] = None, config=None) -> pd.DataFrame:
    config = config or ConfigLimpieza()
    df = (cargar_datos(ruta_entrada)
          .pipe(eliminar_duplicados)
          .pipe(lambda d: manejar_nulos(d, config))
          .pipe(lambda d: estandarizar_texto(d, config))
          .pipe(convertir_fechas)
          .pipe(lambda d: validar_numericos(d, config)))
    if ruta_salida:
        df.to_csv(ruta_salida, index=False)
        logger.info(f"Guardado: {ruta_salida}")
    logger.info(f"Final: {df.shape}")
    return df

# =====================================
# CLI - INTERFAZ LÍNEA DE COMANDOS
# =====================================
# argparse profesional con help detallado
# Parámetros: input/output/nulos/min_num
def main():
    parser = argparse.ArgumentParser(description='Limpieza datos: py Limpienza_Datos.py -i archivo.xlsx')
    parser.add_argument('-i', '--input', required=True, help='Input CSV/Excel')
    parser.add_argument('-o', '--output', help='Output CSV (default limpio.csv)')
    parser.add_argument('--nulos', choices=['delete','fill_mean','fill_median','fill_zero'], default='delete')
    parser.add_argument('--min-num', type=float, default=0.0)
    args = parser.parse_args()
    
    config = ConfigLimpieza()
    config.manejar_nulos = args.nulos
    config.min_valor_numerico = args.min_num
    output = args.output or 'limpio.csv'
    
    df = limpiar_datos_completo(args.input, output, config)
    print(f" Listo: {df.shape}. Archivo: {output}")

# =====================================
# PUNTO DE ENTRADA PRINCIPAL
# =====================================
if __name__ == '__main__':
    main()

# =====================================
# EJEMPLO DE USO CLI
# =====================================
# py Limpienza_Datos.py -i BD-Sales.xlsx -o ventas_limpias.csv --nulos fill_mean --min-num 0
