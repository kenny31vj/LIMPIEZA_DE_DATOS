#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =====================================
# MÓDULO PRINCIPAL LIMPINZA_DE_DATOS.PY - FIXED VERSION
# =====================================

import pandas as pd
import numpy as np
import logging
from typing import Optional
import argparse
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('limpieza.log'), logging.StreamHandler()])
logger = logging.getLogger(__name__)

class ConfigLimpieza:
    def __init__(self):
        self.manejar_nulos = 'delete'
        self.estandarizar_texto = True
        self.validar_numericos = True
        self.min_valor_numerico = 0.0

def cargar_datos(ruta: str) -> pd.DataFrame:
    logger.info(f"Cargando: {ruta}")
    if ruta.endswith('.csv'):
        df = pd.read_csv(ruta)
    elif ruta.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(ruta)
    else:
        raise ValueError("Solo CSV/Excel")
    logger.info(f"Cargado: {df.shape}")
    return df

def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    inicial = len(df)
    df = df.drop_duplicates()
    logger.info(f"Duplicados eliminados: {inicial-len(df)}")
    return df

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

def limpiar_texto_completo(df: pd.DataFrame, config: ConfigLimpieza) -> pd.DataFrame:
    """Limpieza texto avanzada: upper + strip + caracteres especiales (español)"""
    if not config.estandarizar_texto:
        return df
    
    texto_cols = df.select_dtypes(include=['object']).columns
    regex_especiales = r'[^A-Za-zÁÉÍÓÚÑáéíóúñ0-9 ]'
    
    for col in texto_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.upper()
            .str.strip()
            .str.replace(regex_especiales, '', regex=True)
        )
        logger.info(f"Texto completo: {col}")
    return df

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

def validar_numericos(df: pd.DataFrame, config: ConfigLimpieza) -> pd.DataFrame:
    """Validación numérica + reglas negocio avanzadas"""
    if not config.validar_numericos:
        return df
    
    num_cols = df.select_dtypes(np.number).columns
    for col in num_cols:
        mask = df[col] < config.min_valor_numerico
        count = mask.sum()
        if count > 0:
            df = df[~mask]
            logger.warning(f"Min-valor - {col}: eliminados {count}")
    
    return df

def validar_reglas_negocio(df: pd.DataFrame) -> pd.DataFrame:
    """Reglas específicas: precio/cantidad >0, fechas válidas"""
    filas_inicial = len(df)
    
    cols_precio = [col for col in df.columns if any(p in col.lower() for p in ['precio', 'price', 'valor'])]
    cols_cantidad = [col for col in df.columns if any(p in col.lower() for p in ['cantidad', 'qty', 'quantity', 'unidades'])]
    
    for col in cols_precio + cols_cantidad:
        if col in df and df[col].dtype in ['float64', 'int64']:
            mask = df[col] <= 0
            count = mask.sum()
            df = df[~mask]
            if count > 0:
                logger.warning(f"Negocio-{col}: {count} eliminados (<=0)")
    
    logger.info(f"Reglas negocio: {filas_inicial} → {len(df)}")
    return df

def limpiar_datos_completo(ruta_entrada: str, ruta_salida: Optional[str] = None, config=None) -> pd.DataFrame:
    config = config or ConfigLimpieza()
    df = (cargar_datos(ruta_entrada)
          .pipe(eliminar_duplicados)
          .pipe(lambda d: manejar_nulos(d, config))
          .pipe(lambda d: limpiar_texto_completo(d, config))
          .pipe(convertir_fechas)
          .pipe(lambda d: validar_numericos(d, config))
          .pipe(validar_reglas_negocio))
    if ruta_salida:
        df.to_csv(ruta_salida, index=False)
        logger.info(f"Guardado: {ruta_salida}")
    logger.info(f"Final: {df.shape}")
    return df

def main():
    parser = argparse.ArgumentParser(description='Limpieza datos: py Limpieza_Datos_FIX.py -i archivo.xlsx')
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

if __name__ == '__main__':
    main()

