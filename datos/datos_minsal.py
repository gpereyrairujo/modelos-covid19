import pandas as pd

# variables de entrada
carpeta_origen = './'
archivo_origen = 'covid19casos.csv'
carpeta_destino = carpeta_origen
archivo_destino = 'datos_minsal.csv'

# leer datos
ruta = carpeta_origen + archivo_origen
datos = pd.read_csv(ruta)

# procesar datos

# dejar sólo casos confirmados
datos = datos.loc[datos['clasificacion_resumen']=='Confirmado']

# corregir errores
datos['fecha_fis'] = datos['fecha_fis'].replace(to_replace = '2019-04-18', value = '2020-04-18')
datos['fecha_fis'] = datos['fecha_fis'].replace(to_replace = '2019-04-24', value = '2020-04-24')

# crear nueva columna con edad en años a partir de la edad en años o meses
datos['edad_años'] = datos['edad']
datos.loc[datos['edad_años_meses']=='Meses','edad_años'] = 0

# crear nueva columna para valor de 'alta_laboratorio'
datos['alta_laboratorio'] = 'NO'
datos.loc[datos['clasificacion_manual']=='Caso confirmado con criterio laboratorial para ALTA','alta'] = 'SI'

# seleccionar columnas para exportar
columnas_origen = [
    'edad_años',
    'sexo',
    'cuidado_intensivo',
    'asistencia_respiratoria_mecanica',
    'alta_laboratorio',
    'fallecido',
    'fecha_fis',
    'fecha_apertura',
    'fecha_cuidado_intensivo',
    'fecha_fallecimiento',
    'provincia_residencia',
    'departamento_residencia'
]
datos = datos[columnas_origen]

ruta = carpeta_destino + archivo_destino
datos.to_csv(ruta, index=False)