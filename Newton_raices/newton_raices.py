# METODO DE NEWTON RAICES
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# INGRESO DE DATOS
x = sp.symbols('x')
# el programa utiliza la librería sympy para interpretar la fórmula que escribes como texto.
funcion_str = input("Ingrese la función f(x) (ej. x**3 - 6*x**2 + 9*x + 1): ")

f_sym = sp.sympify(funcion_str)
# el código solo necesita calcular la primera derivada de la función
f1_sym = sp.diff(f_sym, x)
# Usa lambdify para convertir la función original y su derivada en herramientas numéricas que la computadora pueda evaluar rápidamente
f = sp.lambdify(x, f_sym, 'numpy')
f1 = sp.lambdify(x, f1_sym, 'numpy')

xi = float(input("Ingrese valor inicial xi: "))
tol = float(input("Tolerancia: "))
max_iter = int(input("Máximo número de iteraciones: "))

# METODO NEWTON PARA RAÍCES
# este tiene un objetivo distinto: busca el punto exacto donde la función cruza el eje X (es decir, donde f(x) = 0).
tabla = []
errores = []
# El código toma el valor inicial que le das (xi) y comienza un ciclo for que se repetirá hasta el límite de iteraciones que se definen (max_iter).
for i in range(max_iter):

    fx = f(xi)
    fpx = f1(xi)

    tabla.append([i, xi, fx, fpx])
    # Aquí se divide la función original entre la primera derivada
    xi1 = xi - (fx / fpx)
    error = abs(xi1 - xi)
    errores.append(error)
    # El programa calcula la distancia entre el nuevo punto y el anterior
    # Si esta diferencia es menor a tu tolerancia (tol), el bucle se detiene de inmediato usando break.
    if error < tol:
        break

    xi = xi1

# TABLA
df = pd.DataFrame(tabla, columns=["i", "x", "f(x)", "f'(x)"])
print("\n --- METODO DE NEWTON RAICES ---")
print("\nTabla de Iteraciones:")
print(df)

# Resultado
x_raiz = xi1
print("\nRaíz aproximada x =", x_raiz)


# GRAFICA ERROR VS ITERACIONES
plt.figure(figsize=(8, 4))
plt.plot(range(1, len(errores) + 1), errores, color='indigo',
         linewidth=1.8, marker='o', markersize=4, label='Error aproximado')

plt.axhline(y=errores[-1], color='gray', linestyle=':', linewidth=1,
            label=f'Error final: {errores[-1]:.4f}%')

plt.annotate(f'{errores[-1]:.4f}%',
             xy=(len(errores), errores[-1]),
             xytext=(len(errores) - 1.5, errores[-1] + max(errores) * 0.05),
             fontsize=8, color='steelblue')

plt.xlabel("Iteración")
plt.ylabel("Error aproximado (%)")
plt.title("Convergencia del error")
plt.legend(fontsize=8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# GRAFICA DE LA FUNCION
x_vals = np.linspace(x_raiz - 5, x_raiz + 5, 400)
y_vals = f(x_vals)
y_raiz = f(x_raiz)

plt.figure(figsize=(8, 5))
plt.plot(x_vals, y_vals, color='springgreen', linewidth=2, label='f(x)')

plt.axvline(x_raiz, color='gray', linestyle=':', linewidth=1)
plt.axhline(0, color='gray', linestyle=':', linewidth=1)

plt.scatter(x_raiz, y_raiz, color='crimson', zorder=5, s=70,
            label=f'raíz = {x_raiz:.4f}\nf(raíz) ≈ {y_raiz:.4e}')

plt.annotate(f'  ({x_raiz:.3f}, {y_raiz:.3e})',
             xy=(x_raiz, y_raiz),
             xytext=(x_raiz + 0.3, y_raiz + (max(y_vals) - min(y_vals)) * 0.05),
             fontsize=8, color='crimson')

plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Función y raíz aproximada")
plt.legend(fontsize=8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
