import pandas as pd
import random
from sklearn.metrics import mean_squared_error
from math import sqrt
from modelo_SEIR_importados import modelo_SEIR_importados
from ajuste_modelos import ajuste_por_periodos, ajuste_global
from graficar_resultados import graficar_resultados

# datos de entrada y salida
carpeta_origen = './ajuste_SEIR_contactos_estrechos_casos_argentina/'
archivo_origen = 'SEIR_contactos_estrechos_casos_argentina.csv'
carpeta_destino = carpeta_origen
archivo_destino = 'ajuste_SEIR_contactos_estrechos_casos_argentina.csv'
imagen_destino_casos = 'ajuste_SEIR_contactos_estrechos_casos_argentina.png'
imagen_destino_casos_log = 'ajuste_SEIR_contactos_estrechos_casos_argentina_log.png'
imagen_destino_R0 = 'ajuste_SEIR_contactos_estrechos_casos_argentina_R0.png'

# parámetros generales para el ajuste
serie_estimados = 'Ia'
serie_observados = 'Confirmados'
serie_parametro = 'R0'
duracion_periodo = 20

# leer datos iniciales
ruta = carpeta_origen + archivo_origen
datos_iniciales = pd.read_csv(ruta)

# ejecutar paso 1: ajuste preliminar por períodos
print('Paso 1 - ajuste preliminar para cada período')
variacion_aleatoria = 0.05
ajuste_paso1 = ajuste_por_periodos(modelo_SEIR_importados, datos_iniciales, serie_estimados, serie_observados, serie_parametro, duracion_periodo, variacion_aleatoria)

# ejecutar paso 2: optimización de parámetros simultáneamente para todos los períodos
print('Paso 2 - ajuste global para todos los períodos')
variacion_aleatoria = 0.005
ajuste_paso2 = ajuste_global(modelo_SEIR_importados, ajuste_paso1, serie_estimados, serie_observados, serie_parametro, duracion_periodo, variacion_aleatoria)

resultado = ajuste_paso2

# graficar el mejor ajuste obtenido
columnas_grafico = [
    'Ia',
    'I',
    'R',
    'Confirmados']
colores_grafico = [
    [0.26,0.46,0.81],  # azul
    [0.90,0.80,0.10],  # amarillo
    'darkgreen',  # verde
    [0.26,0.46,0.81]]  # azul
estilos_grafico = [
    '-',
    '-',
    '-',
    '.']
ruta = carpeta_destino + imagen_destino_casos
graficar_resultados(resultado, 'Fecha', columnas_grafico, colores_grafico, estilos_grafico, ruta, log=False)

# graficar en escala logarítmica
ruta = carpeta_destino + imagen_destino_casos_log
graficar_resultados(resultado, 'Fecha', columnas_grafico, colores_grafico, estilos_grafico, ruta, log=True)

# graficar el mejor R0 obtenido
columnas_grafico = ['R0']
colores_grafico = [[0.26,0.46,0.81]]  # azul
estilos_grafico = ['-']
ruta = carpeta_destino + imagen_destino_R0
graficar_resultados(resultado, 'Fecha', columnas_grafico, colores_grafico, estilos_grafico, ruta, log=False)

# guardar el mejor ajuste en csv
ruta = carpeta_destino + archivo_destino
resultado.to_csv(ruta, index = False)