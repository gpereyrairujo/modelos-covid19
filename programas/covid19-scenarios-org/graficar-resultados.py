import pandas as pd
import matplotlib.pyplot as plt
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
    'Críticos',
    'Críticos exceso',
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
datos['Críticos'] = datos['Críticos'] + datos['Críticos exceso']

# datos para el gráfico
columnas_grafico = [
    'Total',
    'Severos',
    'Críticos',
    'Fallecidos']
colores_grafico = [
    [0.26,0.46,0.81],  # azul
    [0.88,0.60,0.08],  # naranja
    [0.82,0.30,0.06],  # rojo
    [0.05,0.05,0.05]]  # negro

# estilo del gráfico
plt.style.use('seaborn')
plt.rcParams["figure.figsize"] = [5, 4]
plt.rcParams["figure.dpi"] = 100
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['grid.color'] = "silver"
plt.rcParams['grid.linewidth'] = 0.75
plt.rcParams['grid.linestyle'] = ":"

# crear gráfico
fig = plt.figure()
ax = fig.add_subplot(111)

# graficar datos
for columna, color_linea in zip(columnas_grafico, colores_grafico):
    x = datos['Fecha']
    x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in x]  # transformar fecha en formato texto a formato datetime
    ax.plot(x, datos[columna], alpha=1, lw=2, color=color_linea, solid_capstyle='round', label=columna)

# ejes y leyenda
ax.set_xlabel('Mes')
ax.set_ylabel('Casos')
plt.yscale('log')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m'))  # formato de fecha
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # escala por meses
legend = ax.legend(edgecolor='white')

# guardar y mostrar gráfico
ruta = carpeta_destino + imagen_destino
plt.savefig(ruta)
plt.show()
