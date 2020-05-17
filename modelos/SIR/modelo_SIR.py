def modelo_SIR(datos, fila_inicio, fila_fin):

    '''
    Modelo SIR de paso diario

    Variables de entrada:
        datos: dataframe con (al menos) las siguientes columnas:
            Gamma: parámetro Gamma, un valor para cada fila/día
            Beta: parámetro Beta, un valor para cada fila/dia
            S: individuos susceptibles, valor para fila inicial
            I: individuos infectados, valor para fila inicial
            R: individuos recuperados/removidos, valor para fila inicial
        fila_inicio: fila correspondiente al día 0 de la simulación
        fila_fin: fila correspondiente al último día de la simulación
    
    Salida: mismo dataframe de entrada con los resultados de individuos S, I, R
    '''

    for d in range(fila_inicio, fila_fin):

        # leer valores dia actual
        S = datos.loc[d,'S']
        I = datos.loc[d,'I']
        R = datos.loc[d,'R']
        N = S+I+R

        # leer parámetros día actual
        gamma = datos.loc[d,'Gamma']
        beta = datos.loc[d,'Beta']
        
        # calcular valores día siguiente
        R = R + I * gamma
        I = I + (beta * I * S / N) - gamma * I
        S = N - I - R

        # escribir datos día siguiente
        datos.loc[d+1,'S'] = S
        datos.loc[d+1,'I'] = I
        datos.loc[d+1,'R'] = R

    # resultado
    return datos

