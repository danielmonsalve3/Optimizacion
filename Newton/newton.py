import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# INGRESO DE DATOS
x = sp.symbols('x')

funcion_str = input("Ingrese la función f(x) (ej. x**3 - 6*x**2 + 9*x + 1): ")
tipo = input("¿Desea maximizar o minimizar? (max/min): ")

f_sym = sp.sympify(funcion_str)
f1_sym = sp.diff(f_sym, x)
f2_sym = sp.diff(f1_sym, x)

f = sp.lambdify(x, f_sym, 'numpy')
f1 = sp.lambdify(x, f1_sym, 'numpy')
f2 = sp.lambdify(x, f2_sym, 'numpy')

xi = float(input("Ingrese valor inicial xi: "))
tol = float(input("Tolerancia: "))
max_iter = int(input("Máximo número de iteraciones: "))

# METODO NEWTON
tabla = []
errores = []

for i in range(max_iter):

    fx = f(xi)
    fpx = f1(xi)
    fppx = f2(xi)

    tabla.append([i, xi, fx, fpx, fppx])

    xi1 = xi - (fpx / fppx)
    error = abs(xi1 - xi)
    errores.append(error)

    if error < tol:
        break

    xi = xi1

# TABLA
df = pd.DataFrame(tabla, columns=["i", "x", "f(x)", "f'(x)", "f''(x)"])
print("\nTabla de Iteraciones:")
print(df)

# Resultado
x_opt = xi1
print("\nPunto óptimo x =", x_opt)
print("f(x) =", f(x_opt))

if f2(x_opt) > 0:
    print("Es un MÍNIMO")
else:
    print("Es un MÁXIMO")

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
x_vals = np.linspace(x_opt - 5, x_opt + 5, 400)
y_vals = f(x_vals)
y_opt  = f(x_opt)

plt.figure(figsize=(8, 5))
plt.plot(x_vals, y_vals, color='springgreen', linewidth=2, label='f(x)')

plt.axvline(x_opt, color='gray', linestyle=':', linewidth=1)
plt.axhline(y_opt,  color='gray', linestyle=':', linewidth=1)

plt.scatter(x_opt, y_opt, color='crimson', zorder=5, s=70,
            label=f'xopt = {x_opt:.4f}\nf(xopt) = {y_opt:.4f}')

plt.annotate(f'  ({x_opt:.3f}, {y_opt:.3f})',
             xy=(x_opt, y_opt),
             xytext=(x_opt + 0.3, y_opt + (max(y_vals) - min(y_vals)) * 0.05),
             fontsize=8, color='crimson')

plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Función y punto óptimo")
plt.legend(fontsize=8)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()