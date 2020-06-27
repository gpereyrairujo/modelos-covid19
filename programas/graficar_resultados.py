import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

def graficar_resultados(datos, columna_fecha, series_y, colores_series, estilos_series, ruta_imagen, log=False):

    '''
    Función para graficar la evolución en el tiempo de variables de modelos epidémicos

    Variables de entrada:
        datos: dataframe con las series de datos a graficar
        columna_fecha: nombre de la columna que contiene la fecha (en formato aaaa-mm-dd)
        series_y: lista de los nombres de columna de cada una de las series de datos a graficar
        colores_series: lista de colores para cada una de las series
        estilos_series: lista de estilos de línea o símbolos para cada una de las series
            estilos de línea: -, --, :, -.
            estios de símbolo: ., o, ^, s, D, *
            intervalo: i (se grafica una franja de color entre dos series)
        ruta_imagen: ruta donde se guarda el gráfico (extensión .png)
        log: usar escala logarítmica en el eje y (True/False)

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

    # graficar series de datos
    intervalo_incompleto = False
    for columna, color_linea, estilo_linea in zip(series_y, colores_series, estilos_series):

        # datos eje x
        x = datos[columna_fecha]
        x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in x]  # transformar fecha en formato texto a formato datetime

        # estilo intervalo entre 2 series
        if(estilo_linea=='i'):
            if(intervalo_incompleto==False):
                # primera serie para graficar como intervalo
                limite_inferior = datos[columna]
                intervalo_incompleto = True
            else:
                # segunda serie para graficar como intervalo
                limite_superior = datos[columna]
                ax.fill_between(x, limite_inferior, limite_superior, alpha=0.2, lw=0.75, color=color_linea, label=columna)
                intervalo_incompleto = False

        # estilo serie individual (símbolos y/o líneas)
        else:
            ax.plot(x, datos[columna], estilo_linea, alpha=1, color=color_linea, label=columna)

    # ejes y leyenda
    if(log): plt.yscale('log')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Casos')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m'))  # formato de fecha
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # escala por meses
    legend = ax.legend(edgecolor='white')

    # guardar y mostrar gráfico
    plt.savefig(ruta_imagen)
    plt.show()
