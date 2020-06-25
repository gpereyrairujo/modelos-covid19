import random
from sklearn.metrics import mean_squared_error
from math import sqrt


def ajuste_modelos(modelo, datos, serie_estimados, serie_observados, serie_parametro, duracion_periodo, variacion_aleatoria=0.05, maximo_iteraciones=500, maximo_iteraciones_sin_cambios=30):
    
    ajuste_preliminar = datos.copy()
    cantidad_datos = ajuste_preliminar[serie_observados].count()
    ultima_fila = cantidad_datos - 1
    cantidad_periodos = ultima_fila - 3
    mejor_rmse = -1
    
    for p in range(cantidad_periodos):

        # inicio y fin de cada período
        inicio_periodo = p
        fin_periodo = min(ultima_fila, inicio_periodo+duracion_periodo) - 1

        # iterar para mejorar el ajuste
        for i in range(maximo_iteraciones):

            # correr el modelo
            modelo(ajuste_preliminar, inicio_periodo, fin_periodo + 1)

            # calcular RMSE
            datos_estimados = ajuste_preliminar.loc[inicio_periodo+1:fin_periodo+1, serie_estimados]
            datos_observados = ajuste_preliminar.loc[inicio_periodo+1:fin_periodo+1, serie_observados]
            rmse = sqrt(mean_squared_error(datos_estimados, datos_observados))

            # verificar si el RMSE mejoró o si es la primera corrida con los datos iniciales
            if(rmse<mejor_rmse or i==0):
                mejor_rmse = rmse
                mejor_ajuste = ajuste_preliminar.copy()
                iteraciones_sin_cambios = 0
            # si no, volver al mejor ajuste anterior
            else:
                ajuste_preliminar = mejor_ajuste.copy()
                iteraciones_sin_cambios = iteraciones_sin_cambios + 1

            # aleatorizar el valor del parámetro para el período
            aleatorizar_parametro(ajuste_preliminar, serie_parametro, inicio_periodo, fin_periodo, variacion_aleatoria)

            # mostrar progreso
            print(
                'Período', p+1, 'de', cantidad_periodos, 
                '- Iteración', i+1, 'de', maximo_iteraciones, 
                '- RMSE:', int(rmse), 
                '- Mejor RMSE:', int(mejor_rmse), 
                ' '*10, end="\r")

            if(iteraciones_sin_cambios > maximo_iteraciones_sin_cambios): break

        # copiar en la tabla de datos iniciales el mejor mejor_ajuste obtenido de cada período, antes de pasar al siguiente
        ajuste_preliminar = mejor_ajuste.copy()

        # bajar una línea
        print('')

    return mejor_ajuste


def ajuste_por_periodos(modelo, datos, serie_estimados, serie_observados, serie_parametro, duracion_periodo, variacion_aleatoria, maximo_iteraciones=1000, maximo_iteraciones_sin_cambios=50):
    # ajuste de parámetros por períodos por separado
    
    ajuste_preliminar = datos.copy()
    cantidad_datos = ajuste_preliminar[serie_observados].count()
    ultima_fila = cantidad_datos - 1
    cantidad_periodos = int(ultima_fila/duracion_periodo) + 1
    mejor_rmse = -1
    
    for p in range(cantidad_periodos):

        # inicio y fin de cada período
        inicio_periodo = p * duracion_periodo
        fin_periodo = min(ultima_fila, inicio_periodo+duracion_periodo) - 1

        # iterar para mejorar el ajuste
        for i in range(maximo_iteraciones):

            # correr el modelo
            modelo(ajuste_preliminar, inicio_periodo, fin_periodo + 1)

            # calcular RMSE
            datos_estimados = ajuste_preliminar.loc[inicio_periodo+1:fin_periodo+1, serie_estimados]
            datos_observados = ajuste_preliminar.loc[inicio_periodo+1:fin_periodo+1, serie_observados]
            rmse = sqrt(mean_squared_error(datos_estimados, datos_observados))

            # verificar si el RMSE mejoró o si es la primera corrida con los datos iniciales
            if(rmse<mejor_rmse or i==0):
                mejor_rmse = rmse
                mejor_ajuste = ajuste_preliminar.copy()
                iteraciones_sin_cambios = 0
            # si no, volver al mejor ajuste anterior
            else:
                ajuste_preliminar = mejor_ajuste.copy()
                iteraciones_sin_cambios = iteraciones_sin_cambios + 1

            # aleatorizar el valor del parámetro para el período
            aleatorizar_parametro(ajuste_preliminar, serie_parametro, inicio_periodo, fin_periodo, variacion_aleatoria)

            # mostrar progreso
            print(
                'Período', p+1, 'de', cantidad_periodos, 
                '- Iteración', i+1, 'de', maximo_iteraciones, 
                '- RMSE:', int(rmse), 
                '- Mejor RMSE:', int(mejor_rmse), 
                ' '*10, end="\r")

            if(iteraciones_sin_cambios > maximo_iteraciones_sin_cambios): break

        # copiar en la tabla de datos iniciales el mejor mejor_ajuste obtenido de cada período, antes de pasar al siguiente
        ajuste_preliminar = mejor_ajuste.copy()

        # bajar una línea
        print('')

    return mejor_ajuste

def ajuste_global(modelo, datos, serie_estimados, serie_observados, serie_parametro, duracion_periodo, variacion_aleatoria, maximo_iteraciones=1000, maximo_iteraciones_sin_cambios=50):

    ajuste_preliminar = datos.copy()
    cantidad_datos = ajuste_preliminar[serie_observados].count()
    ultima_fila = cantidad_datos - 1
    cantidad_periodos = int(ultima_fila/duracion_periodo) + 1
    mejor_rmse = -1

    # iterar para mejorar el ajuste
    for i in range(maximo_iteraciones):

        # correr el modelo
        modelo(ajuste_preliminar, 0, ultima_fila)

        # calcular RMSE
        datos_estimados = ajuste_preliminar[serie_estimados]
        datos_observados = ajuste_preliminar[serie_observados]
        rmse = sqrt(mean_squared_error(datos_estimados, datos_observados))

        # verificar si el RMSE mejoró o si es la primera corrida con los datos iniciales
        if(rmse<mejor_rmse or i==0):
            mejor_rmse = rmse
            mejor_ajuste = ajuste_preliminar.copy()
            iteraciones_sin_cambios = 0
        # si no, volver al mejor ajuste anterior
        else:
            ajuste_preliminar = mejor_ajuste.copy()
            iteraciones_sin_cambios = iteraciones_sin_cambios + 1
        
        # aleatorizar parámetro
        for p in range(cantidad_periodos):
            inicio_periodo = p * duracion_periodo
            fin_periodo = min(ultima_fila, inicio_periodo+duracion_periodo) - 1
            aleatorizar_parametro(ajuste_preliminar, serie_parametro, inicio_periodo, fin_periodo, variacion_aleatoria)

        # mostrar progreso
        print(
            'Iteración', i+1, 'de', maximo_iteraciones, 
            '- RMSE:', int(rmse), 
            '- Mejor RMSE:', int(mejor_rmse), 
            ' '*10, end="\r")

        if(iteraciones_sin_cambios > maximo_iteraciones_sin_cambios): break

    # bajar una línea
    print('')

    return mejor_ajuste

def aleatorizar_parametro(datos, serie_parametro, inicio_periodo, fin_periodo, variacion_aleatoria):

    # tomar el valor promedio del parámetro de cada período
    parametro = datos.loc[inicio_periodo:fin_periodo, serie_parametro].mean()
    
    # aleatorizar el parámetro
    multiplicador = random.uniform(1-variacion_aleatoria, 1+variacion_aleatoria)
    parametro = parametro * multiplicador

    # poner el nuevo valor del parámetro en la planilla de datos
    datos.loc[inicio_periodo:fin_periodo, serie_parametro] = parametro

