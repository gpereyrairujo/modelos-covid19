import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import datetime as dt
import matplotlib.dates as mdates

# variables de entrada
carpeta_origen = './ejemplo/'
archivo_origen = 'c19s.results.summary.tsv'
carpeta_destino = carpeta_origen
archivo_destino = 'resultados.csv'
imagen_destino = 'resultados.png'

columnas_origen = [
    'time',
    'infectious (total) median',
    'severe (total) median',
    'ICU (total) median',
    'overflow (total) median',
    'cumulative recovered (total) median',
    'cumulative fatality (total) median']
columnas_destino = [
    'Fecha',
    'Infecciosos',
    'Severos',
    'UTI',
    'UTI exceso',
    'Recuperados',
    'Fallecidos']

# leer datos
ruta = carpeta_origen + archivo_origen
if(ruta[-4:]=='.tsv'):
    datos = pd.read_csv(ruta, sep='\t')
else:
    datos = pd.read_csv(ruta)

# seleccionar y renombrar columnas
datos = datos[columnas_origen]
datos.columns = columnas_destino

# procesar datos
datos['Total'] = datos.sum(axis=1)
datos['UTI'] = datos['UTI'] + datos['UTI exceso']

# datos para el gráfico
columnas_grafico = [
    'Total',
    'Recuperados',
    'Infecciosos',
    'Severos',
    'UTI',
    'Fallecidos']

# estilo del gráfico
plt.style.use('seaborn')
plt.rcParams["figure.figsize"] = [5, 4]
plt.rcParams["figure.dpi"] = 100
plt.rc('grid', linestyle="-", linewidth=0.75, color='white')

# crear gráfico
fig = plt.figure()
ax = fig.add_subplot(111)

# graficar datos
for columna in columnas_grafico:
    x = datos['Fecha']
    x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in x]  # transformar fecha en formato texto a formato datetime
    ax.plot(x, datos[columna], alpha=0.5, lw=2, label= columna)

# ejes y leyenda
ax.set_xlabel('Fecha')
ax.set_ylabel('Casos')
plt.yscale('log')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))  # formato de fecha
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # escala por meses
legend = ax.legend()
legend.get_frame().set_alpha(0.5)

# guardar y mostrar gráfico
ruta = carpeta_destino + imagen_destino
plt.savefig(ruta)
plt.show()
