import pandas as pd
from modelo_SIR import modelo_SIR
from graficar_resultados import graficar_resultados


# variables de entrada
carpeta_origen = './ejemplo/'
archivo_origen = 'ejemplo.csv'
carpeta_destino = carpeta_origen
archivo_destino = 'resultados.csv'
imagen_destino = 'resultados.png'

# leer datos iniciales
ruta = carpeta_origen + archivo_origen
datos = pd.read_csv(ruta)

# correr el modelo
resultado = modelo_SIR(datos, 0, 60)

# calcular infectados acumulados
resultado['I acum'] = resultado['I'] + resultado ['R']

# datos para el gráfico
columnas_grafico = [
    'I acum',
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

# graficar los resultados
ruta = carpeta_destino + imagen_destino
graficar_resultados(resultado, 'Fecha', columnas_grafico, colores_grafico, estilos_grafico, ruta)

# guardar los resultados en csv
ruta = carpeta_destino + archivo_destino
resultado.to_csv(ruta, index = False)