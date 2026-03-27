# METODO DE FALSA POSICION
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify
# le pide al usuario que ingrese una función matemática como texto
x = symbols('x')
while True:
    funcion_str = input("Ingresa f(x) (ej. 4*x**4 - 9*x**2 + 1): ").strip()
    try:
        # transforma ese texto en una expresión matemática abstracta.
        expr = sympify(funcion_str) 
        # convierte esa expresión abstracta en una función ejecutable real (f(x)) que puede procesar valores numéricos.
        f    = lambdify(x, expr, modules=['numpy', 'math'])
        _    = float(f(1))   # prueba de evaluación
        print(f"  → f(x) = {expr}")
        break
    # captura el fallo y le pide que lo intente de nuevo sin detener el programa.
    except Exception as e:
        print(f"  ✗ Función inválida: {e}. Inténtalo de nuevo.")

def falsap(f, xl, xu, iteraciones=1000, error_r=0.00001, expr_str="f(x)"):
    # Evaluar los límites iniciales
    fl = f(xl)
    fu = f(xu)

    # Evaluar si la raíz está dentro del intervalo
    if fl * fu > 0:
        print("No existe solución garantizada en ese intervalo (la función no cambia de signo).")
        return

    # Inicializar variables
    xr_anterior = 0
    contador = 0
    error_calculado = 100.0 # Iniciar error

    # Guardado de Iteraciones
    historial_errores = []
    historial_iteraciones = []
    tabla_datos = []
    # iterar hasta alcanzar el límite máximo o hasta que el error sea muy pequeño.
    while contador < iteraciones:
        contador += 1

        # Calcular la nueva aproximación
        xr = xu - ((fu * (xl - xu)) / (fl - fu))
        fr = f(xr)
        error_actual = np.nan

        # Calcular el error (a partir de la segunda iteración)
        if contador > 1:
            if xr != 0: # Prevenir división por cero
                error_calculado = abs((xr - xr_anterior) / xr) * 100
                error_actual = error_calculado
            else: 
              error_calculado = 0
              error_actual = 0

            historial_errores.append(error_calculado)
            historial_iteraciones.append(contador - 1)
        
        fila = {
            'Iteración': contador, #
            'xl': xl,
            'xu': xu,
            'xr': xr,
            'f(xr)': fr,
            'Error': error_actual # Usamos el valor calculado (con 'NaN' en la primera fila)
        }
        tabla_datos.append(fila)
        

        # Condición de parada (Raíz exacta o error cumplido)
        if error_calculado <= error_r or fr == 0:
            break

        # Redefinir nuevo intervalo
        if fl * fr < 0:
            xu = xr
            fu = fr
        else:
            xl = xr
            fl = fr

        xr_anterior = xr

    # Imprimir el resultado
    print("\n--- METODO DE FALSA POSICION ---")
    print("\n--- Resultados ---")
    print("La raíz aproximada es: {:.6f}".format(xr))
    print("Encontrada en: {} iteraciones".format(contador))
    print("Con un error relativo de: {:.5f}%".format(error_calculado))

    print("\n                   --- Tabla de Iteraciones ---")
    df_tabla = pd.DataFrame(tabla_datos)
    print(df_tabla)

    #--- Graficas ---
    # Grafica de f(x)
    plt.figure(figsize = (14,5))


    plt.subplot(1, 2, 1)
    margen = (xu - xl) * 0.5 if xu != xl else 1
    x_vals = np.linspace(xl - margen, xu + margen, 200)
    y_vals = f(x_vals)

    plt.plot(x_vals, y_vals, label = "Curva $f(x)$", color = "blue")
    plt.axhline(0, color="black", linewidth = 1)
    plt.axvline(xl, color = "green", linestyle="--", alpha= 0.6, label="xl (Limite Inf)")
    plt.axvline(xu, color="orange", linestyle="--", alpha=0.6, label="xu (Limite Sup)")
    plt.plot(xr, f(xr), "ro", label="Raiz Encontrada")

    plt.title(f"Funcion {expr_str}")
    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Grafica del Error:
    plt.subplot(1, 2, 2)
    plt.plot(historial_iteraciones, historial_errores, marker='o', linestyle='-', color='red')
    plt.title("Error vs Iteraciones")
    plt.xlabel("Numero de Iteracion")
    plt.ylabel("Error Relativo Porcentual (%)")
    plt.grid(True, alpha=0.3)

    # Mostrar
    print()
    plt.tight_layout()
    plt.show()


# Inputs del usuario
xl = float(input("Ingrese el límite inferior (xl): "))
xu = float(input("Ingrese el límite superior (xu): "))
err = float(input("Ingrese el error tolerado en porcentaje (ej. 0.001): "))

# Llamada a la función
falsap(f, xl, xu, error_r=err, expr_str=str(expr))