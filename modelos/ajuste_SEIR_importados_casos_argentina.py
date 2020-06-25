import pandas as pd
from modelo_SEIR_importados import modelo_SEIR_importados
from ajuste_modelos import ajuste_modelos
from graficar_resultados import graficar_resultados

# datos de entrada y salida
carpeta_origen = './ajustes_casos_argentina/'
archivo_origen = 'SEIR_importados_casos_argentina.csv'
carpeta_destino = carpeta_origen
archivo_destino = 'ajuste_SEIR_importados_casos_argentina.csv'
imagen_destino_casos = 'ajuste_SEIR_importados_casos_argentina.png'
imagen_destino_casos_log = 'ajuste_SEIR_importados_casos_argentina_log.png'
imagen_destino_R0 = 'ajuste_SEIR_importados_casos_argentina_R0.png'

# parámetros generales para el ajuste
serie_estimados = 'Ia'
serie_observados = 'Confirmados'
serie_parametro = 'R0'
duracion_periodo = 21

# leer datos iniciales
ruta = carpeta_origen + archivo_origen
datos_iniciales = pd.read_csv(ruta)

# ajuste de parámetros
print('Ajuste de parámetros diarios en base a los datos de los '+str(duracion_periodo)+' días posteriores')
resultado = ajuste_modelos(modelo_SEIR_importados, datos_iniciales, serie_estimados, serie_observados, serie_parametro, duracion_periodo, maximo_iteraciones_sin_cambios=50)

# graficar el ajuste obtenido
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