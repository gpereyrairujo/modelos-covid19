import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np

carpeta_origen = './'
carpeta_destino = carpeta_origen
archivo_datos_mapa = 'kml_municipios/municipios.shp'
archivo_casos_municipios = 'datos_minsal_acumulados_municipios_bsas.csv'
archivo_destino_imagen = 'mapa_casos_region.png'

# leer datos mapa base
ruta = carpeta_origen + archivo_datos_mapa
datos_mapa = gpd.read_file(ruta, encoding='utf-8')
# dejar sólo pcia de bs as (código comienza con 06)
datos_mapa = datos_mapa.loc[datos_mapa['IN1'].str[:2]=='06']
# corrección de errores
datos_mapa.loc[datos_mapa['NAM']=='General las  Heras', 'NAM'] = 'General Las Heras'
datos_mapa.loc[datos_mapa['NAM']=='General la Madrid', 'NAM'] = 'General La Madrid'

# leer datos de casos municipios
ruta = carpeta_origen + archivo_casos_municipios
datos_casos_municipios = pd.read_csv(ruta)
# unir la tabla de casos de municipios de la pcia de bs as y los datos del mapa base
datos_mapa = datos_mapa.merge(datos_casos_municipios, left_on='NAM', right_on='Municipio', how='left')
# calcular casos totales
datos_mapa['total']=datos_mapa['Activo']+datos_mapa['Fallecido']+datos_mapa['Recuperado']
# calcular logaritmo para usar esos valores para la escala de color del mapa
datos_mapa['log_total'] = np.log10(datos_mapa['total'])
# fecha de última actualización
ultima_actualizacion = datos_mapa.ix[1, 'ultima_actualizacion']


# mapas

# paleta de colores
paleta_colores = plt.cm.get_cmap('Blues')
paleta_colores.set_under('white')                   # valores por debajo del mínimo en color blanco
color_fondo = 'white'
color_bordes = 'darkred'


# mapa provincia
# figura, tamaño, ejes
fig, ax = plt.subplots(1, figsize=(4.3, 5))       # crear figura y asignar tamaño
plt.axis('equal')                               # mantener proporción latitud y longitud
ax.set_axis_off()                               # quitar ejes
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.margins(0.05,0.05)                          # margen alrededor del mapa
fig.patch.set_facecolor(color_fondo)               # color del fondo
# datos para el mapa
ax = datos_mapa.plot(
    column='log_total',                         # valores a usar para la escala de colores
    cmap=paleta_colores, vmin=0, vmax=3,        # escala de colores entre valores log 0 y 3 (entre 1 y 1000)
    edgecolor=color_bordes, linewidth=0.1,          # color de los bordes
    ax=ax
    )
# leyendas
izquierda, derecha = plt.xlim()     # límites del mapa en x
abajo, arriba = plt.ylim()          # límites del mapa en y
plt.text((izquierda+derecha)/2, arriba, 'Casos confirmados Pcia. de Bs. As.', {'color': 'black', 'fontsize': 10, 'ha': 'center', 'fontweight': 'bold'})
plt.text(izquierda, abajo, 'Elaborado en base a datos del Ministerio de Salud del día '+ultima_actualizacion, {'color': 'black', 'fontsize': 6})
# leyenda rangos de colores 
for i in range(4):
    valor = 10**i
    color = paleta_colores(i/3)
    posicion_y = abajo - (4-i) * (abajo-arriba)/20
    posicion_x = derecha - (derecha-izquierda)/30
    plt.text(
        posicion_x, posicion_y,
        str(valor),
        {'color':'black', 'fontsize':7, 'ha':'right', 'va':'center'},
        bbox=dict(boxstyle="round", facecolor=color, edgecolor=color_bordes, linewidth=0.1)
    )
# guardar y mostrar mapa
ruta_imagen = carpeta_destino + 'mapa_casos_provincia.png'
plt.savefig(ruta_imagen, facecolor=fig.get_facecolor(), bbox_inches = 'tight', pad_inches = 0.1)


# mapa region centro-sudeste

# filtrar por latitud y longitud
datos_mapa = datos_mapa.loc[(datos_mapa['Latitud']<-35.7) & (datos_mapa['Longitud']>-60.8)]

# dibujar mapa
# figura, tamaño, ejes
fig, ax = plt.subplots(1, figsize=(7, 5))       # crear figura y asignar tamaño
plt.axis('equal')                               # mantener proporción latitud y longitud
ax.set_axis_off()                               # quitar ejes
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.margins(0.05,0.05)                          # margen alrededor del mapa
fig.patch.set_facecolor(color_fondo)               # color del fondo
# datos para el mapa
ax = datos_mapa.plot(
    column='log_total',                         # valores a usar para la escala de colores
    cmap=paleta_colores, vmin=0, vmax=3,        # escala de colores entre valores log 0 y 3 (entre 1 y 1000)
    edgecolor=color_bordes, linewidth=0.1,          # color de los bordes
    ax=ax
    )
# rótulos para cada municipio
for idx, fila in datos_mapa.iterrows():
    if(fila['total']>0):
        plt.text(
            fila['Longitud'], fila['Latitud'],                                                      # ubicación
            fila['Municipio']+'\n'+str(int(fila['total'])),                                         # texto
            {'color':'black', 'fontsize':7, 'ha':'center', 'va':'center'},     # formato
            bbox=dict(boxstyle="round", facecolor='lightgrey', edgecolor='white', alpha=0.5, linewidth=0.1)           # cuadro de texto
        )
# leyendas
izquierda, derecha = plt.xlim()     # límites del mapa en x
abajo, arriba = plt.ylim()          # límites del mapa en y
plt.text((izquierda+derecha)/2, arriba, 'Casos confirmados en la región', {'color': 'black', 'fontsize': 10, 'ha': 'center', 'fontweight': 'bold'})
plt.text(izquierda, abajo, 'Elaborado en base a datos del Ministerio de Salud del día '+ultima_actualizacion, {'color': 'black', 'fontsize': 6})
# leyenda rangos de colores 
for i in range(4):
    valor = 10**i
    color = paleta_colores(i/3)
    posicion_y = abajo - (4-i) * (abajo-arriba)/20
    posicion_x = derecha - (derecha-izquierda)/30
    plt.text(
        posicion_x, posicion_y,
        str(valor),
        {'color':'black', 'fontsize':7, 'ha':'right', 'va':'center'},
        bbox=dict(boxstyle="round", facecolor=color, edgecolor=color_bordes, linewidth=0.1)
    )
# guardar y mostrar mapa
ruta_imagen = carpeta_destino + archivo_destino_imagen
plt.savefig(ruta_imagen, facecolor=fig.get_facecolor(), bbox_inches = 'tight', pad_inches = 0.1)
#plt.show()