import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# variables de entrada
# actualizar al último archivo
# chequear columnas con fechas, separador (, o ;), encoding (utf-8 o 16)
# fuente: https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv
# fuente: http://datos.salud.gob.ar/dataset/covid-19-casos-registrados-en-la-republica-argentina
carpeta_origen = './'
archivo_origen = 'Covid19Casos_2020-06-23.csv'
columnas_con_fechas = [8,9,11,13,15,22,24]
separador = ','
codificacion = 'utf-16'
archivo_municipios = 'municipios-latitud-longitud.csv'
carpeta_destino = carpeta_origen
archivo_destino_datos_completos = 'datos_minsal_completos_bsas.csv'
archivo_destino_datos_actuales = 'datos_minsal_actuales_bsas.csv'

# leer datos
ruta = carpeta_origen + archivo_origen
datos = pd.read_csv(ruta, sep=separador, encoding=codificacion, skipinitialspace=True, parse_dates=columnas_con_fechas, infer_datetime_format=True)

# leer listado de municipios
ruta = carpeta_origen + archivo_municipios
datos_municipios = pd.read_csv(ruta)

# procesar datos

# dejar sólo casos confirmados
datos = datos.loc[datos['clasificacion_resumen']=='Confirmado']
# dejar sólo casos de Prov de Bs As
datos = datos.loc[datos['residencia_provincia_nombre']=='Buenos Aires']
# dejar sólo casos de municipios Región Sanitaria VIII
datos = datos.loc[datos['residencia_departamento_nombre'].isin(datos_municipios['Municipio'])]

# simplificar la clasificación de casos en Activo, Recuperado y Fallecido
datos.loc[datos['Clasificacion']=='Caso confirmado - Fallecido', 'clasificacion'] = 'Fallecido'
datos.loc[datos['Clasificacion'].isin([
    'Caso confirmado - No activo (por laboratorio y tiempo de evolución)',
    'Caso confirmado - No Activo por criterio de laboratorio',
    'Caso confirmado - No activo (por tiempo de evolución)']), 'clasificacion'] = 'Recuperado'
datos.loc[datos['Clasificacion'].isin([
    'Caso confirmado - Activo ',
    'Caso confirmado - Activo Internado',
    'Caso confirmado - Activo con seguimiento negativo']), 'clasificacion'] = 'Activo'

# crear nueva columna con edad en años a partir de la edad en años o meses
datos['edad_actual_anios'] = datos['edad']
datos.loc[datos['edad_años_meses']=='Meses','edad_actual_anios'] = 0

# estadísticas resumen
print('Total confirmados:', datos['clasificacion'].count())
print('Activos:', datos.loc[datos['clasificacion']=='Activo', 'id_evento_caso'].count())
print('Recuperados:', datos.loc[datos['clasificacion']=='Recuperado', 'id_evento_caso'].count())
print('Fallecidos:', datos.loc[datos['clasificacion']=='Fallecido', 'id_evento_caso'].count())
print('Edad promedio confirmados:', round(datos['edad_actual_anios'].mean(),1))
print('Edad promedio activos:', round(datos.loc[datos['clasificacion']=='Activo', 'edad_actual_anios'].mean(),1))
print('Edad promedio recuperados:', round(datos.loc[datos['clasificacion']=='Recuperado', 'edad_actual_anios'].mean(),1))
print('Edad promedio fallecidos:', round(datos.loc[datos['clasificacion']=='Fallecido', 'edad_actual_anios'].mean(),1))
ultima_actualizacion = datos['ultima_actualizacion'].max().strftime('%d/%m/%Y')
print('Datos correspondientes al día',ultima_actualizacion)

# seleccionar columnas para exportar
columnas_origen = [
    'id_evento_caso',
    'residencia_provincia_nombre',
    'residencia_departamento_nombre',
    'clasificacion',
    'edad_actual_anios',
    'sexo',
    'cuidado_intensivo',
    'asistencia_respiratoria_mecanica',
    'fallecido',
    'fecha_inicio_sintomas',
    'fecha_apertura',
    'fecha_diagnostico',
    'fecha_internacion',
    'fecha_cui_intensivo',
    'fecha_fallecimiento',
    'ultima_actualizacion'
]
datos = datos[columnas_origen]

# exportar datos completos
ruta = carpeta_destino + archivo_destino_datos_completos
datos.to_csv(ruta, index=False)

# armar tabla con total de casos activos, fallecidos y recuperados en cada municipio
datos['casos'] = 1
resultado = datos.pivot_table(
    index=['residencia_departamento_nombre'], columns='clasificacion', values='casos',
    fill_value=0, aggfunc=np.sum
)

# unir la tabla con los datos de población y coordenadas de cada municipio y la tabla de casos
datos_municipios = pd.merge(datos_municipios, resultado, right_index=True, left_on='Municipio', how='left')
# completar datos faltantes (NaN) con ceros
datos_municipios = datos_municipios.fillna(0)
# agregar fecha de última actualización
datos_municipios['ultima_actualizacion'] = ultima_actualizacion

print(datos_municipios)

# exportar datos casos actuales
ruta = carpeta_destino + archivo_destino_datos_actuales
datos_municipios.to_csv(ruta, index=False)
