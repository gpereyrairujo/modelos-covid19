import pandas as pd
from modelo_SEIR import modelo_SEIR
from graficar_resultados import graficar_resultados


# variables de entrada
carpeta_origen = './ejemplo/'
archivo_origen = 'ejemplo.csv'
carpeta_destino = carpeta_origen
archivo_destino = 'resultado_ejemplo_SEIR.csv'
imagen_destino = 'resultado_ejemplo_SEIR.png'

# leer datos iniciales
ruta = carpeta_origen + archivo_origen
datos = pd.read_csv(ruta)

# correr el modelo
modelo_SEIR(datos)

# datos para el gráfico
columnas_grafico = [
    'Ia',
    'I',
    'E',
    'R',
    'Confirmados']
colores_grafico = [
    [0.26,0.46,0.81],  # azul
    [0.90,0.80,0.10],  # amarillo
    [0.90,0.80,0.10],  # amarillo
    'darkgreen',  # verde
    [0.26,0.46,0.81]]  # azul
   
estilos_grafico = [
    '-',
    '-',
    ':',
    '-',
    '.']

# graficar los resultados
ruta = carpeta_destino + imagen_destino
graficar_resultados(datos, 'Fecha', columnas_grafico, colores_grafico, estilos_grafico, ruta, log=False)

# guardar los resultados en csv
ruta = carpeta_destino + archivo_destino
datos.to_csv(ruta, index = False)