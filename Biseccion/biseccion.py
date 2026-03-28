# METODO DE BISECCION 
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify

#  Ingreso interactivo de la función
x = symbols('x')
while True:
    funcion_str = input("Ingresa f(x) (ej. 3*x**2 - 120*x + 100): ").strip()
    try:
        expr = sympify(funcion_str)
        f    = lambdify(x, expr, modules=['numpy', 'math'])
        _    = float(f(1))   # prueba de evaluación
        print(f"  → f(x) = {expr}")
        break
    except Exception as e:
        print(f"  x Función inválida: {e}. Inténtalo de nuevo.")

# Método de bisección con tabla
def biseccion(f, xl, xu, tolerancia):

    if f(xl) * f(xu) > 0:
        print("No existe raíz en el intervalo dado")
        return None

    iteraciones = []
    xr_old = xl
    i = 0

    while True:
        xr    = (xl + xu) / 2
        error = abs((xr - xr_old) / xr) if i > 0 else None

        iteraciones.append([i, xl, xu, xr, f(xr), error])

        if f(xr) == 0 or (error is not None and error < tolerancia):
            break

        if f(xl) * f(xr) < 0:
            xu = xr
        else:
            xl = xr

        xr_old = xr
        i += 1

    tabla = pd.DataFrame(iteraciones,
                         columns=["Iteración", "xl", "xu", "xr", "f(xr)", "Error"])
    return xr, tabla

# Parámetros y ejecución 
x_lower    = float(input("Ingrese el limite inferior: "))
x_upper    =  float(input("Ingrese el limite superior: "))
tolerancia =  0.0001

raiz, tabla = biseccion(f, x_lower, x_upper, tolerancia)

print("\n --- METODO DE BISECCION ---")
print("\nRaíz aproximada:", raiz)
print(tabla)


#Gráfica 1: Función f(x) con la raíz encontrada

x_vals = np.linspace(x_lower - 5, x_upper + 5, 500)
y_vals = f(x_vals)

fig, ax = plt.subplots(figsize=(9, 5))

# Curva de la función
ax.plot(x_vals, y_vals, color='steelblue', linewidth=2.2, label=r'$f(x) = 3x^2 - 120x + 100$')

# Eje horizontal
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')

# Intervalo inicial
ax.axvline(x_lower, color='orange', linewidth=1.5, linestyle=':', label=f'$x_l = {x_lower}$')
ax.axvline(x_upper, color='green',  linewidth=1.5, linestyle=':', label=f'$x_u = {x_upper}$')

# Raíz encontrada
ax.scatter([raiz], [f(raiz)], color='red', zorder=5, s=80, label=f'Raíz ≈ {raiz:.6f}')
ax.axvline(raiz, color='red', linewidth=1, linestyle='--', alpha=0.5)
ax.annotate(f'  xr ≈ {raiz:.4f}',
            xy=(raiz, 0), xytext=(raiz + 1.5, max(y_vals) * 0.3),
            arrowprops=dict(arrowstyle='->', color='red'),
            color='red', fontsize=10)

ax.set_title('Gráfica de $f(x)$ y raíz encontrada por bisección', fontsize=13, fontweight='bold')
ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('$f(x)$', fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()

errores = tabla["Error"].dropna()

# Crear la figura con un tamaño estándar
fig, ax = plt.subplots(figsize=(8, 4))

# Eje X
x = range(1, len(errores) + 1)

# Línea principal básica con marcadores de puntos
ax.plot(x, errores, color="blue", marker="o", markersize=4, linewidth=1.5)

# Rejilla
ax.grid(True, linestyle="--", alpha=0.6)

# Etiquetas y título estándar
ax.set_title("Error vs Iteraciones", fontsize=13, fontweight="bold")
ax.set_xlabel("Iteración", fontsize=11)
ax.set_ylabel("Error relativo", fontsize=11)

plt.tight_layout()
plt.show()