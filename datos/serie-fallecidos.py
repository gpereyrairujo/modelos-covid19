import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/16-bnsDdmmgtSxdWbVMboIHo5FRuz76DBxsz_BbsEVWA/export?format=csv&id=16-bnsDdmmgtSxdWbVMboIHo5FRuz76DBxsz_BbsEVWA&gid=1627928258'
columnas_origen = [fecha','edad_hombre','edad_mujer']
columnas_destino = ['Fecha','Edad hombre','Edad mujer']
archivo_destino = 'serie-fallecidos.csv'

# leer datos
datos = pd.read_csv(url)

# seleccionar y renombrar columnas
datos = datos[columnas_origen]
datos.columns = columnas_destino

# corregir errores
datos['Fecha'] = datos['Fecha'].replace(to_replace = '03/05/0202', value = '03/05/2020')
datos['Fecha'] = datos['Fecha'].replace(to_replace = '04/052020', value = '04/05/2020')

# cambiar formato de fecha
datos['Fecha'] = pd.to_datetime(datos['Fecha'], format='%d/%m/%Y')
datos['Fecha'] = datos['Fecha'].dt.strftime('%Y-%m-%d')

# guardar datos
datos.to_csv(archivo_destino, index=False)