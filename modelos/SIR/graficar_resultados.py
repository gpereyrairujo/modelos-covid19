import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

def graficar_resultados(datos, columna_fecha, series_y, colores_series, estilos_series, ruta_imagen):

    '''
    Función para graficar la evolución en el tiempo de variables de modelos epidémicos

    Variables de entrada:
        datos: dataframe con las series de datos a graficar
        columna_fecha: nombre de la columna que contiene la fecha (en formato aaaa-mm-dd)
        series_y: lista de los nombres de columna de cada una de las series de datos a graficar
        colores_series: lista de colores para cada una de las series
        ruta_imagen: ruta donde se guarda el gráfico (extensión .png)
    '''
    
    # estilo del gráfico
    plt.style.use('seaborn')
    plt.rcParams["figure.figsize"] = [5, 4]
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = 'white'
    plt.rcParams['grid.color'] = "silver"
    plt.rcParams['grid.linewidth'] = 0.75
    plt.rcParams['grid.linestyle'] = ":"

    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['lines.solid_capstyle'] = 'round'

    # crear gráfico
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # graficar datos
    for columna, color_linea, estilo_linea in zip(series_y, colores_series, estilos_series):
        x = datos[columna_fecha]
        x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in x]  # transformar fecha en formato texto a formato datetime
        ax.plot(x, datos[columna], estilo_linea, alpha=1, color=color_linea, label=columna)

    # ejes y leyenda
    ax.set_xlabel('Mes')
    ax.set_ylabel('Casos')
    plt.yscale('log')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m'))  # formato de fecha
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # escala por meses
    legend = ax.legend(edgecolor='white')

    # guardar y mostrar gráfico
    plt.savefig(ruta_imagen)
    plt.show()
